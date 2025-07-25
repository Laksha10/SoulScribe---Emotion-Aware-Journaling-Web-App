# File: routes/emotion_monitor.py

import os
import jwt
from flask import Blueprint, request, jsonify
from db.models import JournalEntry, JournalThread
from datetime import datetime, timedelta
from sqlalchemy import and_
from collections import defaultdict, Counter
from db.connection import db

emotion_monitor_bp = Blueprint("emotion_monitor", __name__)

# Low emotions considered indicators of prolonged distress
LOW_EMOTIONS = {
    "anger", "annoyance", "confusion", "disappointment", "disapproval",
    "disgust", "embarrassment", "fear", "grief", "nervousness",
    "remorse", "sadness"
}

@emotion_monitor_bp.route("/emotional_status", methods=["GET"])
def get_emotional_status():
    try:
        # === Auth ===
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
            user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # === Configurable parameters ===
        window_days = 14
        red_zone_threshold = 0.75

        now = datetime.utcnow()
        cutoff = now - timedelta(days=window_days)

        user_threads = JournalThread.query.filter_by(user_id=user_id).all()
        if not user_threads:
            return jsonify({"message": "No journaling activity yet", "status": "neutral"}), 200

        from db.models import UserRedZoneLog, UserSupportContact, User, UserCopingActivity
        from utils.email import send_email

        # === Group threads by session_id ===
        sessions = defaultdict(list)
        for thread in user_threads:
            sessions[thread.session_id].append(thread.id)

        session_emotion_statuses = []
        for session_id, thread_ids in sessions.items():
            session_entries = (
                JournalEntry.query
                .filter(
                    and_(
                        JournalEntry.thread_id.in_(thread_ids),
                        JournalEntry.timestamp >= cutoff,
                        JournalEntry.role == "user"
                    )
                )
                .all()
            )

            if not session_entries:
                continue

            all_emotions = []
            for entry in session_entries:
                if entry.predicted_emotions:
                    all_emotions.extend(entry.predicted_emotions.split(", "))

            if not all_emotions:
                continue

            emotion_counts = Counter(all_emotions)
            dominant_emotion, _ = emotion_counts.most_common(1)[0]
            is_distressed = dominant_emotion in LOW_EMOTIONS
            session_emotion_statuses.append(is_distressed)

        total_sessions = len(session_emotion_statuses)
        distressed_sessions = sum(session_emotion_statuses)

        if total_sessions == 0:
            return jsonify({"message": "No recent sessions", "status": "neutral"}), 200

        distress_ratio = distressed_sessions / total_sessions

        if distress_ratio >= red_zone_threshold:
            # === Log red zone alert only once per session ===
            last_log = (
                UserRedZoneLog.query
                .filter_by(user_id=user_id)
                .order_by(UserRedZoneLog.timestamp.desc())
                .first()
            )
            if not last_log or (now - last_log.timestamp).total_seconds() > 3600:
                new_log = UserRedZoneLog(
                    user_id=user_id,
                    timestamp=now,
                    response="pending"  # Default state until user responds
                )
                db.session.add(new_log)
                db.session.commit()

            # === Fetch support contacts ===
            contacts = UserSupportContact.query.filter_by(user_id=user_id).all()
            contact_data = [
                {
                    "name": contact.name,
                    "relationship": contact.relationship,
                    "email": contact.email
                }
                for contact in contacts
            ]

            # === Fetch coping activities ===
            activities = UserCopingActivity.query.filter_by(user_id=user_id).all()
            coping_data = [
                {
                    "label": activity.label,
                    "detail": activity.detail
                }
                for activity in activities
            ]

            # === Check for escalation condition ===
            recent_logs = (
                UserRedZoneLog.query
                .filter_by(user_id=user_id)
                .order_by(UserRedZoneLog.timestamp.desc())
                .limit(3)
                .all()
            )
            ignored_count = sum(1 for log in recent_logs if log.response == "ignored")
            if ignored_count == 3:
                user = User.query.get(user_id)
                for contact in contacts:
                    subject = f"⚠️ {user.name or 'A loved one'} might need support"
                    body = (
                        f"Hi {contact.name},\n\n"
                        f"{user.name or 'Someone you care about'} has been showing signs of emotional distress.\n"
                        "They've ignored support nudges multiple times recently.\n\n"
                        "You were listed as a trusted contact. This is just a gentle heads-up to check in when you can.\n\n"
                        "With care,\nSoulScribe"
                    )
                    send_email(to=contact.email, subject=subject, body=body)

            # === Return red zone status with options ===
            return jsonify({
                "status": "red_zone",
                "message": f"{distressed_sessions} out of {total_sessions} sessions showed dominant low emotions.",
                "support_contacts": contact_data,
                "coping_activities": coping_data
            }), 200

        return jsonify({"status": "neutral", "message": "Emotionally stable in recent sessions."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
