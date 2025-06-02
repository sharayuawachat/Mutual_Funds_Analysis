import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.title("🇮🇳 Mutual Fund 1-Year Return Visualizer")

# Load dataset from file
try:
    df = pd.read_csv("mutual_funds_india.csv")
except FileNotFoundError:
    st.error("❌ File 'mutual_funds_india.csv' not found. Please make sure it's in the same folder as this app.")
    st.stop()

# Required columns
required_cols = ['category', 'AMC_name', 'Mutual Fund Name', 'return_1yr']

# Validate columns
if not all(col in df.columns for col in required_cols):
    st.error(f"Dataset must contain the following columns: {required_cols}")
    st.stop()

# Clean data
df = df.dropna(subset=required_cols)
df['return_1yr'] = pd.to_numeric(df['return_1yr'], errors='coerce')
df = df.dropna(subset=['return_1yr'])

# Sidebar filters
selected_category = st.selectbox("Select Category", sorted(df['category'].unique()))
df_category = df[df['category'] == selected_category]

selected_amc = st.selectbox("Select AMC", sorted(df_category['AMC_name'].unique()))
df_filtered = df_category[df_category['AMC_name'] == selected_amc]

# Plot
if df_filtered.empty:
    st.warning("No mutual funds found for this combination.")
else:
    st.subheader(f"1-Year Returns for '{selected_amc}' in '{selected_category}'")
    fig, ax = plt.subplots(figsize=(12, 6))
    sb.barplot(data=df_filtered, x='Mutual Fund Name', y='return_1yr', palette='hot', ax=ax)
    plt.xticks(rotation=90)
    plt.ylabel("Return (1 Year %)")
    st.pyplot(fig)
