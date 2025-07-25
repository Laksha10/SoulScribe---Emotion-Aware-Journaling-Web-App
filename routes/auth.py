# File: routes/auth.py
import jwt
from flask import current_app
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db.connection import db
from db.models import User
from pytz import timezone
from db.models import User, UserSupportContact, UserCopingActivity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
def now_ist():
    return datetime.now(timezone("Asia/Kolkata"))

# === REGISTER ROUTE ===
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    support_contacts = data.get("support_contacts", [])  # List of dicts
    coping_activities = data.get("coping_activities", [])  # List of strings
    ok_to_notify = data.get("ok_to_notify", True)  # Optional boolean

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    password_hash = generate_password_hash(password)
    print("🧠 User class being used:", User)
    print("🧠 User module:", User.__module__)
    print("🧠 User columns:", User.__table__.columns.keys())

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        ok_to_notify=ok_to_notify
    )
    db.session.add(user)
    db.session.flush()  # So we can use user.id before commit

    # 🧑‍🤝‍🧑 Add support contacts
    for contact in support_contacts:
        if all(k in contact for k in ("name", "relationship", "email")):
            db.session.add(UserSupportContact(
                user_id=user.id,
                name=contact["name"],
                relationship=contact["relationship"],
                email=contact["email"]
            ))

    # 🧘 Add coping activities
    for activity in coping_activities:
        if isinstance(activity, str) and activity.strip():
            db.session.add(UserCopingActivity(
                user_id=user.id,
                label=activity.strip()
            ))

    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id
    }), 201


# === LOGIN ROUTE ===
# === LOGIN ROUTE ===
@auth_bp.route("/login", methods=["POST"])
def login():
    print("✅ Login route hit")

    data = request.get_json()
    print("📥 Received data:", data)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        print("❌ Missing username or password")
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        print("❌ Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401

    # ✅ Import here to avoid circular import issues
    from db.models import Session  

    # 🔢 Determine next user_session_number
    latest_session = (
        Session.query.filter_by(user_id=user.id)
        .order_by(Session.user_session_number.desc())
        .first()
    )
    next_user_session_number = (latest_session.user_session_number if latest_session else 0) + 1

    # ✅ Create session with required fields
    new_session = Session(
        user_id=user.id,
        start_time=now_ist(),
        user_session_number=next_user_session_number
    )
    db.session.add(new_session)
    db.session.commit()

    # ✅ Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": now_ist() + timedelta(days=1)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    print("✅ Login successful for:", user.username)
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "token": token,
        "session_id": new_session.id
    }), 200


# === LOGOUT ROUTE ===
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)  # Remove user from session
    return jsonify({"message": "Logged out successfully"}), 200
