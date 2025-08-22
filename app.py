# Importing libraries
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

from src import preprocessing
from src import helper

# Ignore warnings
warnings.filterwarnings("ignore")

# Display all columns in pandas
pd.set_option("display.max_columns", None)

# ================== Load Data ==================
points_table = pd.read_csv("IPL/points_table.csv")
batting_card = pd.read_csv("IPL/all_season_batting_card.csv")
bowling_card = pd.read_csv("IPL/all_season_bowling_card.csv")
season_detailed = pd.read_csv("IPL/all_season_details.csv")
season_summary = pd.read_csv("IPL/all_season_summary.csv")

# ================== Data Preprocessing ==================
# Handle inning scores
for col in ["1st_inning_score", "2nd_inning_score"]:
    preprocessing.inning_score_format(season_summary, col)
    preprocessing.fillna_mean(season_summary, col)

# Handle boundaries
for col in ["home_boundaries", "away_boundaries"]:
    preprocessing.fillna_median(season_summary, col)

# New derived columns
season_summary["avg_inning_score"] = (
    season_summary["1st_inning_score"] + season_summary["2nd_inning_score"]
) / 2
season_summary["total_boundaries"] = (
    season_summary["home_boundaries"] + season_summary["away_boundaries"]
)

# ================== Sidebar ==================
st.sidebar.title("IPL ANALYSIS")
st.sidebar.image(r"D:\Skills\Project\IPL_Analysis\Notebook\ipl_logo.jpg")

user_menu = st.sidebar.radio(
    "Select an Option", ("Overview", "Team Analysis", "Player Analysis")
)

# ================== Overview ==================
if user_menu == "Overview":
    total_seasons = season_summary["season"].nunique()
    total_teams = points_table["name"].nunique()
    total_matches = season_summary["id"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Seasons", total_seasons)
    col2.metric("Total Teams", total_teams)
    col3.metric("Total Matches", total_matches)

    # Qualifying Teams
    st.subheader("Qualifying Teams by Season")
    st.table(helper.qualify_teams(points_table))

    # Avg runs by season
    st.subheader("Average Runs Per Inning by Season")
    avg_runs = helper.avg_score_season(season_summary)
    fig = px.line(avg_runs, x=avg_runs.index, y="avg_inning_score")
    fig.update_layout(xaxis_title="Season", yaxis_title="Runs")
    st.plotly_chart(fig)

    # Run distribution
    st.subheader("Distribution of Runs (IPL History)")
    run_dist = season_detailed["runs"].value_counts().to_frame()[:-1]
    fig = px.pie(run_dist, values="count", names=run_dist.index)
    st.plotly_chart(fig)

    # Avg boundaries
    st.subheader("Average Boundaries Per Match by Season")
    avg_boundaries = helper.avg_boundary_season(season_summary)
    fig = px.line(avg_boundaries, x=avg_boundaries.index, y="total_boundaries")
    fig.update_layout(xaxis_title="Season", yaxis_title="Boundaries")
    st.plotly_chart(fig)

    # Stadiums
    st.subheader("Top 10 Most Used Stadiums")
    stadiums = helper.top_stadium(season_summary).head(10)
    fig = px.bar(stadiums, x=stadiums.index, y="count", color_discrete_sequence=["#0068c9"])
    st.plotly_chart(fig)

    # TV Umpires
    st.subheader("Most Used TV Umpires")
    umpires = helper.top_tvumpires(season_summary).head(10)
    fig = px.bar(umpires, x=umpires.index, y="count", color_discrete_sequence=["#0068c9"])
    st.plotly_chart(fig)

    # Wides & No-balls %
    st.subheader("Wides and No Balls Percentage")
    df1, df2, df3 = helper.wide_noball_percent(bowling_card)
    fig = px.line(x=df1.index, y=(df2["wides"] / df1["total_balls"]) * 100, labels={"x": "Season", "y": "Percentage"})
    fig.add_scatter(x=df1.index, y=(df3["noballs"] / df1["total_balls"]) * 100, mode="lines", name="No Balls")
    fig.data[1].line.color = "#e70c3e"
    st.plotly_chart(fig)

# ================== Team Analysis ==================
elif user_menu == "Team Analysis":
    teams, seasons = helper.season_n_teams(points_table)
    selected_team = st.sidebar.selectbox("Select Team", teams)
    selected_season = st.sidebar.selectbox("Select Season", seasons)

    st.title(f"{selected_team} Performance in {selected_season}")
    performance = helper.performance_of_team(points_table, selected_team, selected_season).set_index("season")
    st.table(performance)

    # Overwise Analysis
    st.subheader("Over-wise Runs, Boundaries & Wickets")
    field = st.selectbox("Select Metric", ["runs", "Boundary", "wicket"])
    overs = st.slider("Select Overs", 0, 20, (0, 5))
    season_range = st.slider("Select Seasons", 2008, 2023, (2018, 2021))

    overwise_df = helper.overwise_analysis(season_detailed, field, season_range[0], season_range[1], selected_team, overs[0], overs[1])

    fig, ax = plt.subplots()
    sns.barplot(x="over", y=field, hue="season", data=overwise_df, ci=None, palette="bright", estimator=sum if field != "runs" else np.mean, ax=ax)
    ax.legend(title="Season", bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)

    # Top Batsmen & Bowlers
    st.subheader(f"Top 5 Batsmen for {selected_team} ({selected_season})")
    top_batsman = helper.top_batsman(batting_card, selected_team, selected_season)
    st.plotly_chart(px.bar(top_batsman, x=top_batsman.values, y=top_batsman.index, orientation="h", color_discrete_sequence=["#0068c9"]))

    st.subheader(f"Top 5 Bowlers for {selected_team} ({selected_season})")
    top_bowler = helper.top_bowler(bowling_card, selected_team, selected_season)
    st.plotly_chart(px.bar(top_bowler, x=top_bowler.values, y=top_bowler.index, orientation="h", color_discrete_sequence=["#9C2AB0"]))

    # Venue Win %
    st.subheader(f"{selected_team} Winning Percentage by Venue")
    st.table(helper.venue_win(season_summary, selected_team))

# ================== Player Analysis ==================
elif user_menu == "Player Analysis":
    _, seasons = helper.season_n_teams(points_table)
    selected_season = st.sidebar.selectbox("Select Season", seasons)

    st.subheader("Batsman vs Bowler Faceoff")
    batsmen = sorted(season_detailed[season_detailed["season"] == selected_season]["batsman1_name"].unique())
    selected_batsman = st.selectbox("Select Batsman", batsmen)
    bowlers = sorted(season_detailed[(season_detailed["season"] == selected_season) & (season_detailed["batsman1_name"] == selected_batsman)]["bowler1_name"].unique())
    selected_bowler = st.selectbox("Select Bowler", bowlers)

    st.table(helper.faceoff(season_detailed, selected_season, selected_batsman, selected_bowler))

    # Season Top Players
    st.subheader(f"Top Batsmen of {selected_season}")
    st.plotly_chart(px.bar(helper.top_batsman_season(batting_card, selected_season), orientation="h"))

    st.subheader(f"Top Bowlers of {selected_season}")
    st.plotly_chart(px.bar(helper.top_bowler_season(bowling_card, selected_season), orientation="h", color_discrete_sequence=["#2C2AC0"]))

    st.subheader(f"Top Four Hitters of {selected_season}")
    st.plotly_chart(px.bar(helper.top_four_scorer(batting_card, selected_season), orientation="h", color_discrete_sequence=["#5C36AA"]))

    st.subheader(f"Top Six Hitters of {selected_season}")
    st.plotly_chart(px.bar(helper.top_six_scorer(batting_card, selected_season), orientation="h", color_discrete_sequence=["#D44040"]))
