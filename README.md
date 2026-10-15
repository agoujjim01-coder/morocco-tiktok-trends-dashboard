# 🇲🇦 Morocco TikTok Trends Dashboard

## 📌 Project Overview

An interactive data analytics dashboard developed with Python and Streamlit to explore TikTok videos associated with Morocco.

The project analyzes video popularity, engagement rates, creator performance, and Morocco-related content.

**Live Dashboard:** https://morocco-tiktok-trends-dashboard-7uqk5o5a5jktaxbikpwxhz.streamlit.app/

## 🎯 Project Objectives

- Analyze TikTok video performance using views, likes, and comments.
- Identify highly engaging videos and creators.
- Explore the relationship between video views and engagement rates.
- Identify videos mentioning Morocco-related topics.
- Present insights through interactive visualizations.

## 🛠️ Technologies Used

- **Python:** Data processing and analysis
- **Pandas:** Data cleaning and calculations
- **Streamlit:** Interactive dashboard development
- **Plotly:** Data visualization
- **Google Colab:** Data collection and updating
- **GitHub:** Version control and project hosting

## 📊 Dashboard Features

1. **Dataset Overview:** Summary of videos, views, likes, and comments.
2. **Top Videos:** Ranking of videos by views.
3. **Engagement Analysis:** Engagement statistics and correlation analysis.
4. **Creator Performance:** Creator rankings by views and engagement rates.
5. **Morocco Relevance Analysis:** Identification of videos containing Morocco-related keywords.
6. **Hashtag Analysis:** Exploration of frequently occurring hashtags.
7. **Interactive Filters:** Filter Morocco-related videos by creator and select table columns.
8. **CSV Export:** Download Morocco-related video data.

## 📐 Methodology

The dashboard uses a collected sample of TikTok videos and their available engagement statistics.

Data is cleaned using Pandas, and duplicate video IDs are removed.

Engagement rate is calculated as:

**Engagement Rate (%) = (Likes + Comments) / Views × 100**

Morocco-related videos are identified through keyword matching in video captions, including references to Moroccan cities, languages, and events.

## 🔍 Key Findings

In the analyzed sample of 38 videos:

- 31 videos (81.6%) contain Morocco-related keywords.
- Video views and engagement rates show little consistent relationship (Spearman correlation approximately -0.05).
- Creators with the most views are not necessarily those with the highest engagement rates.

These findings describe the collected sample and may change as the dataset is updated.

## ⚠️ Limitations

- The dataset is a limited sample and is not representative of all TikTok activity in Morocco.
- Keyword matching does not prove that a video originated in Morocco or is trending among Moroccan users.
- TikTok engagement statistics can change over time.
- Correlation does not imply causation.

## 🚀 Run Locally

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Start the Streamlit application:

```bash
streamlit run app.py
```

## 📁 Project Structure

- `app.py` — Streamlit dashboard
- `data/tiktok_dashboard_data.csv` — Dataset
- `scripts/` — Data collection and refresh scripts
- `requirements.txt` — Python dependencies

## 🎓 Internship Project

This project demonstrates practical skills in data collection, data cleaning, exploratory data analysis, data visualization, and interactive dashboard development.
