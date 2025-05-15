import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_dashboard():
    st.title("📊 Trade Dashboard")
    
    # Get data from session state
    if 'trade_data_instance' in st.session_state:
        data = st.session_state.trade_data_instance.get_sample_trade_data()
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_trade = data['TradeValue'].sum() / 1e9  # Convert to billions
            st.metric("Total Trade Value", f"${total_trade:.2f}B")
            
        with col2:
            n_countries = len(data['Reporter'].unique())
            st.metric("Trading Countries", n_countries)
            
        with col3:
            avg_trade = data['TradeValue'].mean() / 1e6  # Convert to millions
            st.metric("Average Trade Value", f"${avg_trade:.2f}M")
        
        # Trade flow distribution
        st.subheader("Trade Flow Distribution")
        trade_flow = data.groupby('TradeFlow')['TradeValue'].sum().reset_index()
        fig = px.pie(trade_flow, values='TradeValue', names='TradeFlow', 
                     title='Import vs Export Distribution')
        st.plotly_chart(fig)
        
        # Top trading partners
        st.subheader("Top Trading Partners")
        top_partners = data.groupby('Partner')['TradeValue'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(top_partners, title='Top 10 Trading Partners')
        st.plotly_chart(fig)
        
        # Trade trends over time
        st.subheader("Trade Trends")
        yearly_trade = data.groupby('Year')['TradeValue'].sum().reset_index()
        fig = px.line(yearly_trade, x='Year', y='TradeValue', 
                      title='Trade Value Over Time')
        st.plotly_chart(fig)
        
    else:
        st.warning("No trade data available. Please initialize the data first.") 