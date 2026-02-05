import streamlit as st
import pandas as pd

st.set_page_config(page_title="Market Impact Intelligence Engine", layout="wide")

st.title("📊 Market Impact Intelligence Engine")
st.markdown(
    """
    This dashboard shows how different **macro-economic and geopolitical events**
    influence stock market behavior over time.
    """
)

# Load data
impact_df = pd.read_csv("data/processed/event_impact_summary.csv")

st.subheader("📌 Event-wise Market Impact Summary")
st.dataframe(impact_df)

# Event selector
event = st.selectbox("Select an Event Type", impact_df["event_type"].unique())

filtered = impact_df[impact_df["event_type"] == event]

st.subheader(f"📈 Impact Analysis for: {event}")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Return (1 Day)", f"{filtered['avg_ret_1d'].values[0]:.4f}")
col2.metric("Avg Return (3 Days)", f"{filtered['avg_ret_3d'].values[0]:.4f}")
col3.metric("Avg Return (7 Days)", f"{filtered['avg_ret_7d'].values[0]:.4f}")

st.subheader("📉 Volatility Response")

vol_df = filtered[
    ["volatility_1d", "volatility_3d", "volatility_7d"]
].T
vol_df.columns = ["Volatility"]
vol_df.index = ["1 Day", "3 Days", "7 Days"]

st.bar_chart(vol_df)
