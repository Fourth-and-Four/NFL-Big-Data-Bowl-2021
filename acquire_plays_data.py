import pandas as pd

def get_plays_data():
    '''
    This function retrieves the data from a csv saved locally containing the plays data
    '''
    df = pd.read_csv('plays.csv')
    return df

print("Acquire.py Loaded Successfully")