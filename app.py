
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
