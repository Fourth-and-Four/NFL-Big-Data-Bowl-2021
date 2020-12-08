import pandas as pd
import acquire_plays_data

def prep_plays_data():
    df = acquire_plays_data.get_plays_data()
    df = df[['playDescription', 'quarter', 'down', 'yardsToGo', 'possessionTeam',
             'offenseFormation', 'personnelO', 'defendersInTheBox', 'numberOfPassRushers', 
             'personnelD', 'typeDropback', 'gameClock', 'absoluteYardlineNumber', 'epa', 'playType']]
    df.personnelO = df.personnelO.str.replace(r'\D',"")
    df.personnelD = df.personnelD.str.replace(r'\D',"")
    df = df[df.playType == 'play_type_pass']
    return df

print("Prep.py Loaded Successfully")