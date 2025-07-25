#file: routes/emotion_arc.py
import ast
from flask import Blueprint, jsonify, g
from db.models import Session
from collections import Counter
from pytz import timezone
from utils.auth2 import token_required

emotion_arc_bp = Blueprint("emotion_arc", __name__)

POSITIVE_EMOTIONS = {
    "admiration", "amusement", "approval", "caring", "curiosity",
    "excitement", "gratitude", "joy", "love", "optimism",
    "pride", "realization", "relief", "surprise"
}

NEGATIVE_EMOTIONS = {
    "anger", "annoyance", "confusion", "desire", "disappointment",
    "disapproval", "disgust", "embarrassment", "fear", "grief",
    "nervousness", "remorse", "sadness"
}

def classify_emotion_group(emotions):
    counts = Counter(emotions)
    pos = sum(counts[e] for e in POSITIVE_EMOTIONS)
    neg = sum(counts[e] for e in NEGATIVE_EMOTIONS)

    if pos > neg:
        return "Positive"
    elif neg > pos:
        return "Negative"
    else:
        return "Neutral"

@emotion_arc_bp.route("/emotion_arc", methods=["GET"])
@token_required
def get_emotion_arc():
    try:
        user_id = g.current_user.id
        sessions = Session.query.filter_by(user_id=user_id).order_by(Session.start_time).all()
        result = []

        for session in sessions:
            entries = []
            for thread in session.threads:
                for entry in thread.entries:
                    if entry.role == "user" and entry.predicted_emotions:
                        try:
                            emotions = (
                                entry.predicted_emotions
                                if isinstance(entry.predicted_emotions, list)
                                else ast.literal_eval(entry.predicted_emotions)
                                if entry.predicted_emotions.startswith("[")
                                else entry.predicted_emotions.split(", ")
                            )
                        except Exception:
                            emotions = entry.predicted_emotions.split(", ")

                        entries.append({
                            "timestamp": entry.timestamp.astimezone(timezone("Asia/Kolkata")).isoformat(),
                            "emotions": emotions,
                            "user_thread_number": thread.user_thread_number
                        })

            entries.sort(key=lambda x: x["timestamp"])

            if not entries:
                continue

            # Add entry_number field after sorting
            for idx, entry in enumerate(entries, start=1):
                entry["entry_number"] = idx  # ✅ Add this field

            split_index = int(len(entries) * 0.6)
            first_part = [e for entry in entries[:split_index] for e in entry["emotions"]]
            second_part = [e for entry in entries[split_index:] for e in entry["emotions"]]

            first_emotion_type = classify_emotion_group(first_part)
            second_emotion_type = classify_emotion_group(second_part)
            arc_type = f"{first_emotion_type} → {second_emotion_type}"

            result.append({
                "user_session_number": session.user_session_number,
                "start_time": session.start_time.astimezone(timezone("Asia/Kolkata")).isoformat(),
                "entry_emotions": entries,
                "arc_type": arc_type
            })

        return jsonify(result), 200

    except Exception as e:
        print("❌ Error in /emotion_arc:", str(e))
        return jsonify({"error": "Server error"}), 500
