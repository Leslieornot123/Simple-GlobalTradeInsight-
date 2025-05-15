import streamlit as st
import plotly.express as px
import numpy as np

def show_analysis():
    st.title("🔍 Trade Analysis")
    
    if 'trade_data_instance' in st.session_state:
        data = st.session_state.trade_data_instance.get_sample_trade_data()
        
        # Analysis type selector
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Trade Balance", "Country Analysis", "Time Series Analysis", "Trade Flow Analysis"]
        )
        
        if analysis_type == "Trade Balance":
            st.subheader("Trade Balance Analysis")
            
            # Calculate trade balance for each country
            exports = data[data['TradeFlow'] == 'Export'].groupby('Reporter')['TradeValue'].sum()
            imports = data[data['TradeFlow'] == 'Import'].groupby('Reporter')['TradeValue'].sum()
            trade_balance = (exports - imports).sort_values(ascending=False)
            
            fig = px.bar(
                x=trade_balance.index,
                y=trade_balance.values / 1e9,  # Convert to billions
                title="Trade Balance by Country (Billion USD)",
                labels={'x': 'Country', 'y': 'Trade Balance (Billion USD)'}
            )
            st.plotly_chart(fig)
            
        elif analysis_type == "Country Analysis":
            st.subheader("Country Analysis")
            
            # Country selector
            country = st.selectbox("Select Country", sorted(data['Reporter'].unique()))
            
            # Filter data for selected country
            country_data = data[data['Reporter'] == country]
            
            # Show top trading partners
            st.write(f"Top Trading Partners for {country}")
            partners = country_data.groupby('Partner')['TradeValue'].sum().sort_values(ascending=False).head(5)
            fig = px.bar(
                x=partners.index,
                y=partners.values / 1e9,
                title=f"Top 5 Trading Partners for {country} (Billion USD)",
                labels={'x': 'Partner Country', 'y': 'Trade Value (Billion USD)'}
            )
            st.plotly_chart(fig)
            
        elif analysis_type == "Time Series Analysis":
            st.subheader("Time Series Analysis")
            
            # Calculate yearly trends
            yearly_data = data.groupby(['Year', 'TradeFlow'])['TradeValue'].sum().reset_index()
            
            fig = px.line(
                yearly_data,
                x='Year',
                y='TradeValue',
                color='TradeFlow',
                title="Trade Trends Over Time",
                labels={'TradeValue': 'Trade Value (USD)', 'Year': 'Year'}
            )
            st.plotly_chart(fig)
            
        elif analysis_type == "Trade Flow Analysis":
            st.subheader("Trade Flow Analysis")
            
            # Calculate trade flow distribution
            flow_data = data.groupby('TradeFlow')['TradeValue'].agg(['sum', 'count', 'mean']).reset_index()
            flow_data.columns = ['Trade Flow', 'Total Value', 'Number of Transactions', 'Average Value']
            
            # Format values
            flow_data['Total Value'] = flow_data['Total Value'] / 1e9  # Convert to billions
            flow_data['Average Value'] = flow_data['Average Value'] / 1e6  # Convert to millions
            
            st.write("Trade Flow Summary")
            st.dataframe(flow_data.style.format({
                'Total Value': '${:,.2f}B',
                'Average Value': '${:,.2f}M'
            }))
            
            # Visualization
            fig = px.pie(
                flow_data,
                values='Total Value',
                names='Trade Flow',
                title="Trade Flow Distribution"
            )
            st.plotly_chart(fig)
    
    else:
        st.warning("No trade data available. Please initialize the data first.") 