import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analytics", layout="wide")

# --- PROTECT PAGE ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("📈 Analytics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Threats", 14, "+2")

with col2:
    st.metric("Resolved Incidents", 32, "+5")

with col3:
    st.metric("Open Tickets", 6, "-1")

data = pd.DataFrame({
    "Time": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "CPU Usage": [45, 55, 70, 60, 50]
})

st.line_chart(data, x="Time", y="CPU Usage")
