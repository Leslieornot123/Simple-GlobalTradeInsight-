import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def show_dashboard():
    st.title("📊 Trade Dashboard")
    
    # Load data
    trade_data = st.session_state.trade_data_instance.get_sample_trade_data()
    
    # Key metrics with enhanced styling
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card fade-in">', unsafe_allow_html=True)
        export_data = trade_data[trade_data['TradeFlow'] == 'Export']['TradeValue'].sum()
        import_data = trade_data[trade_data['TradeFlow'] == 'Import']['TradeValue'].sum()
        total_trade = export_data + import_data
        st.metric(
            "Total Trade Volume",
            f"${total_trade/1e9:.1f}B",
            f"{((total_trade - (total_trade/1.1))/total_trade)*100:.1f}% YoY"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card fade-in">', unsafe_allow_html=True)
        trade_balance = export_data - import_data
        st.metric(
            "Trade Balance",
            f"${trade_balance/1e9:.1f}B",
            f"{((trade_balance - (trade_balance/1.05))/trade_balance)*100:.1f}% YoY"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card fade-in">', unsafe_allow_html=True)
        top_partner = trade_data.groupby('Partner')['TradeValue'].sum().idxmax()
        partner_share = trade_data[trade_data['Partner'] == top_partner]['TradeValue'].sum() / total_trade * 100
        st.metric(
            "Top Trading Partner",
            top_partner,
            f"{partner_share:.1f}% of total trade"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trade flow visualization
    st.subheader("Trade Flow Map")
    with st.spinner("Generating trade flow map..."):
        fig = st.session_state.viz.create_trade_flow_map(trade_data, st.session_state.theme)
        st.plotly_chart(fig, use_container_width=True)
    
    # Trade trends chart
    st.subheader("Trade Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = st.session_state.viz.create_trade_balance_chart(trade_data, st.session_state.theme)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = st.session_state.viz.create_growth_trend_chart(trade_data, st.session_state.theme)
        st.plotly_chart(fig, use_container_width=True)
    
    # Market share analysis
    st.subheader("Market Share Analysis")
    fig = st.session_state.viz.create_market_share_chart(trade_data, st.session_state.theme)
    st.plotly_chart(fig, use_container_width=True) 