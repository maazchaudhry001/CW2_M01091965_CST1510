# analytics.py

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Analytics", layout="wide")

# Authentication check
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You need to sign in to continue.")
    st.stop()

# Page title and intro
st.title("📈 Analytics Overview")
st.write(
    "This page gives a quick overview of key metrics and visualizations based on "
    "CSV files found in the project and the `it_tickets.csv` dataset."
)

# Top summary metrics
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Threats", 14, "+2")

    with col2:
        st.metric("Incidents Closed", 32, "+5")

    with col3:
        st.metric("Pending Tickets", 6, "-1")

# Simple sample line chart
sample_data = pd.DataFrame(
    {
        "Time": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "CPU Usage (%)": [45, 55, 70, 60, 50],
    }
)
st.subheader("CPU Usage Over the Week (Sample Data)")
st.line_chart(sample_data, x="Time", y="CPU Usage (%)")

st.divider()

# ---------------- CSV loading & visualisation ---------------- #

base_dir = Path(__file__).parents[1]
data_dir = base_dir / "DATA"

# Collect CSV files from project root
csv_files = sorted(base_dir.glob("*.csv"))

# Also include CSVs from DATA/ if it exists
if data_dir.exists():
    csv_files += sorted(data_dir.glob("*.csv"))

# Remove duplicates and limit to maximum 3 CSVs
csv_files = list(dict.fromkeys(csv_files))[:3]

if not csv_files:
    st.warning("No CSV files found in project root or DATA/ folder.")
else:
    st.subheader("CSV Visualizations")
    st.caption("Up to 3 CSV files are loaded automatically. You can choose how to display each file.")

    for fp in csv_files:
        st.markdown(f"### 📄 {fp.name}")

        # Safely load CSV
        try:
            df = pd.read_csv(fp)
        except Exception as e:
            st.error(f"Failed to read {fp.name}: {e}")
            continue

        # Detect column types
        num_cols = list(df.select_dtypes(include="number").columns)
        cat_cols = list(df.select_dtypes(include="object").columns)
        dt_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

        # Try to detect/parse date/time columns if none detected
        if not dt_cols:
            for c in df.columns:
                if "date" in c.lower() or "time" in c.lower():
                    try:
                        df[c] = pd.to_datetime(df[c], errors="coerce")
                        if df[c].notna().any():
                            dt_cols.append(c)
                            break
                    except Exception:
                        continue

        # Choose visualization type
        viz_type = st.selectbox(
            f"Visualization type for {fp.name}",
            ["Table", "Bar", "Pie"],
            key=f"viz_{fp.name}",
        )

        # ---------- TABLE VIEW ----------
        if viz_type == "Table":
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Showing first 10 rows — total: {len(df)} rows × {len(df.columns)} columns.")
            continue

        # ---------- BAR CHART ----------
        if viz_type == "Bar":
            if cat_cols and num_cols:
                x_choice = st.selectbox(
                    "Select categorical column (X-axis)",
                    cat_cols,
                    key=f"bar_x_{fp.name}",
                )
                y_choice = st.selectbox(
                    "Select numeric column (Y-axis)",
                    num_cols,
                    key=f"bar_y_{fp.name}",
                )

                agg = df.groupby(x_choice)[y_choice].sum().reset_index()
                st.write(f"**Bar chart: {y_choice} by {x_choice}**")
                st.bar_chart(agg, x=x_choice, y=y_choice)

            elif num_cols:
                # If there is no categorical column, just plot the first numeric
                y_choice = num_cols[0]
                st.write(f"**Bar chart: {y_choice}**")
                st.bar_chart(df, y=y_choice)

            else:
                st.info("No numeric data available for a bar chart — showing a table instead.")
                st.dataframe(df.head(10), use_container_width=True)

            continue

        # ---------- “PIE” OPTION (shown as BAR) ----------
        if viz_type == "Pie":
            # Case 1: category + numeric → show bar of sums
            if cat_cols and num_cols:
                label_col = st.selectbox(
                    "Select category column (labels)",
                    cat_cols,
                    key=f"pie_label_{fp.name}",
                )
                value_col = st.selectbox(
                    "Select numeric column (values)",
                    num_cols,
                    key=f"pie_value_{fp.name}",
                )

                agg = df.groupby(label_col)[value_col].sum().reset_index()
                st.write(f"**(Bar representation of pie): {value_col} by {label_col}**")
                st.bar_chart(agg, x=label_col, y=value_col)

            # Case 2: only category → show bar of counts
            elif cat_cols:
                label_col = st.selectbox(
                    "Select category column (labels)",
                    cat_cols,
                    key=f"pie_label_counts_{fp.name}",
                )

                counts = df[label_col].value_counts().reset_index()
                counts.columns = [label_col, "count"]

                st.write(f"**(Bar representation of pie): counts by {label_col}**")
                st.bar_chart(counts, x=label_col, y="count")

            # Case 3: nothing suitable
            else:
                st.info("No suitable categorical column for this chart — showing a table instead.")
                st.dataframe(df.head(10), use_container_width=True)

            continue

# ---------------- Extra visuals from DATA/it_tickets.csv ---------------- #

tickets_path = base_dir / "DATA" / "it_tickets.csv"

if tickets_path.exists():
    try:
        tickets = pd.read_csv(
            tickets_path,
            parse_dates=["created_date", "resolved_date"],
        )

        st.divider()
        st.subheader("Additional Visualizations from it_tickets.csv")

        # 1) Tickets by Priority
        if "priority" in tickets.columns:
            st.markdown("#### Tickets by Priority")
            prio_counts = tickets["priority"].fillna("N/A").value_counts().reset_index()
            prio_counts.columns = ["priority", "count"]
            st.bar_chart(prio_counts, x="priority", y="count")

        # 2) Status by Priority
        if {"status", "priority"}.issubset(tickets.columns):
            st.markdown("#### Ticket Status by Priority (Table + Bar)")

            status_prio = (
                tickets.fillna("N/A")
                .groupby(["status", "priority"])
                .size()
                .reset_index(name="count")
            )
            st.dataframe(status_prio, use_container_width=True)

            status_counts = (
                tickets["status"].fillna("N/A").value_counts().reset_index()
            )
            status_counts.columns = ["status", "count"]
            st.bar_chart(status_counts, x="status", y="count")

        # 3) Tickets Created Per Month
        if "created_date" in tickets.columns:
            tickets["created_date"] = pd.to_datetime(
                tickets["created_date"],
                errors="coerce",
            )

            ts = tickets.dropna(subset=["created_date"]).copy()
            if not ts.empty:
                ts["month"] = ts["created_date"].dt.to_period("M").astype(str)
                monthly_counts = ts.groupby("month").size().reset_index(name="count")

                st.markdown("#### Tickets Created Per Month")
                st.line_chart(monthly_counts, x="month", y="count")

        # 4) Assigned-To Distribution
        if "assigned_to" in tickets.columns:
            st.markdown("#### Assigned-To Distribution")
            assigned_counts = (
                tickets["assigned_to"]
                .fillna("Unassigned")
                .value_counts()
                .reset_index()
            )
            assigned_counts.columns = ["assigned_to", "count"]
            st.bar_chart(assigned_counts, x="assigned_to", y="count")

    except Exception as e:
        st.error(f"Failed to build additional visuals from {tickets_path.name}: {e}")
else:
    st.info("Additional graphs skipped: DATA/it_tickets.csv not found.")
