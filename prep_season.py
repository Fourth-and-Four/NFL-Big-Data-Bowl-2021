import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

########################### ALT Prep Season function ############################

def prep_season():
    '''
    This function acquires the players csv and prepares
    it to merge with other csv's
    '''
    
    # Acquire the players csv
    players= pd.read_csv('players.csv')
    # Convert the birthdate to datetime to get rid of different date formats
    players.birthDate = pd.to_datetime(players.birthDate)
    # Creating a age column that takes the start date of the 2018 season and subtracts the birthdate
    players['age'] = (pd.to_datetime('09/06/2018') - players.birthDate).astype('<m8[Y]')
    # Function that converts heights
    def conv_height(value):
        if len(re.findall(r'(\d+)-(\d+)', value)) > 0:
            feet = int(re.findall(r'(\d+)-(\d+)', value)[0][0])
            inches = int(re.findall(r'(\d+)-(\d+)', value)[0][1])
            return (feet * 12) + inches
        else:
            return value
    # Changing height column to equal just inches
    players['height'] = players.height.apply(conv_height)
    players['height'] = players['height'].astype(int)
    
    # Bringing in the week csv's
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
    
    # adding columns to measure time taken to travel and force of players
    df['time_since_last_x'] = (df.dis / df.s).round(4)        
    # Calculate force by converting the weight to Kg's then divide by gravity (9.81 m/s^2) * acceleration
    # This will provide a players force in Newtons
    df['force_per_second'] = (((df.weight * 0.45359237)/ (9.8)) * (df.s / 1.094)).round(4)
    
    
    # replacing the event column with target variable
    df.drop(df.index[df['event'] == 'None'], inplace = True)
    df.drop(df.index[df['event'] == 'ball_snap'], inplace = True)
    df.drop(df.index[df['event'] == 'pass_forward'], inplace = True)
    df.drop(df.index[df['event'] == 'pass_arrived'], inplace = True)
    df.drop(df.index[df['event'] == 'tackle'], inplace = True)
    df.drop(df.index[df['event'] == 'first_contact'], inplace = True)
    df.drop(df.index[df['event'] == 'play_action'], inplace = True)
    df.drop(df.index[df['event'] == 'out_of_bounds'], inplace = True)
    df.drop(df.index[df['event'] == 'line_set'], inplace = True)
    df.drop(df.index[df['event'] == 'man_in_motion'], inplace = True)
    df.drop(df.index[df['event'] == 'touchdown'], inplace = True)
    df.drop(df.index[df['event'] == 'pass_tipped'], inplace = True)
    df.drop(df.index[df['event'] == 'pass_outcome_touchdown'], inplace = True)
    df.drop(df.index[df['event'] == 'fumble'], inplace = True)
    df.drop(df.index[df['event'] == 'shift'], inplace = True)
    df.drop(df.index[df['event'] == 'fumble_defense_recovered'], inplace = True)
    df.drop(df.index[df['event'] == 'handoff'], inplace = True)
    df.drop(df.index[df['event'] == 'pass_shovel'], inplace = True)
    df.drop(df.index[df['event'] == 'penalty_flag'], inplace = True)
    df.drop(df.index[df['event'] == 'fumble_offense_recovered'], inplace = True)
    df.drop(df.index[df['event'] == 'touchback'], inplace = True)
    df.drop(df.index[df['event'] == 'penalty_accepted'], inplace = True)
    df.drop(df.index[df['event'] == 'field_goal_blocked'], inplace = True)
    df.drop(df.index[df['event'] == 'pass_lateral'], inplace = True)
    df.drop(df.index[df['event'] == 'lateral'], inplace = True)
    df.drop(df.index[df['event'] == 'snap_direct'], inplace = True)
    df.drop(df.index[df['event'] == 'run_pass_option'], inplace = True)
    df.drop(df.index[df['event'] == 'huddle_break_offense'], inplace = True)
    df.drop(df.index[df['event'] == 'huddle_start_offense'], inplace = True)
    df.drop(df.index[df['event'] == 'qb_strip_sack'], inplace = True)
    df.drop(df.index[df['event'] == 'timeout_home'], inplace = True)
    df.drop(df.index[df['event'] == 'qb_sack'], inplace = True)
    df.drop(df.index[df['event'] == 'qb_spike'], inplace = True)
    df.drop(df.index[df['event'] == 'run'], inplace = True)
    df.drop(df.index[df['event'] == 'punt_fake'], inplace = True)
    df.drop(df.index[df['event'] == 'field_goal_fake'], inplace = True)
    df.drop(df.index[df['event'] == 'safety'], inplace = True)
    df.drop(df.index[df['event'] == 'field_goal_play'], inplace = True)
    df['event'].replace({'pass_outcome_caught': 0,'pass_outcome_incomplete' : 1,'pass_outcome_interception' : 1}, inplace=True)
    df.reset_index(inplace=True)

    # Dropping undefined route
    df.drop(df.index[df['route'] == 'undefined'], inplace =True) 
    # Write DataFrame to csv file for future use
    df.to_csv('season.csv')
    print('CSV Successfully Created')
    return df


def get_season_data():
    
    ''' This function will acquire the csv file needed to work with the season data, if there is not csv saved,
    then it ill iterate through the function above and create one for you'''
    
    if os.path.isfile('season.csv'):
        df = pd.read_csv('season.csv')
        df = df.drop(columns = {'Unnamed: 0', 'index'})
        print('Season Data Imported Successfully')
    else:
        df = prep_season()
        df = df.drop(columns = {'index'})
        print('Season Data Imported Successfully')
    return df

def clean_season():
    df = get_season_data()
    df.route.fillna(value='NONE', inplace=True)
    df = df.dropna()
    df = df.rename(columns = {'event':'pass_stopped'})
    # 1 is play shifted to left side of field, 0 is play shifted to right side
    df['playDirection'] = df.playDirection.replace({'left': 1, 'right': 0})
    df['is_home'] = df.team.replace({'home': 1, 'away': 0})
    df = df.drop(columns = {'team'})
    df['time_since_last_x'] = df.time_since_last_x.replace([np.inf, -np.inf], np.nan)
    df['time_since_last_x'] = df.time_since_last_x.replace([np.inf, -np.inf], np.nan).dropna()
    df['is_defense'] = df.position.replace({'QB': 0, 'SS': 1, 'WR': 0, 'FS': 1, 'RB': 0, 'MLB': 1, 'CB': 1, 'TE': 0,
                                                 'LB': 1, 'FB': 0, 'OLB': 1,'HB': 0, 'ILB': 1, 'DL': 1, 'DB': 1,
                                                 'S': 1, 'NT': 1, 'DE': 1, 'P': 0, 'LS': 0, 'K': 0, 'DT': 1})
    return df

def get_viz(df):
    agedf = df.groupby('age')['event'].sum().reset_index()
    agedf = agedf.sort_values(by='event', ascending=False).head(7)
    sns.barplot(data=agedf, x='age', y= 'event', palette = 'mako')
    plt.title('Age and Incompletions', fontsize=13)
    plt.xlabel('age', fontsize=13)
    plt.ylabel('Incomplete Passes', fontsize=13)
    plt.show()

    ### College
    collegedf = df.groupby('collegeName')['event'].sum().reset_index()
    college20 = collegedf.sort_values(by='event', ascending=False).head(7)
    sns.barplot(data=college20, x='collegeName', y= 'event',palette='mako' )
    plt.title('College and Incompletions', fontsize=13)
    plt.xlabel('College', fontsize=13)
    plt.ylabel('Incomplete Passes', fontsize=13)
    #plt.xticks(rotation=30)
    plt.show()

    ### Height
    heightdf = df.groupby('height')['event'].sum().reset_index()
    heightdf = heightdf.sort_values(by='event', ascending=False).head(7)
    sns.barplot(data=heightdf, x='height', y= 'event', palette='mako')
    plt.title('Height and Incompletions', fontsize=13)
    plt.xlabel('height', fontsize=13)
    plt.ylabel('Incomplete Passes', fontsize=13)
    plt.xticks(rotation=30)
    plt.show()

    ### Weight
    weightdf = df.groupby('weight')['event'].sum().reset_index()
    weight20 = weightdf.sort_values(by='event', ascending=False).head(7)
    sns.barplot(data=weight20, x='weight', y= 'event', palette='mako')
    plt.title('Weight and Incompletions', fontsize=13)
    plt.xlabel('Weight', fontsize=13)
    plt.ylabel('Incomplete Passes', fontsize=13)
    plt.xticks(rotation=30)
    plt.show()



print('Prep_Season.py Loaded Successfully')