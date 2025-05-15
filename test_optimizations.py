import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from cloud_storage import CloudStorage

# Configure Streamlit page
st.set_page_config(
    page_title="Data Visualization App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_large_dataset():
    """Generate a large dataset for visualization"""
    data = np.random.rand(1000000, 10)
    return pd.DataFrame(data, columns=[f'Feature {i}' for i in range(10)])

def process_data(df):
    """Process data for visualization"""
    # Calculate some statistics
    stats = df.describe()
    # Add some derived features
    df['Sum'] = df.sum(axis=1)
    df['Mean'] = df.mean(axis=1)
    return df, stats

def main():
    st.title("📊 Interactive Data Visualization")
    
    # Sidebar controls
    st.sidebar.header("Controls")
    if st.sidebar.button("Generate New Data"):
        st.session_state.df = None
    
    # Generate and process data
    if 'df' not in st.session_state or st.session_state.df is None:
        with st.spinner("🔄 Generating data..."):
            df = generate_large_dataset()
            df, stats = process_data(df)
            st.session_state.df = df
            st.session_state.stats = stats
    
    # Display data
    st.subheader("📈 Dataset Overview")
    st.write(f"Total rows: {len(st.session_state.df):,}")
    st.write("First 5 rows:")
    st.dataframe(st.session_state.df.head())
    
    # Statistics
    st.subheader("📊 Statistics")
    st.dataframe(st.session_state.stats)
    
    # Visualizations
    st.subheader("📉 Visualizations")
    
    # Feature distribution
    col1, col2 = st.columns(2)
    with col1:
        selected_feature = st.selectbox(
            "Select feature for distribution",
            st.session_state.df.columns[:-2]  # Exclude Sum and Mean
        )
        fig = px.histogram(st.session_state.df, x=selected_feature, title=f"Distribution of {selected_feature}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(st.session_state.df, y=selected_feature, title=f"Box Plot of {selected_feature}")
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("🌡️ Correlation Heatmap")
    corr = st.session_state.df.corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu'
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Save data option
    if st.sidebar.button("💾 Save to Cloud"):
        with st.spinner("Saving data..."):
            storage = CloudStorage()
            success, path = storage.upload_dataframe(st.session_state.df, "user", "visualization_data")
            if success:
                st.sidebar.success(f"Data saved to: {path}")
            else:
                st.sidebar.error(f"Failed to save: {path}")

if __name__ == "__main__":
    main() 