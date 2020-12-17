import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import prep_season
import prep_plays
import os


# In[ ]:


def prep_nfl():
    df = prep_season.clean_season()
    df['force_per_second'] = (((df.weight * 0.45359237)/ (9.8)) * (df.s / 1.094)).round(2)
    df['uniqueId'] = (df.gameId.astype(str) + df.playId.astype(str)).astype(int)
    df2 = prep_plays.prep_plays_data()
    df2['uniqueId'] = (df2.gameId.astype(str) + df2.playId.astype(str)).astype(int)
    df = pd.merge(df, df2, how='left', on='uniqueId')
    df = df.drop(columns = {'playId_y', 'gameId_y', 'pass_stopped_y'})
    df = df.rename(columns = {'gameId_x': 'gameId','playId_x': 'playId', 'pass_stopped_x': 'pass_stopped'})
    df = df.dropna()
    df3 = prep_plays.get_weeksnplays_data()
    df3['uniqueId'] = df3.playid.rename({'playid': 'uniqueId'}).astype(int)
    df = pd.merge(df, df3, how='left', on='uniqueId')
    df = df.drop(columns = {'week_y', 'playid', 'playDescription_y', 'quarter_y', 'down_y',
                            'yardsToGo_y', 'team_by_comp_yds_y', 'defendersInTheBox_y',
                            'numberOfPassRushers_y', 'QB_under_pressure_y', 'gameClock_y',
                            'absoluteYardlineNumber_y', 'epa_y', 'pass_stopped_y', 'playResult_y',
                            'RB_y', 'TE_y', 'WR_y', 'DL_y', 'LB_y', 'DB_y', 'EMPTY_y', 'I_FORM_y',
                            'JUMBO_y', 'PISTOL_y', 'SHOTGUN_y', 'SINGLEBACK_y', 'WILDCAT_y',
                            'four_three_y', 'three_four_y', 'nickel_y', 'dime_y'})
    df = df.rename(columns = {'week_x': 'week', 'playDescription_x': 'playDescription',
                              'quarter_x': 'quarter', 'down_x': 'down', 'yardsToGo_x': 'yardsToGo',
                              'team_by_comp_yds_x': 'team_by_comp_yds', 'defendersInTheBox_x': 'defendersInTheBox',
                              'numberOfPassRushers_x': 'numberOfPassRushers', 'QB_under_pressure_x': 'QB_under_pressure',
                              'gameClock_x': 'gameClock','absoluteYardlineNumber_x': 'absoluteYardlineNumber',
                              'epa_y': 'epa', 'pass_stopped_x': 'pass_stopped', 'playResult_x': 'playResult',
                              'RB_x': 'RB', 'TE_x': 'TE', 'WR_x': 'WR', 'DL_x': 'DL', 'LB_x': 'LB', 'DB_x': 'DB',
                              'EMPTY_y': 'EMPTY', 'I_FORM_x': 'I_FORM','JUMBO_x': 'JUMBO', 'PISTOL_x': 'PISTOL',
                              'SHOTGUN_x': 'SHOTGUN', 'SINGLEBACK_x': 'SINGLEBACK', 'WILDCAT_x': 'WILDCAT',
                              'four_three_x': 'four_three', 'three_four_x': 'three_four', 'nickel_x': 'nickel',
                              'dime_x': 'dime', 'pass_stopped_x': 'pass_stopped', 'epa_x': 'epa'})
    df = df.dropna()
    df.to_csv('clean_nfl.csv')
    print('Prep_NFL.py Loaded Successfully')
    return df

def get_nfl_data():
    
    ''' This function will acquire the csv file needed to work with the season data, if there is not csv saved,
    then it ill iterate through the function above and create one for you'''
    
    if os.path.isfile('clean_nfl.csv'):
        df = pd.read_csv('clean_nfl.csv')
        df = df.drop(columns = {'Unnamed: 0'})
        print('Dataframe Ready For Use')
    else:
        df = prep_nfl()
        print('Dataframe Ready For Use')
    return df

print('Prep_NFL.py Imported Successfully')