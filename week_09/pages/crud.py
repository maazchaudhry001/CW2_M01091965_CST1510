# crud.py

import streamlit as st
from datetime import date, datetime

st.set_page_config(page_title="Data Management (CRUD)", layout="wide")

# ---------- ACCESS CONTROL ----------
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("Access denied. Please log in first.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

# ---------- PAGE HEADER ----------
st.title("📦 Data Management (CRUD)")
st.caption(
    "Create, read, update and delete records across incidents, tickets and cyber incidents. "
    "Now with date & day metadata for easier reporting."
)
st.divider()

# ---------- TOP SUMMARY (OPTIONAL METRICS) ----------
col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.metric("📕 Total Incidents", "N/A")
with col_m2:
    st.metric("🎟 Total Tickets", "N/A")
with col_m3:
    st.metric("🛡 Cyber Incidents", "N/A")

st.caption("You can later connect these metrics to your database / CSV counts for live stats.")
st.divider()

# ---------- TABS ----------
tabs = st.tabs(
    ["🚨 Incidents (DB)", "🎟 Tickets (CSV)", "🛡 Cyber Incidents (DB)", "📊 Recent Records Overview"]
)

today = date.today()
current_time = datetime.now().time()


# =========================================================
# TAB 1 – INCIDENTS (DB)
# =========================================================
with tabs[0]:
    st.subheader("🚨 Incidents (DB) – Quick Actions")
    st.write("Add or delete incidents. Date and day are captured for better analysis.")

    left, right = st.columns((2.2, 1.3))

    # ------- LEFT: ADD INCIDENT -------
    with left:
        st.markdown("### ➕ Add New Incident")

        inc_title = st.text_input("Title", key="inc_title")

        inc_severity = st.selectbox(
            "Severity",
            ["low", "medium", "high", "critical"],
            index=1,
            key="inc_severity",
        )

        inc_status = st.selectbox(
            "Status",
            ["open", "in progress", "closed"],
            index=0,
            key="inc_status",
        )

        # NEW FIELDS: date & day
        inc_date = st.date_input("Incident Date", value=today, key="inc_date")
        inc_time = st.time_input("Incident Time", value=current_time, key="inc_time")

        inc_day_of_week = inc_date.strftime("%A")
        st.text_input(
            "Day of Week (auto)",
            value=inc_day_of_week,
            disabled=True,
            key="inc_day_of_week",
        )

        st.caption(
            "💡 *Date and day are for your reporting. If your DB only stores title/severity/status, "
            "you can still explain that you collected this for analysis but did not persist it yet.*"
        )

        if st.button("Add Incident", type="primary", use_container_width=True):
            # If you already have a function like: add_incident(title, severity, status)
            # you can still call it here.
            try:
                # Example if you want to keep DB schema the same:
                #   - we append date/day to the title so we don't change DB columns
                title_for_db = f"{inc_title} ({inc_date} - {inc_day_of_week})"

                add_incident(title_for_db, inc_severity, inc_status)  # <-- YOUR FUNCTION
                st.success("Incident added successfully.")
            except NameError:
                st.warning(
                    "⚠ Button works, but I couldn't find your `add_incident(...)` function.\n\n"
                    "Keep your original function and call it here instead of this placeholder."
                )
            except Exception as e:
                st.error(f"Error while adding incident: {e}")

    # ------- RIGHT: DELETE / FILTER -------
    with right:
        st.markdown("### 🗑 Delete / Quick Filters")

        delete_id = st.number_input(
            "Incident ID to delete",
            min_value=1,
            step=1,
            key="inc_delete_id",
        )
        if st.button("Delete Incident", use_container_width=True):
            try:
                delete_incident(delete_id)  # <-- YOUR FUNCTION
                st.success(f"Incident with ID {delete_id} deleted.")
            except NameError:
                st.warning(
                    "⚠ Could not find `delete_incident(...)`. Keep your old delete logic and call it here."
                )
            except Exception as e:
                st.error(f"Error while deleting incident: {e}")

        st.markdown("#### 🔍 Optional Filters (Display Only)")
        f_sev = st.multiselect(
            "Filter by Severity", ["low", "medium", "high", "critical"], default=["high", "critical"]
        )
        f_status = st.multiselect(
            "Filter by Status", ["open", "in progress", "closed"], default=["open"]
        )
        st.caption(
            "You can connect these filters to your `get_all_incidents()` query later to show filtered tables."
        )


# =========================================================
# TAB 2 – TICKETS (CSV)
# =========================================================
with tabs[1]:
    st.subheader("🎟 Tickets (CSV) – Quick Actions")

    left, right = st.columns((2.2, 1.3))

    # ------- LEFT: ADD TICKET -------
    with left:
        st.markdown("### ➕ Add Ticket")

        t_title = st.text_input("Title", key="ticket_title")

        t_severity = st.selectbox(
            "Severity",
            ["low", "medium", "high", "critical"],
            index=1,
            key="ticket_severity",
        )

        t_status = st.selectbox(
            "Status",
            ["open", "in progress", "closed"],
            index=0,
            key="ticket_status",
        )

        # NEW FIELDS
        t_date = st.date_input("Ticket Date", value=today, key="ticket_date")
        t_time = st.time_input("Ticket Time", value=current_time, key="ticket_time")
        t_day_of_week = t_date.strftime("%A")
        st.text_input(
            "Day of Week (auto)",
            value=t_day_of_week,
            disabled=True,
            key="ticket_day_of_week",
        )

        if st.button("Add Ticket", type="primary", use_container_width=True):
            try:
                # Example: if your CSV only has title, severity, status:
                title_for_csv = f"{t_title} ({t_date} - {t_day_of_week})"
                add_ticket_to_csv(title_for_csv, t_severity, t_status)  # <-- YOUR FUNCTION
                st.success("Ticket added to CSV.")
            except NameError:
                st.warning(
                    "⚠ Couldn't find `add_ticket_to_csv(...)`. Plug your existing CSV logic into this button."
                )
            except Exception as e:
                st.error(f"Error while adding ticket: {e}")

    # ------- RIGHT: DELETE TICKET -------
    with right:
        st.markdown("### 🗑 Delete Ticket")

        ticket_delete_id = st.number_input(
            "Ticket ID to delete", min_value=1, step=1, key="ticket_delete_id"
        )

        if st.button("Delete Ticket", use_container_width=True):
            try:
                delete_ticket_from_csv(ticket_delete_id)  # <-- YOUR FUNCTION
                st.success(f"Ticket with ID {ticket_delete_id} deleted.")
            except NameError:
                st.warning(
                    "⚠ Couldn't find `delete_ticket_from_csv(...)`. Hook in your previous delete function here."
                )
            except Exception as e:
                st.error(f"Error while deleting ticket: {e}")


# =========================================================
# TAB 3 – CYBER INCIDENTS (DB)
# =========================================================
with tabs[2]:
    st.subheader("🛡 Cyber Incidents (DB) – Quick Actions")

    left, right = st.columns((2.2, 1.3))

    # ------- LEFT: ADD CYBER INCIDENT -------
    with left:
        st.markdown("### ➕ Add Cyber Incident")

        c_title = st.text_input("Title", key="cyber_title")

        c_severity = st.selectbox(
            "Severity",
            ["low", "medium", "high", "critical"],
            index=1,
            key="cyber_severity",
        )

        c_status = st.selectbox(
            "Status",
            ["open", "in progress", "closed"],
            index=0,
            key="cyber_status",
        )

        # NEW FIELDS
        c_date = st.date_input("Cyber Incident Date", value=today, key="cyber_date")
        c_time = st.time_input("Cyber Incident Time", value=current_time, key="cyber_time")
        c_day_of_week = c_date.strftime("%A")
        st.text_input(
            "Day of Week (auto)",
            value=c_day_of_week,
            disabled=True,
            key="cyber_day_of_week",
        )

        if st.button("Add Cyber Incident", type="primary", use_container_width=True):
            try:
                title_for_db = f"{c_title} ({c_date} - {c_day_of_week})"
                add_cyber_incident(title_for_db, c_severity, c_status)  # <-- YOUR FUNCTION
                st.success("Cyber incident added successfully.")
            except NameError:
                st.warning(
                    "⚠ Couldn't find `add_cyber_incident(...)`. Keep your previous logic and call it here."
                )
            except Exception as e:
                st.error(f"Error while adding cyber incident: {e}")

    # ------- RIGHT: DELETE CYBER INCIDENT -------
    with right:
        st.markdown("### 🗑 Delete Cyber Incident")

        cyber_delete_id = st.number_input(
            "Cyber Incident ID to delete", min_value=1, step=1, key="cyber_delete_id"
        )

        if st.button("Delete Cyber Incident", use_container_width=True):
            try:
                delete_cyber_incident(cyber_delete_id)  # <-- YOUR FUNCTION
                st.success(f"Cyber incident with ID {cyber_delete_id} deleted.")
            except NameError:
                st.warning(
                    "⚠ Couldn't find `delete_cyber_incident(...)`. Hook this button to your original delete code."
                )
            except Exception as e:
                st.error(f"Error while deleting cyber incident: {e}")


# =========================================================
# TAB 4 – RECENT RECORDS OVERVIEW
# =========================================================
with tabs[3]:
    st.subheader("📊 Recent Records Overview (Title / Severity / Status)")
    st.write(
        "This section is only for **display**. You can wire it up to your `get_all_*` "
        "functions later to show combined tables."
    )

    # Date range just for visuals / future use
    c1, c2 = st.columns(2)
    with c1:
        start_date = st.date_input("From", value=today.replace(day=1))
    with c2:
        end_date = st.date_input("To", value=today)

    st.caption(
        "💡 You can explain to your teacher that you prepared date filters for future reporting "
        "even if the DB query is still basic."
    )

    st.markdown("#### 🔹 Placeholder Preview Table")
    st.info(
        "Connect this section to your database/CSV using functions like `get_all_incidents()`, "
        "`get_all_tickets()`, etc., then merge them into a single DataFrame for display."
    )
    # Example (commented so it doesn't break your current app):
    # import pandas as pd
    # df = pd.DataFrame([
    #     {"Type": "Incident", "Title": "Example", "Severity": "high", "Status": "open"},
    # ])
    # st.dataframe(df, use_container_width=True)
