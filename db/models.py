from db.connection import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from pytz import timezone

# 🇮🇳 IST time helper
def now_ist():
    return datetime.now(timezone("Asia/Kolkata"))

# ✅ USER MODEL
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(512), nullable=False)
    ok_to_notify = db.Column(db.Boolean, default=False)
    threads = db.relationship('JournalThread', backref='user', lazy=True)
    sessions = db.relationship('Session', backref='user', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# ✅ SESSION MODEL
class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    start_time = db.Column(db.DateTime(timezone=True), default=now_ist)

    dominant_emotion = db.Column(db.String(50), nullable=True)
    top_emotions = db.Column(JSON, nullable=True)

    user_session_number = db.Column(db.Integer, nullable=False)
    threads = db.relationship('JournalThread', backref='session', lazy=True)

    def __repr__(self):
        return f"<Session {self.id} | User {self.user_id} | Emotion: {self.dominant_emotion}>"

# ✅ JOURNAL THREAD
class JournalThread(db.Model):
    __tablename__ = 'journal_threads'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=now_ist)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=True, index=True)

    user_thread_number = db.Column(db.Integer, nullable=False)
    entries = db.relationship('JournalEntry', backref='thread', lazy=True)

    def __repr__(self):
        return f"<Thread {self.id} | User {self.user_id} | Session {self.session_id}>"

# ✅ JOURNAL ENTRY
class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    predicted_emotions = db.Column(db.Text, nullable=False)
    reflection = db.Column(db.Text, nullable=True)
    conversation = db.Column(JSON, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=now_ist)

    thread_id = db.Column(db.Integer, db.ForeignKey('journal_threads.id'), nullable=True, index=True)
    role = db.Column(db.String(10), nullable=True)  # "user" or "soul"

    def __repr__(self):
        return (
            f"<JournalEntry {self.id} | Emotions: {self.predicted_emotions} | "
            f"Role: {self.role} | Thread: {self.thread_id}>"
        )

# ✅ SUPPORT CONTACT
class UserSupportContact(db.Model):
    __tablename__ = 'user_support_contacts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    name = db.Column(db.String(120), nullable=False)
    relationship = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(32), nullable=True)

    preferred_channel = db.Column(db.String(20), default="email")
    ok_to_notify = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime(timezone=True), default=now_ist)
    updated_at = db.Column(db.DateTime(timezone=True), default=now_ist, onupdate=now_ist)

    user = db.relationship('User', backref=db.backref('support_contacts', lazy=True))

    def __repr__(self):
        return f"<SupportContact {self.name} ({self.relationship})>"

# ✅ COPING ACTIVITY
class UserCopingActivity(db.Model):
    __tablename__ = 'user_coping_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    label = db.Column(db.String(120), nullable=False)
    detail = db.Column(db.Text, nullable=True)
    mood_tag = db.Column(db.String(32), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    sort_order = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref=db.backref('coping_activities', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'label', name='uq_user_coping_label'),
    )

    def __repr__(self):
        return f"<CopingActivity {self.label}>"

# ✅ RED ZONE LOG
class UserRedZoneLog(db.Model):
    __tablename__ = 'user_red_zone_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False, index=True)
    triggered_at = db.Column(db.DateTime(timezone=True), default=now_ist)

    did_contact = db.Column(db.Boolean, default=False)
    did_activity = db.Column(db.Boolean, default=False)
    did_grounding = db.Column(db.Boolean, default=False)
    escalation_sent = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('red_zone_logs', lazy=True))
    batch_id = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<RedZoneLog User {self.user_id} | Contacted: {self.did_contact} | Activity: {self.did_activity}>"
