import glob
import time

import json_lines


# To run, type: python main.py
import csv
import pprint as pp
import pandas as pd

from sofifa_players.sofifa_players.methods import retrievePlayerAttributes

start = time.time()

def main():

    # Step 1; Run: scrapy crawl test -o data/test1.jsonlines
    # Step 2: Run this main file


    # file_name = "data//test1.jsonlines"
    # file_name = "data//test1.csv"
    # file_name ='test1.jsonlines'

    #footBallTeamNameExtraction(file_name)
    #footBallTeamAtributesExtraction(file_name)
    # footballTeamAttributeExtraction(file_name)
    # playerAttributeExtraction(file_name)
    # csv = read_file_name(file_name)
    # for row in csv:
    #     print(type(row))

    # file_name = "data//2021_04.jsonlines"
    # contents = retrievePlayerAttributes(file_name, num=1000)
    # # print(type(contents[0]))
    # # print((contents[0].keys()))
    # # print(len(contents))
    #
    # columns = ['date', 'Team', 'PlayerID', 'name', 'age', 'OVA', 'POT', 'Height', 'Weight',
    #            'FOOT', 'BOV', 'BP', 'GROWTH', 'ATTACHING', 'CROSSING', 'FINISHING', 'HEADING_ACCURACY',
    #            'SHORT_PASSING', 'Volleys', 'TotalSkill', 'Dribbing', 'Curve', 'FkAccuracy', 'LONG_PASSING',
    #            'BallControl', 'TotalMovement', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
    #            'TotalPower', 'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'TotalMentary',
    #            'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure', 'DEFENDING',
    #            'Marking', 'StandingStackle', 'SlidingTackle', 'GOALKEEPING', 'GKDriving', 'GKHandling',
    #            'GKKicking', 'GKPositioning', 'GKReflexes', 'TotalStats',
    #            'BaseStats', 'AttackingWorkRate', 'DefensiveWorkRate', 'Pac', 'SHO', 'Pas', 'Dri', 'DEF', 'PHY']
    # frame = []
    # for content in contents:
    #     df = pd.DataFrame(content)
    #     frame.append(df)
    # print(frame)
    #
    # df1 = pd.concat(frame)
    # df1.reset_index(drop=True, inplace= True)
    # df1.to_csv("2021_players.csv")
    # print(df1.head(10))

    file_path = glob.glob(r'data//2020_2021//*.jsonlines')

    list = []
    for file_name in file_path:
        # file_name = "data//2021_04.jsonlines"
        print(file_name)
        contents = retrievePlayerAttributes(file_name, num=11)
        # print(type(contents[0]))
        # print((contents[0].keys()))
        # print(len(contents))

        columns = ['date', 'Team', 'PlayerID', 'name', 'age', 'OVA', 'POT', 'Height', 'Weight',
                   'FOOT', 'BOV', 'BP', 'GROWTH', 'ATTACHING', 'CROSSING', 'FINISHING', 'HEADING_ACCURACY',
                   'SHORT_PASSING', 'Volleys', 'TotalSkill', 'Dribbing', 'Curve', 'FkAccuracy', 'LONG_PASSING',
                   'BallControl', 'TotalMovement', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                   'TotalPower', 'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'TotalMentary',
                   'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure', 'DEFENDING',
                   'Marking', 'StandingStackle', 'SlidingTackle', 'GOALKEEPING', 'GKDriving', 'GKHandling',
                   'GKKicking', 'GKPositioning', 'GKReflexes', 'TotalStats',
                   'BaseStats', 'AttackingWorkRate', 'DefensiveWorkRate', 'Pac', 'SHO', 'Pas', 'Dri', 'DEF', 'PHY']
        frame = []
        for content in contents:
            df = pd.DataFrame(content)
            frame.append(df)
        # print(frame)

        players_month = pd.concat(frame)

        list.append(players_month)
    sofifa_players_stats_list =pd.concat(list)
    sofifa_players_stats_list.reset_index(drop=True, inplace=True)
    sofifa_players_stats_list['date'] = sofifa_players_stats_list['date'] + "-01"
    names = sofifa_players_stats_list['name']
    teams =sofifa_players_stats_list['Team']
    sofifa_players_stats_list.drop(columns='Height', axis='columns', inplace=True)
    sofifa_players_stats_list.drop(columns='Weight', axis='columns', inplace=True)
    sofifa_players_stats_list.drop(columns='FOOT', axis='columns', inplace=True)

    lastName = []
    firstName = []

    original_name = []
    for name in names:
        original_name.append(name)
        splited_name = name.split()
        if (len(splited_name) == 2):
            lastName.append(splited_name[-1])
            firstName.append(splited_name[0])

        elif (len(splited_name) >= 3):
            lastName.append(splited_name[-2] + ' ' + splited_name[-1])
            firstName.append(splited_name[0])
        else:
            lastName.append(splited_name[0])
            firstName.append(splited_name[0])
    # print(lastName)
    print(original_name)
    sofifa_players_stats_list['firstName'] = firstName
    sofifa_players_stats_list['lastName'] = lastName

    team_list = []

    for team in teams:
        if(team == 'Wolverhampton Wanderers'):
            team = 'Wolves'
        if (team == 'Brighton & Hove Albion'):
            team = 'Brighton'
        if (team == 'Manchester City'):
            team = 'Man City'
        if (team == 'Manchester United'):
            team = 'Man Utd'
        if (team == 'Newcastle United'):
            team = 'Newcastle'
        if (team == 'Leeds United'):
            team = 'Leeds'
        if (team == 'Tottenham Hotspur'):
            team = 'Spurs'
        if (team == 'West Ham United'):
            team = 'West Ham'
        if (team == 'Leicester City'):
            team = 'Leicester'
        if (team == 'West Bromwich Albion'):
            team = 'West Brom'
        if (team == 'Sheffield United'):
            team = 'Sheffield Utd'
        if (team == 'Norwich City'):
            team = 'Norwich'
        # print(team)
        team_list.append(team)


    sofifa_players_stats_list['Team'] = team_list


    sofifa_players_stats_list.to_csv("2020_2021_sofifa_players_stats.csv")
    print(sofifa_players_stats_list.columns)


if __name__ == "__main__":
    main()

print("\n" + 40 * "#")
print(time.time() - start)
print(40 * "#" + "\n")