import pandas as pd
import numpy as np
import acquire_plays_data
import re
from sklearn.model_selection import train_test_split

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
    df['possessionTeam'].replace({'TB': 1, 'PIT': 2, 'KC': 4, 'ATL': 3, 'LA': 5, 'GB': 7, 'PHI': 8,
                                  'NE': 9, 'NYG': 10, 'CLE': 11, 'IND': 6, 'HOU': 12, 'SF': 17, 'OAK': 16,
                                  'CAR': 15, 'MIN': 14, 'NO': 13, 'LAC': 19, 'DAL': 18, 'DET': 20, 'CHI': 22,
                                  'CIN': 24, 'DEN': 23, 'BAL': 21, 'JAX': 25, 'NYJ': 26, 'MIA': 28, 'WAS': 27,
                                  'TEN': 29, 'BUF': 31, 'ARI': 32, 'SEA': 30}, inplace=True)  
    
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
    # creating formation columns
    df['four_three'] = np.where((df['DL'] == 4) & (df['LB'] == 3),1,0)
    df['three_four'] = np.where((df['DL'] == 3) & (df['LB'] == 4),1,0)
    df['nickel'] = np.where(df['DB'] == 5, 1, 0)
    df['dime'] = np.where(df['DB'] == 6, 1, 0)
    df = df.reset_index(drop=True)
    df = df.dropna()
    return df



### Function for returning Passing Team Rank

def passing_team_rank():
    # brings in the plays csv
    plays = pd.read_csv('plays.csv')
    # returns only pass plays
    plays = plays[plays.playType == 'play_type_pass']
    # groups by team and sums the offense play result regardless of penalties
    team_rank = plays.groupby('possessionTeam')['offensePlayResult'].sum().reset_index()
    # sorts the summed results from highest to lowest
    team_rank = team_rank.sort_values(by='offensePlayResult', ascending=False)
    # returns the team rank
    return team_rank


def explore_plays_data():
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
    # creates 0 or 1 for tradtional and scramble
    df['typeDropback'].replace({'TRADITIONAL':0,'SCRAMBLE_ROLLOUT_RIGHT':1,
                                 'SCRAMBLE':1,'DESIGNED_ROLLOUT_RIGHT':0,
                                 'SCRAMBLE_ROLLOUT_LEFT':1,'DESIGNED_ROLLOUT_LEFT':0,
                                 'UNKNOWN':0}, inplace=True)
    df = df.rename(columns = {'typeDropback' : 'QB_under_pressure', 'passResult' : 'pass_stopped', 'possessionTeam': 'team_by_comp_yds'})
    # cleaning up the pass result column to only pass complete and pass incomplete
    df['pass_stopped'].replace({'C': 0,'I' : 1, 'IN' : 1}, inplace=True)         
    # filter out any data that is not a pass play
    df = df[df.playType == 'play_type_pass']
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
    #create a temporary dataframe containing the personnelD 
    #column split by a comma and space
    temp = df.tempD.str.split(', ', expand = True)
    # create a new column with the number of DL on the field
    df['DL'] = temp[0].str.replace(r' DL', '')
    # create a new column with the number of LB on the field
    df['LB'] = temp[1].str.replace(r' LB', '')
    # create a new column with the number of DB on the field
    df['DB'] = temp[2].str.replace(r' DB', '')
    # Changing datatype from object to int
    df = df.astype({'DL':'int', 'LB':'int','DB':'int'})
    # creating formation columns
    df['four_three'] = np.where((df['DL'] == 4) & (df['LB'] == 3),1,0)
    df['three_four'] = np.where((df['DL'] == 3) & (df['LB'] == 4),1,0)
    df['nickel'] = np.where(df['DB'] == 5, 1, 0)
    df['dime'] = np.where(df['DB'] == 6, 1, 0)
    
    # drop temporary columns and duplicates
    df = df.drop(columns = {'tempO', 'tempD'})
    df = df.reset_index(drop=True)
    df = df.dropna()
    # split df into test (30%) and train_validate (70%)
    train_validate, test = train_test_split(df, test_size=.3, random_state=123, stratify = df.pass_stopped)

    # split train_validate off into train (60% of 70% = 42%) and validate (40% of 70% = 28%)
    train, validate = train_test_split(train_validate, test_size=.4, random_state=123, stratify = train_validate.pass_stopped)
    return train, validate, test



###################################################################################
############################## PHASE 2 ############################################
###################################################################################
        
        
############################### prep plays csv to combine with weeks ##############


def prep_plays_for_weeks():
    '''
    This function retrieves calls the function that acquires 
    the plays csv and prepares it for weeks.csv.
    This is the same as the prepare file above without 
    train, validate, test split.
    '''
    # acquire the plays csv and save it as a dataframe
    df = acquire_plays_data.get_plays_data()
    # keep only the useful columns for mvp
    df = df[['gameId', 'playId', 'playDescription', 'quarter', 'down', 'yardsToGo', 'possessionTeam',
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
    df['possessionTeam'].replace({'TB': 1, 'PIT': 2, 'KC': 4, 'ATL': 3, 'LA': 5, 'GB': 7, 'PHI': 8,
                                  'NE': 9, 'NYG': 10, 'CLE': 11, 'IND': 6, 'HOU': 12, 'SF': 17, 'OAK': 16,
                                  'CAR': 15, 'MIN': 14, 'NO': 13, 'LAC': 19, 'DAL': 18, 'DET': 20, 'CHI': 22,
                                  'CIN': 24, 'DEN': 23, 'BAL': 21, 'JAX': 25, 'NYJ': 26, 'MIA': 28, 'WAS': 27,
                                  'TEN': 29, 'BUF': 31, 'ARI': 32, 'SEA': 30}, inplace=True)  
    
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


################################### prep week csv ###########################

def filter_nfl_weeks():
    '''
    This function creates a copy of the weeks.csv
    that only contain pass_forward
    '''
    
    for i in range(1,18):
        # read a week csv
        df = pd.read_csv('week' + str(i) + '.csv')
        # keep only 5 events from the df
        df = df[(df.event == 'pass_forward')]
        # fill null values in position to none
        df.position = df.position.fillna('BALL')
        # reset the index
        df.reset_index(drop=True)
        # save the df as a new csv
        df.to_csv('week' + str(i) + 'filtered.csv', index=False)
        # print the week number after you run through the above steps
        print(f'{i}')
    #had to drop playId '3640' because it was assigned pass_forward on two different frames
    week9 = pd.read_csv('week9filtered.csv')
    week9 = week9[week9.playId != 3640]
    week9.to_csv('week9filtered.csv')
    #had to drop plaId '2650' because it was assigned pass_forward on three different frames
    week10 = pd.read_csv('week10filtered.csv')
    week10 = week10[week10.playId != 2650]
    week10.to_csv('week10filtered.csv')
    

################################## getting new features ###########################
    
    
def combine_week_and_plays(week_num):
    '''
    This function combines the week.csv's
    with the plays data and returns
    playid and week number, name and distance 
    of closest defender with their coordindates
    '''
    ##############################################################
    #first we load our prepped plays and create a unique idetifier
    ##############################################################
    #loading prepped plays data
    plays = prep_plays_for_weeks()
    #changing gameid into string
    plays.gameId = plays.gameId.astype(str)
    #changing playid into string
    plays.playId = plays.playId.astype(str)
    #concat to create a unique identifier
    plays['playid'] = plays.gameId + plays.playId
    #drop old columns
    plays = plays.drop(columns = {'gameId', 'playId'})
    #drop any duplicates
    plays.drop_duplicates(inplace=True)
    ##############################################################
    #second we load our week data and create a unique identifier
    ##############################################################
    #read in week data that contains only plays when pass is being released
    week = pd.read_csv('week' + str(week_num) + 'filtered.csv')
    #changing gameid into string
    week.gameId = week.gameId.astype(str)
    #changing playid into string
    week.playId = week.playId.astype(str)
    #concat to create a unique identifier
    week['playid'] = week.gameId + week.playId
    #drop old columns
    week = week.drop(columns = {'gameId', 'playId'})
    #drop any duplicates
    week.drop_duplicates(inplace=True)
    ##############################################################
    #third we merge the dataframe
    ##############################################################
    #merge plays and week1 so we can have a play description
    df = pd.merge(plays, week, left_on = 'playid', right_on = 'playid', how = 'inner')
    #drop duplicates
    df.drop_duplicates(inplace=True)
    ##############################################################
    #forth we extract the intended receiver from the play description
    ##############################################################
    #extracting names from play description
    #second name will be the intended reciever
    desc = df.playDescription.str.findall(r'(\b[A-Z]+\.\b[A-Z]+\w+)').apply(','.join)
    #split the desc names by comma
    temp = desc.str.split(',', expand = True)
    #saving name of receiver
    df['receiver_last_name'] = temp[1]
    #splitting first and last name of player
    temp2 = df.displayName.str.split(' ', expand = True)
    #getting first initial
    initial = temp2[0].astype(str).str[0]
    #getting last name
    last_name = temp2[1]
    #saving player last name as first inital dot last name
    df['player_last_name'] = initial + '.' + last_name
    #filtering out the football
    df = df[df.displayName != 'Football']
    #resetting the index
    df = df.reset_index(drop=True)
    #labeling incorrect receivers with their surname
    df.loc[(df.receiver_last_name == 'J.Smith'),'receiver_last_name'] = 'J.Smith-Schuster'
    df.loc[(df.receiver_last_name == 'A.Seferian'),'receiver_last_name'] = 'A.Seferian-Jenkins'
    df.loc[(df.receiver_last_name == 'R.Seals'),'receiver_last_name'] = 'R.Seals-Jones'
    df.drop_duplicates(inplace=True)
    #########################################################################################################
    #fifth we create a function that will find the distance of the closest defender to the intended receiver
    ########################################################################################################
    newdf = pd.DataFrame(columns = ['playid', 'closest_dist', 'closest_x', 'closest_y', 'defender_receiver', 'week'])
    playids = [play for play in df.playid.unique()]

    #loop through each playid in playids
    for play in playids:
        #reset shortest distance
        closest_distance = 100
        #reset shortest x
        closest_x = 0
        #reset shortest y
        closest_y = 0
        #filter for all players in current play
        current_play = df[df.playid == play]
        #create a dataframe of offensive players
        offense = current_play[(current_play.position == 'QB') | (current_play.position == 'RB') | (current_play.position == 'WR') | (current_play.position == 'FB') | (current_play.position == 'HB') | (current_play.position == 'TE')]
        #create a dataframe of defensive players
        defense = current_play[(current_play.position == 'CB') | (current_play.position == 'OLB') | (current_play.position == 'FS') | (current_play.position == 'SS') | (current_play.position == 'ILB') | (current_play.position == 'MLB') | (current_play.position == 'LB') | (current_play.position == 'DB') | (current_play.position == 'S') | (current_play.position == 'DL') | (current_play.position == 'DE') | (current_play.position == 'NT')]
        #for x in coordinates of players
        for name in defense.displayName:
            if (offense.receiver_last_name == offense.player_last_name).any():
                #retrieve y coordinate of this player
                x = defense.loc[defense.displayName == name].x.item()
                #retrieve y coordinate of this player
                y = defense.loc[defense.displayName == name].y.item()
                #retrive x coordinate of reciever
                x1= offense.loc[offense.receiver_last_name == offense.player_last_name].x.item()
                # retrieve y coordinate of reciever
                y1= offense.loc[offense.receiver_last_name == offense.player_last_name].y.item()
                #solve for distance
                distance = ((x-x1)**2+(y-y1)**2)**(1/2)
                #if the distance is the shortest distance
                if distance < closest_distance:
                    #save the distance
                    closest_distance = distance
                    #save the x coordinate
                    closest_x = x
                    #save the y coordinate
                    closest_y = y
                    #save the defender name
                    def_name = name
            else:
                #fill with unrealistic values 
                closest_distance = 0
                closest_x = 0
                closest_y = 0
                def_name = "unknown"
        newdf = newdf.append({'playid': play, 'closest_dist': closest_distance, 'closest_x': closest_x, 'closest_y': closest_y, 'defender_receiver': def_name, 'week': week_num}, ignore_index=True)
    return newdf


################################ adding new features to original df ##########################


def combine_all_weeks_and_plays():
    '''
    This function creates new features from week.csv's
    and adds them to original prep_plays_for_weeks
    '''
    #create new features from week 1
    df = combine_week_and_plays(1)
    print(1)
    #create new features for remaining weeks
    for i in range(2,18):
        newdf = combine_week_and_plays(i)
        #append new features from weeks to each other
        df = df.append(newdf).reset_index(drop=True)
        #print week number when done
        print(i)
    #load prepped plays df    
    plays = prep_plays_for_weeks()
    #changing gameid into string
    plays.gameId = plays.gameId.astype(str)
    #changing playid into string
    plays.playId = plays.playId.astype(str)
    #concat to create a unique identifier
    plays['playid'] = plays.gameId + plays.playId
    #drop old columns
    plays = plays.drop(columns = {'gameId', 'playId'})
    #drop any duplicates
    plays.drop_duplicates(inplace=True)  
    #merge new features with old
    total_df = pd.merge(plays, df, left_on = 'playid', right_on = 'playid', how = 'inner')
    return total_df
