import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Page config
st.set_page_config(page_title="Mutual Fund Visualizer", layout="wide")

st.title("📊 Mutual Fund Return Explorer - India")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df = df.dropna(subset=['category', 'AMC_name', 'Mutual Fund Name', 'return_1yr'])
    df['return_1yr'] = pd.to_numeric(df['return_1yr'], errors='coerce')
    df = df.dropna(subset=['return_1yr'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")
category = st.sidebar.selectbox("Select Category", sorted(df['category'].unique()))
df_cat = df[df['category'] == category]

amc = st.sidebar.selectbox("Select AMC", sorted(df_cat['AMC_name'].unique()))
df_amc = df_cat[df_cat['AMC_name'] == amc]

# Search for Mutual Fund
search_query = st.sidebar.text_input("🔍 Search Mutual Fund Name")

if search_query:
    df_filtered = df_amc[df_amc['Mutual Fund Name'].str.contains(search_query, case=False, na=False)]
else:
    df_filtered = df_amc.copy()

# Limit number of top funds
top_n = st.sidebar.slider("Top N Funds by Return", min_value=1, max_value=30, value=10)
sort_order = st.sidebar.radio("Sort by Return", options=["Descending", "Ascending"])

# Sort and limit
df_filtered = df_filtered.sort_values(by='return_1yr', ascending=(sort_order == "Ascending"))
df_filtered = df_filtered.head(top_n)

# Display
st.markdown(f"### 🏢 {amc} – {category} Category")
st.markdown(f"Showing top **{top_n}** funds based on **1-Year Return**")

# Plot
if df_filtered.empty:
    st.warning("No results found with current filters/search.")
else:
    fig, ax = plt.subplots(figsize=(14, 6))
    sb.barplot(data=df_filtered, x='Mutual Fund Name', y='return_1yr', palette='flare', ax=ax)
    plt.xticks(rotation=90)
    plt.ylabel("1-Year Return (%)")
    plt.xlabel("")
    st.pyplot(fig)

    # Show data
    with st.expander("🔍 View Table Data"):
        st.dataframe(df_filtered[['Mutual Fund Name', 'return_1yr']].reset_index(drop=True))

    # Download filtered data
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", csv, file_name='filtered_mutual_funds.csv', mime='text/csv')
