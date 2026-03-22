import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIG ---
# This must be the very first Streamlit command
st.set_page_config(
    page_title="Pakistan Startup Insights 2026",
    page_icon="🇵🇰",
    layout="wide"
)

# --- 2. CUSTOM CSS FOR STYLING ---
# Fixing the 'unsafe_allow_html' parameter here
st.markdown("""
    <style>
    /* Background color for the entire app */
    .stApp {
        background-color: #f4f7f9;
    }
    
    /* Styling the Metric Cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Titles and Header coloring */
    h1, h2, h3 {
        color: #1e3d59;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOAD & CLEAN DATA ---
@st.cache_data
def load_data():
    # Ensure the file is in the same directory as this script
    df = pd.read_csv("final_pak_startups_for_analysis.csv")
    
    # Cleaning
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    df['founded_date'] = pd.to_datetime(df['founded_date'], errors='coerce')
    df['founded_year'] = df['founded_date'].dt.year
    
    # Fill NAs for filters to avoid errors
    df['city'] = df['city'].fillna("Unknown")
    df['industry_vertical'] = df['industry_vertical'].fillna("Other")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV file not found. Please ensure 'final_pak_startups_for_analysis.csv' is in the folder.")
    st.stop()

# --- 4. SIDEBAR FILTERS ---
st.sidebar.header("🎯 Dashboard Filters")
st.sidebar.write("Refine the data shown on the right.")

city_list = sorted(df['city'].unique())
city_filter = st.sidebar.multiselect("Select Cities", options=city_list, default=city_list[:5])

industry_list = sorted(df['industry_vertical'].unique())
industry_filter = st.sidebar.multiselect("Select Industries", options=industry_list, default=industry_list[:5])

# Apply filters
filtered_df = df[
    (df['city'].isin(city_filter)) & 
    (df['industry_vertical'].isin(industry_filter))
]

# --- 5. MAIN DASHBOARD ---
st.title("🇵🇰 Pakistan Startup Ecosystem")
st.markdown("An interactive analysis of growth, funding, and industry distribution.")

# Key Performance Indicators (KPIs)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Startups", f"{len(filtered_df)}")
m2.metric("Active Cities", f"{filtered_df['city'].nunique()}")
m3.metric("Avg Founded Year", int(filtered_df['founded_year'].mean()) if not filtered_df.empty else 0)
m4.metric("Key Industry", filtered_df['industry_vertical'].mode()[0] if not filtered_df.empty else "N/A")

st.markdown("---")

# Visualizations Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Cities by Startup Count")
    city_counts = filtered_df['city'].value_counts().head(10).reset_index()
    fig_city = px.bar(city_counts, x='city', y='count', 
                      color='count', color_continuous_scale='GnBu')
    st.plotly_chart(fig_city, use_container_width=True)

with col2:
    st.subheader("Industry Distribution")
    ind_counts = filtered_df['industry_vertical'].value_counts().head(8).reset_index()
    fig_ind = px.pie(ind_counts, values='count', names='industry_vertical', hole=0.5)
    st.plotly_chart(fig_ind, use_container_width=True)

# Visualizations Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Founding Trends (Year-on-Year)")
    year_trends = filtered_df.groupby('founded_year').size().reset_index(name='count')
    fig_trend = px.line(year_trends, x='founded_year', y='count', markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with col4:
    st.subheader("Funding Distribution")
    # Assuming the column exists from your original snippet
    if 'funding_round_1_investment' in filtered_df.columns:
        fig_fund = px.histogram(filtered_df, x='funding_round_1_investment', 
                                nbins=20, color_discrete_sequence=['#1e3d59'])
        st.plotly_chart(fig_fund, use_container_width=True)
    else:
        st.info("Funding data column not found.")

# --- 6. RAW DATA SECTION ---
st.markdown("---")
with st.expander("🔍 Explore Raw Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='pak_startup_data.csv',
        mime='text/csv',
    )