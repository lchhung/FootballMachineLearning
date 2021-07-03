import copy
import glob
import pprint as pp


from six import StringIO
from sklearn.ensemble import RandomForestClassifier
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

    # h_win_label = []
    # for label in final_dataset['label']:
    #     if label > 0:
    #         h_win = 1
    #
    #     elif (label == 0):
    #         h_win = 0
    #     else:
    #         h_win = 2
    #
    #     h_win_label.append(h_win)

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

    attachking = [ 'H_CROSSING', 'A_CROSSING',
                  'H_FINISHING', 'A_FINISHING', 'H_HEADING_ACCURACY', 'A_HEADING_ACCURACY',

                  'H_AttackingWorkRate', 'A_AttackingWorkRate']

    attachking_remain = ['H_ATTACKING', 'A_ATTACKING', 'H_SHORT_PASSING', 'A_SHORT_PASSING',   'H_VOLLEYS', 'A_VOLLEYS',]
    final_dataset.drop(attachking, axis=1, inplace=True)

    MOVEMENT= [
               'H_Reactions', 'A_Reactions', 'H_Balance', 'A_Balance']

    MOVEMENT_REMAIN = ['H_SprintSpeed', 'A_SprintSpeed', 'H_Agility', 'A_Agility', 'H_Acceleration', 'A_Acceleration',]

    final_dataset.drop(MOVEMENT, axis=1, inplace=True)

    POWER= ['H_ShotPower', 'A_ShotPower', 'H_Jumping', 'A_Jumping',
            'H_Stamina', 'A_Stamina', 'H_Strength', 'A_Strength', 'H_LongShots', 'A_LongShots']
    final_dataset.drop(POWER, axis=1, inplace=True)

    MENTALITY= ['H_Aggression', 'A_Aggression', 'H_Interceptions', 'A_Interceptions', 'H_Positioning', 'A_Positioning',
                 'H_Penalties', 'A_Penalties', 'A_Composure', 'H_Composure']

    # Much better result when keep this
    MENTALITY_REMAIN = ['A_Vision', 'H_Vision',]

    final_dataset.drop(MENTALITY, axis=1, inplace=True)

    DEFENDING= ['H_Marking', 'A_Marking', 'H_StandingStackle', 'A_StandingStackle', 'A_SlidingTackle',
                'H_SlidingTackle', 'H_DefensiveWorkRate', 'A_DefensiveWorkRate']

    final_dataset.drop(DEFENDING, axis=1, inplace=True)

    GOALKEEPING= ['H_GKDriving', 'A_GKDriving', 'A_GKHandling', 'H_GKHandling', 'H_GKKicking', 'A_GKKicking',
                  'H_GKPositioning', 'A_GKPositioning', 'H_GKReflexes', 'A_GKReflexes', 'H_GOALKEEPING',
                  'A_GOALKEEPING']

    final_dataset.drop(GOALKEEPING, axis=1, inplace=True)

    OVERALL= ['H_BOV', 'A_BOV', 'A_DEFENDING', 'H_DEFENDING', 'H_TotalPower',
             'A_TotalPower', 'H_totalSKILL', 'A_totalSKILL', 'H_TotalMovement', 'A_TotalMovement',
            'H_TotalStats', 'A_TotalStats', 'H_TotalMentary', 'A_TotalMentary']

    OVERALL_REMAIN = ['H_OVA', 'A_OVA',  'H_POT', 'A_POT']

    final_dataset.drop(OVERALL, axis=1, inplace=True)


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
    X_train, X_test, y_train, y_test = train_test_split(standadised_X, y_true, test_size=0.3, random_state=42)
    print(X_train.shape)
    model_name = "RandForest"
    # model = RandomForestClassifier(random_state=42)
    # model = DecisionTreeClassifier(random_state = 42)
    # model = SVC(random_state=42)
    # model = GaussianNB()
    # model = BernoulliNB()
    # model = KNeighborsClassifier(n_neighbors=50)
    # model =  MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 3),
    #                        learning_rate = 'constant', max_iter = 150 , random_state=42)
    model = LogisticRegression(solver = 'newton-cg' , random_state=42)

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