import streamlit as st
import os
from dotenv import load_dotenv

def show_settings():
    st.title("⚙️ Settings")
    
    # Theme settings
    st.subheader("Theme Settings")
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    selected_theme = st.selectbox(
        "Select Theme",
        ["Light", "Dark", "Opera GX"],
        index=["light", "dark", "opera_gx"].index(st.session_state.theme)
    )
    
    # Update theme
    if selected_theme.lower().replace(" ", "_") != st.session_state.theme:
        st.session_state.theme = selected_theme.lower().replace(" ", "_")
        st.rerun()
    
    # Data settings
    st.subheader("Data Settings")
    
    # Data refresh interval
    refresh_interval = st.selectbox(
        "Data Refresh Interval",
        ["Manual", "Daily", "Weekly", "Monthly"],
        index=0
    )
    
    # Cache settings
    st.subheader("Cache Settings")
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared successfully!")
    
    # Export settings
    st.subheader("Export Settings")
    default_format = st.selectbox(
        "Default Export Format",
        ["CSV", "Excel"],
        index=0
    )
    
    # Display settings
    st.subheader("Display Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Show Data Tables", value=True, key="show_tables")
        st.checkbox("Show Charts", value=True, key="show_charts")
    
    with col2:
        st.checkbox("Show Statistics", value=True, key="show_stats")
        st.checkbox("Show Filters", value=True, key="show_filters")
    
    # Save settings
    if st.button("Save Settings"):
        # Save settings to session state
        st.session_state.update({
            'refresh_interval': refresh_interval,
            'default_format': default_format
        })
        st.success("Settings saved successfully!")
        
        # Update environment variables
        os.environ["THEME"] = selected_theme
        os.environ["DATA_REFRESH"] = refresh_interval
        os.environ["EXPORT_FORMAT"] = default_format
        
        # Reload environment variables
        load_dotenv() 