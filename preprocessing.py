import numpy as np
def inning_score_format(df,column):
    df[column]=df[column].str.split("/").str[0]
   


def fillna_mean(df,column):
    df[column].fillna(df[column].astype('float').mean(),inplace=True)
    df[column]=df[column].astype('int')

def fillna_median(df,column):
    df[column].fillna(df[column].astype('float').median(),inplace=True)
    df[column]=df[column].astype('int')
   

def overwise_preprocess(df):
    copy_sdetails=df.copy()
    copy_sdetails['isBoundary']=copy_sdetails['isBoundary'].astype('bool')
    
    copy_sdetails['Boundary'] = np.where(copy_sdetails['isBoundary'] == True, 1, 0)

    copy_sdetails['wicket']=np.where(copy_sdetails['wicket_id'].isnull(), 0,1)

    copy_sdetails=copy_sdetails[copy_sdetails['season'] != ' do we have a reserve day?"" --- Yep']

    copy_sdetails=copy_sdetails[copy_sdetails['season'] != ''' you can <a href=""https://www.espncricinfo.com/game/playandwatch"">Play and Watch with ESPNcricinfo\'s new game</a>.</b></p><p>Afeef : ""First time I remember watching Ambati Rayudu was in 2011 in the match where Sachin scored his IPL century. Rayudu scored 55 and was outscoring Sachin that day. I have been his fan since then. Feeling quite emotional knowing that this will be his last game. An amazing player.""</p><p><strong>6.30pm</strong> The <strong>covers are coming on</strong> at Motera. ""The pitch is covered''']

    copy_sdetails=copy_sdetails[copy_sdetails['season'] != ''' Shashank Kishore says from Ahmedabad. ""It\'s very''']

    copy_sdetails=copy_sdetails[copy_sdetails['season'] != ''' Team winning the toss have advantage. But these 2 teams have almost always stayed on top throughout the tournament and toss wouldn\'t matter to them. Hoping for a close contest.""</p><p><strong>6.05pm</strong> Ambati Rayudu''']

    copy_sdetails['season'].fillna('2023',inplace=True)

    copy_sdetails['season']=copy_sdetails['season'].astype('int')

    copy_sdetails.dropna(subset=['match_id'], inplace=True)

    copy_sdetails['over']=copy_sdetails['over'].astype('int')

    copy_sdetails['runs']=copy_sdetails['runs'].astype('int')

    return copy_sdetails

   