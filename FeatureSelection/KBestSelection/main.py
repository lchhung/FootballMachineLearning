import copy
import glob
import pprint as pp


from six import StringIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import confusion_matrix, classification_report, cohen_kappa_score

from sklearn.model_selection import train_test_split

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler

from sklearn.tree import export_graphviz
from IPython.display import Image
from pydot import graph_from_dot_data


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
    # drop_feat = ['season', 'h_matchId',
    #              'a_matchId', 'h_matchDate',
    #              'a_matchDate','h_homeTeamId',
    #              'a_homeTeamId','h_awayTeamId',
    #              'a_awayTeamId', 'h_homeTeamScore',
    #              'h_awayTeamScore',
    #              'H_Dri', 'A_Dri', 'H_BaseStats',
    #              'A_BaseStats', 'H_Pac', 'A_Pac',
    #              'A_PHY', 'H_PHY', 'H_Pas', 'A_Pas',
    #              'H_SHO', 'A_SHO',
    #              'H_GROWTH', 'A_GROWTH', 'A_DEF', 'H_DEF']

    # drop_feat = ['season', 'h_matchId',
    #              'a_matchId', 'h_matchDate',
    #              'a_matchDate', 'h_homeTeamId',
    #              'a_homeTeamId', 'h_awayTeamId',
    #              'a_awayTeamId', 'h_homeTeamScore',
    #              'h_awayTeamScore', "A_Dri", "H_Dri", "A_SHO", "H_SHO", "A_Pas", "H_Pas",
    #              "A_Pac", "H_Pac", "A_DEF", "H_DEF", "A_PHY", "H_PHY"]

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
            h_win = -1

        h_win_label.append(h_win)



    final_dataset['home_win'] = h_win_label

    # print(final_dataset)

    # See what feature has strong correlation with home_win
    by_label = final_dataset.groupby("home_win").mean()
    # print(by_label)

    # 7. Drop some more features because they have low correlation with home_win_label

    drop_label = ['label']

    final_dataset.drop(drop_label, axis=1, inplace=True)



    # Assign y_true
    y_true = final_dataset['home_win']
    # print(y_true)

    # Drop y-true from X for training and testing
    final_dataset.drop('home_win', axis=1, inplace= True)


    # Values of features
    X = final_dataset
    X.reset_index(inplace=True, drop=True)
    print(X)

    # Adopt MinMaxScaler() to scale feature values into a standadised range.
    standadised_X = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=X.columns)
    print(standadised_X.shape)

    # Calculate Chi-Square score and select the top highest scored features
    bestfeatures = SelectKBest(score_func=chi2, k=110)
    fit = bestfeatures.fit(standadised_X, y_true)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(standadised_X.columns)
    featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    featureScores.columns = ['Features', 'Score']  # naming the dataframe columns
    print(featureScores.nlargest(40, 'Score'))  # print 40 best features
    get_score = featureScores.nlargest(40, 'Score')
    get_score.to_csv("feature_score_40_1.csv")

    featureScores.reset_index(drop=True, inplace=True)
    y = []
    x= []
    for term_x in featureScores['Score']:
        x.append(term_x)
    for term_y in featureScores['Features']:
        y.append(term_y)

    # plt.show()

    plt.figure(figsize=(20, 20))
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    feat_rank = pd.Series(x, index=standadised_X.columns)
    nlargest = 60
    feat_rank.nlargest(nlargest).plot(kind='barh')
    plt.title("Chi-Square scores for " + str(nlargest) +" features", fontdict={'fontsize': 18}, pad= 18)
    plt.ylabel("Features", fontdict={'fontsize': 18})
    plt.xlabel("Chi-Square score", fontdict={'fontsize': 18})

    plt.show()

if __name__ == "__main__":
    main()