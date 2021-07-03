# Author: Chi-Hung Le
# UIoT, Insight Centre, NUI Galway
# For thesis in MSc of Software Engineering, NUI Galway

#To run: from Anaconda Protm, type: scrapy crawl pl -o data/test1.jsonlines
import time

import scrapy

from ..items import PlayerAttributes


class PlayerInforExtractionFifa(scrapy.Spider):
    name = "pl"


    def start_requests(self):

        url = 'https://sofifa.com/players?keyword=Calum&r=170098&set=true'

        r = 150054 # Please change this value according to sofifa website
        domain = url.format(r)

        offsets = [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600]  # To nevagite the page
        date = '2015-08-14'
        for offset in offsets:

            yield scrapy.Request(url=domain, callback=self.parse, meta = {'date': date})

        time.sleep(2)
        yield scrapy.Request(url=url, callback=self.parse, meta={'date': date})


    def parse(self, response):

        items = PlayerAttributes()

        playerInfor = response.css("tbody.list")

        for player_attributes in playerInfor:

            # fullName = player_attributes.css("td.col-name >a.tooltip ::attr(data-tooltip)").get()
            name = player_attributes.css("td.col-name >a.tooltip> div.bp3-text-overflow-ellipsis ::text").extract()
            age = player_attributes.css('td.col.col-ae ::text').extract()
            OVA = player_attributes.css('td.col.col-oa.col-sort> span ::text').extract()
            POT = player_attributes.css("td.col.col-pt > span ::text").extract()
            Team = player_attributes.css("td.col-name > div.bp3-text-overflow-ellipsis > a ::text").extract()
            PlayerID = player_attributes.css("td.col.col-pi ::text").extract()
            Height = player_attributes.css('td.col.col-hi ::text').extract()
            Weight = player_attributes.css('td.col.col-wi ::text').extract()
            FOOT = player_attributes.css('td.col.col-pf ::text').extract()
            BOV = player_attributes.css('td.col.col-bo > span ::text').extract()
            BP = player_attributes.css('td.col.col-bp > a > span ::text').extract()
            GROWTH = player_attributes.css('td.col.col-gu > span ::text').extract()
            ATTACHING = player_attributes.css('td.col.col-ta > span ::text').extract()
            CROSSING = player_attributes.css('td.col.col-cr > span ::text').extract()
            FINISHING = player_attributes.css('td.col.col-fi > span ::text').extract()
            HEADING_ACCURACY = player_attributes.css('td.col.col-he > span ::text').extract()
            SHORT_PASSING = player_attributes.css('td.col.col-sh > span ::text').extract()
            Volleys = player_attributes.css('td.col.col-vo > span ::text').extract()
            TotalSkill = playerInfor.css('td.col.col-ts > span ::text').extract()
            Dribbing = playerInfor.css('td.col.col-dr > span ::text').extract()
            Curve = playerInfor.css('td.col.col-cu > span ::text').extract()
            FkAccuracy = playerInfor.css('td.col.col-fr > span ::text').extract()
            LONG_PASSING = player_attributes.css('td.col.col-lo > span ::text').extract()
            BallControl = player_attributes.css('td.col.col-bl > span ::text').extract()
            TotalMovement = player_attributes.css('td.col.col-to > span ::text').extract()
            Acceleration =  player_attributes.css('td.col.col-ac > span ::text').extract()
            SprintSpeed = player_attributes.css('td.col.col-sp > span ::text').extract()
            Agility = player_attributes.css('td.col.col-ag > span ::text').extract()
            Reactions = player_attributes.css('td.col.col-re > span ::text').extract()
            Balance = player_attributes.css('td.col.col-ba > span ::text').extract()
            TotalPower = player_attributes.css('td.col.col-tp > span ::text').extract()
            ShotPower = player_attributes.css('td.col.col-so > span ::text').extract()
            Jumping = player_attributes.css('td.col.col-ju > span ::text').extract()
            Stamina = player_attributes.css('td.col.col-st > span ::text').extract()
            Strength = player_attributes.css('td.col.col-sr > span ::text').extract()
            LongShots = player_attributes.css('td.col.col-ln > span ::text').extract()
            TotalMentary = player_attributes.css('td.col.col-te > span ::text').extract()
            Aggression = player_attributes.css('td.col.col-ar > span ::text').extract()
            Interceptions = player_attributes.css('td.col.col-in > span ::text').extract()
            Positioning = player_attributes.css('td.col.col-po > span ::text').extract()
            Vision = player_attributes.css('td.col.col-vi > span ::text').extract()
            Penalties = player_attributes.css('td.col.col-pe > span ::text').extract()
            Composure = player_attributes.css('td.col.col-pe > span ::text').extract()
            DEFENDING = player_attributes.css('td.col.col-cm > span ::text').extract()
            Marking = player_attributes.css('td.col.col-ma > span ::text').extract()
            StandingStackle = player_attributes.css('td.col.col-sa > span ::text').extract()
            SlidingTackle = player_attributes.css('td.col.col-sl > span ::text').extract()
            GOALKEEPING = player_attributes.css('td.col.col-tg > span ::text').extract()
            GKDriving = player_attributes.css('td.col.col-gd > span ::text').extract()
            GKHandling = player_attributes.css('td.col.col-gh > span ::text').extract()
            GKKicking = player_attributes.css('td.col.col-gc > span ::text').extract()
            GKPositioning = player_attributes.css('td.col.col-gp > span ::text').extract()
            GKReflexes = player_attributes.css('td.col.col-gr > span ::text').extract()
            TotalStats = player_attributes.css('td.col.col-tt > span ::text').extract()
            BaseStats = player_attributes.css('td.col.col-bs > span ::text').extract()
            AttackingWorkRate = playerInfor.css('td.col.col-aw ::text').extract()
            DefensiveWorkRate = playerInfor.css('td.col.col-dw ::text').extract()
            Pac = player_attributes.css('td.col.col-pac > span ::text').extract()
            SHO = player_attributes.css('td.col.col-sho > span ::text').extract()
            Pas = player_attributes.css('td.col.col-pas > span ::text').extract()
            Dri = player_attributes.css('td.col.col-dri > span ::text').extract()
            DEF = player_attributes.css('td.col.col-def > span ::text').extract()
            PHY = player_attributes.css('td.col.col-phy > span ::text').extract()

            # More player atributes will be added here
            items['date']= response.meta['date']
            items['Team'] = Team
            items['PlayerID'] = PlayerID
            # items['fullName'] = fullName
            items['name'] = name
            items['age'] = age
            items['OVA'] = OVA
            items['POT'] = POT
            items['Height'] = Height
            items['Weight'] = Weight
            items['FOOT'] = FOOT
            items['BOV'] = BOV
            items['BP'] = BP
            items['GROWTH'] = GROWTH
            items['ATTACHING'] = ATTACHING
            items['CROSSING'] = CROSSING
            items['FINISHING'] = FINISHING
            items['HEADING_ACCURACY'] = HEADING_ACCURACY
            items['SHORT_PASSING'] = SHORT_PASSING
            items['Volleys'] = Volleys
            items['TotalSkill'] = TotalSkill
            items['Dribbing'] = Dribbing
            items['Curve'] = Curve
            items['FkAccuracy'] = FkAccuracy
            items['LONG_PASSING'] = LONG_PASSING
            items['BallControl'] = BallControl
            items['TotalMovement'] = TotalMovement
            items['Acceleration'] = Acceleration
            items['SprintSpeed']= SprintSpeed
            items['Agility'] = Agility
            items['Reactions'] = Reactions
            items['Balance'] = Balance
            items['TotalPower'] = TotalPower
            items['ShotPower'] = ShotPower
            items['Jumping'] = Jumping
            items['Stamina'] = Stamina
            items['Strength'] = Strength
            items['LongShots'] = LongShots
            items['TotalMentary'] = TotalMentary
            items['Aggression'] = Aggression
            items['Interceptions'] = Interceptions
            items['Positioning'] = Positioning
            items['Vision'] = Vision
            items['Penalties'] = Penalties
            items['Composure'] = Composure
            items['DEFENDING'] = DEFENDING
            items['Marking']= Marking
            items['StandingStackle']= StandingStackle
            items['SlidingTackle']= SlidingTackle
            items['GOALKEEPING']= GOALKEEPING
            items['GKDriving']= GKDriving
            items['GKHandling']= GKHandling
            items['GKKicking']= GKKicking
            items['GKPositioning']= GKPositioning
            items['GKReflexes']= GKReflexes
            items['TotalStats']= TotalStats
            items['BaseStats']= BaseStats
            items['AttackingWorkRate'] = AttackingWorkRate
            items['DefensiveWorkRate'] = DefensiveWorkRate
            items['Pac']= Pac
            items['SHO']= SHO
            items['Pas']= Pas
            items['Dri']= Dri
            items['DEF']= DEF
            items['PHY']= PHY

            yield items
