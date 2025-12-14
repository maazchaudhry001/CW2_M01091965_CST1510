# Settings.py

import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Settings", layout="wide")

# ---------- ACCESS CONTROL ----------
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("Access denied. Please log in to continue.")
    if st.button("Back to Login Page"):
        # Adjust to your home page name if different
        st.switch_page("Home.py")
    st.stop()

# ---------- DEFAULT SESSION VALUES ----------
st.session_state.setdefault("username", "guest")
st.session_state.setdefault("email", "")
st.session_state.setdefault("display_name", st.session_state.username)
st.session_state.setdefault("theme", "Dark")
st.session_state.setdefault("language", "English")
st.session_state.setdefault("compact_mode", False)

st.session_state.setdefault("notify_email", True)
st.session_state.setdefault("notify_push", True)
st.session_state.setdefault("notify_critical_only", False)

st.session_state.setdefault("two_factor_enabled", False)
st.session_state.setdefault("auto_logout_minutes", 30)

st.session_state.setdefault("last_login", datetime.now().strftime("%Y-%m-%d %H:%M"))

# ---------- PAGE HEADER ----------
st.title("Application Settings")
st.write(f"Signed in as: *{st.session_state.display_name}*")
st.divider()

# ---------- TABS ----------
tab_account, tab_prefs, tab_notify, tab_security, tab_data, tab_about = st.tabs(
    ["Account", "Preferences", "Notifications", "Security", "Data & Privacy", "About"]
)

# =========================================================
# TAB 1: ACCOUNT
# =========================================================
with tab_account:
    st.subheader("Account")

    left, right = st.columns([2, 1])

    with left:
        with st.form("account_form", clear_on_submit=False):
            username = st.text_input("Username (login ID)", st.session_state.username)
            display_name = st.text_input("Display name", st.session_state.display_name)
            email = st.text_input("Email address", st.session_state.email)

            submitted = st.form_submit_button("Save account details")
            if submitted:
                st.session_state.username = username.strip() or st.session_state.username
                st.session_state.display_name = display_name.strip() or st.session_state.display_name
                st.session_state.email = email.strip()
                st.success("Account details saved.")

    with right:
        st.caption("Last login")
        st.write(st.session_state.last_login)

        st.caption("Account type")
        st.write("Standard user")  # you can change this later

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.success("You have been logged out.")
            st.rerun()

        st.markdown("")
        delete_confirm = st.checkbox("I understand the consequences")
        if st.button("Delete demo account", use_container_width=True):
            if delete_confirm:
                # demo only: clear session and send back to login
                st.session_state.clear()
                st.success("Demo account removed. Returning to login…")
                st.rerun()
            else:
                st.warning("Please confirm before deleting your account.")

# =========================================================
# TAB 2: PREFERENCES
# =========================================================
with tab_prefs:
    st.subheader("Appearance & Preferences")

    c1, c2 = st.columns(2)

    with c1:
        theme = st.selectbox(
            "Theme",
            ["Dark", "Light", "System"],
            index=["Dark", "Light", "System"].index(st.session_state.theme)
            if st.session_state.theme in ["Dark", "Light", "System"]
            else 0,
        )
        compact = st.checkbox(
            "Compact layout (less padding)",
            value=st.session_state.compact_mode,
        )
        language = st.selectbox(
            "Language",
            ["English", "Arabic", "French"],
            index=["English", "Arabic", "French"].index(st.session_state.language)
            if st.session_state.language in ["English", "Arabic", "French"]
            else 0,
        )

        if st.button("Save preferences"):
            st.session_state.theme = theme
            st.session_state.compact_mode = compact
            st.session_state.language = language
            st.success("Preferences updated (demo only).")

    with c2:
        st.markdown("##### Preview")
        st.write(f"- **Theme:** {st.session_state.theme}")
        st.write(f"- **Language:** {st.session_state.language}")
        st.write(
            "- **Layout:** " + ("Compact" if st.session_state.compact_mode else "Comfortable")
        )
        st.info("These settings are stored in your local session for now.")

# =========================================================
# TAB 3: NOTIFICATIONS
# =========================================================
with tab_notify:
    st.subheader("Notification Settings")

    st.write("Control how you receive alerts about tickets, incidents and system status.")

    email_col, push_col = st.columns(2)

    with email_col:
        email_on = st.checkbox(
            "Email notifications", value=st.session_state.notify_email
        )
        critical_only = st.checkbox(
            "Only send critical alerts by email",
            value=st.session_state.notify_critical_only,
        )

    with push_col:
        push_on = st.checkbox(
            "In-app / push notifications",
            value=st.session_state.notify_push,
        )
        freq = st.select_slider(
            "Summary frequency",
            options=["Never", "Daily", "Weekly"],
            value="Daily",
        )

    if st.button("Save notification settings"):
        st.session_state.notify_email = email_on
        st.session_state.notify_critical_only = critical_only
        st.session_state.notify_push = push_on
        st.session_state.notify_summary_frequency = freq
        st.success("Notification preferences saved (demo).")

    st.markdown("---")
    st.caption(
        "Tip: In a real deployment these options would control emails/SMS or integrate with tools "
        "like Slack, Teams or OpsGenie."
    )

# =========================================================
# TAB 4: SECURITY
# =========================================================
with tab_security:
    st.subheader("Security & Sessions")

    st.write("Strengthen your account security and control session behaviour.")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("##### Two-Factor Authentication (2FA)")
        twofa = st.checkbox(
            "Enable two-factor authentication",
            value=st.session_state.two_factor_enabled,
        )
        if st.button("Update 2FA setting"):
            st.session_state.two_factor_enabled = twofa
            st.success(
                "2FA setting updated (demo). In production this would trigger QR / OTP setup."
            )

        st.markdown("---")

        auto_logout = st.slider(
            "Auto-logout after minutes of inactivity",
            min_value=5,
            max_value=120,
            step=5,
            value=int(st.session_state.auto_logout_minutes),
        )
        if st.button("Save session policy"):
            st.session_state.auto_logout_minutes = auto_logout
            st.success("Session policy saved (demo).")

    with col_b:
        st.markdown("##### Active sessions")
        st.info(
            "For demo purposes we treat this browser as a single session.\n\n"
            "In a real app you could list all devices and allow the user to revoke access."
        )
        if st.button("Log out from all devices"):
            st.success("All sessions would be revoked in a real system.")
        st.markdown("---")
        st.caption("Password reset and recovery options would also live here.")

# =========================================================
# TAB 5: DATA & PRIVACY
# =========================================================
with tab_data:
    st.subheader("Data & Privacy")

    st.write("Control how your data is handled inside this demo application.")

    col_dl, col_clear = st.columns(2)

    with col_dl:
        st.markdown("##### Download my data")
        fake_data = {
            "username": st.session_state.username,
            "display_name": st.session_state.display_name,
            "email": st.session_state.email,
            "preferences": {
                "theme": st.session_state.theme,
                "language": st.session_state.language,
            },
        }
        json_bytes = json.dumps(fake_data, indent=2).encode("utf-8")

        st.download_button(
            label="Download account snapshot (JSON)",
            data=json_bytes,
            file_name="my_account_export.json",
            mime="application/json",
        )

    with col_clear:
        st.markdown("##### Clear local cached data")
        st.write(
            "This will clear local session information used for this demo (preferences, "
            "notification settings, etc.). You will stay logged in."
        )
        if st.button("Clear cached settings"):
            keys_to_keep = ["logged_in", "username"]
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            st.success("Cached settings cleared. Some values reset to defaults.")
            st.rerun()

# =========================================================
# TAB 6: ABOUT
# =========================================================
with tab_about:
    st.subheader("About this application")

    st.write(
        """
        This settings page is part of an internal **IT Service & Security Dashboard** demo.

        **Features included in this demo:**
        - Local session-based authentication (no external backend).
        - Analytics views over CSV data.
        - CRUD tools for tickets/incidents.
        - Customizable user preferences and notification options.

        In a production system, these settings would integrate with:
        - Your identity provider (Azure AD, Okta, etc.)
        - Email/SMS gateways for alerting
        - Central configuration service for themes and localization
        """
    )

    st.caption("Version: 0.1.0 • Built with Streamlit")
