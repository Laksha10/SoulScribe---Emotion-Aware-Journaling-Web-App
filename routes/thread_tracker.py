import os
from flask import request, jsonify, Blueprint, g
from db.connection import db
from db.models import JournalThread, JournalEntry
from pytz import timezone
from utils.auth2 import token_required
from sqlalchemy.orm import joinedload

tracker_bp = Blueprint("tracker", __name__)

@tracker_bp.route("/get_thread_entries/<int:thread_id>", methods=["GET"])
@token_required
def get_thread_entries(thread_id):
    try:
        user_id = g.current_user.id

        # ✅ Eagerly load session to avoid None issues
        thread = (
            db.session.query(JournalThread)
            .options(joinedload(JournalThread.session))
            .filter_by(id=thread_id)
            .first()
        )

        if not thread:
            return jsonify({"error": "Thread not found"}), 404

        if thread.user_id != user_id:
            return jsonify({"error": "Access denied: Not your thread"}), 403

        entries = (
            JournalEntry.query
            .filter_by(thread_id=thread_id)
            .order_by(JournalEntry.timestamp.asc())
            .all()
        )

        if not entries:
            return jsonify({"error": "No entries found for this thread"}), 404

        result = {
            "thread_id": thread.id,
            "user_thread_number": thread.user_thread_number,
            "session_id": thread.session_id,
            "user_session_number": thread.session.user_session_number if thread.session else None,
            "entries": [
                {
                    "role": entry.role,
                    "text": entry.text,
                    "emotions": entry.predicted_emotions.split(", ") if entry.predicted_emotions else [],
                    "timestamp": entry.timestamp.astimezone(timezone("Asia/Kolkata")).isoformat()
                }
                for entry in entries
            ]
        }

        return jsonify(result), 200

    except Exception as e:
        print("❌ Error fetching thread entries:", str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500
