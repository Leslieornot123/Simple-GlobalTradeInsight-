import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_generator import TradeDataGenerator
import json
import os
import streamlit as st

class TradeData:
    def __init__(self):
        self.generator = TradeDataGenerator()
        self.sample_data_dir = 'sample_data'
        os.makedirs(self.sample_data_dir, exist_ok=True)
        
        # Load sample data if it exists
        self.trade_data = self._load_data()
        self.market_insights = self._load_insights()
        self.sample_reports = self._load_reports()
    
    def _load_data(self):
        """Load trade data from CSV file"""
        # Always generate fresh data
        data = self.generator.generate_trade_data(years=3)
        file_path = os.path.join(self.sample_data_dir, 'trade_data.csv')
        data.to_csv(file_path, index=False)
        return data
    
    def _load_insights(self):
        """Load market insights from JSON file"""
        file_path = os.path.join(self.sample_data_dir, 'market_insights.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        insights = {country: self.generator.generate_market_insights(country) 
                   for country in self.generator.countries[:10]}
        with open(file_path, 'w') as f:
            json.dump(insights, f)
        return insights
    
    def _load_reports(self):
        """Load sample reports from JSON file"""
        file_path = os.path.join(self.sample_data_dir, 'sample_reports.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        reports = {country: self.generator.generate_report_data(country, 2023) 
                  for country in self.generator.countries[:5]}
        with open(file_path, 'w') as f:
            json.dump(reports, f)
        return reports
    
    def get_sample_trade_data(self):
        """Get sample trade data"""
        return self.trade_data
    
    def get_market_insights(self, country):
        """Get market insights for a country"""
        if country in self.market_insights:
            return self.market_insights[country]
        return self.generator.generate_market_insights(country)
    
    def generate_report(self, report_type, start_date, end_date, country, product_category):
        """Generate a trade report"""
        if country in self.sample_reports:
            report = self.sample_reports[country].copy()
        else:
            report = self.generator.generate_report_data(country, end_date.year)
        
        # Customize report based on parameters
        report['type'] = report_type
        report['period'] = f"{start_date} to {end_date}"
        report['product_category'] = product_category
        
        return report
    
    def get_commodity_categories(self):
        """Get list of commodity categories"""
        return list(self.generator.commodities.keys())
    
    def get_commodity_items(self, category):
        """Get items for a specific commodity category"""
        return self.generator.commodities.get(category, [])
    
    def get_countries(self):
        """Get list of available countries"""
        return self.generator.countries
    
    def get_risk_factors(self):
        """Get risk factor categories and factors"""
        return self.generator.risk_factors 