import streamlit as st
import plotly.express as px
import pandas as pd

def show_reports():
    st.title("📄 Trade Reports")
    
    if 'trade_data_instance' in st.session_state:
        data = st.session_state.trade_data_instance.get_sample_trade_data()
        
        # Report type selector
        report_type = st.selectbox(
            "Select Report Type",
            ["Trade Summary", "Country Profile", "Trade Flow Report", "Custom Report"]
        )
        
        if report_type == "Trade Summary":
            st.subheader("Trade Summary Report")
            
            # Summary statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Trade Value Statistics (USD)")
                total_value = data['TradeValue'].sum()
                stats = data['TradeValue'].describe()
                stats_df = pd.DataFrame({
                    'Metric': ['Total', 'Mean', 'Std Dev', 'Min', 'Max'],
                    'Value': [
                        f"${total_value/1e9:.2f}B",
                        f"${stats['mean']/1e6:.2f}M",
                        f"${stats['std']/1e6:.2f}M",
                        f"${stats['min']/1e6:.2f}M",
                        f"${stats['max']/1e6:.2f}M"
                    ]
                })
                st.dataframe(stats_df)
            
            with col2:
                st.write("Trade Flow Distribution")
                flow_dist = data['TradeFlow'].value_counts()
                fig = px.pie(values=flow_dist.values, names=flow_dist.index)
                st.plotly_chart(fig)
            
        elif report_type == "Country Profile":
            st.subheader("Country Profile Report")
            
            # Country selector
            country = st.selectbox("Select Country", sorted(data['Reporter'].unique()))
            
            # Filter data for selected country
            country_data = data[data['Reporter'] == country]
            
            # Trade statistics
            total_trade = country_data['TradeValue'].sum()
            exports = country_data[country_data['TradeFlow'] == 'Export']['TradeValue'].sum()
            imports = country_data[country_data['TradeFlow'] == 'Import']['TradeValue'].sum()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trade", f"${total_trade/1e9:.2f}B")
            col2.metric("Total Exports", f"${exports/1e9:.2f}B")
            col3.metric("Total Imports", f"${imports/1e9:.2f}B")
            
            # Trade partners
            st.write("Top Trading Partners")
            partners = country_data.groupby('Partner')['TradeValue'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(x=partners.index, y=partners.values/1e9,
                        labels={'x': 'Partner', 'y': 'Trade Value (Billion USD)'})
            st.plotly_chart(fig)
            
        elif report_type == "Trade Flow Report":
            st.subheader("Trade Flow Report")
            
            # Time period selector
            years = sorted(data['Year'].unique())
            start_year = st.selectbox("Start Year", years, index=0)
            end_year = st.selectbox("End Year", years, index=len(years)-1)
            
            # Filter data for selected period
            period_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
            
            # Trade flow trends
            flow_trends = period_data.groupby(['Year', 'TradeFlow'])['TradeValue'].sum().reset_index()
            fig = px.line(flow_trends, x='Year', y='TradeValue', color='TradeFlow',
                         title='Trade Flows Over Time')
            st.plotly_chart(fig)
            
            # Trade flow summary table
            st.write("Trade Flow Summary")
            flow_summary = period_data.groupby('TradeFlow').agg({
                'TradeValue': ['sum', 'mean', 'count']
            }).round(2)
            flow_summary.columns = ['Total Value', 'Average Value', 'Number of Transactions']
            st.dataframe(flow_summary)
            
        elif report_type == "Custom Report":
            st.subheader("Custom Report")
            
            # Filters
            col1, col2 = st.columns(2)
            
            with col1:
                selected_years = st.multiselect(
                    "Select Years",
                    options=sorted(data['Year'].unique()),
                    default=sorted(data['Year'].unique())[-5:]
                )
                
                selected_flows = st.multiselect(
                    "Select Trade Flows",
                    options=sorted(data['TradeFlow'].unique()),
                    default=sorted(data['TradeFlow'].unique())
                )
            
            with col2:
                selected_countries = st.multiselect(
                    "Select Countries",
                    options=sorted(data['Reporter'].unique()),
                    default=sorted(data['Reporter'].unique())[:5]
                )
                
                min_value = st.number_input(
                    "Minimum Trade Value (USD)",
                    value=0.0,
                    step=1000000.0
                )
            
            # Filter data based on selections
            filtered_data = data[
                (data['Year'].isin(selected_years)) &
                (data['TradeFlow'].isin(selected_flows)) &
                (data['Reporter'].isin(selected_countries)) &
                (data['TradeValue'] >= min_value)
            ]
            
            # Show filtered data
            st.write(f"Filtered Data ({len(filtered_data)} records)")
            st.dataframe(filtered_data)
            
            # Download button
            if not filtered_data.empty:
                csv = filtered_data.to_csv(index=False)
                st.download_button(
                    "Download Report",
                    csv,
                    "trade_report.csv",
                    "text/csv",
                    key='download-csv'
                )
    
    else:
        st.warning("No trade data available. Please initialize the data first.") 