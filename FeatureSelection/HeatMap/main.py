import glob

import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns



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
    # drop_feat = ['A_AttackingWorkRate',
    #              'H_AttackingWorkRate', 'A_DefensiveWorkRate',
    #              'H_DefensiveWorkRate', 'A_TotalStats',
    #              'H_TotalStats', 'A_BaseStats', 'H_BaseStats', 'label',
    #              'H_TotalMentary', 'A_TotalMentary']
    final_dataset.drop(drop_label, axis=1, inplace=True)

    scaled_featured = final_dataset.copy()
    scaled_featured.drop('home_win', axis=1, inplace= True)
    feat_name = scaled_featured.columns

    features = final_dataset[feat_name]

    # print(features)

    # standadised_X = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=X.columns)
    # scaler = StandardScaler().fit_transform(final_dataset[feat_name] )
    scaled = MinMaxScaler().fit_transform(final_dataset[feat_name])

    # features = scaler.transform(features.values)
    # print(scaler)
    final_dataset[feat_name] = scaled
    final_dataset.reset_index(inplace=True)
    # print(final_dataset)
    score = final_dataset.corr()[['home_win']].sort_values(by='home_win', ascending=False)
    print(score)
    score.to_csv("heat_map_score.csv")
    plt.figure(figsize=(20, 20))
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    heatmap = sns.heatmap(final_dataset.corr()[['home_win']].sort_values(by='home_win', ascending=False), vmin=-1,
                          vmax=1, annot=False, cmap='BrBG')
    heatmap.set_title('HeatMap for correlation between features and match outcome', fontdict={'fontsize': 20}, pad=26)

    plt.ylabel("Features", fontdict={'fontsize': 18})
    plt.xlabel("home_win", fontdict={'fontsize': 18})

    plt.show()



    # cor = X.corr()[['home_win']].sort_values(by='home_win', ascending=False)
    # plt.figure(figsize=(8, 12))
    # heatmap = sns.heatmap(X.corr()[['home_win']].sort_values(by='home_win', ascending=False), vmin=-1,
    #                       vmax=1, annot=True, cmap='BrBG')
    # heatmap.set_title('Features Correlating with Sales Price', fontdict={'fontsize': 18}, pad=16);
    # plt.show()


if __name__ == "__main__":
    main()