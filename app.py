"""
Zomato Restaurant Intelligence Dashboard
Author: Yash Chavan | VIT Pune CSE-DS | 2024-28
Production-grade Streamlit application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato Restaurant Intelligence",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #f8f8f8; }

    /* Header */
    .header-banner {
        background: linear-gradient(135deg, #E23744 0%, #b02030 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .header-banner h1 { font-size: 2rem; margin: 0; font-weight: 700; }
    .header-banner p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.95rem; }

    /* KPI cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #E23744;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #E23744; }
    .kpi-label { font-size: 0.8rem; color: #888; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.05em; }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        border-bottom: 2px solid #E23744;
        padding-bottom: 0.4rem;
        margin: 1.5rem 0 1rem;
    }

    /* Insight box */
    .insight-box {
        background: #fff8f8;
        border: 1px solid #fcc;
        border-left: 4px solid #E23744;
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        margin: 0.8rem 0;
        font-size: 0.88rem;
        color: #555;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #1a1a2e; }
    section[data-testid="stSidebar"] .stMarkdown { color: white; }
    section[data-testid="stSidebar"] label { color: #ccc !important; }

    /* Hide streamlit branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load and return the cleaned Bengaluru dataset with engineered columns."""
    df = pd.read_csv("bengaluru_cleaned.csv")

    # Rating categories
    bins   = [0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.1]
    labels = ["Poor", "Below Avg", "Average", "Good", "Very Good", "Excellent"]
    df["rating_category"] = pd.cut(df["rate"], bins=bins, labels=labels)

    # Cost brackets
    df["cost_bracket"] = pd.cut(
        df["cost_for_two"],
        bins=[0, 300, 600, 900, 1200, 99999],
        labels=["Budget (<300)", "Economy (300-600)", "Mid (600-900)",
                "Premium (900-1200)", "Luxury (1200+)"],
    )

    # Primary cuisine
    df["primary_cuisine"] = df["cuisines"].str.split(",").str[0].str.strip()

    # Human-readable labels
    df["order_label"]   = df["online_order"].map({1: "Online Order", 0: "No Online Order"})
    df["booking_label"] = df["book_table"].map({1: "Table Booking", 0: "No Booking"})

    return df


# ─── SIDEBAR FILTERS ────────────────────────────────────────────────────────
def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return filtered dataframe."""
    st.sidebar.markdown("""
    <div style='padding: 1rem 0 0.5rem;'>
        <span style='color:#E23744; font-size:1.4rem; font-weight:700;'>🍕 Zomato</span>
        <span style='color:white; font-size:1rem;'> Intelligence</span>
    </div>
    <p style='color:#aaa; font-size:0.75rem; margin-top:-0.3rem;'>
        Restaurant Analytics Dashboard
    </p>
    <hr style='border-color:#333; margin: 0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("**📍 Location**")
    locations = sorted(df["location"].dropna().unique())
    selected_locations = st.sidebar.multiselect(
        "Select locations",
        options=locations,
        default=[],
        placeholder="All locations",
    )

    st.sidebar.markdown("**🍜 Cuisine**")
    cuisines = sorted(df["primary_cuisine"].dropna().unique())
    selected_cuisines = st.sidebar.multiselect(
        "Select cuisines",
        options=cuisines,
        default=[],
        placeholder="All cuisines",
    )

    st.sidebar.markdown("**💰 Price Range**")
    price_options = ["Budget (<300)", "Economy (300-600)", "Mid (600-900)",
                     "Premium (900-1200)", "Luxury (1200+)"]
    selected_prices = st.sidebar.multiselect(
        "Select price range",
        options=price_options,
        default=[],
        placeholder="All price ranges",
    )

    st.sidebar.markdown("**⭐ Min Rating**")
    min_rating = st.sidebar.slider("Minimum rating", 1.0, 5.0, 1.0, 0.1)

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <p style='color:#888; font-size:0.72rem;'>
        Built by <b style='color:#E23744;'>Yash Chavan</b><br>
        VIT Pune | CSE-DS | 2024-28<br>
        <a href='https://github.com/yashtc2239-ops/zomato-data-analysis'
           style='color:#E23744;'>GitHub Repository ↗</a>
    </p>
    """, unsafe_allow_html=True)

    # Apply filters
    filtered = df.copy()
    if selected_locations:
        filtered = filtered[filtered["location"].isin(selected_locations)]
    if selected_cuisines:
        filtered = filtered[filtered["primary_cuisine"].isin(selected_cuisines)]
    if selected_prices:
        filtered = filtered[filtered["cost_bracket"].astype(str).isin(selected_prices)]
    filtered = filtered[filtered["rate"] >= min_rating]

    return filtered


# ─── KPI CARDS ──────────────────────────────────────────────────────────────
def render_kpi_cards(df: pd.DataFrame) -> None:
    """Render the four top-level KPI metric cards."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{len(df):,}</div>
            <div class='kpi-label'>Total Restaurants</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        avg_r = df["rate"].mean()
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{avg_r:.2f}</div>
            <div class='kpi-label'>Avg Rating</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        avg_c = df["cost_for_two"].mean()
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>₹{avg_c:,.0f}</div>
            <div class='kpi-label'>Avg Cost for Two</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        total_v = df["votes"].sum()
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{total_v/1e6:.1f}M</div>
            <div class='kpi-label'>Total Votes</div>
        </div>""", unsafe_allow_html=True)


# ─── PAGE 1: OVERVIEW ───────────────────────────────────────────────────────
def render_overview(df: pd.DataFrame) -> None:
    """Render the Executive Overview page."""
    render_kpi_cards(df)

    col1, col2 = st.columns([3, 2])

    # Rating distribution
    with col1:
        st.markdown("<div class='section-header'>📊 Rating Distribution</div>",
                    unsafe_allow_html=True)

        rating_counts = (
            df["rating_category"]
            .value_counts()
            .reindex(["Poor", "Below Avg", "Average", "Good", "Very Good", "Excellent"])
            .dropna()
        )
        colors = ["#d73027", "#fc8d59", "#fee08b", "#91cf60", "#1a9850", "#006837"]

        fig = px.bar(
            x=rating_counts.values,
            y=rating_counts.index,
            orientation="h",
            color=rating_counts.index,
            color_discrete_sequence=colors,
            labels={"x": "Restaurants", "y": ""},
        )
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=280,
            margin=dict(l=0, r=20, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        )
        fig.update_traces(
            text=rating_counts.values,
            textposition="outside",
            textfont_size=11,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""<div class='insight-box'>
            💡 <b>Insight:</b> 43.6% of restaurants fall in the Good (3.5–4.0) tier.
            Only <b>1.4%</b> achieve Excellent status — a genuine differentiator for premium restaurants.
        </div>""", unsafe_allow_html=True)

    # Donut charts
    with col2:
        st.markdown("<div class='section-header'>🔄 Service Distribution</div>",
                    unsafe_allow_html=True)

        # Online order donut
        order_counts = df["order_label"].value_counts()
        fig_donut1 = px.pie(
            values=order_counts.values,
            names=order_counts.index,
            hole=0.55,
            color_discrete_sequence=["#E23744", "#ddd"],
        )
        fig_donut1.update_layout(
            height=180,
            margin=dict(l=0, r=0, t=30, b=0),
            title=dict(text="Online Order", x=0.5, font_size=12),
            showlegend=False,
            paper_bgcolor="white",
        )
        fig_donut1.update_traces(textinfo="percent", textfont_size=11)
        st.plotly_chart(fig_donut1, use_container_width=True)

        # Table booking donut
        book_counts = df["booking_label"].value_counts()
        fig_donut2 = px.pie(
            values=book_counts.values,
            names=book_counts.index,
            hole=0.55,
            color_discrete_sequence=["#1a9850", "#ddd"],
        )
        fig_donut2.update_layout(
            height=180,
            margin=dict(l=0, r=0, t=30, b=0),
            title=dict(text="Table Booking", x=0.5, font_size=12),
            showlegend=False,
            paper_bgcolor="white",
        )
        fig_donut2.update_traces(textinfo="percent", textfont_size=11)
        st.plotly_chart(fig_donut2, use_container_width=True)

    # Cost bracket chart
    st.markdown("<div class='section-header'>💰 Does Price = Quality?</div>",
                unsafe_allow_html=True)

    cost_rating = (
        df.groupby("cost_bracket", observed=True)["rate"]
        .mean()
        .reset_index()
    )
    fig_cost = px.bar(
        cost_rating,
        x="cost_bracket",
        y="rate",
        color="rate",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        labels={"cost_bracket": "Price Range", "rate": "Avg Rating"},
        text=cost_rating["rate"].round(2),
    )
    fig_cost.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=260,
        margin=dict(l=0, r=0, t=10, b=10),
        coloraxis_showscale=False,
        yaxis=dict(range=[3.0, 4.5]),
    )
    fig_cost.update_traces(textposition="outside", textfont_size=12)
    st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("""<div class='insight-box'>
        💡 <b>Insight:</b> Pearson correlation = 0.38. Price moderately predicts quality —
        Luxury restaurants (₹1200+) avg <b>4.16</b> vs Budget at <b>3.57</b>.
        But price explains only 14% of rating variance — other factors dominate.
    </div>""", unsafe_allow_html=True)


# ─── PAGE 2: LOCATION INTELLIGENCE ─────────────────────────────────────────
def render_location(df: pd.DataFrame) -> None:
    """Render the Location Intelligence page."""
    st.markdown("<div class='section-header'>📍 Top vs Bottom Locations by Avg Rating</div>",
                unsafe_allow_html=True)

    # Guard: empty dataframe
    if df.empty:
        st.warning("No data for selected filters. Try adjusting the sidebar.")
        return

    location_stats = (
        df.groupby("location")
        .agg(
            avg_rating=("rate", "mean"),
            restaurant_count=("name", "count"),
            avg_cost=("cost_for_two", "mean"),
            total_votes=("votes", "sum"),
        )
        .reset_index()
    )
    # Lower threshold when filters reduce data
    min_count = 5 if len(df) < 2000 else 50
    location_stats = location_stats[location_stats["restaurant_count"] >= min_count].reset_index(drop=True)

    if location_stats.empty:
        st.info("Not enough location data for these filters. Try selecting fewer options.")
        return

    location_stats["demand_pressure"] = (
        location_stats["total_votes"] / location_stats["restaurant_count"]
    ).round(0)

    col1, col2 = st.columns(2)

    with col1:
        top10 = location_stats.nlargest(10, "avg_rating")
        fig = px.bar(
            top10.sort_values("avg_rating"),
            x="avg_rating",
            y="location",
            orientation="h",
            color="avg_rating",
            color_continuous_scale=["#91cf60", "#006837"],
            text=top10.sort_values("avg_rating")["avg_rating"].round(2),
            labels={"avg_rating": "Avg Rating", "location": ""},
        )
        fig.update_layout(
            title="🟢 Top 10 Locations",
            plot_bgcolor="white", paper_bgcolor="white",
            height=360, margin=dict(l=0, r=20, t=40, b=10),
            coloraxis_showscale=False,
            xaxis=dict(range=[3.5, 4.4]),
        )
        fig.update_traces(textposition="outside", textfont_size=10)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        bot10 = location_stats.nsmallest(10, "avg_rating")
        fig = px.bar(
            bot10.sort_values("avg_rating", ascending=False),
            x="avg_rating",
            y="location",
            orientation="h",
            color="avg_rating",
            color_continuous_scale=["#d73027", "#fc8d59"],
            text=bot10.sort_values("avg_rating", ascending=False)["avg_rating"].round(2),
            labels={"avg_rating": "Avg Rating", "location": ""},
        )
        fig.update_layout(
            title="🔴 Bottom 10 Locations",
            plot_bgcolor="white", paper_bgcolor="white",
            height=360, margin=dict(l=0, r=20, t=40, b=10),
            coloraxis_showscale=False,
            xaxis=dict(range=[3.0, 3.8]),
        )
        fig.update_traces(textposition="outside", textfont_size=10)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<div class='insight-box'>
        💡 <b>Insight:</b> Lavelle Road leads at <b>4.14</b> avg rating.
        Bommanahalli trails at <b>3.19</b> — a 0.95 point gap signals
        significant quality inequality across Bengaluru.
    </div>""", unsafe_allow_html=True)

    # Expansion priority table
    st.markdown("<div class='section-header'>🚀 Expansion Priority — Demand vs Supply</div>",
                unsafe_allow_html=True)

    from sklearn.preprocessing import MinMaxScaler

    # Need at least 2 rows for MinMaxScaler to work
    if len(location_stats) < 2:
        st.info("Need more locations to calculate expansion scores. Try removing some filters.")
        return

    scaler = MinMaxScaler(feature_range=(0, 100))

    location_stats["score_demand"] = scaler.fit_transform(
        location_stats[["demand_pressure"]]).round(1)
    location_stats["score_rating"] = scaler.fit_transform(
        location_stats[["avg_rating"]]).round(1)
    location_stats["score_supply_gap"] = (
        100 - scaler.fit_transform(location_stats[["restaurant_count"]])).round(1)
    location_stats["expansion_score"] = (
        location_stats["score_demand"] * 0.40 +
        location_stats["score_rating"] * 0.35 +
        location_stats["score_supply_gap"] * 0.25
    ).round(1)
    location_stats["priority"] = pd.cut(
        location_stats["expansion_score"],
        bins=[0, 40, 60, 80, 101],
        labels=["Low", "Medium", "High", "Critical"],
    )

    display_df = (
        location_stats
        .sort_values("expansion_score", ascending=False)
        .head(15)[["location", "restaurant_count", "avg_rating",
                   "avg_cost", "demand_pressure", "expansion_score", "priority"]]
        .rename(columns={
            "location": "Location",
            "restaurant_count": "Restaurants",
            "avg_rating": "Avg Rating",
            "avg_cost": "Avg Cost (₹)",
            "demand_pressure": "Demand Pressure",
            "expansion_score": "Expansion Score",
            "priority": "Priority",
        })
        .reset_index(drop=True)
    )
    display_df["Avg Rating"] = display_df["Avg Rating"].round(2)
    display_df["Avg Cost (₹)"] = display_df["Avg Cost (₹)"].round(0).astype(int)

    def color_priority(val):
        colors_map = {
            "Critical": "background-color:#006837; color:white; font-weight:bold",
            "High": "background-color:#1a9850; color:white",
            "Medium": "background-color:#fee08b; color:#333",
            "Low": "background-color:#fc8d59; color:white",
        }
        return colors_map.get(str(val), "")

    # pandas >= 2.1 renamed applymap → map; support both versions
    try:
        styled = display_df.style.map(color_priority, subset=["Priority"])
    except AttributeError:
        styled = display_df.style.applymap(color_priority, subset=["Priority"])
    st.dataframe(styled, use_container_width=True, height=420)


# ─── PAGE 3: CUISINE ANALYSIS ───────────────────────────────────────────────
def render_cuisine(df: pd.DataFrame) -> None:
    """Render the Cuisine & Business Analysis page with robust error handling."""
    
    # 1. Immediate guard clause: If no data, stop here
    if df.empty:
        st.warning("No data for selected filters. Try adjusting the sidebar.")
        return
        
    col1, col2 = st.columns(2)

    # --- TOP 10 SUPPLIED CUISINES ---
    with col1:
        st.markdown("<div class='section-header'>🍜 Top 10 Cuisines by Supply</div>", unsafe_allow_html=True)
        cuisine_list = df["cuisines"].dropna().str.split(",").explode().str.strip()
        if not cuisine_list.empty:
            cuisine_counts = cuisine_list.value_counts().head(10)
            fig = px.bar(
                x=cuisine_counts.values[::-1],
                y=cuisine_counts.index[::-1],
                orientation="h",
                color=cuisine_counts.values[::-1],
                color_continuous_scale=["#aad4f5", "#1565c0"],
                text=cuisine_counts.values[::-1],
                labels={"x": "Restaurant Count", "y": ""},
            )
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=340, margin=dict(l=0, r=20, t=10, b=10), coloraxis_showscale=False)
            fig.update_traces(textposition="outside", textfont_size=10)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cuisine data available.")

    # --- TOP 10 QUALITY CUISINES ---
    with col2:
        st.markdown("<div class='section-header'>⭐ Top 10 Cuisines by Quality</div>", unsafe_allow_html=True)
        
        cuisine_rating = (
            df.groupby("primary_cuisine")["rate"]
            .agg(["mean", "count"])
            .query("count >= 1")
            .sort_values("mean", ascending=False)
            .head(10)
            .reset_index()
        )

        if not cuisine_rating.empty:
            fig = px.bar(
                cuisine_rating,
                x='mean',
                y='primary_cuisine',
                orientation="h",
                color='mean',
                color_continuous_scale=["#91cf60", "#006837"],
                text=cuisine_rating['mean'].round(2),
                labels={"mean": "Avg Rating", "primary_cuisine": ""},
            )
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                height=340, margin=dict(l=0, r=20, t=10, b=10),
                coloraxis_showscale=False,
                xaxis=dict(range=[3.5, 4.7]),
            )
            fig.update_traces(textposition="outside", textfont_size=10)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for cuisine quality analysis.")

    # --- TABLE BOOKING SECTION ---
    st.markdown("<div class='section-header'>📅 Table Booking — Premium Segment Signal</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    booking_stats = df.groupby("booking_label")[["rate", "cost_for_two"]].mean().reset_index()

    with col3:
        if not booking_stats.empty:
            fig = px.bar(
                booking_stats,
                x="booking_label",
                y="rate",
                color="booking_label",
                color_discrete_map={"Table Booking": "#1a9850", "No Booking": "#E23744"},
                text=booking_stats["rate"].round(2),
                labels={"booking_label": "", "rate": "Avg Rating"},
            )
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False, height=280, margin=dict(l=0, r=0, t=10, b=10), yaxis=dict(range=[3.0, 4.5]))
            fig.update_traces(textposition="outside", textfont_size=14, textfont_color="black")
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if not booking_stats.empty:
            fig = px.bar(
                booking_stats,
                x="booking_label",
                y="cost_for_two",
                color="booking_label",
                color_discrete_map={"Table Booking": "#1a9850", "No Booking": "#E23744"},
                text=booking_stats["cost_for_two"].round(0),
                labels={"booking_label": "", "cost_for_two": "Avg Cost (₹)"},
            )
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False, height=280, margin=dict(l=0, r=0, t=10, b=10))
            fig.update_traces(textposition="outside", textfont_size=13, textfont_color="black")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<div class='insight-box'>
        💡 <b>Insight:</b> Table booking restaurants rate <b>0.52 points higher</b>
        (4.14 vs 3.62) and charge <b>2.6x more</b> (₹1,276 vs ₹482).
        This is the single strongest binary predictor of restaurant quality in the dataset.
    </div>""", unsafe_allow_html=True)

# ─── PAGE 4: ML MODEL ───────────────────────────────────────────────────────
def render_ml(df: pd.DataFrame) -> None:
    """Render the ML Model Insights page."""
    if df.empty:
        st.warning("No data for selected filters. Try adjusting the sidebar.")
        return
    st.markdown("""
    <div style='background:#fff8f8; border:1px solid #fcc; border-left:4px solid #E23744;
         border-radius:8px; padding:1rem 1.5rem; margin-bottom:1.2rem;'>
        <b>🤖 Random Forest Model</b> trained on 41,410 restaurants &nbsp;|&nbsp;
        <b>R² = 0.8157</b> &nbsp;|&nbsp; <b>RMSE = 0.19</b> rating points &nbsp;|&nbsp;
        Outperforms Linear Regression by <b>179%</b>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>🔍 Feature Importance</div>",
                    unsafe_allow_html=True)

        features = {
            "Votes (engagement)": 0.693,
            "Cost for Two":       0.147,
            "Restaurant Type":    0.109,
            "Online Order":       0.030,
            "Table Booking":      0.021,
        }
        feat_df = pd.DataFrame(list(features.items()), columns=["Feature", "Importance"])

        fig = px.bar(
            feat_df.sort_values("Importance"),
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale=["#fc8d59", "#E23744"],
            text=feat_df.sort_values("Importance")["Importance"].apply(
                lambda x: f"{x:.1%}"),
            labels={"Importance": "Importance Score", "Feature": ""},
        )
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=300, margin=dict(l=0, r=20, t=10, b=10),
            coloraxis_showscale=False,
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""<div class='insight-box'>
            💡 <b>Key Finding:</b> Customer votes (engagement) drive <b>69.3%</b>
            of rating prediction — <b>4.7x more important than price</b>.
            Zomato should weight engagement metrics higher in their ranking algorithm.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-header'>📊 Model Comparison</div>",
                    unsafe_allow_html=True)

        model_data = {
            "Model": ["Linear Regression", "Random Forest"],
            "R² Score": [0.292, 0.816],
            "RMSE": [0.370, 0.189],
        }
        model_df = pd.DataFrame(model_data)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="R² Score",
            x=model_df["Model"],
            y=model_df["R² Score"],
            marker_color=["#aaa", "#E23744"],
            text=model_df["R² Score"],
            texttemplate="%{text:.3f}",
            textposition="outside",
        ))
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=300, showlegend=False,
            margin=dict(l=0, r=0, t=20, b=10),
            yaxis=dict(range=[0, 1.1]),
            title="R² Score Comparison (higher = better)",
            title_font_size=12,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Stats table
        st.dataframe(
            model_df.style
            .highlight_max(subset=["R² Score"], color="#c8f7c5")
            .highlight_min(subset=["RMSE"], color="#c8f7c5")
            .format({"R² Score": "{:.4f}", "RMSE": "{:.4f}"}),
            use_container_width=True,
        )

    # Rating predictor
    st.markdown("<div class='section-header'>🎯 Live Rating Predictor</div>",
                unsafe_allow_html=True)
    st.markdown("*Adjust inputs to see predicted rating range based on our model insights.*")

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        cost_input = st.number_input("Cost for Two (₹)", 100, 6000, 500, 50)
    with p2:
        votes_input = st.number_input("No. of Votes", 0, 5000, 100, 10)
    with p3:
        order_input = st.selectbox("Online Order", ["Yes", "No"])
    with p4:
        book_input = st.selectbox("Table Booking", ["Yes", "No"])

    # Simple heuristic prediction based on feature importance
    base = 3.70
    cost_effect   = (cost_input - 603) / 464 * 0.147 * 0.44
    votes_effect  = min((votes_input - 351) / 882, 1.5) * 0.693 * 0.3
    order_effect  = 0.06 if order_input == "Yes" else 0
    book_effect   = 0.52 if book_input == "Yes" else 0
    predicted     = np.clip(base + cost_effect + votes_effect + order_effect + book_effect,
                            1.8, 4.9)

    st.markdown(f"""
    <div style='background:white; border-radius:12px; padding:1.2rem 1.5rem;
         box-shadow:0 2px 8px rgba(0,0,0,0.08); margin-top:0.5rem;
         display:flex; align-items:center; gap:1rem;'>
        <div style='font-size:2.5rem; font-weight:700; color:#E23744;'>{predicted:.1f}</div>
        <div>
            <div style='font-weight:600;'>Estimated Rating</div>
            <div style='color:#888; font-size:0.82rem;'>
                Based on weighted feature importance from Random Forest model.
                Actual prediction requires the trained model file.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN APP ───────────────────────────────────────────────────────────────
def main() -> None:
    # Header
    st.markdown("""
    <div class='header-banner'>
        <h1>🍕 Zomato Restaurant Intelligence</h1>
        <p>End-to-End Data Analytics | 41,410 Bengaluru Restaurants |
           Python · SQL · Power BI · Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    with st.spinner("Loading data..."):
        df_raw = load_data()

    # Sidebar & filtering
    df = render_sidebar(df_raw)

    if len(df) == 0:
        st.warning("No restaurants match your filters. Try adjusting the sidebar filters.")
        return

    # Show filter status
    if len(df) < len(df_raw):
        st.info(f"🔍 Showing **{len(df):,}** of {len(df_raw):,} restaurants based on your filters.")

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Overview",
        "📍 Location Intelligence",
        "🍜 Cuisine & Business",
        "🤖 ML Model Insights",
    ])

    with tab1:
        render_overview(df)
    with tab2:
        render_location(df)
    with tab3:
        render_cuisine(df)
    with tab4:
        render_ml(df)


if __name__ == "__main__":
    main()
