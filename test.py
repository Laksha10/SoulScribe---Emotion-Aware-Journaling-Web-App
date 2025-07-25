# # # from db.connection import db
# # # from db.models import User, JournalThread
# # # from app import app  # Your Flask app

# # # with app.app_context():
# # #     users = User.query.all()

# # #     for user in users:
# # #         threads = (
# # #             JournalThread.query
# # #             .filter_by(user_id=user.id)
# # #             .order_by(JournalThread.created_at.asc(), JournalThread.id.asc())
# # #             .all()
# # #         )

# # #         print(f"\n🧪 Fixing threads for User {user.id} ({user.username})")
# # #         for i, thread in enumerate(threads, start=1):
# # #             if thread.user_thread_number != i:
# # #                 print(f"  🔄 Fixing Thread ID {thread.id} from {thread.user_thread_number} → {i}")
# # #                 thread.user_thread_number = i
# # #                 db.session.add(thread)

# # #         db.session.commit()
# # #         print(f"✅ User {user.id} → Thread numbering fixed, total {len(threads)} threads.")
# # from sqlalchemy import create_engine, text
# # from sqlalchemy.orm import sessionmaker
# # import os

# # # --- Load your DB URL ---
# # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Laksha%4010%2E07%2E2004@db.iysyzdzhagnybzqamxdj.supabase.co:5432/postgres")
# # engine = create_engine(DATABASE_URL)
# # Session = sessionmaker(bind=engine)
# # session = Session()

# # print("📦 Fetching all users...\n")

# # # --- 1. Print users in DB ---
# # users = session.execute(text("SELECT id, username, email FROM users ORDER BY id")).fetchall()

# # if not users:
# #     print("❌ No users found.")
# # else:
# #     print("👤 Current users in DB:")
# #     for user in users:
# #         print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

# # # --- 2. Check current sequence value ---
# # seq_name = "users_id_seq"
# # current_val = session.execute(text(f"SELECT last_value FROM {seq_name}")).scalar()
# # print(f"\n🔢 Current sequence value: {current_val}")

# # # --- 3. Prompt and optionally reset ---
# # user_input = input("\nDo you want to reset the sequence to MAX(id)? (yes/no): ").strip().lower()

# # if user_input == "yes":
# #     max_id = session.execute(text("SELECT MAX(id) FROM users")).scalar()
# #     session.execute(text(f"SELECT setval('{seq_name}', :max_id)"), {'max_id': max_id})
# #     session.commit()
# #     print(f"✅ Sequence '{seq_name}' reset to {max_id}.")
# # else:
# #     print("ℹ️ No changes made.")

# # session.close()
# # File: check_support_contacts_in_db.py

# from db.connection import db
# from db.models import User, UserSupportContact
# from flask import Flask
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# def check_support_contacts(username):
#     with app.app_context():
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             print(f"❌ No user found with username: {username}")
#             return

#         contacts = UserSupportContact.query.filter_by(user_id=user.id).all()
#         if not contacts:
#             print(f"⚠️ No support contacts found for user '{username}' (id={user.id})")
#         else:
#             print(f"✅ Found {len(contacts)} support contacts for user '{username}':\n")
#             for c in contacts:
#                 print(f"  - {c.name} ({c.relationship}) | {c.email}")

# # 🔁 Replace with the username you registered
# check_support_contacts("laksha01")
# File: test_batches.py
from app import app, db
from db.models import User, UserRedZoneLog

def print_all_batches_for_user(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"No user found with username: {username}")
            return

        logs = (
            UserRedZoneLog.query
            .filter_by(user_id=user.id)
            .order_by(UserRedZoneLog.triggered_at.asc())
            .all()
        )

        if not logs:
            print(f"No logs found for user {username}")
            return

        print(f"Batch IDs for user {username}:")
        for log in logs:
            print(f"ID: {log.id}, Batch: {log.batch_id}, Escalated: {log.escalation_sent}, Time: {log.triggered_at}")

if __name__ == "__main__":
    print_all_batches_for_user("thea")
