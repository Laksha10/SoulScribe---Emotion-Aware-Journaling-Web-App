import streamlit as st

def show_header():
    st.markdown("""
        <style>
            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #e0c3fc;
                padding: 0.8rem 1.2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
            }
            .app-title {
                font-size: 1.6rem;
                font-weight: 700;
                color: white;
            }
            .nav-buttons {
                display: flex;
                gap: 0.8rem;
            }
            .nav-buttons button {
                background-color: #fffaf2;
                color: #3c3c3c;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 0.4rem 1rem;
                cursor: pointer;
            }
            .nav-buttons button:hover {
                background-color: #f2e7ff;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logic for buttons based on login status
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<div class="app-title">SoulScribe</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)

    if "jwt_token" in st.session_state and st.session_state.jwt_token:
        if st.button("Logout"):
            st.session_state.jwt_token = None
            st.session_state.conversation = []
            st.session_state.thread_id = None
            st.session_state.last_emotions = []
            st.rerun()
    else:
        if st.button("Login"):
            st.switch_page("pages/login.py")  # ✅ Just the page title, no path or extension
        if st.button("Register"):
            st.switch_page("pages/register.py")

    st.markdown('</div></div>', unsafe_allow_html=True)
