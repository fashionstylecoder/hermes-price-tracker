import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("hermes_price_data.csv")

# App title
st.title("Hermès Price Tracker")
st.markdown("Select a bag style and color to view retail and resale price trends (2019–2024)")

# Sidebar filters
style_options = sorted(df["Style"].unique())
selected_style = st.selectbox("Select Bag Style:", style_options)

color_options = sorted(df[df["Style"] == selected_style]["Color"].unique())
selected_color = st.selectbox("Select Color:", color_options)

# Filtered DataFrame
filtered_df = df[(df["Style"] == selected_style) & (df["Color"] == selected_color)]

# Plotting
fig, ax = plt.subplots()
ax.plot(filtered_df["Year"], filtered_df["Retail Price"], label="Retail Price", linewidth=2)
ax.plot(filtered_df["Year"], filtered_df["Resale - New"], label="Resale – New", linestyle='--')
ax.plot(filtered_df["Year"], filtered_df["Resale - Pre-Owned"], label="Resale – Pre-Owned", linestyle=':')
ax.set_ylabel("Price (USD)")
ax.set_xlabel("Year")
ax.set_title(f"{selected_style} in {selected_color}")
ax.legend()
st.pyplot(fig)
