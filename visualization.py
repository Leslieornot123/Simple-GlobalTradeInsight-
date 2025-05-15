import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional

class TradeVisualization:
    def __init__(self):
        # Cache for country coordinates
        self._coord_cache: Dict[str, Tuple[float, float]] = {}
        # Opera GX inspired theme colors
        self._theme_colors = {
            'light': {
                'background': 'rgb(255, 255, 255)',
                'text': 'rgb(0, 0, 0)',
                'grid': 'rgba(0, 0, 0, 0.1)',
                'land': 'rgb(243, 243, 243)',
                'ocean': 'rgb(204, 229, 255)',
                'card': 'rgb(240, 242, 246)',
                'border': 'rgba(0, 0, 0, 0.1)',
                'accent1': 'rgb(255, 100, 100)',
                'accent2': 'rgb(100, 200, 255)',
                'accent3': 'rgb(100, 255, 100)'
            },
            'dark': {
                'background': 'rgb(20, 20, 20)',
                'text': 'rgb(255, 255, 255)',
                'grid': 'rgba(255, 255, 255, 0.1)',
                'land': 'rgb(40, 40, 40)',
                'ocean': 'rgb(0, 30, 60)',
                'card': 'rgb(30, 30, 30)',
                'border': 'rgba(255, 100, 100, 0.2)',
                'accent1': 'rgb(255, 100, 100)',
                'accent2': 'rgb(100, 200, 255)',
                'accent3': 'rgb(100, 255, 100)'
            },
            'opera_gx': {
                'background': 'rgb(15, 15, 15)',
                'text': 'rgb(255, 255, 255)',
                'grid': 'rgba(255, 100, 100, 0.1)',
                'land': 'rgb(30, 30, 30)',
                'ocean': 'rgb(0, 20, 40)',
                'card': 'rgb(25, 25, 25)',
                'border': 'rgba(255, 100, 100, 0.3)',
                'accent1': 'rgb(255, 100, 100)',
                'accent2': 'rgb(100, 200, 255)',
                'accent3': 'rgb(100, 255, 100)'
            }
        }
        
    def create_trade_flow_map(self, trade_data: pd.DataFrame, theme: str = "light") -> go.Figure:
        """Create an optimized trade flow map with one line per country"""
        # Aggregate trade data by country pair
        trade_flows = trade_data.groupby(['Reporter', 'Partner'])['TradeValue'].sum().reset_index()
        
        # Get unique coordinates for each country
        unique_countries = pd.concat([
            trade_flows['Reporter'].unique(),
            trade_flows['Partner'].unique()
        ]).unique()
        
        # Create coordinates dictionary (you'll need to maintain a proper coordinates database)
        coordinates = {country: self.get_country_coordinates(country) for country in unique_countries}
        
        # Create the base map
        fig = go.Figure()

        # Theme-based colors
        colors = {
            "light": {
                "land": "#E5E5E5",
                "ocean": "#F5F5F5",
                "line": "#1E88E5"
            },
            "dark": {
                "land": "#2D2D2D",
                "ocean": "#1A1A1A",
                "line": "#2196F3"
            },
            "opera_gx": {
                "land": "#151515",
                "ocean": "#0A0A0A",
                "line": "#FF0F4F"
            }
        }

        # Add the base map
        fig.add_trace(go.Scattergeo(
            lon=[],
            lat=[],
            mode='lines',
            line=dict(width=1, color=colors[theme]["land"]),
            showlegend=False
        ))

        # Add trade flows with reduced complexity
        for _, flow in trade_flows.iterrows():
            if flow['Reporter'] in coordinates and flow['Partner'] in coordinates:
                start = coordinates[flow['Reporter']]
                end = coordinates[flow['Partner']]
                
                # Calculate line width based on trade value (with a maximum)
                width = min(np.log10(flow['TradeValue']) / 2, 3)
                
                # Add a single line with hover information
                fig.add_trace(go.Scattergeo(
                    lon=[start[1], end[1]],
                    lat=[start[0], end[0]],
                    mode='lines',
                    line=dict(
                        width=width,
                        color=colors[theme]["line"]
                    ),
                    opacity=0.6,
                    hoverinfo='text',
                    text=f"{flow['Reporter']} → {flow['Partner']}<br>Trade Value: ${flow['TradeValue']/1e9:.1f}B",
                    showlegend=False
                ))

        # Update layout for better performance
        fig.update_layout(
            showlegend=False,
            geo=dict(
                showland=True,
                showocean=True,
                showcountries=True,
                landcolor=colors[theme]["land"],
                oceancolor=colors[theme]["ocean"],
                countrycolor=colors[theme]["land"],
                lataxis=dict(range=[-60, 90]),
                lonaxis=dict(range=[-180, 180]),
                projection_type="equirectangular",
                showcoastlines=False,
                showframe=False
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=600
        )

        return fig
    
    def create_trade_balance_chart(self, data: pd.DataFrame, theme: str = 'light') -> go.Figure:
        """Create an enhanced trade balance chart with theme support"""
        colors = self._theme_colors[theme]
        
        # Calculate trade balance over time
        trade_balance = (
            data.pivot_table(
                index=['Year', 'Reporter'],
                columns='TradeFlow',
                values='TradeValue',
                aggfunc='sum'
            )
            .reset_index()
        )
        
        trade_balance['Balance'] = trade_balance['Export'] - trade_balance['Import']
        
        fig = go.Figure()
        
        # Add traces with enhanced styling and animations
        traces = []
        for name, color, fill_color in [
            ('Export', colors['accent2'], f"{colors['accent2']}20"),
            ('Import', colors['accent1'], f"{colors['accent1']}20"),
            ('Balance', colors['accent3'], f"{colors['accent3']}20")
        ]:
            traces.append(
                go.Scatter(
                    x=trade_balance['Year'],
                    y=trade_balance[name],
                    name=name,
                    line=dict(color=color, width=3),
                    fill='tozeroy',
                    fillcolor=fill_color,
                    hoverlabel=dict(
                        bgcolor=colors['background'],
                        font=dict(color=colors['text'])
                    )
                )
            )
        
        fig.add_traces(traces)
        
        # Enhanced layout with theme support
        fig.update_layout(
            title='Trade Balance Over Time',
            xaxis_title='Year',
            yaxis_title='Value (USD)',
            hovermode='x unified',
            width=1200,
            height=600,
            template='plotly_white' if theme == 'light' else 'plotly_dark',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor=colors['background'],
                font=dict(color=colors['text'])
            ),
            hoverlabel=dict(
                bgcolor=colors['background'],
                font_size=12,
                font_family="Rockwell",
                font=dict(color=colors['text'])
            ),
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'],
            font=dict(color=colors['text']),
            xaxis=dict(
                gridcolor=colors['grid'],
                zerolinecolor=colors['grid'],
                showgrid=True,
                showline=True,
                linecolor=colors['border']
            ),
            yaxis=dict(
                gridcolor=colors['grid'],
                zerolinecolor=colors['grid'],
                showgrid=True,
                showline=True,
                linecolor=colors['border']
            )
        )
        
        return fig
    
    def create_market_share_chart(self, data: pd.DataFrame, theme: str = 'light') -> go.Figure:
        """Create an enhanced market share chart with theme support"""
        colors = self._theme_colors[theme]
        
        # Calculate market share by commodity
        market_share = (
            data.groupby('Commodity')['TradeValue']
            .sum()
            .sort_values(ascending=True)
            .tail(10)
        )
        
        # Create a horizontal bar chart with enhanced styling
        fig = go.Figure(
            go.Bar(
                x=market_share.values,
                y=market_share.index,
                orientation='h',
                marker=dict(
                    color=colors['accent2'],
                    line=dict(color=colors['border'], width=1)
                ),
                text=market_share.values,
                texttemplate='$%{x:,.0f}',
                textposition='auto',
                hoverinfo='text',
                hovertext=[f"Value: ${val:,.0f}" for val in market_share.values],
                hoverlabel=dict(
                    bgcolor=colors['background'],
                    font=dict(color=colors['text'])
                )
            )
        )
        
        # Enhanced layout with theme support
        fig.update_layout(
            title='Top 10 Commodities by Trade Value',
            xaxis_title='Trade Value (USD)',
            yaxis_title='Commodity',
            width=1200,
            height=600,
            template='plotly_white' if theme == 'light' else 'plotly_dark',
            hovermode='closest',
            hoverlabel=dict(
                bgcolor=colors['background'],
                font_size=12,
                font_family="Rockwell",
                font=dict(color=colors['text'])
            ),
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'],
            font=dict(color=colors['text']),
            xaxis=dict(
                gridcolor=colors['grid'],
                zerolinecolor=colors['grid'],
                showgrid=True,
                showline=True,
                linecolor=colors['border']
            ),
            yaxis=dict(
                gridcolor=colors['grid'],
                zerolinecolor=colors['grid'],
                showgrid=True,
                showline=True,
                linecolor=colors['border']
            )
        )
        
        return fig
    
    def create_growth_trend_chart(self, data: pd.DataFrame, theme: str = 'light') -> go.Figure:
        """Create an enhanced growth trend chart with theme support"""
        colors = self._theme_colors[theme]
        
        # Calculate year-over-year growth
        yearly_trade = (
            data.groupby(['Year', 'TradeFlow'])['TradeValue']
            .sum()
            .unstack()
            .fillna(0)
        )
        
        yearly_trade['Total'] = yearly_trade['Export'] + yearly_trade['Import']
        yearly_trade['Growth'] = yearly_trade['Total'].pct_change() * 100
        
        fig = go.Figure()
        
        # Add growth trend with enhanced styling
        fig.add_trace(
            go.Scatter(
                x=yearly_trade.index,
                y=yearly_trade['Growth'],
                mode='lines+markers',
                name='YoY Growth',
                line=dict(color=colors['accent1'], width=3),
                marker=dict(
                    size=8,
                    color=colors['accent1'],
                    line=dict(width=2, color='white')
                ),
                fill='tozeroy',
                fillcolor=f"{colors['accent1']}20",
                hoverlabel=dict(
                    bgcolor=colors['background'],
                    font=dict(color=colors['text'])
                )
            )
        )
        
        # Enhanced layout with theme support
        fig.update_layout(
            title='Year-over-Year Trade Growth',
            xaxis_title='Year',
            yaxis_title='Growth Rate (%)',
            width=1200,
            height=600,
            template='plotly_white' if theme == 'light' else 'plotly_dark',
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor=colors['background'],
                font_size=12,
                font_family="Rockwell",
                font=dict(color=colors['text'])
            ),
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'],
            font=dict(color=colors['text']),
            xaxis=dict(
                gridcolor=colors['grid'],
                zerolinecolor=colors['grid'],
                showgrid=True,
                showline=True,
                linecolor=colors['border']
            ),
            yaxis=dict(
                gridcolor=colors['grid'],
                zerolinecolor=colors['grid'],
                showgrid=True,
                showline=True,
                linecolor=colors['border']
            )
        )
        
        return fig
    
    def _get_latitude(self, country: str) -> float:
        """Get cached latitude for a country"""
        if country not in self._coord_cache:
            # Use a simple mapping for demo purposes
            # In production, use a proper geocoding service
            self._coord_cache[country] = (0.0, 0.0)  # Default coordinates
        return self._coord_cache[country][0]
    
    def _get_longitude(self, country: str) -> float:
        """Get cached longitude for a country"""
        if country not in self._coord_cache:
            # Use a simple mapping for demo purposes
            # In production, use a proper geocoding service
            self._coord_cache[country] = (0.0, 0.0)  # Default coordinates
        return self._coord_cache[country][1]

class TradeVisualization:
    @staticmethod
    def create_trade_flow_map(df, title="Trade Flow Map"):
        """Create an interactive trade flow map"""
        fig = go.Figure()
        
        # Add trade flow lines
        for _, row in df.iterrows():
            fig.add_trace(go.Scattergeo(
                lon=[row['Reporter_Lon'], row['Partner_Lon']],
                lat=[row['Reporter_Lat'], row['Partner_Lat']],
                mode='lines',
                line=dict(width=row['TradeValue']/1000000, color='blue'),
                text=f"{row['Reporter']} → {row['Partner']}: ${row['TradeValue']:,.0f}",
                hoverinfo='text'
            ))
        
        fig.update_layout(
            title=title,
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
            ),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_trade_balance_chart(df, title="Trade Balance Over Time"):
        """Create a trade balance chart"""
        # Calculate trade balance
        trade_balance = df.groupby(['Year', 'Reporter', 'TradeFlow'])['TradeValue'].sum().unstack()
        trade_balance['Balance'] = trade_balance['Export'] - trade_balance['Import']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=trade_balance.index.get_level_values('Year'),
            y=trade_balance['Balance'],
            name='Trade Balance',
            marker_color=np.where(trade_balance['Balance'] >= 0, 'green', 'red')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title="Trade Balance (USD)",
            barmode='group'
        )
        
        return fig
    
    @staticmethod
    def create_market_share_chart(df, title="Market Share Analysis"):
        """Create a market share pie chart"""
        market_share = df.groupby('Partner')['TradeValue'].sum().reset_index()
        
        fig = px.pie(
            market_share,
            values='TradeValue',
            names='Partner',
            title=title,
            hole=0.3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return fig
    
    @staticmethod
    def create_growth_trend_chart(df, title="Trade Growth Trends"):
        """Create a growth trend line chart"""
        growth_data = df.groupby('Year')['GrowthRate'].mean().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=growth_data['Year'],
            y=growth_data['GrowthRate'],
            mode='lines+markers',
            name='Growth Rate',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_comparative_analysis(df, title="Comparative Trade Analysis"):
        """Create a comparative analysis chart"""
        fig = go.Figure()
        
        for country in df['Reporter'].unique():
            country_data = df[df['Reporter'] == country]
            trade_values = country_data.groupby('Year')['TradeValue'].sum()
            
            fig.add_trace(go.Bar(
                x=trade_values.index,
                y=trade_values.values,
                name=country
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title="Trade Value (USD)",
            barmode='group'
        )
        
        return fig
    
    @staticmethod
    def create_risk_assessment_chart(risks, title="Risk Assessment"):
        """Create a radar chart for risk assessment"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=risks['values'],
            theta=risks['categories'],
            fill='toself',
            name='Risk Level'
        ))
        
        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False
        )
        
        return fig 