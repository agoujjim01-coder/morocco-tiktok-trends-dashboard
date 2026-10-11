
import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Morocco TikTok Trends",
    page_icon="🇲🇦",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

DATA_PATH = "data/tiktok_dashboard_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, dtype={"video_id": "string"})

    for col in ["views", "likes", "comments", "engagement_rate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df.drop_duplicates(subset="video_id").copy()

    return df

df = load_data()

# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("🇲🇦 Morocco TikTok Trends Dashboard")

st.write(
    "Explore Moroccan TikTok content, engagement, "
    "hashtags, and emerging creator opportunities."
)

st.caption(
    "Historical TikTok sample — not a live or representative "
    "ranking of all trending videos in Morocco."
)

if st.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

st.divider()

# ==========================================
# DATASET OVERVIEW
# ==========================================

st.header("📊 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Analyzed Videos", len(df))
c2.metric("Total Views", f"{int(df['views'].sum()):,}")
c3.metric("Total Likes", f"{int(df['likes'].sum()):,}")
c4.metric("Total Comments", f"{int(df['comments'].sum()):,}")

st.divider()


# ==========================================
# TOP TRENDING VIDEOS
# ==========================================

st.header("🔥 Which TikTok videos attracted the most views?")

top_videos = (
    df.nlargest(10, "views")
    .sort_values("views", ascending=True)
    .copy()
)

fig_top = px.bar(
    top_videos,
    x="views",
    y="title_caption",
    orientation="h",
    hover_data=["creator", "likes", "comments"],
    labels={
        "views": "Views",
        "title_caption": "TikTok Video"
    },
    title="Top 10 Videos by Views"
)

fig_top.update_layout(
    height=600,
    yaxis_title=None
)

st.plotly_chart(fig_top, use_container_width=True)

st.caption(
    "These are the most-viewed videos within the collected "
    "TikTok sample, not an official TikTok Morocco ranking."
)

st.divider()


# ==========================================
# ENGAGEMENT ANALYSIS
# ==========================================

st.header("❤️ How are audiences engaging with TikTok videos?")

st.write(
    "Engagement rate measures likes and comments "
    "as a percentage of video views."
)

# Calculate engagement rate if needed
df["engagement_rate"] = (
    (df["likes"] + df["comments"])
    / df["views"].replace(0, float("nan"))
    * 100
).fillna(0)

e1, e2, e3 = st.columns(3)

e1.metric(
    "Average Engagement Rate",
    f"{df['engagement_rate'].mean():.2f}%"
)

e2.metric(
    "Median Engagement Rate",
    f"{df['engagement_rate'].median():.2f}%"
)

e3.metric(
    "Highest Engagement Rate",
    f"{df['engagement_rate'].max():.2f}%"
)

# Views versus likes
fig_engagement = px.scatter(
    df,
    x="views",
    y="likes",
    hover_name="title_caption",
    hover_data=["creator", "comments", "engagement_rate"],
    labels={
        "views": "Views",
        "likes": "Likes"
    },
    title="Views vs Likes"
)

st.plotly_chart(
    fig_engagement,
    use_container_width=True
)

st.caption(
    "The relationship between views and likes is descriptive "
    "and does not establish causation."
)

st.divider()

# ==========================================
# TOP ENGAGEMENT INSIGHTS
# ==========================================

st.subheader("📈 Engagement Rate vs. Views")

fig_engagement_views = px.scatter(
    df[df["views"] > 0],
    x="views",
    y="engagement_rate",
    log_x=True,
    hover_name="title_caption",
    hover_data=["creator", "likes", "comments"],
    labels={
        "views": "Video Views",
        "engagement_rate": "Engagement Rate (%)"
    },
    title="Do More Views Mean Higher Engagement?"
)

fig_engagement_views.update_traces(
    marker=dict(size=11, opacity=0.7)
)
fig_engagement_views.update_xaxes(
    tickmode="array",
    tickvals=[1000, 10000, 100000, 1000000, 10000000],
    ticktext=["1K", "10K", "100K", "1M", "10M"]
)

st.plotly_chart(
    fig_engagement_views,
    use_container_width=True
)

st.caption(
    "Each dot represents one video. "
    "This chart shows the relationship between views "
    "and engagement rate within the collected sample, "
    "not a causal relationship."
)

# ==========================================
# AUTOMATIC ENGAGEMENT INSIGHT
# ==========================================

st.subheader("💡 Key Insight")

insight_df = df[df["views"] > 0].copy()

if len(insight_df) >= 3:
    correlation = (
        insight_df["views"].rank().corr(
            insight_df["engagement_rate"].rank(),
            method="pearson"
        )
    )

    if pd.isna(correlation):
        st.info(
            "There is not enough variation in the data "
            "to calculate a meaningful relationship."
        )
    elif correlation > 0.3:
        st.info(
            "📈 Videos with more views tend to have "
            "higher engagement rates in this sample."
        )
    elif correlation < -0.3:
        st.info(
            "📉 Videos with more views tend to have "
            "lower engagement rates in this sample."
        )
    else:
        st.info(
            "📊 There is no strong monotonic relationship "
            "between views and engagement rates in this sample."
        )

    if pd.notna(correlation):
        st.caption(
            f"Spearman correlation: {correlation:.2f}. "
            "This describes an association, not causation."
        )
else:
    st.info("Not enough videos to calculate this insight.")
    
st.divider()

st.subheader("🏆 Top 5 Most Engaging Videos")

top_engaging = df[df["views"] > 0].nlargest(
    5, "engagement_rate"
)

st.dataframe(
    top_engaging[
        [
            "title_caption",
            "creator",
            "views",
            "engagement_rate",
            "url"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "engagement_rate": st.column_config.NumberColumn(
            "Engagement Rate (%)",
            format="%.2f%%"
        ),
        "url": st.column_config.LinkColumn(
            "Watch on TikTok"
        )
    }
)

st.caption(
    "Ranked by (likes + comments) / views × 100. "
    "Results describe only the collected sample."
)

st.divider()

# ==========================================
# HASHTAG ANALYSIS
# ==========================================

st.header("🏷️ Which hashtags appear most often?")

from collections import Counter

hashtag_counts = Counter()

for tags in df["hashtags"].fillna(""):
    unique_tags = {
        tag.strip().lower()
        for tag in str(tags).split(",")
        if tag.strip()
    }

    hashtag_counts.update(unique_tags)

top_hashtags = pd.DataFrame(
    hashtag_counts.most_common(15),
    columns=["Hashtag", "Videos"]
)

if not top_hashtags.empty:

    fig_hashtags = px.bar(
        top_hashtags.sort_values("Videos"),
        x="Videos",
        y="Hashtag",
        orientation="h",
        title="Top 15 Hashtags in the Collected TikTok Sample"
    )

    fig_hashtags.update_layout(
        height=550,
        yaxis_title=None
    )

    st.plotly_chart(
        fig_hashtags,
        use_container_width=True
    )

    st.dataframe(
        top_hashtags,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Each hashtag is counted once per video. "
        "These frequencies describe the collected sample, "
        "not all TikTok activity in Morocco."
    )

else:
    st.info("No hashtags were found in the dataset.")

st.divider()


# ==========================================
# SEARCHABLE VIDEO TABLE
# ==========================================

st.header("🔎 Explore the TikTok Videos")

search = st.text_input(
    "Search by caption, creator, or hashtag",
    placeholder="Try: morocco, football, cooking..."
)

filtered_df = df.copy()

if search.strip():
    search_text = search.strip()

    mask = (
        filtered_df["title_caption"].fillna("").astype(str)
        .str.contains(search_text, case=False, regex=False)
        |
        filtered_df["creator"].fillna("").astype(str)
        .str.contains(search_text, case=False, regex=False)
        |
        filtered_df["hashtags"].fillna("").astype(str)
        .str.contains(search_text, case=False, regex=False)
    )

    filtered_df = filtered_df[mask]

st.write(f"Showing {len(filtered_df)} videos")

table_columns = [
    "title_caption",
    "creator",
    "views",
    "likes",
    "comments",
    "engagement_rate",
    "hashtags",
    "url"
]

st.dataframe(
    filtered_df[table_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "url": st.column_config.LinkColumn(
            "Watch on TikTok"
        )
    }
)

st.caption(
    "Search results are limited to the collected TikTok sample."
)
