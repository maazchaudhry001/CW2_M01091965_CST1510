import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

# --- PROTECT PAGE ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("⚙️ Settings")

st.write(f"Logged in user: **{st.session_state.username}**")

if st.button("Clear Session"):
    st.session_state.clear()
    st.success("Session cleared. Please restart the app.")
