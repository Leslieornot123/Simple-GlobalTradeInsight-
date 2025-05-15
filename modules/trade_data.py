import pandas as pd
import numpy as np
from datetime import datetime
import os

class TradeData:
    def __init__(self):
        self.data = None
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample trade data"""
        # Create sample data
        np.random.seed(42)
        years = range(2010, 2023)
        countries = ['USA', 'China', 'Germany', 'Japan', 'UK', 'France', 'India', 'Brazil', 'Canada', 'Australia']
        
        data = []
        for year in years:
            for reporter in countries:
                for partner in countries:
                    if reporter != partner:
                        trade_value = np.random.uniform(1e6, 1e9)
                        trade_flow = np.random.choice(['Import', 'Export'])
                        data.append({
                            'Year': year,
                            'Reporter': reporter,
                            'Partner': partner,
                            'TradeValue': trade_value,
                            'TradeFlow': trade_flow
                        })
        
        self.data = pd.DataFrame(data)
    
    def get_sample_trade_data(self):
        """Return the sample trade data"""
        return self.data
    
    def refresh_data(self):
        """Refresh the trade data"""
        try:
            self.load_sample_data()
            return True
        except Exception as e:
            print(f"Error refreshing data: {str(e)}")
            return False
    
    def export_data(self, format='csv'):
        """Export the trade data in the specified format"""
        if self.data is None:
            return False, "No data available to export"
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"trade_data_{timestamp}"
            
            if format.lower() == 'csv':
                export_path = f"{filename}.csv"
                self.data.to_csv(export_path, index=False)
                return True, f"Data exported successfully to {export_path}"
            elif format.lower() == 'excel':
                export_path = f"{filename}.xlsx"
                self.data.to_excel(export_path, index=False)
                return True, f"Data exported successfully to {export_path}"
            else:
                return False, f"Unsupported export format: {format}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def filter_data(self, years=None, countries=None, min_trade_value=None, trade_type=None):
        """Filter the trade data based on specified criteria"""
        if self.data is None:
            return None
        
        filtered_data = self.data.copy()
        
        if years:
            filtered_data = filtered_data[filtered_data['Year'].isin(years)]
        
        if countries:
            filtered_data = filtered_data[
                (filtered_data['Reporter'].isin(countries)) |
                (filtered_data['Partner'].isin(countries))
            ]
        
        if min_trade_value is not None:
            filtered_data = filtered_data[filtered_data['TradeValue'] >= min_trade_value]
            
        if trade_type and trade_type.lower() != 'all':
            filtered_data = filtered_data[filtered_data['TradeFlow'] == trade_type]
        
        return filtered_data 