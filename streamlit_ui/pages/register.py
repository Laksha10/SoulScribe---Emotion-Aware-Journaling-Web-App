# File: streamlit_ui/pages/Register.py

import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Register – SoulScribe", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

        .stApp {
            background-color: #fefae0;
            color: #3c3c3c;
            font-family: 'Quicksand', sans-serif;
        }

        .register-box {
            background-color: #fffaf2;
            border: 1px solid #d3cce3;
            padding: 2rem;
            border-radius: 12px;
            max-width: 400px;
            margin: auto;
        }

        .register-title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 700;
            color: #b497d6;
            margin-bottom: 1rem;
        }

        .stButton > button {
            background-color: #e0c3fc !important;
            color: #3c3c3c !important;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1.5rem;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #d1b3ff !important;
        }

        .login-link {
            text-align: center;
            margin-top: 1rem;
            color: #7a6fa3;
            cursor: pointer;
            font-weight: 600;
        }

        .login-link:hover {
            text-align: center;
            color: #b497d6;
            text-decoration: underline;
        }

        label, .stTextInput label, .stPasswordInput label {
            color: #b497d6 !important;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI Content ---
st.markdown("<div class='register-box'>", unsafe_allow_html=True)
st.markdown("<div class='register-title'>📝 Create your SoulScribe Account</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

username = st.text_input(
    label="👤 Choose a username",
    placeholder="Type here...",
    key="reg_username",
    label_visibility="visible"
)

email = st.text_input(
    label="📧 Your email",
    placeholder="Type here...",
    key="reg_email",
    label_visibility="visible"
)

password = st.text_input(
    label="🔐 Create a password",
    placeholder="Type here...",
    type="password",
    key="reg_password",
    label_visibility="visible"
)
st.markdown("---")
# Styled Subheader for Support Contacts
# Support Contacts Instructions
st.markdown("""
    <h4 style='color: #b497d6; font-weight: 700; margin-top: 2rem;'>📞 Add Support Contacts</h4>
    <p style='color: #b497d6; font-size: 15px; font-weight: 500;'>
        Add people you trust. We'll notify them only during repeated signs of emotional distress.<br>
        <strong>All fields are required — Name, Relation, and Email.</strong>
    </p>
""", unsafe_allow_html=True)
# Global expander styling
# EXPANDER STYLING FIX FOR BACKGROUND
st.markdown("""
    <style>
    /* Expander container */
    div[data-testid="stExpander"] {
        background-color: #fefae0 !important;  /* soft neutral */
        border: 1.5px solid #d3cce3;
        border-radius: 6px;
        padding: 6px 10px;
        margin-bottom: 0.75rem;
    }

    /* Expander header text (Contact 1 / Contact 2) */
    div[data-testid="stExpander"] summary {
        color: #b497d6 !important;  /* Lavender */
        font-weight: 700;
        font-size: 15px;
    }

    /* Optional: tighten vertical spacing inside the box */
    div[data-testid="stExpander"] > div {
        padding-top: 0.75rem;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


# Support Contacts Expanders with styled box
support_contacts = []
for i in range(2):
    with st.expander(f"📇 Contact {i + 1}"):
        name = st.text_input("Name", key=f"contact_name_{i}")
        relation = st.text_input("Relation", key=f"contact_relation_{i}")
        email_c = st.text_input("Email", key=f"contact_email_{i}")

        if name and relation and email_c:
            support_contacts.append({
                "name": name,
                "relationship": relation,
                "email": email_c
            })




# Coping Activities Section
st.markdown("""
    <h4 style='color: #b497d6; font-weight: 700; margin-top: 2rem;'>🧘 Add Coping Activities</h4>
    <p style='color: #b497d6; font-size: 15px; font-weight: 500;'>
        These are comforting strategies you can turn to. SoulScribe will suggest them during difficult moments.<br>
        <em style='color: #b497d6;'>This is optional. Write one activity per line.</em>
    </p>
""", unsafe_allow_html=True)

coping_activities = st.text_area(
    "Coping Activities",
    placeholder="Go for a walk\nTalk to a friend\nWrite in journal",
    key="reg_coping"
)
coping_list = [act.strip() for act in coping_activities.split("\n") if act.strip()]

ok_to_notify = st.checkbox(
    "✅ Allow SoulScribe to notify my support contact during emotional emergencies",
    value=True,
    help="We’ll only notify them if repeated signs of emotional distress are detected."
)

register_url = "http://localhost:5050/auth/register"

if st.button("Register", key="register_btn"):
    if not username or not password or not email.strip():
        st.markdown("""
            <div style='background-color: #fff3cd; color: #664d03;
            border-left: 5px solid #ffecb5; padding: 1rem;
            border-radius: 8px; font-weight: 600; margin-top: 1rem;'>
            ⚠️ Username, email, and password are required.
            </div>
        """, unsafe_allow_html=True)
    else:
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "support_contacts": support_contacts,
            "coping_activities": coping_list,
            "ok_to_notify": ok_to_notify
        }

        try:
            response = requests.post(register_url, json=payload)

            if response.status_code == 201:
                st.markdown("""
                    <div style='background-color: #fcd5ce; color: #2e2e38;
                    border-left: 5px solid #e29578; padding: 1rem;
                    border-radius: 8px; font-weight: 600; margin-top: 1rem;'>
                    🎉 Registration successful! You can now log in.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background-color: #f8d7da; color: #842029;
                    border-left: 5px solid #f5c2c7; padding: 1rem;
                    border-radius: 8px; font-weight: 600; margin-top: 1rem;'>
                    ❌ Registration failed: {response.json().get('error', 'Unknown error')}
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
                <div style='background-color: #f8d7da; color: #842029;
                border-left: 5px solid #f5c2c7; padding: 1rem;
                border-radius: 8px; font-weight: 600; margin-top: 1rem;'>
                ⚠️ Network error: {str(e)}
                </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button("🔐 Already have an account? Log in here.", "login")
