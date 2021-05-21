# Author: Chi-Hung Le
# UIoT, Insight Centre, NUI Galway
# For thesis in MSc of Software Engineering, NUI Galway

#To run: from Anaconda Protm, type: scrapy crawl pls -o data/test1.jsonlines

import scrapy

from ..items import PlayerPremier


class PlayerStatsPremier(scrapy.Spider):
    name = "pls"


    def start_requests(self):
        items = PlayerPremier()

        url = 'https://www.premierleague.com/players/4328/Sergio-Ag%C3%BCero/stats?co=1&se=363'
        #
        r = 4985 # Please change this value according to sofifa website
        domain = url.format(r)

        season = '2020/2021'

        # ses = [363]  # To nevagite the page
        # for se in ses:
        yield scrapy.Request(url=url, callback=self.parse, meta = {'season': season})

    def parse(self, response):

        items = PlayerPremier()

        playerInfor = response.css("div.playerStats")

        playerName = response.css("div.wrapper.playerContainer")


        for player_attributes in playerInfor:
            playerId = player_attributes.css("div::attr(data-player)").get()
            cleanSheet = player_attributes.css("div.normalStat > span.stat> span.allStatContainer.statclean_sheet ::text").extract()
            goalsConceded = player_attributes.css("div.normalStat > span.stat> span.allStatContainer.statgoals_conceded ::text").extract()
            goal = player_attributes.css(
                "div.normalStat > span.stat> span.allStatContainer.statgoals ::text").extract_first()


            # More player atributes will be added here
            items['playerId'] = playerId
            items['season'] = response.meta['season']
            items['cleanSheet']= cleanSheet
            items['goalsConceded'] = goalsConceded
            playerName = playerName.css("div.name.t-colour ::text").extract()
            items['playerName'] = playerName
            items['goal'] = goal

            print(response.meta['season'])



            yield items
