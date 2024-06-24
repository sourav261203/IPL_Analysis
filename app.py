#importibg libararies
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
import preprocessing
import helper
#ignoring warnings
warnings.filterwarnings('ignore')

#displaying all columns
pd.set_option('display.max_columns', None) 

#reading data as dataframes
points_table=pd.read_csv("IPL/points_table.csv")

batting_card=pd.read_csv("IPL/all_season_batting_card.csv")

bowling_card=pd.read_csv("IPL/all_season_bowling_card.csv")

season_detailed=pd.read_csv('IPL/all_season_details.csv')

season_summary=pd.read_csv("IPL/all_season_summary.csv")


preprocessing.inning_score_format(season_summary,'1st_inning_score')
preprocessing.inning_score_format(season_summary,'2nd_inning_score')

preprocessing.fillna_mean(season_summary,'1st_inning_score')
preprocessing.fillna_mean(season_summary,'2nd_inning_score')

preprocessing.fillna_median(season_summary,'home_boundaries')
preprocessing.fillna_median(season_summary,'away_boundaries')


#Creating new column named avarage innings score in season_summary dataframe

season_summary['avg_inning_score']=(season_summary['1st_inning_score']+season_summary['2nd_inning_score'])/2
season_summary['total_boundaries']=season_summary['home_boundaries']+season_summary['away_boundaries']


st.sidebar.title("IPL ANALYSIS")
st.sidebar.image(r"D:\Skills\Project\IPL_Analysis\Notebook\ipl_logo.jpg")

user_menu = st.sidebar.radio(
    "Select an Option",
    ( 'Overview', 'Team Analysis', 'Player Analysis')
)

if user_menu == 'Overview':

    total_seasons=season_summary['season'].nunique()
    total_teams=points_table['name'].nunique()
    total_matches=season_summary['id'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Total Season Played")
        st.title(total_seasons)
    with col2:
        st.header('Total Teams Participated')
        st.title(total_teams)
    with col3:
        st.header("Total Matches Played")
        st.title(total_matches)

    
    st.title('Qualifying Teams by Season')

    qualify=helper.Qualify_Teams(points_table)

    st.table(qualify)

    st.title("Average Runs Per Inning by Season")
    data=helper.avg_score_season(season_summary)
    fig = px.line( x=data.index, y=data['avg_inning_score'])
    fig.update_layout(
        # title='Average Runs Scored Per Innings Over IPL Season',
        xaxis_title='Season',
        yaxis_title='Runs',
        margin=dict(l=75, r=20, t=30, b=20),
        legend_title='Type')

    st.plotly_chart(fig)

    st.title("Distribution Of Runs (IPL History)")

    fig=px.pie(season_detailed['runs'].value_counts().to_frame()[:-1],values='count', names=season_detailed['runs'].value_counts().to_frame()[:-1].index)
    st.plotly_chart(fig)

    st.title("Average Boundaries Per Match by Season")
    boundaty_data=helper.avg_boundary_season(season_summary)
    fig = px.line( x=boundaty_data.index, y=boundaty_data['total_boundaries'])
    fig.update_layout(
        xaxis_title='Season',
        yaxis_title='Boundaries',
        margin=dict(l=75, r=20, t=30, b=20),
        legend_title='Type')
    st.plotly_chart(fig)

    st.title("Top 10 Most Used Stadiums")

    stadium=helper.top_Stadium(season_summary)

    fig4 = px.bar(x=stadium.index[0:10], y=stadium['count'][0:10],color_discrete_sequence=["#0068c9"])
    fig4.update_layout(
        xaxis_title='Venue Name',
        yaxis_title='No. Of Matches',
        margin=dict(l=75, r=20, t=30, b=20),
        legend_title='Type')
    st.plotly_chart(fig4)

    st.title("Most Used TV Umpires")
    tvumpire=helper.top_tvumpires(season_summary)
    fig5 = px.bar(x=tvumpire.index[0:10], y=tvumpire['count'][0:10], color_discrete_sequence=["#0068c9"])
    fig5.update_layout(
        xaxis_title='Tv Umpire Names',
        yaxis_title='No. Of Matches',
        legend_title='Type')
    st.plotly_chart(fig5)  

    st.title('Wides and No Balls Percentage')
    df1,df2,df3=helper.wide_noball_percent(bowling_card) 

    fig6 = px.line(
        x=df1.index, 
        y=(df2['wides'] / df1['total_balls']) * 100,
        color_discrete_sequence=["#3e0ce7"],
        labels={'x': 'Index', 'y': 'Percentage'} 
        # Adding labels for clarity
        
    )

    fig6.add_scatter(
        x=df1.index, 
        y=(df3['noballs'] / df1['total_balls']) * 100,
        mode='lines',
        name='No Balls' 
    )

    # Update the second trace color
    fig6.data[1].line.color = "#e70c3e"  # Choose your desired color here

    # Customize layout
    fig6.update_layout(
        xaxis_title='Season',
        yaxis_title='Percentage',
        legend_title='Type'
    )
    st.plotly_chart(fig6)




if user_menu == 'Team Analysis':

    teams,seasons=helper.season_n_teams(points_table)
    selected_team = st.sidebar.selectbox("Select Team", teams)
    selected_season = st.sidebar.selectbox("Select Season", seasons)

    st.title(f'{selected_team} Performance over IPL Seasons')

    performance=helper.Performance_of_team(points_table,selected_team,selected_season)
    performance.set_index('season',inplace=True)

    st.table(performance)


    st.title(f"Season, Over-wise Analysis of Runs,Boundaries & Wickets of {selected_team}")

    select_field=['runs','Boundary','wicket']
    selected_field = st.selectbox("Select Field", select_field)
    overs = st.slider(
        "Select Overs ",
        0, 20, (0,5))

    Seasons = st.slider(
        "Select Seasons ",
        2008, 2023, (2018,2021))


    final_df=helper.Overwise_Analysis(season_detailed,selected_field,Seasons[0],Seasons[1],selected_team,overs[0],overs[1])

    
    fig,ax=plt.subplots()
    if selected_field=='runs':
        palette = sns.color_palette("bright")

        ax = sns.barplot(x="over", 
                 y="runs", 
                 hue="season", 
                 data=final_df, 
                 ci=None, 
                 palette=palette)
        ax.set_ylabel("Average Runs")
        ax.legend(title='Season', loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1, title_fontsize='13', fontsize='9', frameon=True)
        st.pyplot(fig) 

    elif selected_field=='wicket':
        palette = sns.color_palette("bright")
        ax = sns.barplot(x="over", 
                 y="wicket", 
                 hue="season", 
                 data=final_df, 
                 ci=None, 
                 palette=palette,
                 estimator=sum)
        
        ax.legend(title='Season', loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1, title_fontsize='13', fontsize='9', frameon=True)
        st.pyplot(fig) 
        
    else:
        palette = sns.color_palette("bright")
        ax = sns.barplot(x="over", 
                 y="Boundary", 
                 hue="season", 
                 data=final_df, 
                 ci=None, 
                 palette=palette,
                 estimator=sum)
        
        ax.legend(title='Season', loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1, title_fontsize='13', fontsize='9', frameon=True)
        st.pyplot(fig) 

    st.title(f"Top 5  Batsman for {selected_team} in {selected_season}")
    top_batsman=helper.top_5_batsman(batting_card,selected_team,selected_season)
    fig = px.bar(x=top_batsman.values, y=top_batsman.index, orientation='h', color_discrete_sequence=[
        "#0068c9",
        ])
    fig.update_layout(
    xaxis_title='Runs',
    yaxis_title='Player Name',
    margin=dict(l=125, r=20, t=30, b=20),
    legend_title='Type')
    st.plotly_chart(fig)


    st.title(f"Top 5  Bowler for {selected_team} in {selected_season}")
    top_bowler=helper.top_5_bowler(bowling_card,selected_team,selected_season)
    #st.table(top_bowler)

    fig = px.bar(x=top_bowler.values, y=top_bowler.index, orientation='h', color_discrete_sequence=[
        "#9C2AB0",
        ])
    fig.update_layout(
    xaxis_title='Wickets',
    yaxis_title='Player Name',
    margin=dict(l=125, r=20, t=30, b=20),
    legend_title='Type')
    st.plotly_chart(fig)

    st.title(f"{selected_team} Winning Percentage On Different Venue")
    venue_win=helper.venue_win(season_summary,selected_team)
    st.table(venue_win)


if user_menu == 'Player Analysis':
    teams,seasons=helper.season_n_teams(points_table)
    selected_season = st.sidebar.selectbox("Select Season", seasons)  
    st.title('Batsman v/s Bowler FaceOff')
    batsman=season_detailed[(season_detailed['season']==selected_season)]['batsman1_name'].unique()
    batsman.sort()
    selected_batsman = st.selectbox("Select Batsman", batsman) 
    bowler=season_detailed[(season_detailed['season']==selected_season) & (season_detailed['batsman1_name']==selected_batsman)]['bowler1_name'].unique()
    bowler.sort()
    selected_bowler = st.selectbox("Select Bowler", bowler) 

    faceoff=helper.faceoff(season_detailed,selected_season,selected_batsman,selected_bowler)

    st.table(faceoff)

    st.title(f'Top Batman of  {selected_season}')
    TopBatsman_season=helper.top_batsman_season(batting_card,selected_season)
    fig = px.bar(x=TopBatsman_season.values, y=TopBatsman_season.index, orientation='h')
    fig.update_layout(
    xaxis_title='Runs',
    yaxis_title='Player Name',
    margin=dict(l=175, r=20, t=30, b=20),
    legend_title='Type'
)
    st.plotly_chart(fig)


    st.title(f'Top Bowler of  {selected_season}')
    TopBowler_season=helper.top_bowler_season(bowling_card,selected_season)
    fig = px.bar(x=TopBowler_season.values, y=TopBowler_season.index, orientation='h', color_discrete_sequence=[
        "#2C2AC0",
        ])
    fig.update_layout(
    xaxis_title='Wickets',
    yaxis_title='Player Name',
    margin=dict(l=175, r=20, t=30, b=20),
    legend_title='Type')

    st.plotly_chart(fig)


    st.title(f'Top Four Scorer of  {selected_season}')
    top_four=helper.top_four_scorer(batting_card,selected_season)
    fig = px.bar(x=top_four.values, y=top_four.index, orientation='h', color_discrete_sequence=[
        "#5C36AA",
        ])
    fig.update_layout(
    xaxis_title='No of Fours',
    yaxis_title='Player Name',
    margin=dict(l=175, r=20, t=30, b=20),
    legend_title='Type')

    st.plotly_chart(fig)

    st.title(f'Top Six Scorer of {selected_season}')
    top_six=helper.top_six_scorer(batting_card,selected_season)
    fig = px.bar(x=top_six.values, y=top_six.index, orientation='h', color_discrete_sequence=[
        "#D44040",
        ])
    fig.update_layout(
    xaxis_title='No of Sixes',
    yaxis_title='Player Name',
    margin=dict(l=175, r=20, t=30, b=20),
    legend_title='Type')

    st.plotly_chart(fig)






    



    
                                                                            






