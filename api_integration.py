import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class TradeAPI:
    def __init__(self):
        self.base_url = "https://comtrade.un.org/api/get"
        self.api_key = os.getenv('UN_COMTRADE_API_KEY', 'demo')  # Use demo key if not set
    
    def get_trade_data(self, reporter_code, partner_code, period, trade_flow='all'):
        """
        Fetch trade data from UN Comtrade API
        """
        params = {
            'r': reporter_code,  # Reporter country code
            'p': partner_code,   # Partner country code
            'ps': period,        # Time period
            'freq': 'A',         # Annual frequency
            'px': 'HS',          # Harmonized System classification
            'cc': 'TOTAL',       # All commodities
            'fmt': 'json',       # JSON format
            'max': 50000,        # Maximum records
            'type': 'C',         # Commodities
            'head': 'H',         # Human readable
            'token': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'dataset' in data:
                return pd.DataFrame(data['dataset'])
            return pd.DataFrame()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def get_country_codes(self):
        """
        Get list of country codes and names
        """
        try:
            response = requests.get(f"{self.base_url}/refs/da/view/type/area")
            response.raise_for_status()
            data = response.json()
            
            countries = {}
            for item in data:
                countries[item['id']] = item['text']
            return countries
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching country codes: {e}")
            return {}
    
    def get_commodity_codes(self):
        """
        Get list of commodity codes and names
        """
        try:
            response = requests.get(f"{self.base_url}/refs/da/view/type/classification")
            response.raise_for_status()
            data = response.json()
            
            commodities = {}
            for item in data:
                commodities[item['id']] = item['text']
            return commodities
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching commodity codes: {e}")
            return {}
    
    def process_trade_data(self, df):
        """
        Process raw trade data into a more usable format
        """
        if df.empty:
            return df
            
        # Convert values to numeric
        numeric_columns = ['TradeValue', 'NetWeight', 'Quantity']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert period to datetime
        if 'Period' in df.columns:
            df['Period'] = pd.to_datetime(df['Period'], format='%Y')
        
        # Calculate trade balance
        df['TradeBalance'] = df['TradeValue'] * df['TradeFlow'].map({'Export': 1, 'Import': -1})
        
        return df 