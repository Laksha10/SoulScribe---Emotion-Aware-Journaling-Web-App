# File: streamlit_ui/pages/Logout.py

import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Logout – SoulScribe", layout="centered")

# --- CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

        .stApp {
            background-color: #fefae0;
            color: #3c3c3c;
            font-family: 'Quicksand', sans-serif;
        }

        .logout-box {
            background-color: #fffaf2;
            border: 1px solid #d3cce3;
            padding: 2rem 2.5rem;
            border-radius: 12px;
            max-width: 500px;
            margin: auto;
            text-align: center;
        }

        .logout-title {
            font-size: 2rem;
            font-weight: 700;
            color: #b497d6;
            margin-bottom: 1.5rem;
        }

        .logout-message {
            font-size: 1.1rem;
            color: #5f5f5f;
            font-weight: 500;
            text-align: center;
            line-height: 1.6;
            margin-top: 0.5rem;
            margin-bottom: 2.5rem;
        }

        .stButton > button {
            background-color: #e0c3fc !important;
            color: #3c3c3c !important;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1.5rem;
        }

        .stButton > button:hover {
            background-color: #d1b3ff !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.markdown("<div class='logout-box'>", unsafe_allow_html=True)
st.markdown("""
    <h2 style='
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #b497d6;
        margin-bottom: 1.5rem;
        font-family: sans-serif;
    '>👋 Logout</h2>
""", unsafe_allow_html=True)



st.markdown("""
    <div class='logout-message'>
        You’ve made space for your emotions today — and that’s enough. <br>
        SoulScribe is always here when you need to write your heart out again. 💜
    </div>
""", unsafe_allow_html=True)

if st.button("Confirm Logout"):
    st.session_state.jwt_token = None
    st.success("✅ You’ve been logged out.")
    st.markdown("Redirecting to Home...")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
