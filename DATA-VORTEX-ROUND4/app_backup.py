import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DATA VORTEX Social Engine",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("DATA VORTEX")
st.sidebar.caption("Social Engine - Round 4")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Historical Analytics",
        "NLP Intelligence",
        "Conversation Monitor",
        "Integrated Social Engine"
    ]
)

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.title("DATA VORTEX - Social Engine")
    st.caption("Round 4 Integrated Analytics Dashboard")

    st.header("Executive Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Round 1 - Cleaned Posts", "12,000")
    c2.metric("Round 2 - NLP Records", "9,000")
    c3.metric("Round 3 - Live Records", "160")

    c4, c5, c6 = st.columns(3)

    c4.metric("NLP Model Accuracy", "59.49%")
    c5.metric("Platforms Analyzed", "5")
    c6.metric("Round 3 Sources", "News + Reddit")

    st.divider()

    st.subheader("End-to-End Social Engine")

    st.code(
        """Round 1: Historical Behaviour
        ↓
Round 2: NLP Intelligence
        ↓
Round 3: Live Conversation Monitoring
        ↓
Round 4: Integrated Social Engine"""
    )

# =========================================================
# HISTORICAL ANALYTICS
# =========================================================

elif page == "Historical Analytics":

    st.title("Historical Analytics")
    st.caption("Round 1 - Phase 2 SQL Intelligence")

    platform = pd.read_csv(
        "./data/integrated/round1_platform_engagement.csv"
    )

    summary = pd.read_csv(
        "./data/integrated/round1_phase2_summary.csv"
    )

    st.subheader("E3 - Average Total Engagement by Platform")

    fig_platform = px.bar(
        platform,
        x="platform",
        y="average_total_engagement",
        text_auto=".2f",
        title="Average Total Engagement by Platform"
    )

    st.plotly_chart(fig_platform, use_container_width=True)

    st.subheader("M5 - Unusual Sharing Behaviour")

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Qualifying Posts",
        int(summary.loc[
            summary["metric"] == "M5 qualifying posts",
            "value"
        ].iloc[0])
    )

    m2.metric(
        "Highest Total Engagement",
        int(summary.loc[
            summary["metric"] == "M5 highest total engagement",
            "value"
        ].iloc[0])
    )

    m3.metric(
        "Highest Shares",
        int(summary.loc[
            summary["metric"] == "M5 highest post shares",
            "value"
        ].iloc[0])
    )

    st.info(
        "M5 identifies posts where shares exceed the combined "
        "number of likes and comments."
    )

    st.subheader("H4 - High-Engagement Users")

    h1, h2, h3, h4 = st.columns(4)

    h1.metric("Qualifying Users", "16")
    h2.metric("Highest Engagement", "64,753")
    h3.metric("Followers", "1,824")
    h4.metric("Posts", "16")

    st.info(
        "H4 identifies users with fewer than 5,000 followers "
        "who belong to the top 10% engagement group."
    )

# =========================================================
# NLP INTELLIGENCE
# =========================================================

elif page == "NLP Intelligence":

    st.title("NLP Intelligence")
    st.caption("Round 2 - Sentiment Classification Engine")

    st.header("Model Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Training Records", "9,000")
    c2.metric("Test Records", "1,817")
    c3.metric("TF-IDF Features", "25,650")

    st.divider()

    st.subheader("Model Performance Comparison")

    model_data = pd.DataFrame({
        "Model": [
            "Logistic Regression",
            "LinearSVC",
            "MultinomialNB"
        ],
        "Accuracy": [
            58.83,
            57.57,
            59.49
        ]
    })

    fig_models = px.bar(
        model_data,
        x="Model",
        y="Accuracy",
        text="Accuracy",
        title="Sentiment Model Accuracy Comparison"
    )

    fig_models.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_models.update_layout(
        yaxis_title="Accuracy (%)",
        yaxis_range=[0, 70]
    )

    st.plotly_chart(
        fig_models,
        use_container_width=True
    )

    st.success(
        "Final model: Multinomial Naive Bayes + TF-IDF"
    )

    st.metric(
        "Final Model Accuracy",
        "59.49%"
    )

    st.divider()

    st.subheader("Class-wise Performance")

    class_data = pd.DataFrame({
        "Sentiment": [
            "Negative",
            "Neutral",
            "Positive"
        ],
        "Precision": [
            65.59,
            53.83,
            58.58
        ],
        "Recall": [
            62.32,
            47.39,
            68.49
        ],
        "F1 Score": [
            63.91,
            50.40,
            63.15
        ]
    })

    st.dataframe(
        class_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Confusion Matrix")

    confusion = pd.DataFrame(
        [
            [387, 121, 113],
            [133, 281, 179],
            [70, 120, 413]
        ],
        index=["Actual Negative", "Actual Neutral", "Actual Positive"],
        columns=[
            "Predicted Negative",
            "Predicted Neutral",
            "Predicted Positive"
        ]
    )

    fig_cm = px.imshow(
        confusion,
        text_auto=True,
        aspect="auto",
        title="Sentiment Confusion Matrix"
    )

    st.plotly_chart(
        fig_cm,
        use_container_width=True
    )

    st.warning(
        "The largest error pattern is Neutral → Positive "
        "with 179 misclassified records."
    )

# =========================================================
# CONVERSATION MONITOR
# =========================================================

elif page == "Conversation Monitor":

    st.title("Conversation Monitor")
    st.caption("Round 3 - Meta One Live Conversation Intelligence")

    df = pd.read_csv(
        "./data/round3/meta_one_round3_sentiment_FINAL.csv"
    )

    df["date"] = pd.to_datetime(df["published_at"]).dt.date

    st.header("Live Conversation Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Live Records", len(df))
    c2.metric("News Records", int((df["platform"] == "News").sum()))
    c3.metric("Reddit Records", int((df["platform"] == "Reddit").sum()))
    c4.metric("Analysis Days", df["date"].nunique())

    st.divider()

    # -----------------------------------------------------
    # DAILY ACTIVITY
    # -----------------------------------------------------

    st.subheader("Daily Conversation Activity")

    daily = (
        df.groupby("date")
        .size()
        .reset_index(name="records")
    )

    fig_daily = px.line(
        daily,
        x="date",
        y="records",
        markers=True,
        title="Daily Conversation Volume"
    )

    fig_daily.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Records"
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )

    st.info(
        "September 16 shows the highest conversation activity "
        "with 81 collected records."
    )

    # -----------------------------------------------------
    # SENTIMENT DISTRIBUTION
    # -----------------------------------------------------

    st.subheader("Overall Sentiment Distribution")

    sentiment = (
        df["predicted_sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment.columns = ["Sentiment", "Records"]

    fig_sentiment = px.bar(
        sentiment,
        x="Sentiment",
        y="Records",
        text="Records",
        title="Overall Sentiment Distribution"
    )

    st.plotly_chart(
        fig_sentiment,
        use_container_width=True
    )

    # -----------------------------------------------------
    # DAILY SENTIMENT TREND
    # -----------------------------------------------------

    st.subheader("Daily Sentiment Trend")

    daily_sentiment = (
        df.groupby(["date", "predicted_sentiment"])
        .size()
        .reset_index(name="records")
    )

    fig_sentiment_trend = px.line(
        daily_sentiment,
        x="date",
        y="records",
        color="sentiment",
        markers=True,
        title="Sentiment Evolution Over Time"
    )

    fig_sentiment_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Records"
    )

    st.plotly_chart(
        fig_sentiment_trend,
        use_container_width=True
    )

    # -----------------------------------------------------
    # SOURCE DISTRIBUTION
    # -----------------------------------------------------

    st.subheader("Data Source Distribution")

    source_data = (
        df["platform"]
        .value_counts()
        .reset_index()
    )

    source_data.columns = ["Platform", "Records"]

    fig_source = px.pie(
        source_data,
        names="Platform",
        values="Records",
        title="Round 3 Data Sources"
    )

    st.plotly_chart(
        fig_source,
        use_container_width=True
    )


# =========================================================
# INTEGRATED SOCIAL ENGINE
# =========================================================

elif page == "Integrated Social Engine":

    st.title("Integrated Social Engine")
    st.caption("Round 4 - Cross-Phase Intelligence")

    st.header("End-to-End Social Intelligence")

    st.write(
        "The Integrated Social Engine combines historical behaviour, "
        "NLP intelligence, and live conversation signals into one "
        "cross-phase monitoring view."
    )

    st.divider()

    # -----------------------------------------------------
    # CROSS-ROUND KPI SUMMARY
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Historical Posts", "12,000")
    c2.metric("NLP Records", "9,000")
    c3.metric("Live Records", "160")
    c4.metric("NLP Accuracy", "59.49%")

    # -----------------------------------------------------
    # HISTORICAL PLATFORM SIGNAL
    # -----------------------------------------------------

    st.subheader("Historical Behaviour Signal")

    platform = pd.read_csv(
        "./data/integrated/round1_platform_engagement.csv"
    )

    fig_platform = px.bar(
        platform,
        x="platform",
        y="average_total_engagement",
        text_auto=".2f",
        title="Historical Average Engagement by Platform"
    )

    fig_platform.update_layout(
        xaxis_title="Platform",
        yaxis_title="Average Total Engagement"
    )

    st.plotly_chart(
        fig_platform,
        use_container_width=True
    )

    # -----------------------------------------------------
    # NLP MODEL SIGNAL
    # -----------------------------------------------------

    st.subheader("NLP Intelligence Signal")

    model_data = pd.DataFrame({
        "Model": [
            "Logistic Regression",
            "LinearSVC",
            "MultinomialNB"
        ],
        "Accuracy": [
            58.83,
            57.57,
            59.49
        ]
    })

    fig_models = px.bar(
        model_data,
        x="Model",
        y="Accuracy",
        text="Accuracy",
        title="Sentiment Model Performance"
    )

    fig_models.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_models.update_layout(
        yaxis_title="Accuracy (%)",
        yaxis_range=[0, 70]
    )

    st.plotly_chart(
        fig_models,
        use_container_width=True
    )

    # -----------------------------------------------------
    # LIVE CONVERSATION SIGNAL
    # -----------------------------------------------------

    st.subheader("Live Conversation Signal")

    live_df = pd.read_csv(
        "./data/round3/meta_one_round3_sentiment_FINAL.csv"
    )

    live_df["date"] = pd.to_datetime(
        live_df["published_at"]
    ).dt.date

    daily_live = (
        live_df.groupby("date")
        .size()
        .reset_index(name="records")
    )

    fig_live = px.line(
        daily_live,
        x="date",
        y="records",
        markers=True,
        title="Live Conversation Activity"
    )

    fig_live.update_layout(
        xaxis_title="Date",
        yaxis_title="Records Collected"
    )

    st.plotly_chart(
        fig_live,
        use_container_width=True
    )

    # -----------------------------------------------------
    # LIVE SENTIMENT SIGNAL
    # -----------------------------------------------------

    sentiment_data = (
        live_df["predicted_sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_data.columns = [
        "Sentiment",
        "Records"
    ]

    fig_sentiment = px.bar(
        sentiment_data,
        x="Sentiment",
        y="Records",
        text="Records",
        title="Current Live Sentiment Distribution"
    )

    st.plotly_chart(
        fig_sentiment,
        use_container_width=True
    )

    # -----------------------------------------------------
    # INTEGRATED INSIGHTS
    # -----------------------------------------------------

    st.divider()

    st.subheader("Integrated Intelligence Signals")

    i1, i2, i3 = st.columns(3)

    i1.info(
        "Historical Signal\n\n"
        "Instagram recorded the highest average total "
        "engagement in the Round 1 Phase 2 analysis."
    )

    i2.info(
        "NLP Signal\n\n"
        "Multinomial Naive Bayes achieved the highest "
        "accuracy among the evaluated sentiment models."
    )

    i3.info(
        "Live Signal\n\n"
        "September 16 recorded the highest Round 3 "
        "conversation activity with 81 records."
    )

    st.divider()

    st.subheader("Social Engine Pipeline")

    st.code(
        """Historical Behaviour
        │
        ├── Platform Engagement
        ├── Sharing Behaviour
        └── High-Engagement Users
                ↓
        NLP Intelligence
        │
        ├── TF-IDF
        ├── Sentiment Classification
        └── Model Evaluation
                ↓
        Live Conversation Monitoring
        │
        ├── Activity Trend
        ├── Sentiment Trend
        └── Source Monitoring
                ↓
        INTEGRATED SOCIAL ENGINE"""
    )

    st.caption(
        "Round 4 integrates outputs from historical analytics, "
        "sentiment modelling, and live conversation monitoring."
    )
