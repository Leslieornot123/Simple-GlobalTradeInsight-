import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="Large Data Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def generate_large_dataset(rows=1000000, cols=10):
    """Generate a large dataset efficiently"""
    # Use numpy's random generator for better performance
    rng = np.random.default_rng()
    data = rng.random((rows, cols))
    return pd.DataFrame(data, columns=[f'Feature {i}' for i in range(cols)])

@st.cache_data
def process_data(df):
    """Process data efficiently"""
    # Calculate statistics in chunks
    stats = df.describe()
    # Add derived features
    df['Sum'] = df.sum(axis=1)
    df['Mean'] = df.mean(axis=1)
    return df, stats

def main():
    st.title("📊 Large Data Visualization")
    
    # Sidebar controls
    st.sidebar.header("Controls")
    data_size = st.sidebar.slider("Dataset Size (millions of rows)", 1, 10, 1)
    num_features = st.sidebar.slider("Number of Features", 5, 20, 10)
    
    if st.sidebar.button("Generate Data"):
        st.session_state.df = None
    
    # Generate and process data
    if 'df' not in st.session_state or st.session_state.df is None:
        with st.spinner("🔄 Generating large dataset..."):
            start_time = time.time()
            df = generate_large_dataset(rows=data_size * 1000000, cols=num_features)
            df, stats = process_data(df)
            st.session_state.df = df
            st.session_state.stats = stats
            st.session_state.generation_time = time.time() - start_time
    
    # Display dataset info
    st.subheader("📈 Dataset Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", f"{len(st.session_state.df):,}")
    with col2:
        st.metric("Total Columns", len(st.session_state.df.columns))
    with col3:
        st.metric("Generation Time", f"{st.session_state.generation_time:.2f} seconds")
    
    # Data preview
    st.subheader("📋 Data Preview")
    st.dataframe(st.session_state.df.head())
    
    # Statistics
    st.subheader("📊 Statistics")
    st.dataframe(st.session_state.stats)
    
    # Visualizations
    st.subheader("📉 Visualizations")
    
    # Feature selection
    col1, col2 = st.columns(2)
    with col1:
        selected_feature = st.selectbox(
            "Select feature for distribution",
            st.session_state.df.columns[:-2]  # Exclude Sum and Mean
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Distribution", "Box Plot", "Correlation"])
    
    with tab1:
        # Use plotly for better performance with large datasets
        fig = px.histogram(
            st.session_state.df, 
            x=selected_feature,
            title=f"Distribution of {selected_feature}",
            nbins=100
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.box(
            st.session_state.df,
            y=selected_feature,
            title=f"Box Plot of {selected_feature}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Calculate correlation matrix
        corr = st.session_state.df.corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu'
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    # Memory usage
    st.sidebar.subheader("System Information")
    st.sidebar.write(f"Data size: {st.session_state.df.memory_usage().sum() / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main() 