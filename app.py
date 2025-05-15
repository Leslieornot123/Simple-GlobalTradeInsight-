import streamlit as st
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Optional
import requests
import json
from trade_analysis import AdvancedTradeAnalysis
from modules.trade_data import TradeData

# Import page functions
from modules.dashboard_page import show_dashboard
from modules.analysis_page import show_analysis
from modules.reports_page import show_reports
from modules.visualization_page import show_visualization
from modules.settings_page import show_settings

# Load environment variables
load_dotenv()

# Simple Auth class for demonstration
class Auth:
    def __init__(self):
        self.users = {"admin": "admin123"}  # Demo credentials
    
    def login(self, username: str, password: str) -> tuple[bool, str]:
        if username in self.users and self.users[username] == password:
            return True, "demo_token"
        return False, "Invalid credentials"
    
    def guest_login(self) -> tuple[bool, str]:
        return True, "guest_token"
    
    def register(self, username: str, password: str, email: str) -> tuple[bool, str]:
        if username in self.users:
            return False, "Username already exists"
        self.users[username] = password
        return True, "Registration successful"

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.trade_data_instance = TradeData()
    st.session_state.auth = Auth()

class EconomicData:
    def __init__(self):
        self.world_bank_api = "http://api.worldbank.org/v2"
        self.imf_api = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
        self.oecd_api = "https://stats.oecd.org/SDMX-JSON/data"
        
    def calculate_terms_of_trade(self, export_price_index: float, import_price_index: float) -> float:
        """Calculate Terms of Trade (ToT)"""
        return (export_price_index / import_price_index) * 100
    
    def calculate_trade_openness(self, exports: float, imports: float, gdp: float) -> float:
        """Calculate Trade Openness Index"""
        return ((exports + imports) / gdp) * 100
    
    def calculate_export_concentration(self, export_data: pd.DataFrame) -> float:
        """Calculate Herfindahl-Hirschman Index for export concentration"""
        total_exports = export_data['TradeValue'].sum()
        market_shares = (export_data['TradeValue'] / total_exports) * 100
        return (market_shares ** 2).sum()
    
    def get_gdp_growth(self, country: str, start_year: int, end_year: int) -> pd.DataFrame:
        """Fetch GDP growth rates from World Bank"""
        url = f"{self.world_bank_api}/country/{country}/indicator/NY.GDP.MKTP.KD.ZG"
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}"
        }
        response = requests.get(url, params=params)
        data = response.json()[1]
        return pd.DataFrame(data)
    
    def get_inflation(self, country: str, start_year: int, end_year: int) -> pd.DataFrame:
        """Fetch inflation rates from World Bank"""
        url = f"{self.world_bank_api}/country/{country}/indicator/FP.CPI.TOTL.ZG"
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}"
        }
        response = requests.get(url, params=params)
        data = response.json()[1]
        return pd.DataFrame(data)
    
    def get_exchange_rates(self, base_currency: str, target_currency: str, 
                          start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch exchange rates from IMF"""
        url = f"{self.imf_api}/DataStructure"
        response = requests.get(url)
        # Implementation details for IMF API
        return pd.DataFrame()  # Placeholder
    
    def get_interest_rates(self, country: str, start_year: int, end_year: int) -> pd.DataFrame:
        """Fetch interest rates from OECD"""
        url = f"{self.oecd_api}/MEI_FIN/IR3TIB"
        params = {
            "startTime": start_year,
            "endTime": end_year,
            "dimensionAtObservation": "TIME_PERIOD"
        }
        response = requests.get(url, params=params)
        return pd.DataFrame(response.json())
    
    def get_unemployment(self, country: str, start_year: int, end_year: int) -> pd.DataFrame:
        """Fetch unemployment rates from World Bank"""
        url = f"{self.world_bank_api}/country/{country}/indicator/SL.UEM.TOTL.ZS"
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}"
        }
        response = requests.get(url, params=params)
        data = response.json()[1]
        return pd.DataFrame(data)

def initialize_components():
    """Lazy initialization of components"""
    if not st.session_state.initialized:
        # Initialize TradeData instance if not already initialized
        if 'trade_data_instance' not in st.session_state:
            st.session_state.trade_data_instance = TradeData()
        
        # Initialize other components
        st.session_state.economic_data = EconomicData()
        st.session_state.advanced_analysis = AdvancedTradeAnalysis()
        
        # Mark as initialized
        st.session_state.initialized = True

# Page configuration
st.set_page_config(
    page_title="GlobalTradeInsight",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the minimalist theme system
THEMES = {
    "light": {
        "name": "Light",
        "colors": {
            "primary": {
                "main": "#2196F3",
                "light": "#42A5F5",
                "dark": "#1E88E5"
            },
            "background": {
                "default": "#FFFFFF",
                "paper": "#F8F9FA"
            },
            "surface": {
                "default": "#FFFFFF"
            },
            "text": {
                "primary": "#212121",
                "secondary": "#757575"
            },
            "border": {
                "default": "#E0E0E0"
            }
        }
    },
    "dark": {
        "name": "Dark",
        "colors": {
            "primary": {
                "main": "#90CAF9",
                "light": "#BBDEFB",
                "dark": "#64B5F6"
            },
            "background": {
                "default": "#121212",
                "paper": "#1E1E1E"
            },
            "surface": {
                "default": "#1E1E1E"
            },
            "text": {
                "primary": "#FFFFFF",
                "secondary": "#B0B0B0"
            },
            "border": {
                "default": "#333333"
            }
        }
    },
    "opera_gx": {
        "name": "Opera GX",
        "colors": {
            "primary": {
                "main": "#FF0F4F",
                "light": "#FF4D7F",
                "dark": "#CC0C3F"
            },
            "background": {
                "default": "#0A0A0A",
                "paper": "#151515"
            },
            "surface": {
                "default": "#151515"
            },
            "text": {
                "primary": "#FFFFFF",
                "secondary": "#B0B0B0"
            },
            "border": {
                "default": "#333333"
            }
        }
    }
}

def apply_theme(theme_key: str):
    """Apply a minimalist theme while preserving the original theme colors"""
    theme = THEMES[theme_key]
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Theme Variables */
    :root {{
        --primary-main: {theme["colors"]["primary"]["main"]};
        --primary-light: {theme["colors"]["primary"]["light"]};
        --primary-dark: {theme["colors"]["primary"]["dark"]};
        --background-default: {theme["colors"]["background"]["default"]};
        --background-paper: {theme["colors"]["background"]["paper"]};
        --surface-default: {theme["colors"]["surface"]["default"]};
        --text-primary: {theme["colors"]["text"]["primary"]};
        --text-secondary: {theme["colors"]["text"]["secondary"]};
        --border-default: {theme["colors"]["border"]["default"]};
    }}
    
    /* Base styles */
    .stApp {{
        background-color: var(--background-default) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Clean sidebar */
    [data-testid="stSidebar"] {{
        background-color: var(--background-paper) !important;
        border-right: 1px solid var(--border-default) !important;
        padding: 2rem 1rem !important;
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        margin-bottom: 1rem !important;
    }}
    
    h1 {{ font-size: 1.8rem !important; font-weight: 600 !important; }}
    h2 {{ font-size: 1.4rem !important; font-weight: 500 !important; }}
    
    p, .stMarkdown {{
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }}
    
    /* Clean inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {{
        background-color: var(--surface-default) !important;
        border: 1px solid var(--border-default) !important;
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
        padding: 0.5rem !important;
    }}
    
    /* Minimal buttons */
    .stButton > button {{
        background-color: var(--primary-main) !important;
        border: none !important;
        border-radius: 4px !important;
        color: white !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: opacity 0.2s ease !important;
    }}
    
    .stButton > button:hover {{
        background-color: var(--primary-light) !important;
    }}
    
    /* Clean metrics */
    [data-testid="stMetricValue"] {{
        color: var(--primary-main) !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMetricDelta"] {{
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }}
    
    /* Clean tables */
    .stDataFrame {{
        border: 1px solid var(--border-default) !important;
        border-radius: 4px !important;
    }}
    
    .stDataFrame thead tr th {{
        background-color: var(--surface-default) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
    }}
    
    .stDataFrame tbody tr td {{
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
    }}
    
    /* Clean plots */
    .js-plotly-plot {{
        background-color: transparent !important;
    }}
    
    .js-plotly-plot .bg {{
        fill: var(--background-default) !important;
    }}
    
    .js-plotly-plot text {{
        fill: var(--text-primary) !important;
    }}
    
    /* Minimal alerts */
    .stAlert {{
        background-color: var(--surface-default) !important;
        border: 1px solid var(--border-default) !important;
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        padding: 1rem !important;
    }}
    
    /* Clean select boxes */
    .stSelectbox {{
        min-height: auto !important;
    }}
    
    /* Remove excess padding */
    .block-container {{
        padding: 2rem !important;
    }}
    
    /* Clean dividers */
    hr {{
        border: none !important;
        border-top: 1px solid var(--border-default) !important;
        margin: 2rem 0 !important;
    }}
    
    /* Economic Analysis Specific Styles */
    .economic-card {{
        background-color: var(--surface-default) !important;
        border: 1px solid var(--border-default) !important;
        border-radius: 4px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }}
    
    .indicator-grid {{
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
        gap: 1rem !important;
        margin: 1rem 0 !important;
    }}
    
    .trend-arrow-up {{
        color: #00C853 !important;
    }}
    
    .trend-arrow-down {{
        color: #FF1744 !important;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def login_page():
    st.title("Login to GlobalTradeInsight")
    
    with st.container():
        st.markdown('<div class="login-container slide-in">', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if not hasattr(st.session_state, 'auth'):
                    st.session_state.auth = Auth()
                success, message = st.session_state.auth.login(username, password)
                if success:
                    st.session_state.token = message
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error(message)
        
        # Guest login button
        if st.button("Continue as Guest"):
            if not hasattr(st.session_state, 'auth'):
                st.session_state.auth = Auth()
            success, token = st.session_state.auth.guest_login()
            if success:
                st.session_state.token = token
                st.session_state.username = "Guest"
                st.rerun()
        
        # Register link
        st.markdown("Don't have an account? [Register here](#register)")
        st.markdown('</div>', unsafe_allow_html=True)

def register_page():
    st.title("📝 Register New Account")
    
    with st.container():
        st.markdown('<div class="login-container slide-in">', unsafe_allow_html=True)
        
        with st.form("register_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            email = st.text_input("Email")
            submit = st.form_submit_button("Register")
            
            if submit:
                if not hasattr(st.session_state, 'auth'):
                    st.session_state.auth = Auth()
                success, message = st.session_state.auth.register(username, password, email)
                if success:
                    st.success(message)
                    st.session_state['show_register'] = False
                else:
                    st.error(message)
        
        if st.button("Back to Login"):
            st.session_state['show_register'] = False
        
        st.markdown('</div>', unsafe_allow_html=True)

def main_app():
    initialize_components()
    
    # Theme selection
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Apply current theme
    apply_theme(st.session_state.theme)
    
    # Sidebar for navigation
    st.sidebar.title("GlobalTradeInsight")
    
    # Show username in sidebar
    if st.session_state.get("username"):
        st.sidebar.markdown(f"Logged in as: **{st.session_state.username}**")
        if st.session_state.username != "Guest":
            if st.sidebar.button("🚪 Logout"):
                st.session_state.clear()
                st.rerun()
        else:
            if st.sidebar.button("👤 Switch to Full Account"):
                st.session_state.clear()
                st.rerun()
    
    # Main navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("📱 Navigation")
    
    # Create a dictionary for page icons and names
    pages = {
        "📊 Dashboard": "dashboard_page",
        "🔍 Analysis": "analysis_page",
        "📈 Visualization": "visualization_page",
        "📄 Reports": "reports_page",
        "⚙️ Settings": "settings_page"
    }
    
    # Display navigation options with icons
    selected_page = st.sidebar.radio(
        "Navigation Menu",  # Add a proper label
        list(pages.keys()),
        key="nav_radio",
        label_visibility="collapsed"  # Hide the label but keep it accessible
    )
    
    # Quick actions in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ Quick Actions")
    
    # Data management section
    with st.sidebar.expander("📂 Data Management", expanded=True):
        if st.button("🔄 Refresh Data"):
            success = st.session_state.trade_data_instance.refresh_data()
            if success:
                st.success("Data refreshed successfully!")
            else:
                st.error("Failed to refresh data")
        
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "Excel"],
            key="export_format"
        )
        
        if st.button("📥 Export Current View"):
            success, message = st.session_state.trade_data_instance.export_data(format=export_format.lower())
            if success:
                st.success(message)
            else:
                st.error(message)
    
    # Filters section
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    
    # Basic filters in an expander
    with st.sidebar.expander("📊 Basic Filters", expanded=True):
        # Year filter
        years = sorted(st.session_state.trade_data_instance.get_sample_trade_data()['Year'].unique())
        selected_years = st.multiselect(
        "Select Years",
        options=years,
        default=years[-5:],  # Default to last 5 years
        key="year_filter"
    )
    
        # Country filter
        countries = sorted(st.session_state.trade_data_instance.get_sample_trade_data()['Reporter'].unique())
        selected_countries = st.multiselect(
        "Select Countries",
        options=countries,
        default=countries[:5],  # Default to first 5 countries
        key="country_filter"
    )
    
        # Trade value threshold
        min_trade_value = st.slider(
        "Minimum Trade Value (Billion USD)",
        min_value=0.0,
            max_value=float(st.session_state.trade_data_instance.get_sample_trade_data()['TradeValue'].max() / 1e9),
        value=0.0,
        step=0.1,
        format="%.1fB"
    )
    
    # Advanced filters in a separate expander
    with st.sidebar.expander("🔧 Advanced Filters", expanded=False):
        trade_type = st.selectbox(
            "Trade Type",
            ["All", "Import", "Export"],
            key="trade_type"
        )
        
        commodity_category = st.selectbox(
            "Commodity Category",
            ["All", "Agricultural", "Manufactured", "Raw Materials"],
            key="commodity_category"
        )
        
        # Add date range filter
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=365), datetime.now()),
            key="date_range"
        )
    
    # Help & Support section
    st.sidebar.markdown("---")
    with st.sidebar.expander("❓ Help & Support", expanded=False):
        st.markdown("""
        - 📚 [Documentation](#)
        - 🎓 [Tutorials](#)
        - 📧 [Contact Support](#)
        """)
    
    # Page mapping dictionary
    page_functions = {
        "dashboard_page": show_dashboard,
        "analysis_page": show_analysis,
        "reports_page": show_reports,
        "visualization_page": show_visualization,
        "settings_page": show_settings
    }
    
    # Load the appropriate page
    selected_function = pages[selected_page]
    page_functions[selected_function]()

# Main application flow
if 'token' not in st.session_state:
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False
    
    if st.session_state['show_register']:
        register_page()
    else:
        login_page()
else:
    main_app()

# Footer
st.markdown("---")
st.markdown("© 2024 GlobalTradeInsight | For educational purposes") 