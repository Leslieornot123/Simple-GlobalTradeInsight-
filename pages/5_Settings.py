import streamlit as st
import json
import os

def show_settings():
    st.title("⚙️ Settings")
    
    # User Profile Settings
    st.header("User Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=st.session_state.user_profile.get("name", ""))
        email = st.text_input("Email", value=st.session_state.user_profile.get("email", ""))
    with col2:
        role = st.selectbox(
            "Role",
            ["Admin", "Manager", "Analyst", "Viewer"],
            index=["Admin", "Manager", "Analyst", "Viewer"].index(
                st.session_state.user_profile.get("role", "Viewer")
            )
        )
        department = st.text_input(
            "Department",
            value=st.session_state.user_profile.get("department", "")
        )
    
    # Notification Settings
    st.header("Notifications")
    col1, col2 = st.columns(2)
    with col1:
        email_notifications = st.checkbox(
            "Email Notifications",
            value=st.session_state.user_profile.get("notifications", {}).get("email", False)
        )
        push_notifications = st.checkbox(
            "Push Notifications",
            value=st.session_state.user_profile.get("notifications", {}).get("push", False)
        )
    with col2:
        notification_frequency = st.selectbox(
            "Notification Frequency",
            ["Real-time", "Daily", "Weekly", "Monthly"],
            index=["Real-time", "Daily", "Weekly", "Monthly"].index(
                st.session_state.user_profile.get("notifications", {}).get("frequency", "Daily")
            )
        )
    
    # Display Settings
    st.header("Display")
    col1, col2 = st.columns(2)
    with col1:
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "System"],
            index=["Light", "Dark", "System"].index(
                st.session_state.user_profile.get("display", {}).get("theme", "Light")
            )
        )
        language = st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German"],
            index=["English", "Spanish", "French", "German"].index(
                st.session_state.user_profile.get("display", {}).get("language", "English")
            )
        )
    with col2:
        timezone = st.selectbox(
            "Timezone",
            ["UTC", "EST", "PST", "GMT"],
            index=["UTC", "EST", "PST", "GMT"].index(
                st.session_state.user_profile.get("display", {}).get("timezone", "UTC")
            )
        )
        date_format = st.selectbox(
            "Date Format",
            ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"],
            index=["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"].index(
                st.session_state.user_profile.get("display", {}).get("date_format", "YYYY-MM-DD")
            )
        )
    
    # Data Settings
    st.header("Data")
    col1, col2 = st.columns(2)
    with col1:
        data_refresh = st.selectbox(
            "Data Refresh Rate",
            ["5 minutes", "15 minutes", "30 minutes", "1 hour"],
            index=["5 minutes", "15 minutes", "30 minutes", "1 hour"].index(
                st.session_state.user_profile.get("data", {}).get("refresh_rate", "15 minutes")
            )
        )
        data_retention = st.selectbox(
            "Data Retention Period",
            ["30 days", "90 days", "1 year", "Forever"],
            index=["30 days", "90 days", "1 year", "Forever"].index(
                st.session_state.user_profile.get("data", {}).get("retention", "90 days")
            )
        )
    with col2:
        export_format = st.selectbox(
            "Default Export Format",
            ["CSV", "Excel", "PDF"],
            index=["CSV", "Excel", "PDF"].index(
                st.session_state.user_profile.get("data", {}).get("export_format", "Excel")
            )
        )
    
    # Security Settings
    st.header("Security")
    col1, col2 = st.columns(2)
    with col1:
        two_factor = st.checkbox(
            "Two-Factor Authentication",
            value=st.session_state.user_profile.get("security", {}).get("two_factor", False)
        )
        session_timeout = st.selectbox(
            "Session Timeout",
            ["15 minutes", "30 minutes", "1 hour", "Never"],
            index=["15 minutes", "30 minutes", "1 hour", "Never"].index(
                st.session_state.user_profile.get("security", {}).get("session_timeout", "30 minutes")
            )
        )
    with col2:
        password_change = st.button("Change Password")
        if password_change:
            st.session_state.show_password_change = True
    
    if st.session_state.get("show_password_change", False):
        with st.form("password_change_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            submitted = st.form_submit_button("Update Password")
            if submitted:
                if new_password == confirm_password:
                    st.success("Password updated successfully!")
                    st.session_state.show_password_change = False
                else:
                    st.error("New passwords do not match!")
    
    # Save Settings
    if st.button("Save Settings"):
        # Update user profile
        st.session_state.user_profile.update({
            "name": name,
            "email": email,
            "role": role,
            "department": department,
            "notifications": {
                "email": email_notifications,
                "push": push_notifications,
                "frequency": notification_frequency
            },
            "display": {
                "theme": theme,
                "language": language,
                "timezone": timezone,
                "date_format": date_format
            },
            "data": {
                "refresh_rate": data_refresh,
                "retention": data_retention,
                "export_format": export_format
            },
            "security": {
                "two_factor": two_factor,
                "session_timeout": session_timeout
            }
        })
        
        # Save to file
        with open("user_profile.json", "w") as f:
            json.dump(st.session_state.user_profile, f)
        
        st.success("Settings saved successfully!")
    
    # Reset to Defaults
    if st.button("Reset to Defaults"):
        st.session_state.user_profile = {
            "name": "",
            "email": "",
            "role": "Viewer",
            "department": "",
            "notifications": {
                "email": False,
                "push": False,
                "frequency": "Daily"
            },
            "display": {
                "theme": "Light",
                "language": "English",
                "timezone": "UTC",
                "date_format": "YYYY-MM-DD"
            },
            "data": {
                "refresh_rate": "15 minutes",
                "retention": "90 days",
                "export_format": "Excel"
            },
            "security": {
                "two_factor": False,
                "session_timeout": "30 minutes"
            }
        }
        st.success("Settings reset to defaults!") 