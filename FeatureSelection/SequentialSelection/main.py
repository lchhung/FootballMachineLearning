import glob
from time import time

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LassoCV
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import matplotlib.pyplot as plt

from mlxtend.feature_selection import SequentialFeatureSelector as sfs

from sklearn.feature_selection import SequentialFeatureSelector


def main():

    # 1. Input file parth
    file_path = glob.glob('data/*csv')

    # 2. Read the file
    frame = []
    h_win_label = []
    for file in file_path:
        df = pd.read_csv(file)
        frame.append(df)

    # 3. Create a final dataset
    final_dataset = pd.concat(frame)
    pd.set_option('display.max_columns', None)
    # final_dataset = pd.DataFrame(datasets)

    # 4. Drop unecessary features


    drop_feat = ['season', 'h_matchId',
                 'a_matchId', 'h_matchDate',
                 'a_matchDate', 'h_homeTeamId',
                 'a_homeTeamId', 'h_awayTeamId',
                 'a_awayTeamId', 'h_homeTeamScore',
                 'h_awayTeamScore']

    final_dataset.drop(drop_feat, axis= 1,inplace=True)

    # 5. Show variation of features by using describe() method
    # des_feat = final_dataset.describe()
    # print(des_feat)

    #6. Assign win label for home team, and name it as home_win

    # h_win_label = []
    # for label in final_dataset['label']:
    #     if label > 0:
    #         h_win = 1
    #     else:
    #         h_win = 0
    #
    #     h_win_label.append(h_win)

    h_win_label = []
    for label in final_dataset['label']:
        if label > 0:
            h_win = 1

        elif (label == 0):
            h_win = 0
        else:
            h_win = 2

        h_win_label.append(h_win)



    final_dataset['home_win'] = h_win_label

    # print(final_dataset)

    # See what feature has strong correlation with home_win
    by_label = final_dataset.groupby("home_win").mean()
    # print(by_label)

    # 7. Drop some more features because they have low correlation with home_win_label

    drop_label = ['label']

    final_dataset.drop(drop_label, axis=1, inplace=True)



    #8. Assign y_true
    y_true = final_dataset['home_win']
    # print(y_true)

    # Drop y-true from X for training and testing
    final_dataset.drop('home_win', axis=1, inplace= True)


    # print(final_dataset)

    X = final_dataset

    # standadised_X = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=X.columns)
    standadised_X = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)
    # print(standadised_X)

    # 10. Split dataset for training and testing
    X_train, X_test, y_train, y_test = train_test_split(standadised_X, y_true, test_size=0.33, random_state=42)
    # print(X_train)
    model_name = "RandForest"
    model = KNeighborsClassifier(n_neighbors=50)
    # model = RandomForestClassifier(random_state=42)

    sfs1 = sfs(model,
               k_features=10,
               forward=True,
               floating=False,
               verbose=2,
               scoring='accuracy',
               cv=5)
    sfs1 = sfs1.fit(X_train, y_train)
    feat_cols = list(sfs1.k_feature_idx_)
    print(feat_cols)

    model.fit(X_train[:feat_cols], y_train)
    y_pred = model.predict(X_test[:feat_cols])

    report = classification_report(y_test, y_pred, digits=4, output_dict=True)
    print(report)


if __name__ == "__main__":
    main()