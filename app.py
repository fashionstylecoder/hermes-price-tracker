import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("hermes_price_data.csv")

# App title
st.title("Hermès Price Tracker")
st.markdown("Track retail and resale prices for Hermès bags (2015–2025)")

# Sidebar filters
style_options = sorted(df["Style"].unique())
selected_style = st.selectbox("Select Bag Style:", style_options)

color_options = sorted(df[df["Style"] == selected_style]["Color"].unique())
color_options.insert(0, "All Colors")
selected_color = st.selectbox("Select Color:", color_options)

# Filter data
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

# 📈 Price Trend Chart (Plotly)
st.subheader("📈 Price Trend Over Time")

fig_price = go.Figure()
fig_price.add_trace(go.Scatter(
    x=filtered_df["Year"], y=filtered_df["Retail Price"], mode='lines+markers', name='Retail Price',
    hovertemplate='Year: %{x}<br>Retail: $%{y:,.0f}<extra></extra>'
))
fig_price.add_trace(go.Scatter(
    x=filtered_df["Year"], y=filtered_df["Resale - New"], mode='lines+markers', name='Resale – New',
    hovertemplate='Year: %{x}<br>New Resale: $%{y:,.0f}<extra></extra>'
))
fig_price.add_trace(go.Scatter(
    x=filtered_df["Year"], y=filtered_df["Resale - Pre-Owned"], mode='lines+markers', name='Resale – Pre-Owned',
    hovertemplate='Year: %{x}<br>Pre-Owned Resale: $%{y:,.0f}<extra></extra>'
))
fig_price.update_layout(
    title=f"Hermès {selected_style} in {title_color}",
    xaxis_title="Year",
    yaxis_title="Price (USD)",
    hovermode="x unified"
)
st.plotly_chart(fig_price, use_container_width=True)

# 💰 Premium Summary
st.subheader(f"💰 Resale Premium Insights: Hermès {selected_style} in {title_color}")

filtered_df["Premium - New"] = ((filtered_df["Resale - New"] - filtered_df["Retail Price"]) / filtered_df["Retail Price"]) * 100
filtered_df["Premium - Pre-Owned"] = ((filtered_df["Resale - Pre-Owned"] - filtered_df["Retail Price"]) / filtered_df["Retail Price"]) * 100

avg_new = filtered_df["Premium - New"].mean()
avg_pre = filtered_df["Premium - Pre-Owned"].mean()
st.markdown(f"**Average Resale Premium (New):** {avg_new:.1f}%")
st.markdown(f"**Average Resale Premium (Pre-Owned):** {avg_pre:.1f}%")

# 📊 Premium Chart (Plotly)
fig_premium = go.Figure()
fig_premium.add_trace(go.Scatter(
    x=filtered_df["Year"], y=filtered_df["Premium - New"], mode='lines+markers', name='New Resale Premium',
    hovertemplate='Year: %{x}<br>New Premium: %{y:.1f}%<extra></extra>'
))
fig_premium.add_trace(go.Scatter(
    x=filtered_df["Year"], y=filtered_df["Premium - Pre-Owned"], mode='lines+markers', name='Pre-Owned Resale Premium',
    hovertemplate='Year: %{x}<br>Pre-Owned Premium: %{y:.1f}%<extra></extra>'
))
fig_premium.update_layout(
    title=f"Resale Premium for Hermès {selected_style} in {title_color}",
    xaxis_title="Year",
    yaxis_title="Premium (%)",
    hovermode="x unified"
)
st.plotly_chart(fig_premium, use_container_width=True)

# 📥 Download Button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name=f"{selected_style}_{title_color}_price_data.csv",
    mime="text/csv"
)
