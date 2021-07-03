import copy
import glob
import pprint as pp


from six import StringIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, cohen_kappa_score

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
                 'h_awayTeamScore',
                 'H_Dri', 'A_Dri', 'H_BaseStats',
                 'A_BaseStats', 'H_Pac', 'A_Pac',
                 'A_PHY', 'H_PHY', 'H_Pas', 'A_Pas',
                 'H_SHO', 'A_SHO',
                 'H_GROWTH', 'A_GROWTH', 'A_DEF', 'H_DEF']

    final_dataset.drop(drop_feat, axis= 1,inplace=True)

    # 5. Show variation of features by using describe() method
    des_feat = final_dataset.describe()
    print(des_feat)

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
    model_name = "RandForest"
    model = RandomForestClassifier(random_state=42)

    #  Feature selection abd training + testing
    stage = 0

    stage_drop_features_list = []
    stage_feature_remain_list = []

    stage_kappa_drop_features_list = []

    stage_records = []
    stage_kappa_records = []

    # Record highest score after each stage

    # Stage measure
    all_original_scores_list = []
    all_original_scores_name_list = []

    stage_highest_weighted_f_score = []

    stage_highest_accuracy = []
    stage_highest_home_f_score = []
    stage_highest_away_f_score = []
    stage_highest_home_precision = []
    stage_highest_away_precision = []
    stage_highest_home_recall = []
    stage_highest_away_recall = []

    stage_highest_kappa_score = []

    while (stage < 47):

        stage_X_train = copy.deepcopy(X_train)
        stage_X_test = copy.deepcopy(X_test)


        if (stage > 0) :
            stage_X_train.drop(stage_drop_features_list, axis=1, inplace=True)
            stage_X_test.drop(stage_drop_features_list, axis=1, inplace=True)


        drop_num = 46 - stage
        fix_num = 47 - int(len(stage_drop_features_list)/2)

        # Initialise feature to drop + highest scores
        updated_drop_features_list = []
        updated_remain_feature_set = []
        kappa_updated_drop_features_list = []

        highest_weighted_f_score = [0]
        highest_accuracy = [0]
        highest_home_f_score = [0]
        highest_away_f_score = [0]
        highest_home_precision = [0]
        highest_away_precision = [0]
        highest_home_recall = [0]
        highest_away_recall = [0]

        highest_kappa = [0]

        iteration_features = stage_X_train.columns
        feat_list = []

        # Generate feature list for dropping
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

            if (iteration > 0):
                d = [feat_list[drop_num], feat_list[drop_num + fix_num]]
                print("Drop features: ", d)
                updated_X_train.drop(d, axis=1, inplace=True)
                updated_X_test.drop(d, axis=1, inplace=True)
                drop_num -= 1

            model.fit(updated_X_train, y_train)
            y_pred = model.predict(updated_X_test)

            # Measure the performance of the model
            # confusion = confusion_matrix(y_test, y_pred)

            # report = classification_report(y_test, y_pred)
            report = classification_report(y_test, y_pred, digits = 4, output_dict= True)
            current_accuracy = report['accuracy']
            current_weighted_f_score = report['weighted avg']['f1-score']
            current_cohen_kappa_score = cohen_kappa_score(y_test, y_pred)

            # print(pp.pprint(report))

            print("Current accuracy: ", current_accuracy)
            print("Current weighted_f_score: ",current_weighted_f_score)
            print("Current_cohen_kappa_score: ", current_cohen_kappa_score)

            if (iteration == 0 and stage == 0):

                original_accuracy = current_accuracy
                all_original_scores_list.append(original_accuracy)
                all_original_scores_name_list.append('original_accuracy')

                original_home_f_score = report['1']['f1-score']
                all_original_scores_list.append(original_home_f_score)
                all_original_scores_name_list.append('original_home_f_score')

                original_away_f_score = report['0']['f1-score']
                all_original_scores_list.append(original_away_f_score)
                all_original_scores_name_list.append('original_away_f_score')

                original_home_precision = report['1']['precision']
                all_original_scores_list.append(original_home_precision)
                all_original_scores_name_list.append('original_home_precision')

                original_away_precision = report['0']['precision']
                all_original_scores_list.append(original_away_precision)
                all_original_scores_name_list.append('original_away_precision')


                original_home_recall = report['1']['recall']
                all_original_scores_list.append(original_home_recall)
                all_original_scores_name_list.append('original_home_recall')

                original_away_recall = report['0']['recall']
                all_original_scores_list.append(original_away_recall)
                all_original_scores_name_list.append('original_away_recall')

                original_macro_avg_f_score = report['macro avg']['f1-score']
                all_original_scores_list.append(original_macro_avg_f_score)
                all_original_scores_name_list.append('original_macro_avg_f_score')

                original_macro_avg_precision = report['macro avg']['precision']
                all_original_scores_list.append(original_macro_avg_precision)
                all_original_scores_name_list.append('original_macro_avg_precision')

                original_macro_avg_recall = report['macro avg']['recall']
                all_original_scores_list.append(original_macro_avg_recall)
                all_original_scores_name_list.append('original_macro_avg_recall')

                original_weighted_avg_f_score = report['weighted avg']['f1-score']
                all_original_scores_list.append(original_weighted_avg_f_score)
                all_original_scores_name_list.append('original_weighted_avg_f_score')

                original_weighted_avg_precision = report['weighted avg']['precision']
                all_original_scores_list.append(original_weighted_avg_precision)
                all_original_scores_name_list.append('original_weighted_avg_precision')

                original_weighted_avg_recall = report['weighted avg']['recall']
                all_original_scores_list.append(original_weighted_avg_recall)
                all_original_scores_name_list.append('original_weighted_avg_recall')

                original_support = report['weighted avg']['support']
                all_original_scores_list.append(original_support)
                all_original_scores_name_list.append('support')

                original_kapa_score = current_cohen_kappa_score
                all_original_scores_list.append(original_kapa_score)
                all_original_scores_name_list.append("Kapa_score")


            if (iteration == 1):
                highest_accuracy[0] = current_accuracy
                highest_weighted_f_score[0] = report['weighted avg']['f1-score']
                highest_home_f_score[0] = report['1']['f1-score']
                highest_away_f_score[0] = report['0']['f1-score']
                highest_home_precision[0] = report['1']['precision']
                highest_away_precision[0] = report['0']['precision']
                highest_home_recall[0] = report['1']['recall']
                highest_away_recall[0] = report['0']['recall']

                highest_kappa[0] = current_cohen_kappa_score

                updated_drop_features_list.append(feat_list[drop_num])
                updated_drop_features_list.append(feat_list[drop_num + fix_num])

                kappa_updated_drop_features_list.append(feat_list[drop_num])
                kappa_updated_drop_features_list.append(feat_list[drop_num + fix_num])

                updated_remain_feature_set.append(updated_X_train.columns)

            if (iteration > 1):
                if (current_weighted_f_score > highest_weighted_f_score[0]):

                    highest_accuracy[0] = current_accuracy

                    highest_weighted_f_score[0] = current_weighted_f_score
                    highest_home_f_score[0] = report['1']['f1-score']
                    highest_away_f_score[0] = report['0']['f1-score']
                    highest_home_precision[0] = report['1']['precision']
                    highest_away_precision[0] = report['0']['precision']
                    highest_home_recall[0] = report['1']['recall']
                    highest_away_recall[0] = report['0']['recall']


                    updated_drop_features_list[0] = feat_list[drop_num]
                    updated_drop_features_list[1] = feat_list[drop_num + fix_num]
                    updated_remain_feature_set[0] = updated_X_train.columns

                if (current_cohen_kappa_score > highest_kappa[0]):
                    highest_kappa[0] = current_cohen_kappa_score
                    kappa_updated_drop_features_list[0] = feat_list[drop_num]
                    kappa_updated_drop_features_list[1] = feat_list[drop_num + fix_num]


            print("Currently highest weighted_f_score: ", highest_weighted_f_score[0])
            print("iteration highest accuracy: ", highest_accuracy[0])
            print("Currently worst features", updated_drop_features_list)

            print("\n" + 100 * "#")

            print("Number of reduced features = ", len(stage_drop_features_list))


            iteration += 1
        # Update measure by f-score
        stage_drop_features_list.append(updated_drop_features_list[0])
        stage_records.append(stage)

        stage_highest_weighted_f_score.append(highest_weighted_f_score[0])
        stage_highest_accuracy.append(highest_accuracy[0])
        stage_highest_home_f_score.append(highest_home_f_score[0])
        stage_highest_away_f_score.append(highest_away_f_score[0])
        stage_highest_home_precision.append(highest_home_precision[0])
        stage_highest_away_precision.append(highest_away_precision[0])
        stage_highest_home_recall.append(highest_home_recall[0])
        stage_highest_away_recall.append(highest_away_recall[0])

        stage_drop_features_list.append(updated_drop_features_list[1])
        stage_records.append(stage)

        stage_highest_weighted_f_score.append(highest_weighted_f_score[0])
        stage_highest_accuracy.append(highest_accuracy[0])
        stage_highest_home_f_score.append(highest_home_f_score[0])
        stage_highest_away_f_score.append(highest_away_f_score[0])
        stage_highest_home_precision.append(highest_home_precision[0])
        stage_highest_away_precision.append(highest_away_precision[0])
        stage_highest_home_recall.append(highest_home_recall[0])
        stage_highest_away_recall.append(highest_away_recall[0])

        stage_feature_remain_list.append(updated_remain_feature_set)

        # Update by Kappa score
        stage_kappa_drop_features_list.append(kappa_updated_drop_features_list[0])
        stage_kappa_records.append(stage)
        stage_highest_kappa_score.append(highest_kappa[0])

        stage_kappa_drop_features_list.append(kappa_updated_drop_features_list[1])
        stage_kappa_records.append(stage)
        stage_highest_kappa_score.append(highest_kappa[0])

        # print("Remain features", stage_feature_remain_list)
        # print("Stage drop feature list: ", stage_drop_features_list)

        stage += 1

        # Weighted score: https://towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1
        df_original_score = pd.DataFrame(
            {"score_name": all_original_scores_name_list, "scores": all_original_scores_list})
        print(df_original_score)

        df_original_score.to_csv("df_original_scores_" + model_name + ".csv")

        print("\n" + 100 * "#")

        df_f_measure_evaluation = pd.DataFrame({"drop_feature": stage_drop_features_list,
                                                "stage_record": stage_records,
                                                "stage_highest_weighted_f_score": stage_highest_weighted_f_score,
                                                "accuracy": stage_highest_accuracy,
                                                "home_f_score": stage_highest_home_f_score,
                                                "away_f_score": stage_highest_away_f_score,
                                                "home_precision": stage_highest_home_precision,
                                                "away_precision": stage_highest_away_precision,
                                                "home_recall": stage_highest_home_recall,
                                                "away_recall": stage_highest_away_recall})

        print("\n" + 100 * "#")
        print(df_f_measure_evaluation)
        # df_f_measure_evaluation.to_csv("df_f_measure_evaluation_" + model_name + ".csv")

        print("\n" + 100 * "#")

        df_kappa_evaluation = pd.DataFrame({"kapa_drop_feature": stage_kappa_drop_features_list,
                                            "kapa_stage_record": stage_kappa_records,
                                            "kapa_score": stage_highest_kappa_score})

        print("\n" + 100 * "#")
        print(df_kappa_evaluation)
        # df_kappa_evaluation.to_csv("df_kappa_evaluation_" + model_name + ".csv")

if __name__ == "__main__":
    main()