import numpy as np
import pandas as pd


def inning_score_format(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Extracts the runs scored before '/' from the given score column.
    
    Example: '120/5' -> '120'
    """
    df[column] = df[column].str.split("/").str[0]
    return df


def fillna_mean(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Fill NaN values in a column with the mean and cast to int.
    """
    df[column] = df[column].astype(float)
    df[column].fillna(df[column].mean(), inplace=True)
    df[column] = df[column].astype(int)
    return df


def fillna_median(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Fill NaN values in a column with the median and cast to int.
    """
    df[column] = df[column].astype(float)
    df[column].fillna(df[column].median(), inplace=True)
    df[column] = df[column].astype(int)
    return df


def overwise_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess ball-by-ball match details:
    - Cast 'isBoundary' to bool and create numeric 'Boundary'
    - Create 'wicket' column based on wicket_id
    - Remove invalid 'season' text rows
    - Fill missing season with 2023 and cast to int
    - Drop rows with missing match_id
    - Cast numeric columns to int
    """
    copy_df = df.copy()

    # Convert boundary-related columns
    copy_df["isBoundary"] = copy_df["isBoundary"].astype(bool)
    copy_df["Boundary"] = np.where(copy_df["isBoundary"], 1, 0)

    # Wicket column: 1 if wicket_id present, else 0
    copy_df["wicket"] = np.where(copy_df["wicket_id"].notnull(), 1, 0)

    # Remove non-season garbage entries
    invalid_seasons = {
        ' do we have a reserve day?"" --- Yep',
        ''' you can <a href=""https://www.espncricinfo.com/game/playandwatch"">Play and Watch with ESPNcricinfo\'s new game</a>.</b></p><p>Afeef : ""First time I remember watching Ambati Rayudu was in 2011 in the match where Sachin scored his IPL century. Rayudu scored 55 and was outscoring Sachin that day. I have been his fan since then. Feeling quite emotional knowing that this will be his last game. An amazing player.""</p><p><strong>6.30pm</strong> The <strong>covers are coming on</strong> at Motera. ""The pitch is covered''',
        ''' Shashank Kishore says from Ahmedabad. ""It\'s very''',
        ''' Team winning the toss have advantage. But these 2 teams have almost always stayed on top throughout the tournament and toss wouldn\'t matter to them. Hoping for a close contest.""</p><p><strong>6.05pm</strong> Ambati Rayudu'''
    }
    copy_df = copy_df[~copy_df["season"].isin(invalid_seasons)]

    # Fix missing or invalid season
    copy_df["season"].fillna("2023", inplace=True)
    copy_df["season"] = pd.to_numeric(copy_df["season"], errors="coerce")
    copy_df.dropna(subset=["season", "match_id"], inplace=True)
    copy_df["season"] = copy_df["season"].astype(int)

    # Cast numeric columns
    for col in ["over", "runs"]:
        copy_df[col] = pd.to_numeric(copy_df[col], errors="coerce").fillna(0).astype(int)

    return copy_df
