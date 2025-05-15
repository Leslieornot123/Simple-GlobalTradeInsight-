import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def show_analysis():
    st.title("🔍 Trade Analysis")
    
    # Load data
    trade_data = st.session_state.trade_data_instance.get_sample_trade_data()
    
    # Advanced analysis section
    st.subheader("Advanced Trade Analysis")
    
    # Analysis type selection
    analysis_type = st.radio(
        "Select Analysis Type",
        ["Trade Balance Analysis", "Market Concentration", "Growth Analysis"]
    )
    
    if analysis_type == "Trade Balance Analysis":
        # Trade balance analysis
        st.markdown("### Trade Balance Analysis")
        fig = st.session_state.advanced_analysis.analyze_trade_balance(trade_data, st.session_state.theme)
        st.plotly_chart(fig, use_container_width=True)
        
        # Trade balance insights
        insights = st.session_state.advanced_analysis.get_trade_balance_insights(trade_data)
        st.markdown("#### Key Insights")
        for insight in insights:
            st.markdown(f"- {insight}")
    
    elif analysis_type == "Market Concentration":
        # Market concentration analysis
        st.markdown("### Market Concentration Analysis")
        fig = st.session_state.advanced_analysis.analyze_market_concentration(trade_data, st.session_state.theme)
        st.plotly_chart(fig, use_container_width=True)
        
        # Concentration insights
        insights = st.session_state.advanced_analysis.get_market_concentration_insights(trade_data)
        st.markdown("#### Key Insights")
        for insight in insights:
            st.markdown(f"- {insight}")
    
    else:  # Growth Analysis
        # Growth analysis
        st.markdown("### Growth Analysis")
        fig = st.session_state.advanced_analysis.analyze_growth(trade_data, st.session_state.theme)
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth insights
        insights = st.session_state.advanced_analysis.get_growth_insights(trade_data)
        st.markdown("#### Key Insights")
        for insight in insights:
            st.markdown(f"- {insight}")
    
    # Comparative analysis
    st.subheader("Comparative Analysis")
    
    # Select countries for comparison
    countries = sorted(trade_data['Reporter'].unique())
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        options=countries,
        default=countries[:2]
    )
    
    if selected_countries:
        fig = st.session_state.advanced_analysis.compare_countries(
            trade_data, 
            selected_countries,
            st.session_state.theme
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Export analysis results
    if st.button("Export Analysis Results"):
        st.session_state.advanced_analysis.export_analysis(trade_data)
        st.success("Analysis results exported successfully!") 