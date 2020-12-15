import pandas as pd
import numpy as np
import acquire_plays_data
import re
from sklearn.model_selection import train_test_split


def prep_season():
    
    
    
    def prep_players():
        '''
        This function acquires the players csv and prepares
        it to merge with other csv's
        '''
        # Acquire the players csv
        players= pd.read_csv('players.csv')
        # Convert the birthdate to datetime to get rid of different date formats
        players.birthDate = pd.to_datetime(df.birthDate)
        # Creating a age column that takes the start date of the 2018 season and subtracts the birthdate
        players['age'] = (pd.to_datetime('09/06/2018') - df.birthDate).astype('<m8[Y]')
        # Function that converts heights
        def conv_height(value):
            if len(re.findall(r'(\d+)-(\d+)', value)) > 0:
                feet = int(re.findall(r'(\d+)-(\d+)', value)[0][0])
                inches = int(re.findall(r'(\d+)-(\d+)', value)[0][1])
                return (feet * 12) + inches
            else:
                return value
        # Changing height column to equal just inches
        df['height'] = df.height.apply(conv_height)
        return players 
    
    
    def merge_data():
        ''' This function will join together all the weeks and player csvs while incorporating George's changes to players'''
        df2 = players
        week1 = pd.read_csv('week1.csv')
        week1['week'] = 1
        week2 = pd.read_csv('week2.csv')
        week2['week'] = 2
        week3 = pd.read_csv('week3.csv')
        week3['week'] = 3
        week4 = pd.read_csv('week4.csv')
        week4['week'] = 4
        week5 = pd.read_csv('week5.csv')
        week5['week'] = 5
        week6 = pd.read_csv('week6.csv')
        week6['week'] = 6
        week7 = pd.read_csv('week7.csv')
        week7['week'] = 7
        week8 = pd.read_csv('week8.csv')
        week8['week'] = 8
        week9 = pd.read_csv('week9.csv')
        week9['week'] = 9
        week10 = pd.read_csv('week10.csv')
        week10['week'] = 10
        week11 = pd.read_csv('week11.csv')
        week11['week'] = 11
        week12 = pd.read_csv('week12.csv')
        week12['week'] = 12
        week13 = pd.read_csv('week13.csv')
        week13['week'] = 13
        week14 = pd.read_csv('week14.csv')
        week14['week'] = 14
        week15 = pd.read_csv('week15.csv')
        week15['week'] = 15
        week16 = pd.read_csv('week16.csv')
        week16['week'] = 16
        week17 = pd.read_csv('week17.csv')
        week17['week'] = 17
        df1 = pd.concat([week1, week2, week3, week4, week5, week6, week7, week8, week9,
                       week10, week11, week12, week13, week14, week15, week16, week17])
        df = pd.merge(df1, df2, how='inner', on='displayName')
        df = df.drop(columns = {'position_y', 'nflId_y'})
        df = df.rename(columns = {'position_x':'position', 'nflId_x': 'nflId'})

        return df
    
    def convert_event_col(df):
        ''' This function still needs work, I wasn't able to get it to work before I left for my appointment if you'd like 
        to fix it or just import Angels original function'''
        
        df = (df[df.event == 'pass_outcome_caught']) | (df[df.event == 'pass_outcome_incomplete']) |
             (df[df.event =='pass_outcome_interception'])
        df = df['event'].replace({'pass_outcome_caught': 0,'pass_outcome_incomplete' : 1,'pass_outcome_interception' : 1},
                            inplace=True)

        return df
    return df