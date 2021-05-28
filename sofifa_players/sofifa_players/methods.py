'''
Student: Chi-Hung Le
StudentID: 19234245
Class 2021-CT5157 DataMining
'''

import numpy as num
import pandas as pd
import json_lines


def footBallTeamNameExtraction(file_name):

    read_team_name_file = pd.read_json(file_name)
    df = pd.DataFrame(read_team_name_file)

    # df=pd.read_json(orient=file_name)

    # print(df.__len__())

    # for i in range(0,df.__len__()):
    #    if df.team_name[i] != ' English Premier League (1)':
    #        print(i)
    # print(df.team_name[i])

    # df.to_csv('EPL_TEAM_ENGLAND.csv',)

    print(df.drop_duplicates().drop([1]))
    df.drop_duplicates().drop([1]).to_csv("TEAM_NAME.csv")
    # df.drop_duplicates().to_csv("test.csv")
    # s1 = 'English Premier League (1)'
    # if (df.team_name) != s1:
    #    print(df.items)

    # print(df.LONG_PASSING)
    # print(df.ATTACHING)
def footBallTeamAtributesExtraction(file_name):

    read_team_attributes_file = pd.read_json(file_name)

    df = pd.DataFrame(read_team_attributes_file)

    print(df.head(40))
    df.to_csv('TEAM_ID_FILE.csv')

def footballTeamAttributeExtraction(file_name):

    read_team_attribute_file = pd.read_json(file_name)

    df = pd.DataFrame(read_team_attribute_file)

    print(df.head())
    df.to_csv("Players.csv", index= False)

def playerAttributeExtraction(file_name):

    read_player_attribute_file = pd.read_json(file_name)

    df = pd.DataFrame(read_player_attribute_file)

    print(df.head())
    df.to_csv("Players.csv", index= False)

'''
    print(len(art_list))
    print(art_list[0])
    print(art_list[0].keys())
'''

def read_file_name(file_name):
    csv = pd.read_csv(file_name)
    return csv



def retrievePlayerAttributes(file_name, num):

    with open(file_name, "rb") as f:
        obj = json_lines.reader(f)
        # print(len(obj))

        # https://wiki.python.org/moin/Generators

        player_list = []
        while num > 0:
            item = next(obj)
            print(len(item))
            player_list.append(item)
            num = num - 1

        return player_list



