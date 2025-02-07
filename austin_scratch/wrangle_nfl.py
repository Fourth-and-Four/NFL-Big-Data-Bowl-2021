import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

# Turn off warnings
import warnings
warnings.filterwarnings("ignore")

# split_scale
# import split_scale

# libraries needed for preparing the data:
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
import sklearn.preprocessing
from sklearn.cluster import KMeans

def train_validate_test(df):
    '''
    this function takes in a dataframe and splits it into 3 samples, 
    a test, which is 30% of the entire dataframe, 
    a validate, which is 28% of the entire dataframe,
    and a train, which is 42% of the entire dataframe. 
    It then splits each of the 3 samples into a dataframe with independent variables
    and a series with the dependent, or target variable. 
    The function returns 3 dataframes and 3 series:
    X_train (df) & y_train (series), X_validate & y_validate, X_test & y_test. 
    '''
    # split df into test (30%) and train_validate (70%)
    train_validate, test = train_test_split(df, test_size=.3, random_state=123, stratify = df.pass_stopped)

    # split train_validate off into train (60% of 70% = 42%) and validate (40% of 70% = 28%)
    train, validate = train_test_split(train_validate, test_size=.4, random_state=123, stratify = train_validate.pass_stopped)


    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns= ['time', 'nflId', 'displayName',
                                  'jerseyNumber', 'frameId', 'gameId', 'playId',
                                  'route', 'week', 'birthDate'])
    X_validate = validate.drop(columns= ['time', 'nflId', 'displayName',
                                  'jerseyNumber', 'frameId', 'gameId', 'playId',
                                  'route', 'week', 'birthDate'])
    X_test = test.drop(columns= ['time', 'nflId', 'displayName',
                                  'jerseyNumber', 'frameId', 'gameId', 'playId',
                                  'route', 'week', 'birthDate'])

    y_train = train[['pass_stopped']]
    y_validate = validate[['pass_stopped']]
    y_test = test[['pass_stopped']]
    return X_train, y_train, X_validate, y_validate, X_test, y_test


def min_max_scale(X_train, X_validate, X_test):
    '''
    this function takes in 3 dataframes with the same columns, 
    a list of numeric column names (because the scaler can only work with numeric columns),
    and fits a min-max scaler to the first dataframe and transforms all
    3 dataframes using that scaler. 
    it returns 3 dataframes with the same column names and scaled values. 
    '''
    # create the scaler object and fit it to X_train (i.e. identify min and max)
    # if copy = false, inplace row normalization happens and avoids a copy (if the input is already a numpy array).
    X_train = X_train.drop(columns = {'collegeName', 'position', 'pass_stopped',
                                      'playDescription', 'uniqueId', 'gameClock',
                                     'playResult', 'defender_receiver'})
    X_validate = X_validate.drop(columns = {'collegeName', 'position', 'pass_stopped',
                                            'playDescription', 'uniqueId', 'gameClock',
                                           'playResult', 'defender_receiver'})
    X_test = X_test.drop(columns = {'collegeName', 'position', 'pass_stopped',
                                    'playDescription', 'uniqueId', 'gameClock',
                                   'playResult', 'defender_receiver'})
    scaler = MinMaxScaler(copy = True).fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    X_validate_scaled = scaler.transform(X_validate)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns = X_train.columns.values).set_index([X_train.index.values])
    X_validate_scaled = pd.DataFrame(X_validate_scaled, columns =
                                     X_validate.columns.values).set_index([X_validate.index.values])
    X_test_scaled = pd.DataFrame(X_test_scaled, columns = X_test.columns.values).set_index([X_test.index.values])


    return X_train_scaled, X_validate_scaled, X_test_scaled

def add_clusters(X_train_scaled, X_validate_scaled, X_test_scaled, X_train, X_validate, X_test):
    X1_train = X_train_scaled[['height', 'weight', 'age', 'RB', 'TE', 'WR', 'DL',
                               'LB', 'DB', 's', 'a', 'dis']]
    X1_val = X_validate_scaled[['height', 'weight', 'age', 'RB', 'TE', 'WR', 'DL',
                                'LB', 'DB', 's', 'a', 'dis']]
    X1_test = X_test_scaled[['height', 'weight', 'age', 'RB', 'TE', 'WR', 'DL',
                             'LB', 'DB', 's', 'a', 'dis']]
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(X1_train)
    X_train_scaled['pos_att_cluster'] = kmeans.predict(X1_train)
    X_train['pos_att_cluster'] = kmeans.predict(X1_train)
    X_validate_scaled['pos_att_cluster'] = kmeans.predict(X1_val)
    X_validate['pos_att_cluster'] = kmeans.predict(X1_val)
    X_test_scaled['pos_att_cluster'] = kmeans.predict(X1_test)
    X_test['pos_att_cluster'] = kmeans.predict(X1_test)


    X2_train = X_train_scaled[['x', 'y', 'dis', 'o', 'dir', 'playDirection', 'quarter', 'down',
                               'yardsToGo', 'numberOfPassRushers', 'QB_under_pressure']]
    X2_val = X_validate_scaled[['x', 'y', 'dis', 'o', 'dir', 'playDirection', 'quarter', 'down',
                               'yardsToGo', 'numberOfPassRushers', 'QB_under_pressure']]
    X2_test = X_test_scaled[['x', 'y', 'dis', 'o', 'dir', 'playDirection', 'quarter', 'down',
                               'yardsToGo', 'numberOfPassRushers', 'QB_under_pressure']]
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X2_train)
    X_train_scaled['play_cluster'] = kmeans.predict(X2_train)
    X_train['play_cluster'] = kmeans.predict(X2_train)
    X_validate_scaled['play_cluster'] = kmeans.predict(X2_val)
    X_validate['play_cluster'] = kmeans.predict(X2_val)
    X_test_scaled['play_cluster'] = kmeans.predict(X2_test)
    X_test['play_cluster'] = kmeans.predict(X2_test)

    X3_train = X_train_scaled[['RB', 'TE', 'WR', 'DL', 'LB', 'DB', 'I_FORM', 'JUMBO',
                               'PISTOL', 'SHOTGUN', 'SINGLEBACK', 'WILDCAT', 'four_three', 'three_four',
                               'nickel', 'dime']]
    X3_val = X_validate_scaled[['RB', 'TE', 'WR', 'DL', 'LB', 'DB', 'I_FORM', 'JUMBO',
                               'PISTOL', 'SHOTGUN', 'SINGLEBACK', 'WILDCAT', 'four_three', 'three_four',
                               'nickel', 'dime']]
    X3_test = X_test_scaled[['RB', 'TE', 'WR', 'DL', 'LB', 'DB', 'I_FORM', 'JUMBO',
                               'PISTOL', 'SHOTGUN', 'SINGLEBACK', 'WILDCAT', 'four_three', 'three_four',
                               'nickel', 'dime']]
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(X3_train)
    X_train_scaled['offvsdef_cluster'] = kmeans.predict(X3_train)
    X_train['offvsdef_cluster'] = kmeans.predict(X3_train)
    X_validate_scaled['offvsdef_cluster'] = kmeans.predict(X3_val)
    X_validate['offvsdef_cluster'] = kmeans.predict(X3_val)
    X_test_scaled['offvsdef_cluster'] = kmeans.predict(X3_test)
    X_test['offvsdef_cluster'] = kmeans.predict(X3_test)

    X4_train = X_train_scaled[['QB_under_pressure', 'numberOfPassRushers', 'defendersInTheBox', 'force_per_second',
                               'time_since_last_x', 's', 'a']]
    X4_val = X_validate_scaled[['QB_under_pressure', 'numberOfPassRushers', 'defendersInTheBox', 'force_per_second',
                               'time_since_last_x', 's', 'a']]
    X4_test = X_test_scaled[['QB_under_pressure', 'numberOfPassRushers', 'defendersInTheBox', 'force_per_second',
                               'time_since_last_x', 's', 'a']]
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X4_train)
    X_train_scaled['def_react_cluster'] = kmeans.predict(X4_train)
    X_train['def_react_cluster'] = kmeans.predict(X4_train)
    X_validate_scaled['def_react_cluster'] = kmeans.predict(X4_val)
    X_validate['def_react_cluster'] = kmeans.predict(X4_val)
    X_test_scaled['def_react_cluster'] = kmeans.predict(X4_test)
    X_test['def_react_cluster'] = kmeans.predict(X4_test)
    
    return X_train_scaled, X_validate_scaled, X_test_scaled

print('Wrangle_NFL.py Loaded Successfully')