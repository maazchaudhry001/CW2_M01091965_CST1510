import streamlit as st
# Later you will import your Week 8 functions like this:
# from app.data.db import connect_database
# from app.data.incidents import get_all_incidents

st.set_page_config(page_title="Dashboard", layout="wide")

# ---------- PROTECT PAGE ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must login to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

# ---------- HEADER ----------
st.title(f"Welcome, {st.session_state.username}")
st.caption(f"Role: {st.session_state.role}")

# ---------- LOGOUT BUTTON ----------
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")

st.subheader("System Overview")

# ---------- TEMP VALUES (until DB is connected) ----------
active_incidents = 0
resolved_incidents = 0

# When your Week 8 DB is ready, you can do:
# conn = connect_database("DATA/intelligence_platform.db")
# df_incidents = get_all_incidents(conn)
# if not df_incidents.empty:
#     active_incidents = len(df_incidents[df_incidents["status"] != "Closed"])
#     resolved_incidents = len(df_incidents[df_incidents["status"] == "Closed"])

col1, col2, col3 = st.columns(3)
col1.metric("System Status", "Online", "Stable")
col2.metric("Active Incidents", active_incidents)
col3.metric("Resolved Incidents", resolved_incidents)

st.divider()
st.info("Navigate to **Analytics** for charts or **Settings** to manage records.")
