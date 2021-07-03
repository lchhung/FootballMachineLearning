import copy
import glob
import pprint as pp


from six import StringIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, cohen_kappa_score

from sklearn.model_selection import train_test_split

import numpy as np

import pandas as pd
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
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
    drop_feat = ['season', 'h_matchId',
                 'a_matchId', 'h_matchDate',
                 'a_matchDate','h_homeTeamId',
                 'a_homeTeamId','h_awayTeamId',
                 'a_awayTeamId', 'h_homeTeamScore',
                 'h_awayTeamScore',
                 'H_Dri', 'A_Dri', 'H_BaseStats',
                 'A_BaseStats', 'H_Pac', 'A_Pac',
                 'A_PHY', 'H_PHY', 'H_Pas', 'A_Pas',
                 'H_SHO', 'A_SHO',
                 'H_GROWTH', 'A_GROWTH', 'A_DEF', 'H_DEF']

    final_dataset.drop(drop_feat, axis= 1,inplace=True)

    # 5. Show variation of features by using describe() method
    # des_feat = final_dataset.describe()
    # print(des_feat)

    #6. Assign win label for home team, and name it as home_win

    h_win_label = []
    for label in final_dataset['label']:
        if label > 0:
            h_win = 1

        elif (label == 0):
            h_win = 0
        else:
            h_win = -1

        h_win_label.append(h_win)

    # h_win_label = []
    # for label in final_dataset['label']:
    #     if label > 0:
    #         h_win = 1
    #
    #     else:
    #         h_win = 0
    #
    #
    #     h_win_label.append(h_win)




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




    #8. Assign y_true
    y_true = final_dataset['home_win']
    # print(y_true)

    # Drop y-true from X for training and testing
    final_dataset.drop('home_win', axis=1, inplace= True)


    # print(final_dataset)

    X = final_dataset

    standadised_X = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)

    # print(standadised_X)

    # 10. Split dataset for training and testing
    X_train, X_test, y_train, y_test = train_test_split(standadised_X, y_true, test_size=0.4, random_state=42)
    print(X_train.shape)
    model_name = "RandForest"
    # model = RandomForestClassifier(random_state=42)


    # sel = SelectFromModel(RandomForestClassifier(n_estimators=100))
    # sel.fit(X_train, y_train)
    # sel.get_support()
    # selected_feat = X_train.columns[(sel.get_support())]
    # len(selected_feat)
    # print(selected_feat)

    # model = RandomForestClassifier(random_state=42, n_estimators=100)
    model = DecisionTreeClassifier(random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, digits=4, output_dict=True)
    current_accuracy = report['accuracy']
    current_weighted_f_score = report['weighted avg']['f1-score']
    current_cohen_kappa_score = cohen_kappa_score(y_test, y_pred)

    print(pp.pprint(report))
    print(current_cohen_kappa_score)


if __name__ == "__main__":
    main()