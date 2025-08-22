import pandas as pd
import numpy as np
from src import preprocessing


# -------------------------------
# Aggregation Functions
# -------------------------------

def avg_score_season(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate average inning score per season."""
    return df.groupby("season")["avg_inning_score"].mean().to_frame()


def avg_boundary_season(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate average boundaries per season."""
    return df.groupby("season")["total_boundaries"].mean().to_frame()


def top_stadium(df: pd.DataFrame) -> pd.DataFrame:
    """Return stadium frequency count."""
    return df["venue_name"].value_counts().to_frame()


def top_tvumpires(df: pd.DataFrame) -> pd.DataFrame:
    """Return TV umpires frequency count."""
    return df["tv_umpire"].value_counts().to_frame()


# -------------------------------
# Team Qualification & Season
# -------------------------------

def qualify_teams(df: pd.DataFrame) -> pd.DataFrame:
    # Create dataframes for each qualifying position with unique column names
    demo_pt1 = df[df['rank'] == 1][['season', 'name']].rename(columns={'name': 'Qualify 1'})
    demo_pt2 = df[df['rank'] == 2][['season', 'name']].rename(columns={'name': 'Qualify 2'})
    demo_pt3 = df[df['rank'] == 3][['season', 'name']].rename(columns={'name': 'Qualify 3'})
    demo_pt4 = df[df['rank'] == 4][['season', 'name']].rename(columns={'name': 'Qualify 4'})

    # Merge them all on season
    merged_df = (
        demo_pt1
        .merge(demo_pt2, on='season', how='inner')
        .merge(demo_pt3, on='season', how='inner')
        .merge(demo_pt4, on='season', how='inner')
    )

    return merged_df



def season_n_teams(df: pd.DataFrame) -> tuple[list[str], list[int]]:
    """Return sorted list of teams and seasons."""
    teams = sorted(df["short_name"].unique().tolist())
    seasons = sorted(df["season"].unique().tolist())
    return teams, seasons


def performance_of_team(df: pd.DataFrame, team: str, season: int) -> pd.DataFrame:
    """Return performance stats of a given team in a given season."""
    cols = ["season", "name", "matchesplayed", "matcheswon", 
            "matcheslost", "noresult", "matchpoints", "nrr"]
    return df[(df["short_name"] == team) & (df["season"] == season)][cols]


# -------------------------------
# Overwise Analysis
# -------------------------------

def overwise_analysis(
    df: pd.DataFrame, field: str, lower_s: int, upper_s: int, 
    team: str, l_over: int, u_over: int
) -> pd.DataFrame:
    """Analyze runs, boundaries, or wickets over a range of overs and seasons."""
    s_details = preprocessing.overwise_preprocess(df)
    s_details = s_details[["season", "match_id", "current_innings", "over", "runs", "Boundary", "wicket"]]

    grouped = (
        s_details.groupby(["season", "match_id", "current_innings", "over"])[["runs", "Boundary", "wicket"]]
        .sum()
        .reset_index()
    )

    return grouped[
        (grouped["season"].between(lower_s, upper_s)) &
        (grouped["current_innings"] == team) &
        (grouped["over"].between(l_over, u_over))
    ][["season", "over", field]]


# -------------------------------
# Venue Analysis
# -------------------------------

def venue_win(df: pd.DataFrame, team: str) -> pd.DataFrame:
    """Return venue-wise match played and win statistics for a team."""
    played = df[(df["home_team"] == team) | (df["away_team"] == team)]["venue_name"].value_counts()
    won = df[((df["home_team"] == team) | (df["away_team"] == team)) & (df["winner"] == team)]["venue_name"].value_counts()

    result = pd.concat([played, won], axis=1).reset_index()
    result.columns = ["Venue_name", "Match_played", "Match_Won"]

    result["Match_Won"] = result["Match_Won"].fillna(0).astype(int)
    result["%of_win"] = (result["Match_Won"] / result["Match_played"]) * 100

    return result


# -------------------------------
# Player Performance
# -------------------------------

def top_batsman(df: pd.DataFrame, team: str, season: int) -> pd.Series:
    """Return top 5 batsmen by runs for a team in a season."""
    return (
        df[(df["season"] == season) & (df["current_innings"] == team)]
        .groupby("fullName")["runs"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .sort_values()
    )


def top_bowler(df: pd.DataFrame, team: str, season: int) -> pd.Series:
    """Return top 5 bowlers by wickets for a team in a season."""
    return (
        df[(df["season"] == season) & (df["bowling_team"] == team)]
        .groupby("fullName")["wickets"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .sort_values()
    )


def top_bowler_season(df: pd.DataFrame, season: int) -> pd.Series:
    """Return top 5 bowlers by wickets in a season."""
    return df[df["season"] == season].groupby("fullName")["wickets"].sum().nlargest(5)


def top_batsman_season(df: pd.DataFrame, season: int) -> pd.Series:
    """Return top 5 batsmen by runs in a season."""
    return df[df["season"] == season].groupby("fullName")["runs"].sum().nlargest(5)


def top_four_scorer(df: pd.DataFrame, season: int) -> pd.Series:
    """Return top 5 batsmen by number of fours in a season."""
    return df[df["season"] == season].groupby("fullName")["fours"].sum().nlargest(5)


def top_six_scorer(df: pd.DataFrame, season: int) -> pd.Series:
    """Return top 5 batsmen by number of sixes in a season."""
    return df[df["season"] == season].groupby("fullName")["sixes"].sum().nlargest(5)


# -------------------------------
# Special Analysis
# -------------------------------

def wide_noball_percent(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Calculate total balls, wides, and no-balls per season."""
    over_df = pd.DataFrame({
        "over": df["overs"].astype(int),
        "balls": df["overs"] - df["overs"].astype(int),
    })
    over_df["total_balls"] = 6 * over_df["over"] + 10 * over_df["balls"]

    merged = pd.concat([df, over_df], axis=1)

    df1 = merged.groupby("season")["total_balls"].sum().to_frame()
    df2 = merged.groupby("season")["wides"].sum().to_frame()
    df3 = merged.groupby("season")["noballs"].sum().to_frame()

    return df1, df2, df3


def faceoff(df: pd.DataFrame, season: int, batsman: str, bowler: str) -> pd.DataFrame:
    """Analyze batsman vs bowler faceoff statistics in a given season."""

    # Ensure wicket and boundary columns exist
    if "wicket" not in df.columns:
        df["wicket"] = np.where(df["wicket_id"].notna(), 1, 0)
    if "Boundary" not in df.columns:
        df["Boundary"] = np.where(df["isBoundary"], 1, 0)

    # Filter for matchup
    matchup = df[(df["season"] == season) &
                 (df["batsman1_name"] == batsman) &
                 (df["bowler1_name"] == bowler)]

    balls_faced = matchup["ball"].count()
    runs_scored = matchup["runs"].sum()
    strikerate = (runs_scored / balls_faced * 100) if balls_faced > 0 else 0
    wickets = matchup["wicket"].sum()
    boundaries = matchup["Boundary"].sum()
    economy = (runs_scored / (balls_faced / 6)) if balls_faced > 0 else 0

    # Build result DataFrame
    faceoff_df = pd.DataFrame({
        "Batsman Name": [batsman],
        "Bowler Name": [bowler],
        "Runs Scored": [runs_scored],
        "Balls Faced": [balls_faced],
        "Strike Rate": [strikerate],
        "Wicket": [wickets],
        "Boundaries": [boundaries],
        "Economy Rate": [economy]
    })

    return faceoff_df
