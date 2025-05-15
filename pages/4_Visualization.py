import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def show_visualization():
    st.title("📈 Trade Visualization")
    
    # Load data
    trade_data = st.session_state.trade_data_instance.get_sample_trade_data()
    
    # Visualization type selection
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Time Series", "Geographic Map", "Bar Chart", "Pie Chart", "Heatmap"]
    )
    
    # Visualization options
    if viz_type == "Time Series":
        st.subheader("Time Series Analysis")
        metric = st.selectbox(
            "Select Metric",
            ["Trade Volume", "Trade Value", "Balance"]
        )
        fig = st.session_state.visualizer.create_time_series(trade_data, metric)
        st.plotly_chart(fig)
        
    elif viz_type == "Geographic Map":
        st.subheader("Geographic Distribution")
        map_type = st.selectbox(
            "Select Map Type",
            ["Trade Volume", "Trade Partners", "Trade Routes"]
        )
        fig = st.session_state.visualizer.create_geographic_map(trade_data, map_type)
        st.plotly_chart(fig)
        
    elif viz_type == "Bar Chart":
        st.subheader("Comparative Analysis")
        x_axis = st.selectbox(
            "Select X-Axis",
            ["Country", "Product", "Year"]
        )
        y_axis = st.selectbox(
            "Select Y-Axis",
            ["Volume", "Value", "Growth Rate"]
        )
        fig = st.session_state.visualizer.create_bar_chart(trade_data, x_axis, y_axis)
        st.plotly_chart(fig)
        
    elif viz_type == "Pie Chart":
        st.subheader("Composition Analysis")
        category = st.selectbox(
            "Select Category",
            ["Trade Partners", "Product Categories", "Trade Types"]
        )
        fig = st.session_state.visualizer.create_pie_chart(trade_data, category)
        st.plotly_chart(fig)
        
    elif viz_type == "Heatmap":
        st.subheader("Correlation Analysis")
        metrics = st.multiselect(
            "Select Metrics",
            ["Volume", "Value", "Growth Rate", "Balance"],
            default=["Volume", "Value"]
        )
        fig = st.session_state.visualizer.create_heatmap(trade_data, metrics)
        st.plotly_chart(fig)
    
    # Customization options
    st.subheader("Customization Options")
    col1, col2 = st.columns(2)
    with col1:
        color_scheme = st.selectbox(
            "Color Scheme",
            ["Default", "Pastel", "Dark", "Light"]
        )
    with col2:
        chart_style = st.selectbox(
            "Chart Style",
            ["Default", "Minimal", "Professional", "Creative"]
        )
    
    # Export options
    st.subheader("Export Options")
    export_format = st.selectbox(
        "Select Export Format",
        ["PNG", "JPEG", "SVG", "PDF"]
    )
    
    if st.button("Export Visualization"):
        st.session_state.visualizer.export_visualization(
            fig,
            export_format,
            f"{viz_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        st.success(f"Visualization exported as {export_format} successfully!")
    
    # Interactive features
    st.subheader("Interactive Features")
    if st.checkbox("Show Data Table"):
        st.dataframe(trade_data)
    
    if st.checkbox("Show Statistics"):
        stats = st.session_state.visualizer.get_statistics(trade_data)
        st.write(stats)
    
    # Save visualization
    if st.button("Save Visualization"):
        st.session_state.visualizer.save_visualization(fig)
        st.success("Visualization saved successfully!") 