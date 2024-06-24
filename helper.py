import pandas as pd
import preprocessing
import streamlit as st
import numpy as np

def avg_score_season(df):
    demo_df=df[['season','avg_inning_score']]
    grouped=demo_df.groupby('season').mean()
    
    return grouped

def avg_boundary_season(df):
    demo_boundary=df[['season','total_boundaries']]
    grouped_boundary=demo_boundary.groupby('season').mean()

    return grouped_boundary

def top_Stadium(df):
    stadium=df['venue_name'].value_counts().to_frame()

    return stadium

def top_tvumpires(df):
    tvumpire=df['tv_umpire'].value_counts().to_frame()

    return tvumpire

def Qualify_Teams(df):
    demo_pt1=pd.DataFrame()
    demo_pt2=pd.DataFrame()
    demo_pt3=pd.DataFrame()
    demo_pt4=pd.DataFrame()

    demo_pt1[['season','Qualify 1']]=df[df['rank']==1][['season','name']]
    demo_pt2[['season','Qualify 2']]=df[df['rank']==2][['season','name']]
    demo_pt3[['season','Qualify 3']]=df[df['rank']==3][['season','name']]
    demo_pt4[['season','Qualify 4']]=df[df['rank']==4][['season','name']]

    merged_df = demo_pt1.merge(demo_pt2, on='season', how='inner').merge(demo_pt3, on='season', how='inner').merge(demo_pt4, on='season', how='inner')

    return merged_df


def wide_noball_percent(df):
    over_df=pd.DataFrame()
    over_df['over']=df['overs'].astype('int')
    over_df['balls']=df['overs']-over_df['over']
    over_df['total_balls']=6*over_df['over']+10*over_df['balls']
    df1=pd.concat([df,over_df],axis=1)[['season','total_balls']].groupby('season').sum()
    df2=pd.concat([df,over_df],axis=1)[['season','wides']].groupby('season').sum()
    df3=pd.concat([df,over_df],axis=1)[['season','noballs']].groupby('season').sum()

    return df1,df2,df3


def season_n_teams(df):
    team=df['short_name'].unique().tolist()
    team.sort()
    season=df['season'].unique().tolist()
    season.sort()

    return team, season


def Performance_of_team(df,team,season):
    performance=df[(df['short_name']==team) & (df['season']==season)][['season','name','matchesplayed','matcheswon','matcheslost','noresult','matchpoints','nrr']]

    return performance

def Overwise_Analysis(df,field,lower_s,upper_s,team,l_over,u_over):

    s_details=preprocessing.overwise_preprocess(df)
    s_details=s_details[['season','match_id','current_innings','over','runs','Boundary','wicket']]

    

    overwise_analysis=s_details.groupby(['season','match_id','current_innings','over'])[['runs','Boundary','wicket']].sum()
    
    overwise_analysis=overwise_analysis.reset_index()
    # st.title("All good till here332")
    # st.table(overwise_analysis)

    

    demo=overwise_analysis[(overwise_analysis['season'] >= lower_s) & (overwise_analysis['season'] <= upper_s) & (overwise_analysis['current_innings'] == team) & (overwise_analysis['over'] >= l_over) &(overwise_analysis['over'] <= u_over) ][['season','over',field]]

    return demo
 

def venue_win(df,team):
    demo_venue=df[(df['home_team']==team) | (df['away_team']==team)]['venue_name'].value_counts()
    demo_venue_win=df[((df['home_team']==team) | (df['away_team']==team)) & (df['winner']==team)]['venue_name'].value_counts()

    final_venue=pd.concat([demo_venue,demo_venue_win],axis=1).reset_index()

    final_venue.columns=['Venue_name','Match_played','Match_Won']

    final_venue['Match_Won'].fillna(0,inplace=True)
    final_venue['Match_Won']=final_venue['Match_Won'].astype('int')
    final_venue['%of_win']=(final_venue['Match_Won']/final_venue['Match_played'])*100

    return final_venue


def top_5_batsman(df,team,season):
    top_batter=df[(df['season']==season) & (df["current_innings"]==team)].groupby('fullName').sum()['runs'].sort_values(ascending=False).iloc[:5].sort_values()

    return top_batter

def top_5_bowler(df,team,season):

    top_bowler=df[(df['season']==season) & (df["bowling_team"]==team)].groupby('fullName')['wickets'].sum().sort_values(ascending=False).iloc[:5].sort_values()


    return top_bowler


def faceoff(df,season,batsman,bowler):
    df_faceoff=pd.DataFrame()
    df_faceoff["Batsman Name"]=[batsman]
    df_faceoff["Bowler Name"]=[bowler]
    balls_faced=df[(df['season']==season) & (df['batsman1_name']==batsman) & (df['bowler1_name']==bowler)].count()['ball']
    
    run_scored=df[(df['season']==season) & (df['batsman1_name']==batsman) & (df['bowler1_name']==bowler)]['runs'].sum()
    strikerate=(run_scored/balls_faced)*100
    df['wicket']=np.where(df['wicket_id'].notna(), 1,0)
    wicket_taken=df[(df['season']==season) & (df['batsman1_name']==batsman) & (df['bowler1_name']==bowler)]['wicket'].sum()
    df['Boundary'] = np.where(df['isBoundary'] == True, 1, 0)
    score_boundary=df[(df['season']==season) & (df['batsman1_name']==batsman) & (df['bowler1_name']==bowler)]['Boundary'].sum()
    economyrate=(run_scored/(balls_faced/6))


    df_faceoff["Runs Scored"]=[run_scored]
    df_faceoff["Balls Faced"]=[balls_faced]
    df_faceoff["Strike Rate"]=[strikerate]
    df_faceoff["Wicket"]=[wicket_taken]
    df_faceoff["Boundaries"]=[score_boundary]
    df_faceoff["Economy Rate"]=[economyrate]


    return df_faceoff


def top_bowler_season(df,season):
    bowler_season=df[df['season']==season].groupby('fullName')['wickets'].sum().sort_values(ascending=False)[:5]

    return bowler_season



def top_batsman_season(df,season):
    batsman_Season=df[df['season']==season].groupby('fullName')['runs'].sum().sort_values(ascending=False)[:5]

    return batsman_Season

def top_four_scorer(df,season):
    four_season=df[df['season']==season].groupby('fullName')['fours'].sum().sort_values(ascending=False)[:5]

    return four_season

def top_six_scorer(df,season):
    six_season=df[df['season']==season].groupby('fullName')['sixes'].sum().sort_values(ascending=False)[:5]

    return six_season


    
