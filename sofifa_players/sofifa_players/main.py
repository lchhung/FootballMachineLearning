import glob
import time

import json_lines


# To run, type: python main.py
import csv
import pprint as pp
import pandas as pd

from methods import retrievePlayerAttributes

start = time.time()

def main():


    file_path = glob.glob(r'data//2016_2017//*.jsonlines')

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
    sofifa_players_stats_list['date'] = sofifa_players_stats_list['date']
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
        if (team == 'Hull City'):
            team = 'Hull'
        if (team == 'Swansea City'):
            team = 'Swansea'

        # print(team)
        team_list.append(team)


    sofifa_players_stats_list['Team'] = team_list


    sofifa_players_stats_list.to_csv("2016_2017_sofifa_players_stats_add.csv")
    print(sofifa_players_stats_list.columns)


if __name__ == "__main__":
    main()

print("\n" + 40 * "#")
print(time.time() - start)
print(40 * "#" + "\n")