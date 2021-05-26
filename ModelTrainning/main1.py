import copy
import glob


from six import StringIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

from sklearn.model_selection import train_test_split

import numpy as np

import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler

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
    drop_feat = ['season', 'h_matchId',
                 'a_matchId', 'h_matchDate',
                 'a_matchDate','h_homeTeamId',
                 'a_homeTeamId','h_awayTeamId',
                 'a_awayTeamId', 'h_homeTeamScore',
                 'h_awayTeamScore']

    final_dataset.drop(drop_feat, axis= 1,inplace=True)

    # 5. Show variation of features by using describe() method
    # des_feat = final_dataset.describe()
    # print(des_feat)

    #6. Assign win label for home team, and name it as home_win

    h_win_label = []
    for label in final_dataset['label']:
        if label > 0:
            h_win = 1
        else:
            h_win = 0
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
    X_train, X_test, y_train, y_test = train_test_split(standadised_X, y_true, test_size=0.33, random_state=42)
    # print(X_train)

    rf = RandomForestClassifier(criterion='entropy', oob_score=True, random_state=42)

    stage = 0

    stage_drop_features_list = []

    while (stage < 5):

        stage_X_train = copy.deepcopy(X_train)
        stage_X_test = copy.deepcopy(X_test)


        if (stage > 0) :
            stage_X_train.drop(stage_drop_features_list, axis=1, inplace=True)
            stage_X_test.drop(stage_drop_features_list, axis=1, inplace=True)

        stage_drop_feature = []
        # print("Current stage :", stage)
        # Drop each pair of feature types
        drop_num = 54 - stage
        fix_num = 55 - int(len(stage_drop_features_list)/2)

        original_accuracy = 0

        updated_drop_features_list = []
        highest_accuracy = [0]
        iteration_features = stage_X_train.columns
        feat_list = []
        for feat in iteration_features:
            feat_list.append(feat)

        iteration = 0
        while (drop_num >= 0):
            print('Current stage: ', stage)
            print("Stage drop feature: ", stage_drop_features_list)
            print("Drop num:", drop_num)
            print('Fix num: ', fix_num)
            print("Current iteration", iteration)

            # Resest X_train and X_test
            updated_X_train = copy.deepcopy(stage_X_train)
            updated_X_test = copy.deepcopy(stage_X_test)
            print(updated_X_train.shape)

            print("Original accuracy = ", original_accuracy)

            if (iteration > 0):
                d = [feat_list[drop_num], feat_list[drop_num + fix_num]]
                print("Drop features: ", d)
                updated_X_train.drop(d, axis=1, inplace=True)
                updated_X_test.drop(d, axis=1, inplace=True)
                drop_num -= 1

            rf.fit(updated_X_train, y_train)
            y_pred = rf.predict(updated_X_test)

            # Measure the performance of the model
            # confusion = confusion_matrix(y_test, y_pred)
            current_accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            print("report ", report)
            # print("Confusion: ", confusion)
            print("Current accuracy: ", current_accuracy)

            if (iteration == 0):
                original_accuracy = current_accuracy
            if (iteration == 1):
                highest_accuracy[0] = current_accuracy
                updated_drop_features_list.append(feat_list[drop_num])
                updated_drop_features_list.append(feat_list[drop_num + fix_num])
            if (iteration > 1):
                if (current_accuracy > highest_accuracy[0]):
                    highest_accuracy[0] = current_accuracy
                    updated_drop_features_list[0] = feat_list[drop_num]
                    updated_drop_features_list[1] = feat_list[drop_num + fix_num]

            print("Currently highest accuracy", highest_accuracy[0])
            print("Currently worst features", updated_drop_features_list)

            print("\n" + 100 * "#")

            iteration += 1
        stage_drop_features_list.append(updated_drop_features_list[0])
        stage_drop_features_list.append(updated_drop_features_list[1])

        stage += 1

if __name__ == "__main__":
    main()