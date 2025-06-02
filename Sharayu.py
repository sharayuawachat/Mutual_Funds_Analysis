import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Load your dataset (replace with actual file path or uploader)
df = pd.read_csv("your_dataset.csv")  # Update with your file name

st.title("Mutual Fund Return Visualizer")

# Unique categories
categories = df['category'].dropna().unique()
selected_category = st.selectbox("Select Category:", sorted(categories))

# Filter based on category
df_cat = df[df['category'] == selected_category]

# Unique AMC names for the selected category
amc_names = df_cat['AMC_name'].dropna().unique()
selected_amc = st.selectbox("Select AMC Name:", sorted(amc_names))

# Filter based on AMC
df_filtered = df_cat[df_cat['AMC_name'] == selected_amc]

# Plot
st.subheader(f"1-Year Returns for Mutual Funds in {selected_amc} ({selected_category})")
fig, ax = plt.subplots(figsize=(12, 6))
sb.barplot(data=df_filtered, x='MutualFundName', y='return_1yr', palette='hot', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
