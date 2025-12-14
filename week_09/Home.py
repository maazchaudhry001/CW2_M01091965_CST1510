import streamlit as st
import json
import os

st.set_page_config(page_title="Login", layout="centered")

USERS_FILE = "users.json"

def logout():
    """Clears the session state to log the user out."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users_dict):
    with open(USERS_FILE, "w") as file:
        json.dump(users_dict, file, indent=4)

persistent_users = load_users()

# session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# simple page header (replaces the 🔐 text)
st.title("Login Portal")
st.write("Please sign in or create an account to continue.")

# if already logged in, show message + logout only
if st.session_state.logged_in:
    st.info(f"Welcome back, **{st.session_state.username}**! You are already signed in.")
    if st.button("Log Out"):
        logout()
    st.stop()

# tabs for login and registration
login_tab, register_tab = st.tabs(["Log In", "Sign Up"])

# LOGIN
with login_tab:
    st.subheader("Log In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if username in persistent_users and persistent_users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("You are now logged in!")
            st.rerun()
        else:
            st.error("Incorrect username or password.")

# REGISTER
with register_tab:
    st.subheader("Create an Account")

    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm = st.text_input("Re-enter Password", type="password")

    if st.button("Register"):
        if not new_user or not new_pass:
            st.warning("Please fill in all fields.")
        elif new_pass != confirm:
            st.error("Passwords do not match.")
        elif new_user in persistent_users:
            st.error("That username already exists.")
        else:
            persistent_users[new_user] = new_pass
            save_users(persistent_users)
            st.success("Account created successfully! Switch to the Log In tab to sign in.")
