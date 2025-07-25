# # # verify_user_ids.py

# # # from app import app  # imports the Flask app instance with DB initialized
# # # from db.models import User, Session, JournalThread
# # # from sqlalchemy import asc

# # # print("🔎 Verifying per-user session and thread numbering...")

# # # with app.app_context():  # ✅ Push app context
# # #     users = User.query.all()
# # #     issues_found = False

# # #     for user in users:
# # #         print(f"\n👤 User ID {user.id} ({user.username}):")

# # #         # === Check sessions ===
# # #         sessions = Session.query.filter_by(user_id=user.id).order_by(asc(Session.start_time)).all()
# # #         expected_session_number = 1
# # #         for s in sessions:
# # #             if s.user_session_number != expected_session_number:
# # #                 print(f"❌ Session ID {s.id} has user_session_number={s.user_session_number}, expected {expected_session_number}")
# # #                 issues_found = True
# # #             expected_session_number += 1
# # #         if not sessions:
# # #             print("⚠️ No sessions found.")

# # #         # === Check threads ===
# # #         threads = JournalThread.query.filter_by(user_id=user.id).order_by(asc(JournalThread.created_at)).all()
# # #         expected_thread_number = 1
# # #         for t in threads:
# # #             if t.user_thread_number != expected_thread_number:
# # #                 print(f"❌ Thread ID {t.id} has user_thread_number={t.user_thread_number}, expected {expected_thread_number}")
# # #                 issues_found = True
# # #             expected_thread_number += 1
# # #         if not threads:
# # #             print("⚠️ No threads found.")

# # #     if not issues_found:
# # #         print("\n✅ All session and thread IDs verified successfully.")
# # #     else:
# # #         print("\n⚠️ Some mismatches were found.")


# # # filename: check_session_thread_ids.py

# # # from app import app
# # # from db.models import User, Session, JournalThread
# # # from db.connection import db

# # # with app.app_context():
# # #     user = User.query.filter_by(username="Laksha").first()
# # #     if not user:
# # #         print("User 'Laksha' not found.")
# # #     else:
# # #         print(f"\n🧠 Sessions for {user.username}:")
# # #         sessions = Session.query.filter_by(user_id=user.id).order_by(Session.start_time).all()
# # #         for session in sessions:
# # #             print(f"Session #{session.user_session_number} (DB ID: {session.id}) — Started: {session.start_time}")

# # #         print(f"\n🧵 Threads for {user.username}:")
# # #         threads = JournalThread.query.filter_by(user_id=user.id).order_by(JournalThread.created_at).all()
# # #         for thread in threads:
# # #             print(f"Thread #{thread.user_thread_number} (DB ID: {thread.id}) — Created: {thread.created_at}")


# # from app import app
# # from db.models import User, Session, JournalThread

# # def verify_existing_ids(username="testuser2"):
# #     with app.app_context():
# #         user = User.query.filter_by(username=username).first()
# #         if not user:
# #             print(f"❌ User '{username}' not found.")
# #             return

# #         print(f"\n📊 Verifying session and thread IDs for user: {username} (user_id = {user.id})")

# #         # Print sessions
# #         sessions = Session.query.filter_by(user_id=user.id).order_by(Session.start_time).all()
# #         if not sessions:
# #             print("⚠️ No sessions found.")
# #         else:
# #             print(f"\n🧠 Sessions:")
# #             for session in sessions:
# #                 print(f"  - DB ID: {session.id}, user_session_number: {session.user_session_number}, start_time: {session.start_time}")

# #         # Print threads
# #         threads = JournalThread.query.filter_by(user_id=user.id).order_by(JournalThread.id).all()
# #         if not threads:
# #             print("⚠️ No threads found.")
# #         else:
# #             print(f"\n🧵 Threads:")
# #             for thread in threads:
# #                 session = Session.query.get(thread.session_id)
# #                 print(f"  - DB ID: {thread.id}, user_thread_number: {thread.user_thread_number}, user_session_number: {session.user_session_number}")


# # if __name__ == "__main__":
# #     verify_existing_ids()


# import streamlit as st

# st.title("📘 Emotional Arc")

# st.markdown("Each session reveals a journey — let's see how your emotions evolved.")

# st.markdown("### 🎭 Explore Your Emotional Patterns")

# view_option = st.selectbox(
#     "Choose what to explore:",
#     ["Overall Emotional View", "Entry-Level View"],
#     index=0,
#     key="emotion_view_toggle"
# )

# st.write(f"You selected: {view_option}")

# from db.connection import db
# from db.models import User, Session
# from app import app  # ✅ Import your Flask app instance

# with app.app_context():  # ✅ Push the application context
#     users = User.query.all()

#     for user in users:
#         sessions = (
#             Session.query.filter_by(user_id=user.id)
#             .order_by(Session.start_time.asc())  # You can also use .id.asc() if start_time is missing
#             .all()
#         )

#         for i, session in enumerate(sessions, start=1):
#             session.user_session_number = i
#             print(f"User {user.id} → Session {session.id} → Assigned number: {i}")

#     db.session.commit()
#     print("✅ All session numbers updated.")
from db.connection import db
from db.models import User, Session, JournalThread
from app import app  # Your Flask app

with app.app_context():
    users = User.query.all()

    for user in users:
        sessions = (
            Session.query
            .filter_by(user_id=user.id)
            .order_by(Session.user_session_number.asc())
            .all()
        )

        print(f"\n🧪 User {user.id} ({user.username}) has {len(sessions)} sessions:")
        for session in sessions:
            print(f"  - Session ID: {session.id}, Number: {session.user_session_number}")

            # Fetch all journal threads for this session
            threads = (
                JournalThread.query
                .filter_by(session_id=session.id)
                .order_by(JournalThread.user_thread_number.asc())
                .all()
            )

            if threads:
                for thread in threads:
                    print(f"      • Thread ID: {thread.id}, Number: {thread.user_thread_number}")
            else:
                print("      ⚠️ No threads found for this session.")

        # Optional: Check session numbering continuity
        expected_session_numbers = list(range(1, len(sessions) + 1))
        actual_session_numbers = [s.user_session_number for s in sessions]

        if expected_session_numbers != actual_session_numbers:
            print(f"❌ User {user.id} → Mismatch in session numbering!")
            print(f"Expected: {expected_session_numbers}")
            print(f"Actual:   {actual_session_numbers}")
        else:
            print(f"✅ User {user.id} → Session numbers correctly assigned.")

        # Optional: Check thread numbering continuity per session
        for session in sessions:
            threads = (
                JournalThread.query
                .filter_by(session_id=session.id)
                .order_by(JournalThread.user_thread_number.asc())
                .all()
            )
            if threads:
                expected_thread_numbers = list(range(1, len(threads) + 1))
                actual_thread_numbers = [t.user_thread_number for t in threads]
                if expected_thread_numbers != actual_thread_numbers:
                    print(f"❌ Session {session.id} → Mismatch in thread numbering!")
                    print(f"Expected: {expected_thread_numbers}")
                    print(f"Actual:   {actual_thread_numbers}")
                else:
                    print(f"✅ Session {session.id} → Thread numbers correctly assigned.")
