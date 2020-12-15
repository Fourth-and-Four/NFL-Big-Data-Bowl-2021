import pandas as pd
import numpy as np
import acquire_plays_data
import re
from sklearn.model_selection import train_test_split

def prep_players():
    '''
    This function acquires the players csv and prepares
    it to merge with other csv's
    '''
    # Acquire the players csv
    df= pd.read_csv('players.csv')
    # Convert the birthdate to datetime to get rid of different date formats
    df.birthDate = pd.to_datetime(df.birthDate)
    # Creating a age column that takes the start date of the 2018 season and subtracts the birthdate
    df['age'] = (pd.to_datetime('09/06/2018') - df.birthDate).astype('<m8[Y]')
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
    return df