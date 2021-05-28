import datetime
import glob
import json
import re
from methods import get_team_list, get_players, get_player_team, get_final_team_match_file, get_final_player_match_file, \
    get_match_id_list_from_html
import pandas as pd
import pprint as pp
import json_lines

from bs4 import BeautifulSoup


import codecs

from bs4 import BeautifulSoup
import requests
import csv

# https://www.premierleague.com/players/3955/player/stats?co=1&se=-1

def main():

    # Step 1:
    # Read matchID list from html files
    htm_file = "match_id_2015_2016.htm"
    final_match_id_list= get_match_id_list_from_html(htm_file)
    print("Match ID list for the PremierLeague season 2020/2021")
    print(pp.pprint(final_match_id_list))

    #Step 2
    # Get list of team and players for each match
    players_df, team_match_df = get_player_team(final_match_id_list)


    # # Step 3:
    # col = ['matchdate', 'teamId', 'playerId', 'firstName',
    #    'lastName', 'position', 'fullPosition']
    # #
    # player = pd.read_csv('player/PL_player_team_2020_2021.csv', usecols=col)
    # #
    # print(player.columns)
    # print(player)
    #
    # playerId = player['playerId']
    # print(playerId)


    ###########NEW###################

if __name__ == "__main__":
    main()