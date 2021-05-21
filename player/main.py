import requests
from bs4 import BeautifulSoup

import urllib.request

import pprint as pp


def main():

    url = "https://www.premierleague.com/players/4985/player/stats?co=1&se=363"

    playerId = 4985

    # updated_url = url.format(playerId)

    response = requests.get(url)


    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    opener = urllib.request.FancyURLopener({})
    url = url
    f = opener.open(url)
    content = f.read()

    print(pp.pprint(content))





if __name__ =="__main__":
    main()