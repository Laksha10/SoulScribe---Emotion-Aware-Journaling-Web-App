# File: routes/timeline.py

import json
import ast
from flask import Blueprint, jsonify, g
from utils.auth2 import token_required
from db.models import JournalThread, JournalEntry
from pytz import timezone
from sqlalchemy.orm import joinedload  # ✅ Added for eager loading

timeline_bp = Blueprint("timeline", __name__)

@timeline_bp.route("/timeline", methods=["GET"])
@token_required
def get_user_timeline():
    try:
        user_id = g.current_user.id

        # ✅ Eagerly load session with threads
        threads = (
            JournalThread.query
            .options(joinedload(JournalThread.session))
            .filter_by(user_id=user_id)
            .order_by(JournalThread.id.asc())
            .all()
        )

        timeline = []

        for thread in threads:
            entries = (
                JournalEntry.query
                .filter_by(thread_id=thread.id)
                .order_by(JournalEntry.timestamp.asc())
                .all()
            )

            if not entries:
                continue

            session_number = thread.session.user_session_number if thread.session else None

            timeline.append({
                "thread_id": thread.id,
                "user_thread_number": thread.user_thread_number,
                "session_id": thread.session_id,
                "user_session_number": session_number,
                "entries": [
                    {
                        "id": e.id,
                        "role": e.role,
                        "text": e.text,
                        "reflection": e.reflection,
                        "timestamp": e.timestamp.astimezone(timezone("Asia/Kolkata")).strftime("%d %b %Y, %I:%M %p"),
                        "predicted_emotions": (
                            ast.literal_eval(e.predicted_emotions)
                            if isinstance(e.predicted_emotions, str) and e.predicted_emotions.startswith("[")
                            else e.predicted_emotions.split(", ") if isinstance(e.predicted_emotions, str)
                            else []
                        )
                    }
                    for e in entries
                ]
            })

        print("🧪 Timeline API output:\n", json.dumps(timeline, indent=2))
        return jsonify(timeline), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
