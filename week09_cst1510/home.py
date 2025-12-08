import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"   # or "analyst" / "admin" later


login_tab, register_tab = st.tabs(["Login", "Register"])

with login_tab:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.session_state.users
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password")

with register_tab:
    st.subheader("Register")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not new_user or not new_pass:
            st.warning("All fields are required.")
        elif new_pass != confirm:
            st.error("Passwords do not match.")
        elif new_user in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created! Now go to Login tab.")
