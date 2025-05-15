import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def show_reports():
    st.title("📊 Trade Reports")
    
    # Load data
    trade_data = st.session_state.trade_data_instance.get_sample_trade_data()
    
    # Report type selection
    report_type = st.radio(
        "Select Report Type",
        ["Monthly Report", "Quarterly Report", "Annual Report"]
    )
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime(2023, 12, 31))
    
    # Generate report
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            # Generate report content
            report_content = st.session_state.report_generator.generate_report(
                trade_data,
                report_type,
                start_date,
                end_date
            )
            
            # Display report
            st.markdown(report_content)
            
            # Export options
            st.subheader("Export Options")
            export_format = st.selectbox(
                "Select Export Format",
                ["PDF", "Excel", "HTML"]
            )
            
            if st.button("Export Report"):
                st.session_state.report_generator.export_report(
                    report_content,
                    export_format,
                    f"{report_type}_{start_date}_{end_date}"
                )
                st.success(f"Report exported as {export_format} successfully!")
    
    # Report templates
    st.subheader("Report Templates")
    template_type = st.selectbox(
        "Select Template",
        ["Standard Template", "Executive Summary", "Detailed Analysis"]
    )
    
    if st.button("Preview Template"):
        template = st.session_state.report_generator.get_template(template_type)
        st.markdown(template)
        
        if st.button("Use Template"):
            st.session_state.report_generator.set_template(template_type)
            st.success("Template applied successfully!")
    
    # Report history
    st.subheader("Report History")
    history = st.session_state.report_generator.get_report_history()
    if history:
        for report in history:
            with st.expander(f"{report['type']} - {report['date']}"):
                st.markdown(report['content'])
    else:
        st.info("No previous reports found.") 