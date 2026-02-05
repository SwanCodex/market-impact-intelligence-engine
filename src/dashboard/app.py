import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Market Impact Intelligence Engine",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Event Impact Analysis",
        "Sector & Market Prediction",
        "News Traceability"
    ]
)

# Load core datasets
impact_df = pd.read_csv("data/processed/event_impact_summary.csv")
aligned_df = pd.read_csv("data/processed/news_market_aligned.csv")

# ---------------- OVERVIEW ----------------
if page == "Overview":
    st.title("📊 Market Impact Intelligence Engine")

    st.markdown(
        """
        **Market Impact Intelligence Engine** analyzes how macro-economic,
        political, and global trade news influences stock market behavior.

        This is a **research-grade proof-of-concept**, focused on:
        - Interpretability
        - Event-driven reasoning
        - Market impact analysis (not price prediction)
        """
    )

    st.subheader("🔍 What This System Does")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total News Analyzed", len(aligned_df))
    col2.metric("Event Categories", impact_df["event_type"].nunique())
    col3.metric("Market Index", "NIFTY 50")

    st.subheader("📌 Event Categories Covered")
    st.write(list(impact_df["event_type"].unique()))

# ---------------- EVENT IMPACT ----------------
elif page == "Event Impact Analysis":
    st.title("📈 Event-wise Market Impact")

    st.markdown(
        "This section visualizes how different **macro event categories** "
        "affect market returns and volatility."
    )

    # -------- Average Returns --------
    st.subheader("📊 Average Market Returns by Event Type")

    return_df = impact_df[
        ["event_type", "avg_ret_1d", "avg_ret_3d", "avg_ret_7d"]
    ].set_index("event_type")

    st.bar_chart(return_df)

    # -------- Volatility --------
    st.subheader("📉 Market Volatility by Event Type")

    vol_df = impact_df[
        ["event_type", "volatility_1d", "volatility_3d", "volatility_7d"]
    ].set_index("event_type")

    st.bar_chart(vol_df)

    # -------- Raw Table (Optional but Professional) --------
    with st.expander("🔍 View Raw Impact Table"):
        st.dataframe(impact_df)


# ---------------- SECTOR PREDICTION ----------------
elif page == "Sector & Market Prediction":
    st.title("📉 Sector & Market Behavior Prediction")

    st.markdown(
        """
        This section shows **probabilistic market behavior** following different
        macro event categories, computed from **historical returns**.

        These are **not price forecasts**, but likelihood estimates.
        """
    )

    # Select event type
    event = st.selectbox(
        "Select Event Type",
        aligned_df["event_type"].dropna().unique()
    )

    event_df = aligned_df[
        (aligned_df["event_type"] == event) &
        (~aligned_df["ret_1d"].isna())
    ]

    total = len(event_df)

    if total == 0:
        st.warning("Not enough data for this event type.")
    else:
        rise_prob = (event_df["ret_1d"] > 0).sum() / total * 100
        fall_prob = (event_df["ret_1d"] < 0).sum() / total * 100
        neutral_prob = 100 - rise_prob - fall_prob

        col1, col2, col3 = st.columns(3)

        col1.metric("📈 Probability of Rise", f"{rise_prob:.1f}%")
        col2.metric("📉 Probability of Fall", f"{fall_prob:.1f}%")
        col3.metric("➖ Neutral / No Move", f"{neutral_prob:.1f}%")

        prob_df = pd.DataFrame({
            "Outcome": ["Rise", "Fall", "Neutral"],
            "Probability (%)": [rise_prob, fall_prob, neutral_prob]
        }).set_index("Outcome")

        st.subheader("📊 Market Behavior Distribution")
        st.bar_chart(prob_df)

# ---------------- NEWS TRACEABILITY ----------------
elif page == "News Traceability":
    st.title("📰 News Traceability & Explainability")

    st.markdown(
        """
        This section shows **which specific news articles** were used to derive
        market impact insights, ensuring transparency and interpretability.
        """
    )

    # Select event type
    event = st.selectbox(
        "Select Event Type",
        aligned_df["event_type"].dropna().unique()
    )

    trace_df = aligned_df[
        (aligned_df["event_type"] == event)
    ][
        [
            "published_at",
            "source",
            "title",
            "sentiment",
            "sentiment_score",
            "ret_1d"
        ]
    ].copy()

    trace_df = trace_df.sort_values("published_at", ascending=False)

    trace_df.rename(columns={
        "published_at": "Date",
        "ret_1d": "Next-Day Return"
    }, inplace=True)

    st.subheader(f"🧠 News Driving '{event}' Insights")

    st.dataframe(
        trace_df,
        width="stretch"
    )

    st.caption(
        "Returns are next-day market reactions aligned with the news publication date."
    )

