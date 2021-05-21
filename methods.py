import csv
import datetime

import datetime
import glob
import json
import re
import pprint as pp

import pandas as pd

# 1. This method is to get team name, team id, match_date, and score
import requests
from bs4 import BeautifulSoup


def get_team_list(stats):
    team_num = len(stats['teams'])
    home_team_id = []
    away_team_id = []
    home_team_name = []
    away_team_name = []
    home_team_score = []
    away_team_score = []
    season_list = []

    for i in range(0, team_num):
        team = stats['teams'][i]
        teamId = (team['team']['id'])
        teamName = (team['team']['shortName'])
        teamScore = team['score']

        if (i == 0):
            home_team_id.append(teamId)
            home_team_name.append(teamName)
            home_team_score.append(teamScore)

        if (i == 1):
            away_team_id.append(teamId)
            away_team_name.append(teamName)
            away_team_score.append(teamScore)

    matchDate = datetime.datetime.fromtimestamp(stats['kickoff']['millis'] / 1000).strftime('%Y-%m-%d')

    return home_team_id, away_team_id, home_team_name, away_team_name, \
           home_team_score, away_team_score, matchDate


def get_players(stats):
    # Number of team = 2 per match
    team_id_list = []
    player_first_name = []
    player_last_name = []
    t_shirt_num = []
    player_position_short = []
    player_position_long = []
    player_id_list = []
    played_date = []
    for i in range(2):
        print(pp.pprint(stats['teamLists'][i].keys()))
        player_team_id = stats['teamLists'][i]['teamId']

        num_of_player = 11
        for j in range(0, num_of_player):
            line_up = stats['teamLists'][i]['lineup'][j]
            position = line_up['info']['position']
            playerId = line_up['id']
            player_id_list.append(playerId)
            player_position_short.append(position)
            shirtNum = line_up['info']['shirtNum']
            t_shirt_num.append(shirtNum)
            positionInfo = line_up['info']['positionInfo']
            player_position_long.append(positionInfo)
            first_name = line_up['name']['first']
            last_name = line_up['name']['last']
            player_last_name.append(last_name)
            team_id_list.append(player_team_id)
            player_first_name.append(first_name)
            matchDate = datetime.datetime.fromtimestamp(stats['kickoff']['millis'] / 1000).strftime('%Y-%m-%d')
            played_date.append(matchDate)

    return team_id_list, player_first_name, player_last_name, t_shirt_num, \
           player_position_short, player_position_long, player_id_list, played_date


def get_player_team(match_ids):
    url = "https://www.premierleague.com/match/{}"
    # latest_match_id = 59230
    # no_of_match = 1
    match_date = []
    home_team_id = []
    away_team_id = []
    home_team_name = []
    away_team_name = []
    home_team_score = []
    away_team_score = []
    match_id = []
    season_list = []

    # For players

    team_id_list = []
    player_first_name = []
    player_last_name = []
    t_shirt_num = []
    player_position_short = []
    player_position_long = []
    player_id_list = []
    played_date = []

    for i in range(len(match_ids)):
        # for i in range(63, 84):
        # Error at i = 28
        # Error at i = 41
        print(i)
        updated_url = url.format(match_ids[i])

        response = requests.get(updated_url)

        stats = json.loads(re.search(r"data-fixture='({.*})'", response.text).group(1))
        # print(stats.keys())

        home_id, away_id, home_name, \
        away_name, home_score, away_score, matchDate = get_team_list(stats)

        match_date.append(matchDate)

        home_team_id.append(home_id[0])
        home_team_name.append(home_name[0])
        home_team_score.append(home_score[0])

        away_team_id.append(away_id[0])
        away_team_name.append(away_name[0])
        away_team_score.append(away_score[0])
        match_id.append(match_ids[i])
        # print(match_id)

        season = stats['gameweek']['compSeason']['label']

        season_list.append(season)

        # Gte player lineup
        # Number of team = 2 per match
        for i in range(2):
            # print(pp.pprint(stats['teamLists'][i].keys()))
            player_team_id = stats['teamLists'][i]['teamId']
            player_no = 11
            for j in range(0, player_no):
                line_up = stats['teamLists'][i]['lineup'][j]
                position = line_up['info']['position']
                playerId = line_up['id']
                player_id_list.append(playerId)
                player_position_short.append(position)
                # shirtNum = line_up['info']['shirtNum']
                # t_shirt_num.append(shirtNum)
                positionInfo = line_up['info']['positionInfo']
                player_position_long.append(positionInfo)
                first_name = line_up['name']['first']
                last_name = line_up['name']['last']
                player_last_name.append(last_name)
                team_id_list.append(player_team_id)
                player_first_name.append(first_name)
                matchDate = datetime.datetime.fromtimestamp(stats['kickoff']['millis'] / 1000).strftime('%Y-%m-%d')
                played_date.append(matchDate)

    players_df = pd.DataFrame({"matchdate": played_date, "teamId": team_id_list,
                               "playerId": player_id_list, "firstName": player_first_name,
                               "lastName": player_last_name,
                               "position": player_position_short,
                               "fullPosition": player_position_long})

    # players_df = pd.DataFrame({"matchdate": played_date, "teamId": team_id_list,
    #                            "playerId": player_id_list, "firstName": player_first_name,
    #                            "lastName": player_last_name, "tShirtNumber": t_shirt_num,
    #                            "position": player_position_short,
    #                            "fullPosition": player_position_long})

    # print(players_df.head(100))
    players_df.to_csv("player/PL_player_team_2020_2021_n.csv")

    team_match_df = pd.DataFrame(
        {"season": season_list, "matchId": match_id, "matchDate": match_date, "homeTeamId": home_team_id,
         "homeTeamName": home_team_name, "awayTeamID": away_team_id,
         "awayTeamName": away_team_name, "homeTeamScore": home_team_score,
         "awayTeamScore": away_team_score})

    team_match_df.to_csv("team/PL_match_team_2020_2021_n.csv")
    # print(team_match_df.head(100))
    return players_df, team_match_df


def get_final_team_match_file():
    file_path = glob.glob(r'team/*.csv')
    file_list = []
    for file in file_path:
        df = pd.read_csv(file)
        col = ['season', 'matchId', 'matchDate', 'homeTeamId',
               'homeTeamName', 'awayTeamID', 'awayTeamName', 'homeTeamScore',
               'awayTeamScore']

        df1 = pd.DataFrame(df, columns=col)
        file_list.append(df1)

    # print(file_list)
    team_match = pd.concat(file_list)

    team_match.reset_index(level=None, drop=True, inplace=True)

    team_match['id'] = team_match.index

    print(team_match)

    team_match.to_csv("2020_2021_team_list_final_N.csv")


def get_final_player_match_file():
    file_path = glob.glob(r'player/*.csv')
    file_list = []
    for file in file_path:
        df = pd.read_csv(file)

        col = ['matchdate', 'teamId', 'playerId', 'firstName',
               'lastName', 'tShirtNumber', 'position', 'fullPosition']

        df1 = pd.DataFrame(df, columns=col)
        file_list.append(df1)

    # print(file_list)
    player_match = pd.concat(file_list)
    player_match.reset_index(level=None, drop=True, inplace=True)
    player_match['id'] = player_match.index

    print(player_match)
    player_match.to_csv("2020_2021_player_match_final.csv")


# Get match ID list
def get_match_id_list_from_html(htm_file):
    # Read team ID from html file (copy from console in webpage)
    soup_list = []
    with open(htm_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        id = soup.find_all('span', {'class': 'fixtureBroadcast broadcastDataContainer'})

        soup_list.append((id))
        # print((id))
    match_id_list = []
    for item in soup_list[0]:
        # print(item)
        match_id_list.append(str(item))

    # print((match_id_list[2]))

    match_id1 = []
    for term in match_id_list:
        numbers = []
        split_id = term.split()
        match_id1.append(split_id[3])
    # print(match_id1)

    final_id_list = []
    for term in match_id1:
        txt = re.sub('[data" "id= "" ></sp n> ]', " ", term)
        for term in txt.split():
            if term.isdigit():
                final_id_list.append(term)

    # print(final_id_list)

    # for id in final_id_list:
    # #     print(id)
    # print(len(final_id_list))

    # Remove duplicate Id
    final_id_list = list(dict.fromkeys(final_id_list))
    # print(final_id_list)
    return final_id_list
