import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("hermes_price_data.csv")

# App title
st.title("Hermès Price Tracker")
st.markdown("Track retail and resale prices for Hermès bags (2015–2025)")

# Sidebar filters
style_options = sorted(df["Style"].unique())
selected_style = st.selectbox("Select Bag Style:", style_options)

# Dynamically load color options based on selected style
color_options = sorted(df[df["Style"] == selected_style]["Color"].unique())
color_options.insert(0, "All Colors")
selected_color = st.selectbox("Select Color:", color_options)

# Apply filters
if selected_color == "All Colors":
    filtered_df = (
        df[df["Style"] == selected_style]
        .groupby("Year", as_index=False)
        .agg({
            "Retail Price": "mean",
            "Resale - New": "mean",
            "Resale - Pre-Owned": "mean"
        })
    )
    title_color = "All Colors (avg)"
else:
    filtered_df = df[(df["Style"] == selected_style) & (df["Color"] == selected_color)]
    title_color = selected_color

# Line chart of pricing
st.sub
