import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
from scipy import stats

class AdvancedTradeAnalysis:
    def __init__(self):
        self.sitc_codes = {
            '0': 'Food and live animals',
            '1': 'Beverages and tobacco',
            '2': 'Crude materials, inedible',
            '3': 'Mineral fuels, lubricants',
            '4': 'Animal and vegetable oils',
            '5': 'Chemicals',
            '6': 'Manufactured goods',
            '7': 'Machinery and transport',
            '8': 'Miscellaneous manufactured',
            '9': 'Commodities not classified'
        }
        
        self.hs_sections = {
            'I': 'Live animals; animal products',
            'II': 'Vegetable products',
            'III': 'Animal or vegetable fats',
            'IV': 'Prepared foodstuffs',
            'V': 'Mineral products',
            'VI': 'Chemical products',
            'VII': 'Plastics and rubber',
            'VIII': 'Raw hides and skins',
            'IX': 'Wood and articles',
            'X': 'Pulp of wood',
            'XI': 'Textiles and textile articles',
            'XII': 'Footwear, headgear',
            'XIII': 'Articles of stone',
            'XIV': 'Natural or cultured pearls',
            'XV': 'Base metals',
            'XVI': 'Machinery and mechanical',
            'XVII': 'Transport equipment',
            'XVIII': 'Optical, photographic',
            'XIX': 'Arms and ammunition',
            'XX': 'Miscellaneous manufactured',
            'XXI': 'Works of art',
            'XXII': 'Special transactions'
        }
    
    def calculate_rca(self, data: pd.DataFrame, country: str, product: str) -> float:
        """Calculate Revealed Comparative Advantage (RCA)"""
        country_exports = data[data['Reporter'] == country]
        world_exports = data[data['Reporter'] != country]
        
        country_product_share = (
            country_exports[country_exports['Commodity'] == product]['TradeValue'].sum() /
            country_exports['TradeValue'].sum()
        )
        
        world_product_share = (
            world_exports[world_exports['Commodity'] == product]['TradeValue'].sum() /
            world_exports['TradeValue'].sum()
        )
        
        return country_product_share / world_product_share
    
    def calculate_tii(self, data: pd.DataFrame, country1: str, country2: str) -> float:
        """Calculate Trade Intensity Index (TII)"""
        bilateral_trade = data[
            ((data['Reporter'] == country1) & (data['Partner'] == country2)) |
            ((data['Reporter'] == country2) & (data['Partner'] == country1))
        ]['TradeValue'].sum()
        
        total_trade1 = data[data['Reporter'] == country1]['TradeValue'].sum()
        total_trade2 = data[data['Reporter'] == country2]['TradeValue'].sum()
        world_trade = data['TradeValue'].sum()
        
        return (bilateral_trade / (total_trade1 + total_trade2)) / (world_trade / (2 * world_trade))
    
    def calculate_grubel_lloyd(self, data: pd.DataFrame, country: str, product: str) -> float:
        """Calculate Grubel-Lloyd Index for intra-industry trade"""
        exports = data[
            (data['Reporter'] == country) & 
            (data['Commodity'] == product) & 
            (data['TradeFlow'] == 'Export')
        ]['TradeValue'].sum()
        
        imports = data[
            (data['Reporter'] == country) & 
            (data['Commodity'] == product) & 
            (data['TradeFlow'] == 'Import')
        ]['TradeValue'].sum()
        
        return 1 - (abs(exports - imports) / (exports + imports))
    
    def calculate_trade_complementarity(self, data: pd.DataFrame, 
                                      country1: str, country2: str) -> float:
        """Calculate Trade Complementarity Index"""
        country1_exports = data[
            (data['Reporter'] == country1) & 
            (data['TradeFlow'] == 'Export')
        ]
        
        country2_imports = data[
            (data['Reporter'] == country2) & 
            (data['TradeFlow'] == 'Import')
        ]
        
        # Calculate product shares
        country1_export_shares = (
            country1_exports.groupby('Commodity')['TradeValue'].sum() /
            country1_exports['TradeValue'].sum()
        )
        
        country2_import_shares = (
            country2_imports.groupby('Commodity')['TradeValue'].sum() /
            country2_imports['TradeValue'].sum()
        )
        
        # Calculate complementarity
        complementarity = 0
        for product in set(country1_export_shares.index) & set(country2_import_shares.index):
            complementarity += min(
                country1_export_shares[product],
                country2_import_shares[product]
            )
        
        return complementarity
    
    def calculate_trade_potential(self, data: pd.DataFrame, 
                                country1: str, country2: str) -> float:
        """Calculate Trade Potential Index"""
        # Implement gravity model components
        gdp1 = self._get_gdp(country1)
        gdp2 = self._get_gdp(country2)
        distance = self._get_distance(country1, country2)
        
        # Calculate actual trade
        actual_trade = data[
            ((data['Reporter'] == country1) & (data['Partner'] == country2)) |
            ((data['Reporter'] == country2) & (data['Partner'] == country1))
        ]['TradeValue'].sum()
        
        # Calculate predicted trade using gravity model
        predicted_trade = (gdp1 * gdp2) / distance
        
        return actual_trade / predicted_trade
    
    def analyze_value_chain(self, data: pd.DataFrame, product: str) -> pd.DataFrame:
        """Analyze value chain for a specific product"""
        # Group by production stage
        stages = {
            'raw_materials': ['0', '1', '2', '3'],
            'intermediate': ['5', '6'],
            'final': ['7', '8']
        }
        
        analysis = pd.DataFrame()
        for stage, codes in stages.items():
            stage_data = data[data['Commodity'].str.startswith(tuple(codes))]
            analysis[stage] = [
                stage_data['TradeValue'].sum(),
                stage_data['TradeValue'].mean(),
                stage_data['TradeValue'].std()
            ]
        
        return analysis
    
    def calculate_tiva(self, data: pd.DataFrame, country: str) -> pd.DataFrame:
        """Calculate Trade in Value Added (TiVA) metrics"""
        # Implementation of TiVA calculation
        # This is a simplified version - actual TiVA requires input-output tables
        exports = data[
            (data['Reporter'] == country) & 
            (data['TradeFlow'] == 'Export')
        ]
        
        imports = data[
            (data['Reporter'] == country) & 
            (data['TradeFlow'] == 'Import')
        ]
        
        domestic_value = exports['TradeValue'].sum() - imports['TradeValue'].sum()
        foreign_value = imports['TradeValue'].sum()
        
        return pd.DataFrame({
            'Domestic Value Added': [domestic_value],
            'Foreign Value Added': [foreign_value],
            'Total Value Added': [domestic_value + foreign_value]
        })
    
    def analyze_tariffs(self, data: pd.DataFrame, country: str) -> pd.DataFrame:
        """Analyze tariff and non-tariff barriers"""
        # Implementation of tariff analysis
        # This would typically require external tariff data
        return pd.DataFrame()  # Placeholder
    
    def create_sankey_diagram(self, data: pd.DataFrame, 
                            source_country: str) -> go.Figure:
        """Create Sankey diagram for trade flows"""
        # Filter data for source country
        country_data = data[data['Reporter'] == source_country]
        
        # Create nodes
        nodes = list(set(country_data['Partner'].unique()) | {source_country})
        
        # Create links
        links = []
        for _, row in country_data.iterrows():
            links.append({
                'source': nodes.index(source_country),
                'target': nodes.index(row['Partner']),
                'value': row['TradeValue']
            })
        
        # Create figure
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color="blue"
            ),
            link=dict(
                source=[link['source'] for link in links],
                target=[link['target'] for link in links],
                value=[link['value'] for link in links]
            )
        )])
        
        fig.update_layout(title_text=f"Trade Flows from {source_country}")
        return fig
    
    def _get_gdp(self, country: str) -> float:
        """Get GDP for a country (placeholder)"""
        # In production, this would fetch from World Bank API
        return 1.0
    
    def _get_distance(self, country1: str, country2: str) -> float:
        """Get distance between countries (placeholder)"""
        # In production, this would use actual geographic coordinates
        return 1.0 