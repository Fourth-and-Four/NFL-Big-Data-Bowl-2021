import pandas as pd
import numpy as np
import acquire_plays_data
import re

def prep_plays_data():
    '''
    This function retrieves calls the function that acquires 
    the plays csv and prepares it for an mvp
    '''
    # acquire the plays csv and save it as a dataframe
    df = acquire_plays_data.get_plays_data()
    # keep only the useful columns for mvp
    df = df[['playDescription', 'quarter', 'down', 'yardsToGo', 'possessionTeam',
             'offenseFormation', 'personnelO', 'defendersInTheBox', 'numberOfPassRushers', 
             'personnelD', 'typeDropback', 'gameClock', 'absoluteYardlineNumber', 'epa',
             'playType', 'passResult', 'playResult']]
    # filter out any data that is not a pass play
    df = df[df.playType == 'play_type_pass']
    # creates 0 or 1 for tradtional and scramble
    df['typeDropback'].replace({'TRADITIONAL':0,'SCRAMBLE_ROLLOUT_RIGHT':1,
                                 'SCRAMBLE':1,'DESIGNED_ROLLOUT_RIGHT':0,
                                 'SCRAMBLE_ROLLOUT_LEFT':1,'DESIGNED_ROLLOUT_LEFT':0,
                                 'UNKNOWN':0}, inplace=True)
    # ranking the teams with the most cumulative passing yards
    df['possessionTeam'].replace({'TB': 1, 'PIT': 2, 'KC': 3, 'ATL': 4, 'LA': 5, 'GB': 6, 'PHI': 7,
                                  'NE': 8, 'NYG': 9, 'CLE': 10, 'IND': 11, 'HOU': 12, 'SF': 13, 'OAK': 14,
                                  'CAR': 15, 'MIN': 16, 'NO': 17, 'LAC': 18, 'DAL': 19, 'DET': 20, 'CHI': 21,
                                  'CIN': 22, 'DEN': 23, 'BAL': 24, 'JAX': 25, 'NYJ': 26, 'MIA': 27, 'WAS': 28,
                                  'TEN': 29, 'BUF': 30, 'ARI': 31, 'SEA': 32}, inplace=True)  
    
    # cleaning up the pass result column to only pass complete and pass incomplete
    df['passResult'].replace({'C': 0,'I' : 1, 'IN' : 1}, inplace=True)
    # create a new column that extracts 
    # "(number) RB, (number) TE, (number) WR"
    # and saves it as a temporary column
    df['tempO'] = df.personnelO.str.extract(r'(\d RB, \d TE, \d WR)')
    # create a new column that extracts 
    # "(number) DL, (number) LB, (number) DB"
    # and saves it as a temporary column
    df['tempD'] = df.personnelD.str.extract(r'(\d DL, \d LB, \d DB)')
    # keeps the rows that contain only the string in tempO column
    df = df[df.personnelO == df.tempO]
    # keep the rows that contain only the string in tempD column
    df = df[df.personnelD == df.tempD]
    # create a temporary dataframe containing the personnelO 
    # column split by a comma and space
    temp = df.personnelO.str.split(', ', expand = True)
    # create a new column with the number of RB on the field
    df['RB'] = temp[0].str.replace(r' RB', '')
    # create a new column with the number of TE on the field
    df['TE'] = temp[1].str.replace(r' TE', '')
    # create a new column with the number of WR on the field
    df['WR'] = temp[2].str.replace(r' WR', '')
    # create a temporary dataframe containing the personnelD 
    # column split by a comma and space
    temp = df.tempD.str.split(', ', expand = True)
    # create a new column with the number of DL on the field
    df['DL'] = temp[0].str.replace(r' DL', '')
    # create a new column with the number of LB on the field
    df['LB'] = temp[1].str.replace(r' LB', '')
    # create a new column with the number of DB on the field
    df['DB'] = temp[2].str.replace(r' DB', '')
    # create dummies for offensive formation
    formation = pd.get_dummies(df.offenseFormation)
    # Classifying traditional and rollouts into normal dropbacks
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('DESIGNED_ROLLOUT_RIGHT', 'normal'))
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('TRADITIONAL', 'normal'))
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('DESIGNED_ROLLOUT_LEFT', 'normal'))
    # Classifying all scrambles as scrambles
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('SCRAMBLE_ROLLOUT_RIGHT', 'scramble'))
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('SCRAMBLE', 'scramble'))
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('SCRAMBLE_ROLLOUT_LEFT', 'scramble'))
    df.typeDropback = df.typeDropback.apply(lambda value : str(value).replace('scramble_ROLLOUT_LEFT', 'scramble'))   
    df = df.rename(columns = {'typeDropback' : 'QB_under_pressure', 'passResult' : 'pass_stopped', 'possessionTeam': 'team_by_comp_yds'})
    # join all dataframes together
    df = pd.concat([df, formation], axis = 1)
    # drop temporary columns and duplicates
    df = df.drop(columns = {'personnelO', 'personnelD', 'tempO', 'tempD', 'playType', 'offenseFormation'})
    # reorder the index and drop the old index
    # Changing datatype from object to int
    df = df.astype({'DL':'int', 'LB':'int','DB':'int'})
    # crreating formation columns
    df['four_three'] = np.where((df['DL'] == 4) & (df['LB'] == 3),1,0)
    df['three_four'] = np.where((df['DL'] == 3) & (df['LB'] == 4),1,0)
    df['nickel'] = np.where(df['DB'] == 5, 1, 0)
    df['dime'] = np.where(df['DB'] == 6, 1, 0)
    df = df.reset_index(drop=True)
    df = df.dropna()
    return df

print("Prep.py Loaded Successfully")