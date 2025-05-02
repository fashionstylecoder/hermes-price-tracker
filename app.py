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
st.subheader("📈 Price Trend Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_df["Year"], filtered_df["Retail Price"], label="Retail Price", linewidth=2)
ax.plot(filtered_df["Year"], filtered_df["Resale - New"], label="Resale – New", linestyle='--')
ax.plot(filtered_df["Year"], filtered_df["Resale - Pre-Owned"], label="Resale – Pre-Owned", linestyle=':')
ax.set_ylabel("Price (USD)")
ax.set_xlabel("Year")
ax.set_title(f"{selected_style} in {title_color}")
ax.legend()
st.pyplot(fig)

# Uplift Calculations
st.subheader("💰 Resale Uplift Insights")

# Add % uplift columns
filtered_df["Uplift - New"] = ((filtered_df["Resale - New"] - filtered_df["Retail Price"]) / filtered_df["Retail Price"]) * 100
filtered_df["Uplift - Pre-Owned"] = ((filtered_df["Resale - Pre-Owned"] - filtered_df["Retail Price"]) / filtered_df["Retail Price"]) * 100

# Text summaries
avg_new = filtered_df["Uplift - New"].mean()
avg_pre = filtered_df["Uplift - Pre-Owned"].mean()
st.markdown(f"**Average Resale Uplift (New):** {avg_new:.1f}%")
st.markdown(f"**Average Resale Uplift (Pre-Owned):** {avg_pre:.1f}%")

# Uplift chart
fig2, ax
