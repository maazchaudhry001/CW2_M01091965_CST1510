import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Dashboard", layout="wide")

# Basic access control – only allow page if logged in
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("Access restricted. Please log in to your account to continue.")
    if st.button("Go Back to Login"):
        st.switch_page("Home.py")
    st.stop()

# Header row: title on the left, sign-out on the right
header_left, header_right = st.columns([8, 2])

with header_left:
    st.markdown("### 🚀 System Control Dashboard")

with header_right:
    st.write("")  # spacer
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.info("Bye, You have been logged out successfully.")
        st.switch_page("Home.py")

# Red welcome banner
st.markdown(
    f"""
    <div style="
        background-color:#b91c1c;
        padding:14px 18px;
        border-radius:10px;
        margin-top:10px;
        margin-bottom:10px;
        color:white;
        font-weight:600;
        font-size:16px;
    ">
        ✅ Welcome back, {st.session_state.username}! You are now logged in successfully.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("This is your Week 09 workspace where you can view and explore your data.")
st.divider()

# Find CSV files in project root and DATA folder
base_dir = Path(__file__).parents[1]
csv_files = []

csv_files += sorted(base_dir.glob("*.csv"))
data_dir = base_dir / "DATA"
if data_dir.exists():
    csv_files += sorted(data_dir.glob("*.csv"))

# Remove duplicates but keep order
seen = set()
csv_files = [p for p in csv_files if not (p in seen or seen.add(p))]

st.subheader("Available CSV Data Files")

if not csv_files:
    st.info("No CSV files were found in the main folder or the DATA directory.")
    st.stop()

# 1) FILE SELECTOR
file_names = [p.name for p in csv_files]
selected_name = st.selectbox("Choose a data file to explore:", file_names)
selected_path = dict(zip(file_names, csv_files))[selected_name]

st.caption(f"Path: {selected_path}")

# Read the selected CSV
try:
    df = pd.read_csv(selected_path)
except Exception as e:
    st.error(f"Unable to read {selected_name}: {e}")
    st.stop()

# 2) KPI CARDS – simple stats that are easy to explain
total_rows = len(df)
total_cols = len(df.columns)

# These depend on the columns actually existing
open_count = None
critical_count = None

if "status" in df.columns:
    open_count = (df["status"].astype(str).str.lower() == "open").sum()

if "severity" in df.columns:
    critical_count = df["severity"].astype(str).str.lower().isin(["high", "critical"]).sum()

k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Total rows", total_rows)
with k2:
    if open_count is not None:
        st.metric("Open incidents", int(open_count))
    else:
        st.metric("Open incidents", "N/A")
with k3:
    if critical_count is not None:
        st.metric("High/Critical incidents", int(critical_count))
    else:
        st.metric("High/Critical incidents", "N/A")

st.divider()

# 3) SIMPLE FILTERS – only shown if columns exist
with st.expander("Filters", expanded=False):
    severity_filter = None
    status_filter = None

    if "severity" in df.columns:
        severities = sorted(df["severity"].dropna().astype(str).unique())
        severities = ["All"] + severities
        severity_filter = st.selectbox("Filter by severity", severities, index=0)

    if "status" in df.columns:
        statuses = sorted(df["status"].dropna().astype(str).unique())
        statuses = ["All"] + statuses
        status_filter = st.selectbox("Filter by status", statuses, index=0)

# Apply filters (only if selected and column exists)
filtered_df = df.copy()

if severity_filter and severity_filter != "All" and "severity" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["severity"].astype(str) == severity_filter]

if status_filter and status_filter != "All" and "status" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["status"].astype(str) == status_filter]

# Two-column layout: left = data preview, right = summary
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("**Preview of filtered data (first 10 rows)**")
    st.dataframe(filtered_df.head(10), use_container_width=True)

with right_col:
    st.markdown("**Filtered overview**")
    st.write(f"- Rows after filters: **{len(filtered_df)}**")
    st.write(f"- Columns: **{len(filtered_df.columns)}**")
    st.write("- Columns:")
    st.write(", ".join(map(str, filtered_df.columns)))

    try:
        summary = filtered_df.describe(include="all").transpose().fillna("")
        st.markdown("**Summary (numeric & categorical)**")
        st.dataframe(summary, use_container_width=True)
    except Exception:
        pass
