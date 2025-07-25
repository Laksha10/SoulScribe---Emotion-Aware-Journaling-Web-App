# File: streamlit_ui/pages/Login.py

import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Login – SoulScribe", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

        .stApp {
            background-color: #fefae0;
            color: #3c3c3c;
            font-family: 'Quicksand', sans-serif;
        }

        .login-box {
            background-color: #fffaf2;
            border: 1px solid #d3cce3;
            padding: 2rem;
            border-radius: 12px;
            max-width: 400px;
            margin: auto;
        }

        .login-title {
            text-align: center;
            font-size: 2rem;
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

        .register-link {
            text-align: center;
            margin-top: 1rem;
            color: #7a6fa3;
            cursor: pointer;
            font-weight: 600;
        }

        .register-link:hover {
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
st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.markdown("<div class='login-title'>🔐 Login to SoulScribe</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

username = st.text_input(
    label="👤 Username",
    placeholder="Type your username...",
    key="login_username",
    label_visibility="visible"
)

password = st.text_input(
    label="🔐 Password",
    placeholder="Type your password...",
    type="password",
    key="login_password",
    label_visibility="visible"
)

login_url = "http://localhost:5050/auth/login"

if st.button("Log In"):
    if not username or not password:
        st.markdown("""
            <div style='
                background-color: #fff3cd;
                color: #664d03;
                border-left: 5px solid #ffecb5;
                padding: 1rem;
                border-radius: 8px;
                font-weight: 600;
                margin-top: 1rem;
            '>
            ⚠️ Username, email, and password are required.
            </div>
        """, unsafe_allow_html=True)
    else:
        try:
            response = requests.post(login_url, json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                res_json = response.json()
                st.session_state.jwt_token = res_json.get("token")
                st.session_state.user_id = res_json.get("user_id")
                st.session_state.session_id = res_json.get("session_id")

                if st.session_state.jwt_token:
                    st.markdown("""
                        <div style='
                            background-color: #e0c3fc;
                            color: #3c3c3c;
                            border-left: 5px solid #b497d6;
                            padding: 1rem;
                            border-radius: 8px;
                            font-weight: 600;
                            margin-top: 1rem;
                        '>
                        ✅ Logged in successfully!
                        </div>
                    """, unsafe_allow_html=True)
                    st.switch_page("pages/Journal.py")
                else:
                    st.markdown("""
                        <div style='
                            background-color: #fcd5ce;
                            color: #3c3c3c;
                            border-left: 5px solid #b497d6;
                            padding: 1rem;
                            border-radius: 8px;
                            font-weight: 600;
                            margin-top: 1rem;
                        '>
                        ❌ Token not received from server.
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='
                        background-color: #fcd5ce;
                        color: #3c3c3c;
                        border-left: 5px solid #b497d6;
                        padding: 1rem;
                        border-radius: 8px;
                        font-weight: 600;
                        margin-top: 1rem;
                    '>
                    ❌ Invalid username or password.
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
                <div style='
                    background-color: #fcd5ce;
                    color: #3c3c3c;
                    border-left: 5px solid #b497d6;
                    padding: 1rem;
                    border-radius: 8px;
                    font-weight: 600;
                    margin-top: 1rem;
                '>
                ⚠️ Network error: {str(e)}
                </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Register Redirect ---
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button("📝 Don't have an account? Create one", "register")
