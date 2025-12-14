import streamlit as st
from services.auth_manager import AuthenticationService
from services.database_manager import DatabaseManager

st.title("🔐 Login")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

db = DatabaseManager(DB_PATH)
auth = AuthenticationService(db)

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    user = auth.authenticate_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
        st.success(f"Welcome, {user.get_username()}!")
    else:
        st.error("Invalid username or password")
