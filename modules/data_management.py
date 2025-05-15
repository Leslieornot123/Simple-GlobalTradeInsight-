import streamlit as st
import pandas as pd
from cloud_storage import CloudStorage
import plotly.express as px
from visualization import TradeVisualization

def data_management_page():
    st.title("📊 Data Management & Custom Analysis")
    
    # Initialize cloud storage
    storage = CloudStorage()
    
    # Sidebar options
    action = st.sidebar.radio(
        "Choose Action",
        ["Upload Data", "View Datasets", "Custom Analysis"]
    )
    
    if action == "Upload Data":
        st.header("Upload Trade Data")
        
        # File upload
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                # Read and validate data
                df = pd.read_csv(uploaded_file)
                required_columns = ['Year', 'Reporter', 'Partner', 'TradeValue', 'TradeFlow']
                
                if all(col in df.columns for col in required_columns):
                    st.success("File structure validated successfully!")
                    
                    # Preview data
                    st.subheader("Data Preview")
                    st.dataframe(df.head())
                    
                    # Upload to cloud
                    dataset_name = st.text_input("Dataset Name", "trade_data")
                    if st.button("Save Dataset"):
                        success, message = storage.upload_dataframe(
                            df,
                            st.session_state.get('username', 'guest'),
                            dataset_name
                        )
                        if success:
                            st.success(f"Dataset uploaded successfully as {message}")
                        else:
                            st.error(f"Upload failed: {message}")
                else:
                    st.error("Invalid file structure. Please ensure your CSV contains the required columns.")
                    st.write("Required columns:", required_columns)
            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    elif action == "View Datasets":
        st.header("Your Datasets")
        
        # List user's datasets
        datasets = storage.get_user_datasets(st.session_state.get('username', 'guest'))
        
        if datasets:
            selected_dataset = st.selectbox("Select Dataset", datasets)
            
            if selected_dataset:
                df = storage.load_dataset(selected_dataset)
                if df is not None:
                    st.subheader("Dataset Preview")
                    st.dataframe(df.head())
                    
                    # Dataset actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Delete Dataset"):
                            if storage.delete_dataset(selected_dataset):
                                st.success("Dataset deleted successfully")
                                st.rerun()
                            else:
                                st.error("Failed to delete dataset")
                    
                    with col2:
                        if st.button("Download Dataset"):
                            csv = df.to_csv(index=False)
                            st.download_button(
                                "Download CSV",
                                csv,
                                f"{selected_dataset.split('/')[-1]}",
                                "text/csv"
                            )
        else:
            st.info("No datasets found. Upload some data to get started!")
    
    else:  # Custom Analysis
        st.header("Custom Trade Analysis")
        
        # Get available datasets
        datasets = storage.get_user_datasets(st.session_state.get('username', 'guest'))
        
        if datasets:
            selected_dataset = st.selectbox("Select Dataset for Analysis", datasets)
            df = storage.load_dataset(selected_dataset)
            
            if df is not None:
                # Analysis options
                analysis_type = st.selectbox(
                    "Select Analysis Type",
                    ["Trade Flow Map", "Trade Balance", "Market Share",
                     "Growth Trends", "Commodity Analysis", "Seasonal Patterns"]
                )
                
                # Filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    years = sorted(df['Year'].unique())
                    selected_years = st.multiselect("Select Years", years, default=years)
                
                with col2:
                    reporters = sorted(df['Reporter'].unique())
                    selected_reporters = st.multiselect("Select Reporters", reporters, default=reporters[:1])
                
                with col3:
                    partners = sorted(df['Partner'].unique())
                    selected_partners = st.multiselect("Select Partners", partners, default=partners)
                
                # Filter data
                filtered_df = df[
                    (df['Year'].isin(selected_years)) &
                    (df['Reporter'].isin(selected_reporters)) &
                    (df['Partner'].isin(selected_partners))
                ]
                
                # Create visualization
                viz = TradeVisualization()
                
                if analysis_type == "Trade Flow Map":
                    min_value = st.slider(
                        "Minimum Trade Value (USD)",
                        min_value=int(filtered_df['TradeValue'].min()),
                        max_value=int(filtered_df['TradeValue'].max()),
                        value=int(filtered_df['TradeValue'].median())
                    )
                    fig = viz.create_trade_flow_map(filtered_df, min_value=min_value)
                
                elif analysis_type == "Trade Balance":
                    fig = viz.create_trade_balance_chart(filtered_df)
                
                elif analysis_type == "Market Share":
                    top_n = st.slider("Number of Partners", 5, 20, 10)
                    fig = viz.create_market_share_chart(filtered_df, top_n=top_n)
                
                elif analysis_type == "Growth Trends":
                    fig = viz.create_growth_trend_chart(filtered_df)
                
                elif analysis_type == "Commodity Analysis":
                    fig = viz.create_commodity_analysis(filtered_df)
                
                else:  # Seasonal Patterns
                    fig = viz.create_seasonal_analysis(filtered_df)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Download plot
                if st.button("Download Plot"):
                    fig.write_html(f"trade_analysis_{analysis_type}.html")
                    with open(f"trade_analysis_{analysis_type}.html", "rb") as f:
                        st.download_button(
                            "Download HTML",
                            f,
                            f"trade_analysis_{analysis_type}.html"
                        )
        else:
            st.info("No datasets found. Upload some data to perform custom analysis!")

if __name__ == "__main__":
    data_management_page() 