
# Import the functions I will need for modeling
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.ensemble import RandomForestClassifier
import wrangle_plays_data
import prep_plays
import pandas as pd
import numpy as np

def MVP():
    df = prep_plays.prep_plays_data()
    X_train, y_train, X_validate, y_validate, X_test, y_test = wrangle_plays_data.train_validate_test(df)
    X_train_scaled, X_validate_scaled, X_test_scaled = wrangle_plays_data.min_max_scale(X_train, X_validate, X_test)
    rf = RandomForestClassifier(bootstrap=True, 
                            class_weight=None, 
                            criterion='gini',
                            min_samples_leaf=8,
                            n_estimators=100,
                            max_depth=15, 
                            random_state=123)
    
    print('---------------------------- Train -------------------------------')
    
    # fit train data
    rf.fit(X_train_scaled, y_train)
    # assign predicitons
    y_pred = rf.predict(X_train_scaled)
    # assign probabilities
    y_pred_proba = rf.predict_proba(X_train_scaled)
    print('Accuracy of random forest classifier on training set: {:.2f}'
         .format(rf.score(X_train_scaled, y_train)))
    print('Training Data Matrix')
    print(confusion_matrix(y_train, y_pred))
    # print report
    print('Training Data Report')
    print(classification_report(y_train, y_pred))
    
    print('---------------------------- Validate -------------------------------')
    
    # assign predicitions
    y_pred = rf.predict(X_validate_scaled)
    # assign probabilities
    y_pred_proba = rf.predict_proba(X_validate_scaled)
    print('Accuracy of random forest classifier on validate set: {:.2f}'
         .format(rf.score(X_validate_scaled, y_validate)))
    print('Validate Data Matrix')
    print(confusion_matrix(y_validate, y_pred))
    # print report
    print('Validate Data Report')
    print(classification_report(y_validate, y_pred))
    
    print('---------------------------- Test -------------------------------')
    
    # assign predicitions
    y_pred = rf.predict(X_test_scaled)
    # assign probabilities
    y_pred_proba = rf.predict_proba(X_test_scaled)
    print('Accuracy of random forest classifier on test set: {:.2f}'
         .format(rf.score(X_test_scaled, y_test)))
    print('Test Data Matrix')
    print(confusion_matrix(y_test, y_pred))
    # print report
    print('Test Data Report')
    print(classification_report(y_test, y_pred))
    
    print('--------------------- Important Features ---------------------------')
    feature_importances = pd.DataFrame(rf.feature_importances_,
                                   index = X_train_scaled.columns,
                                    columns=['importance']).sort_values('importance',ascending=False)
    return MVP, feature_importances

