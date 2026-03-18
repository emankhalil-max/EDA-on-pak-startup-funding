import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Title
st.title("Pakistan Startup Ecosystem Dashboard")

st.write("Interactive dashboard analyzing startup trends, industries, and funding.")

# Load Data
df = pd.read_csv("final_pak_startups_for_analysis.csv")

# Clean columns
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# Convert dates
df['founded_date'] = pd.to_datetime(df['founded_date'], errors='coerce')
df['founded_year'] = df['founded_date'].dt.year

# Sidebar Filters
st.sidebar.header("Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=df['city'].dropna().unique(),
    default=df['city'].dropna().unique()
)

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=df['industry_vertical'].dropna().unique(),
    default=df['industry_vertical'].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df['city'].isin(city_filter)) &
    (df['industry_vertical'].isin(industry_filter))
]

st.subheader("Dataset Overview")

st.write("Number of Startups:", filtered_df.shape[0])



# 1️⃣ Top Startup Cities
st.subheader("Top Startup Cities")

city_counts = filtered_df['city'].value_counts().head(10)

fig, ax = plt.subplots()
city_counts.plot(kind='bar', ax=ax)
plt.xticks(rotation=45)

st.pyplot(fig)



# 2️⃣ Top Industries
st.subheader("Top Startup Industries")

industry_counts = filtered_df['industry_vertical'].value_counts().head(10)

fig, ax = plt.subplots()
industry_counts.plot(kind='bar', ax=ax)
plt.xticks(rotation=45)

st.pyplot(fig)



# 3️⃣ Startup Growth Over Time
st.subheader("Startup Growth by Year")

year_counts = filtered_df['founded_year'].value_counts().sort_index()

fig, ax = plt.subplots()
year_counts.plot(marker='o', ax=ax)

st.pyplot(fig)


# 4️⃣ Operating Status
st.subheader("Startup Operating Status")

status_counts = filtered_df['operating_status'].value_counts()

fig, ax = plt.subplots()
status_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)

plt.ylabel("")

st.pyplot(fig)



# 5️⃣ Funding Distribution
st.subheader("Funding Distribution")

fig, ax = plt.subplots()

sns.histplot(filtered_df['funding_round_1_investment'].dropna(), bins=20, ax=ax)

st.pyplot(fig)



# Raw Data Section
st.subheader("View Dataset")

if st.checkbox("Show Raw Data"):
    st.write(filtered_df)