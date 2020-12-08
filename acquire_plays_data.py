import pandas as pd

def get_plays_data():
    df = pd.read_csv('plays.csv')
    return df

print("Acquire Loaded Successfully")