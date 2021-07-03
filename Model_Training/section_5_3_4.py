import copy
import glob
import pprint as pp


from six import StringIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, cohen_kappa_score

from sklearn.model_selection import train_test_split, GridSearchCV

import numpy as np

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.svm import SVC

from sklearn.tree import export_graphviz, DecisionTreeClassifier
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

    drop_feat = ['season', 'h_matchId',
                 'a_matchId', 'h_matchDate',
                 'a_matchDate', 'h_homeTeamId',
                 'a_homeTeamId', 'h_awayTeamId',
                 'a_awayTeamId', 'h_homeTeamScore',
                 'h_awayTeamScore']

    final_dataset.drop(drop_feat, axis=1, inplace=True)

    # 5. Show variation of features by using describe() method
    # des_feat = final_dataset.describe()
    # print(des_feat)

    # 6. Assign win label for home team, and name it as home_win

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

    # 8. Assign y_true
    y_true = final_dataset['home_win']
    # print(y_true)

    # Drop y-true from X for training and testing
    final_dataset.drop('home_win', axis=1, inplace=True)

    # print(final_dataset)

    X = final_dataset
    X.reset_index(inplace=True, drop=True)



    standadised_X = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=X.columns)
    print(standadised_X)

    chi_square_32_features = ["H_OVA", "A_OVA", "H_POT", "A_POT", "H_BOV", "A_BOV", "H_BaseStats", "A_BaseStats",
                              "H_Reactions", "A_Reactions", "H_BallControl", "A_BallControl", "H_Dri", "A_Dri",
                              "H_totalSKILL", "A_totalSKILL", "H_Pas", "A_Pas", "H_DEFENDING", "A_DEFENDING",
                              "H_TotalStats", "A_TotalStats", "H_TotalMentary", "A_TotalMentary",
                              "H_TotalMovement", "A_TotalMovement", "H_ATTACKING", "A_ATTACKING", "H_SHORT_PASSING",
                              "A_SHORT_PASSING", "H_LONG_PASSING", "A_LONG_PASSING", "H_SHO", "A_SHO"]

    optimal_chi_square_32_features = ['H_TotalMentary', 'H_SHORT_PASSING', 'H_SHO', 'H_Reactions',
                                   'H_POT', 'H_OVA', 'H_LONG_PASSING', 'H_Dri', 'H_DEFENDING',
                                   'H_BallControl', 'H_BOV', 'A_TotalMentary', 'A_SHORT_PASSING', 'A_SHO',
                                   'A_Reactions',  'A_POT', 'A_OVA', 'A_LONG_PASSING', 'A_Dri',
                                   'A_DEFENDING', 'A_BallControl', 'A_BOV']

    ERT_26_features = ["H_OVA", "A_OVA", "H_BaseStats", "A_BaseStats", "H_BOV", "A_BOV", "H_Reactions", "A_Reactions",
                       "H_SHORT_PASSING", "A_SHORT_PASSING", "H_CROSSING", "A_CROSSING", "H_BallControl",
                       "A_BallControl",
                       "H_POT", "A_POT", "H_SHO", "A_SHO", "H_Pas", "A_Pas", "H_TotalStats", "A_TotalStats",
                       "H_ATTACKING", "A_ATTACKING"]

    HeatMap_34_features = ["H_OVA", "A_OVA", "H_POT", "A_POT", "H_BOV", "A_BOV", "H_Reactions", "A_Reactions",
                           "H_BaseStats", "A_BaseStats", "H_TotalStats", "A_TotalStats", "H_SHO", "A_SHO",
                           "H_Dri", "A_Dri", "H_Vision", "A_Vision", "H_BallControl", "A_BallControl",
                           "H_Pas", "A_Pas", "H_ATTACKING", "A_ATTACKING", "H_SHORT_PASSING", "A_SHORT_PASSING",
                           "H_totalSKILL", "A_totalSKILL", "H_DRIBBLING", "A_DRIBBLING", "H_TotalMentary",
                           "A_TotalMentary"]

    combined_feature = chi_square_32_features + ERT_26_features + HeatMap_34_features
    removed_duplucated_combined_features = list(dict.fromkeys(combined_feature))

    # sorted_features = sorted(removed_duplucated_combined_features, reverse= False)


    # sorted_features = sorted(chi_square_32_features, reverse=True)
    # sorted_features = sorted(ERT_26_features, reverse=True)
    # sorted_features = sorted(HeatMap_34_features, reverse=True)

    sorted_features = sorted(optimal_chi_square_32_features, reverse=True)

    # print((sorted_features))
    # print(len(sorted_features))

    X_final = standadised_X[sorted_features]

    X_train, X_test, y_train, y_test = train_test_split(X_final, y_true, test_size=0.33, random_state=42)


    # max_depth = 2
    f1_scores = []
    accuracy = []
    estimator_num = []
    max_depth = []

    # Generate n_estimator list [from 1 to 150]
    n = 1
    while n <=150:
        estimator_num.append(n)
        n += 1

    # Generate maxium_depth_list [ 1 from  to 5]
    m =1
    while m <=5:
        max_depth.append(m)
        m +=1
    print("n_estimators list: ",estimator_num)
    print("max_depth_list: ", max_depth)

    parameters = {
        'n_estimators': estimator_num,
        'max_depth': max_depth
    }

    model = RandomForestClassifier(random_state=42)

    # Initialise the GridSearchCV with cross-validation of 5 folds.
    gscv = GridSearchCV(model, parameters, cv=5)

    gscv.fit(X_train, y_train)
    get_hyper_param_results(gscv)

def get_hyper_param_results(gscv):
    print("Best parameters: {}\n".format(gscv.best_params_))
    means = gscv.cv_results_['mean_test_score']
    stds = gscv.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, gscv.cv_results_['params']):
        print('{} (+/-{}) for {}'.format(round(mean, 3), round(std*2, 3), params))


if __name__ == "__main__":
    main()