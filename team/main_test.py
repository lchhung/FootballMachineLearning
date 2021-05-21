import requests


def main():

    url = 'https://footballapi.pulselive.com/football/stats/player/13286?comps=1&compSeasons=363'

    response = requests.get(url)

    print(response.text)


if __name__ =="__main__":
    main()