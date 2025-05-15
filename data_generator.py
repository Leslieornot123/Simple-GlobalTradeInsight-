import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import streamlit as st

class TradeDataGenerator:
    def __init__(self):
        self.countries = [
            'USA', 'China', 'Germany', 'Japan', 'UK', 'France', 'India', 
            'Italy', 'Brazil', 'Canada'
        ]  # Reduced from 20 to 10 countries
        
        self.commodities = {
            'Electronics': ['Smartphones', 'Computers', 'Semiconductors'],
            'Automotive': ['Cars', 'Auto Parts', 'Trucks'],
            'Textiles': ['Clothing', 'Fabrics', 'Footwear'],
            'Agriculture': ['Grains', 'Fruits', 'Vegetables'],
            'Energy': ['Crude Oil', 'Natural Gas', 'Coal'],
            'Chemicals': ['Pharmaceuticals', 'Fertilizers', 'Plastics'],
            'Machinery': ['Industrial Equipment', 'Construction Machinery'],
            'Metals': ['Iron & Steel', 'Aluminum', 'Copper']
        }
        
        self.risk_factors = {
            'Political': ['Stability', 'Regulations', 'Trade Policies'],
            'Economic': ['GDP Growth', 'Inflation', 'Exchange Rate'],
            'Market': ['Competition', 'Demand', 'Pricing'],
            'Operational': ['Infrastructure', 'Labor', 'Supply Chain']
        }
    
    def generate_trade_data(self, years=3):  # Reduced from 5 to 3 years
        """Generate realistic trade data for multiple countries and years"""
        data = []
        current_year = datetime.now().year
        
        # Country coordinates (approximate)
        country_coords = {
            'USA': {'lat': 37.0902, 'lon': -95.7129},
            'China': {'lat': 35.8617, 'lon': 104.1954},
            'Germany': {'lat': 51.1657, 'lon': 10.4515},
            'Japan': {'lat': 36.2048, 'lon': 138.2529},
            'UK': {'lat': 55.3781, 'lon': -3.4360},
            'France': {'lat': 46.2276, 'lon': 2.2137},
            'India': {'lat': 20.5937, 'lon': 78.9629},
            'Italy': {'lat': 41.8719, 'lon': 12.5674},
            'Brazil': {'lat': -14.2350, 'lon': -51.9253},
            'Canada': {'lat': 56.1304, 'lon': -106.3468}
        }
        
        for year in range(current_year - years + 1, current_year + 1):
            for reporter in self.countries:
                for partner in self.countries:
                    if reporter != partner:
                        # Generate random but realistic trade values
                        base_value = random.uniform(1000000, 100000000)
                        growth_rate = random.uniform(-0.1, 0.2)
                        
                        # Add some seasonality
                        seasonality = np.sin(2 * np.pi * (year - current_year) / 4) * 0.1
                        
                        # Calculate final trade value
                        trade_value = base_value * (1 + growth_rate + seasonality)
                        
                        # Add some noise
                        noise = random.uniform(-0.05, 0.05)
                        trade_value *= (1 + noise)
                        
                        # Generate commodity distribution
                        commodity_data = self._generate_commodity_data(trade_value)
                        
                        for commodity, value in commodity_data.items():
                            data.append({
                                'Year': year,
                                'Reporter': reporter,
                                'Partner': partner,
                                'Commodity': commodity,
                                'TradeValue': value,
                                'TradeFlow': random.choice(['Export', 'Import']),
                                'GrowthRate': growth_rate * 100,
                                'Reporter_Lat': country_coords[reporter]['lat'],
                                'Reporter_Lon': country_coords[reporter]['lon'],
                                'Partner_Lat': country_coords[partner]['lat'],
                                'Partner_Lon': country_coords[partner]['lon']
                            })
        
        return pd.DataFrame(data)
    
    def _generate_commodity_data(self, total_value):
        """Generate commodity-specific trade data"""
        commodities = {}
        remaining_value = total_value
        
        # Distribute value across commodities
        for category, items in self.commodities.items():
            if remaining_value <= 0:
                break
                
            # Randomly select items from category
            selected_items = random.sample(items, random.randint(1, len(items)))
            
            for item in selected_items:
                if remaining_value <= 0:
                    break
                    
                # Allocate portion of remaining value
                portion = random.uniform(0.1, 0.3)  # 10-30% of remaining value
                value = remaining_value * portion
                commodities[f"{category} - {item}"] = value
                remaining_value -= value
        
        return commodities
    
    def generate_market_insights(self, country):
        """Generate realistic market insights for a country"""
        insights = {
            'market_size': f"${random.randint(10, 100)}B",
            'growth_rate': f"{random.randint(5, 20)}%",
            'ease_of_business': random.choice(['Low', 'Medium', 'High']),
            'risk_level': random.choice(['Low', 'Medium', 'High']),
            'recommendations': self._generate_recommendations(country),
            'risk_factors': self._generate_risk_factors()
        }
        return insights
    
    def _generate_recommendations(self, country):
        """Generate market entry recommendations"""
        recommendations = [
            f"Establish local partnership in {country}",
            f"Focus on major economic centers in {country}",
            f"Consider joint ventures with local companies",
            f"Invest in local marketing and branding",
            f"Adapt products to local market preferences",
            f"Navigate local regulations and compliance",
            f"Build relationships with local distributors",
            f"Consider local production facilities"
        ]
        return random.sample(recommendations, 4)
    
    def _generate_risk_factors(self):
        """Generate risk factor assessments"""
        risks = {}
        for category, factors in self.risk_factors.items():
            risks[category] = {
                'score': random.randint(1, 10),
                'factors': {
                    factor: random.randint(1, 10) for factor in factors
                }
            }
        return risks
    
    def generate_report_data(self, country, year):
        """Generate data for a comprehensive trade report"""
        report = {
            'title': f"Trade Analysis Report - {country} {year}",
            'executive_summary': self._generate_executive_summary(country, year),
            'market_overview': self._generate_market_overview(country),
            'trade_analysis': self._generate_trade_analysis(country, year),
            'opportunities': self._generate_opportunities(country),
            'risks': self._generate_risks(country),
            'recommendations': self._generate_recommendations(country)
        }
        return report
    
    def _generate_executive_summary(self, country, year):
        """Generate executive summary for report"""
        return f"""
        This report provides a comprehensive analysis of trade opportunities in {country} for {year}.
        The market shows strong growth potential with increasing demand across multiple sectors.
        Key opportunities include {random.choice(['technology', 'manufacturing', 'services'])} sector,
        while challenges include {random.choice(['regulatory compliance', 'market competition', 'infrastructure'])}.
        """
    
    def _generate_market_overview(self, country):
        """Generate market overview section"""
        return f"""
        {country}'s market is characterized by:
        - GDP: ${random.randint(100, 1000)}B
        - Population: {random.randint(10, 100)}M
        - Main industries: {', '.join(random.sample(['Technology', 'Manufacturing', 'Agriculture', 'Services'], 3))}
        - Key trading partners: {', '.join(random.sample(self.countries, 3))}
        """
    
    def _generate_trade_analysis(self, country, year):
        """Generate trade analysis section"""
        return f"""
        Trade analysis for {country} in {year} shows:
        - Total trade volume: ${random.randint(50, 500)}B
        - Trade balance: ${random.randint(-50, 50)}B
        - Growth rate: {random.randint(5, 15)}%
        - Main export sectors: {', '.join(random.sample(list(self.commodities.keys()), 3))}
        - Main import sectors: {', '.join(random.sample(list(self.commodities.keys()), 3))}
        """
    
    def _generate_opportunities(self, country):
        """Generate opportunities section"""
        return f"""
        Key opportunities in {country}:
        1. Growing demand in {random.choice(list(self.commodities.keys()))} sector
        2. Favorable trade agreements with {random.choice(self.countries)}
        3. Government incentives for {random.choice(['foreign investment', 'export-oriented businesses'])}
        4. Emerging market segments in {random.choice(['urban areas', 'rural markets'])}
        """
    
    def _generate_risks(self, country):
        """Generate risks section"""
        return f"""
        Potential risks in {country}:
        1. {random.choice(['Political instability', 'Regulatory changes', 'Economic fluctuations'])}
        2. {random.choice(['Currency volatility', 'Trade barriers', 'Competition'])}
        3. {random.choice(['Infrastructure limitations', 'Supply chain issues', 'Labor market challenges'])}
        4. {random.choice(['Cultural differences', 'Market entry barriers', 'Local competition'])}
        """ 