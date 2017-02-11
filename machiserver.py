#!/usr/bin/env python
import random
import pprint

def debug(message):
    print message
    pass

# http://idwgames.com/wp-content/uploads/2015/02/Machi-RULES-reduced.pdf
# http://i2.wp.com/rollindiceshow.com/wp-content/uploads/2015/03/IMG_0003.jpg
allCards = {
    "wheatfield"        :{"cost":1, "type":"primary",   "roll":[1],    "amount":1},
    "ranch"             :{"cost":1, "type":"primary",   "roll":[2],    "amount":1},
    "forest"            :{"cost":3, "type":"primary",   "roll":[5],    "amount":1},
    "mine"              :{"cost":6, "type":"primary",   "roll":[9],    "amount":5},
    "appleorchard"      :{"cost":3, "type":"primary",   "roll":[10],   "amount":3},
    "bakery"            :{"cost":1, "type":"secondary", "roll":[2,3],  "amount":1},
    "conveniencestore"  :{"cost":2, "type":"secondary", "roll":[4],    "amount":3},
    "cheesefactory"     :{"cost":5, "type":"multiplier","roll":[7],
                            "factor":3, "cofactor":["ranch"]},
    "furniturefactory"  :{"cost":3, "type":"multiplier","roll":[8],
                            "factor":3, "cofactor":["mine", "forest"]},
    "market"            :{"cost":2, "type":"multiplier","roll":[11,12],
                            "factor":2, "cofactor":["wheatfield", "appleorchard"]},
    "cafe"              :{"cost":2, "type":"commercial","roll":[3],    "amount":1},
    "restaurant"        :{"cost":3, "type":"commercial","roll":[9-10], "amount":2},
    "stadium"           :{"cost":6, "type":"major",     "roll":[6]               },
    "tvstation"         :{"cost":7, "type":"major",     "roll":[6]               },
    "businesscenter"    :{"cost":8, "type":"major",     "roll":[6]               },
    "trainstation"      :{"cost":4, "type":"landmark"},
    "shoppingmall"      :{"cost":10,"type":"landmark"},
    "amusementpark"     :{"cost":16,"type":"landmark"},
    "radiotower"        :{"cost":22,"type":"landmark"}
    }

primaryCards =    {k:v for k,v in allCards.items() if v["type"] == "primary"}    # blue
secondaryCards =  {k:v for k,v in allCards.items() if v["type"] == "secondary"}  # green
multiplierCards = {k:v for k,v in allCards.items() if v["type"] == "multiplier"} # green
commercialCards = {k:v for k,v in allCards.items() if v["type"] == "commercial"} # red
majorCards =      {k:v for k,v in allCards.items() if v["type"] == "major"}      # purple
landmarkCards =   {k:v for k,v in allCards.items() if v["type"] == "landmark"}   # yellow

class Table:
    """This guy manages the stuff on the table without knowing the rules of the game
    Ask it to do something it cannot, and it will throw an assert.
    This class is not aware of any rules except the amount of which cards in the box,
    it DOES know landmarks from regular cards though as landmarks are attached to players.
    Asking the Table class to build somthing that the buildingbank does not have leads
    to an assert, transferring to much money from a player also leads to assert, building
    a landmark twice also asserts, etc, you get my drift"""
    def __init__(self, playerIds):
        assert(len(set(playerIds)) == len(playerIds) == 4) # 4 unique ids
        self.playerIds = playerIds
        self.buildingBank = {
            "wheatfield"        :10,
            "bakery"            :10,
            "ranch"             :6,
            "forest"            :6,
            "mine"              :6,
            "appleorchard"      :6,
            "conveniencestore"  :6,
            "cheesefactory"     :6,
            "furniturefactory"  :6,
            "market"            :6,
            "cafe"              :6,
            "restaurant"        :6,
            "stadium"           :4,
            "tvstation"         :4,
            "businesscenter"    :4
            }   # does not include landmarks as these are per player
        self.cities = {playerId:[] for playerId in playerIds}
        self.bank =   {playerId:0  for playerId in playerIds}
        for playerId in playerIds:
            self.build(playerId, "wheatfield")
            self.build(playerId, "bakery")
            self.gainCash(playerId, 3)
    def __str__(self):
        return pprint.pformat({
            "bank":self.bank,
            "cities":self.cities,
            "buildingbank":self.buildingBank})
    def availableBuildings(self):
        return [b for b,n in self.buildingBank.items() if n > 0]
    def build(self, playerId, building):
        debug(playerId + " builds a " + building)
        if building in landmarkCards.keys():
            assert(building not in self.cities[playerId])
        else:
            nInBank = self.buildingBank[building]
            assert(nInBank > 0)
            self.buildingBank[building] = nInBank - 1
        self.cities[playerId].append(building)
    def swapBuildings(self, playerIdA, buildingA, playerIdB, builingB):
        cityA = self.cities[playerIdA]
        cityB = self.cities[playerIdB]
        assert(buildingA in cityA and buildingB in cityB)
        cityA.remove(buildingA)
        cityB.remove(buildingB)
        cityA.append(buildingB)
        cityB.append(buildingA)
        debug(playerIdA + " trades its " + buildingA + " with " + playerIdB + "'s " + buildingB)
    def looseCash(self, playerId, amount):
        debug(playerId + " pays " + str(amount) + " to the bank")
        account = self.bank[playerId]
        assert(amount <= account)
        self.bank[playerId] = account - amount
    def gainCash(self, playerId, amount):
        debug(playerId + " gets " + str(amount) + " from the bank")
        account = self.bank[playerId]
        self.bank[playerId] = account + amount
    def transferCash(self, sourceId, targetId, amount):
        debug(sourceId + " pays " + str(actualAmount) + " to " + targetId)
        assert(amount >= self.bank[sourceId])
        self.bank[sourceId] = account - amount
        self.bank[targetId] = account + amount
    def getPlayerIds(self):
        return self.playerIds
    def playerHasN(self, playerId, building):
        assert(building in allCards)
        return self.cities[playerId].count(building)
    def playerCredit(self, playerId):
        return self.bank[playerId]

class RandomDice():
    def roll(self, ndice):
        assert(0 < ndice <= 2)
        return [random.randint(1,6) for i in range(ndice)]

class Game:
    def __init__(self, players):
        self.playerIds = [p.getId() for p in players]
        assert(len(self.playerIds) == len(set(self.playerIds)) == 4) # check for duplicate playerIds
        self.currentPlayerIndex = 0
        self.playerDict = {p.getId():p for p in players}
        self.currentTurnNr = 0
        self.table = Table(self.playerIds)
        self.dice = RandomDice()
    def getWinnerId(self):
        winners = []
        playerIds = self.table.getPlayerIds()
        for playerId in playerIds:
            if all([self.table.playerHasN(playerId, landmark) for landmark in landmarkCards.keys()]):
                winners.append(playerId)
        assert(len(winners) < 2) # two winners are not possible without having one first
        return None if len(winners) == 0 else winners[0]
    def _endTurn(self, extraTurn = False):
        debug("==========   ending turn " + str(self.currentTurnNr) + "   ==========")
        self.currentTurnNr += 1
        if not extraTurn:
            self.currentPlayerIndex = (self.currentPlayerIndex + 1) % len(self.playerIds)
    def play(self):
        while self.getWinnerId() == None:
            playerId = self.playerIds[self.currentPlayerIndex]
            player = self.playerDict[playerId]
            debug(str(self.table))
            debug("==========  starting turn " + str(self.currentTurnNr) + "  ==========")
            debug("-> " + playerId + "'s turn")
            roll = self._rollPhase(player)
            # if you roll doubles and have an amusement park you get an extra turn
            extraTurn = (     self.table.playerHasN(playerId,"amusementpark")
                          and len(roll) == 2
                          and roll[0] == roll[1] )
            if extraTurn:
                debug(playerId + " threw doubles, so gets another turn after this one!")

            self._calcIncome(player, roll)
            self._satanPhase(player, roll) #will only do smth on roll == 6
            self._buildPhase(player)

            self._endTurn(extraTurn = extraTurn)

    def _rollPhase(self, player):
        playerId = player.getId()
        ndice = 1
        if self.table.playerHasN(playerId, "trainstation") > 0:
            request = {"action":"ndice", "options":["1","2"]}
            choice = player.chooseAction(request)
            if choice == "2":
                ndice = 2
        roll = self.dice.roll(ndice)
        debug("rolled " + str(roll))
        if self.table.playerHasN(playerId, "radiotower") > 0:
            request = {"action":"reroll", "lastroll":roll, "options":["y","n"]}
            choice = player.chooseAction(request)
            if choice == "y":
                roll = dice.roll(ndice)
                debug("rerolled " + str(roll))
        return roll

    def _satanPhase(self, player, roll):
        if sum(roll) == 6:
            playerId = player.getId()
            if self.table.playerHasN(playerId, "stadium") > 0:
                for dupee in self._getPayOrder():
                    self.table._tryMoveCash(dupee, playerId, 2)

            if self.table.playerHasN(playerId, "tvstation") > 0:
                orderedOtherIds = self._getPayOrder()  # same relative order for everyone
                accounts = [(p,self.table.playerCredit(p)) for p in orderedOtherIds]
                playersWithCash = [p for p,amount in accounts if amount > 0]
                if playersWithCash:
                    request = {"action":"steal", "options":playersWithCash + [""]}
                    choice = player.chooseAction(request)
                    if choice != "":
                        assert(choice in playersWithCash)
                        self._tryMoveCash(choice, playerId, 5)

            if self.table.playerHasN(playerId, "businesscenter") > 0:
                orderedOtherIds = self._getPayOrder()  # same relative order for everyone
                tradableCards = ( set(allCards.keys())
                                - set(landmarkCards.keys())
                                - set(majorCards.keys()))
                cities = {pId:self.table.getCity(pId) for p in self.playerIds}

                # tradewho
                playersWithTradableCards = \
                    [otherPlayerId for otherPlayerId in orderedOtherIds
                                   if tradableCards.intersection(cities[otherPlayerId])]
                if playersWithTradableCards:
                    request = {"action":"tradewho", "options":playersWithTradableCards + [""]}
                    victimId = player.chooseAction(request)
                    if victimId != "":
                        assert(victimId in playersWithTradableCards)
                        # tradewhat
                        tradeWhatOptions = list(tradableCards.intersection(cities[victimId]))
                        request = {"action":"tradewhat", "options":tradeWhatOptions + [""]}
                        stolen = player.chooseAction(request)
                        if stolen != "":
                            assert(stolen in tradeWhatOptions)
                            # tradefor
                            tradeForOptions = list(tradableCards.intersection(cities[playerId]))
                            request = {"action":"tradefor", "options":tradeForOptions + [""]}
                            given = player.chooseAction(request)
                            if given != "":
                                assert(given in tradeForOptions)
                                self.table.swapBuildings(playerId, given, victimId, stolen)

    def _buildPhase(self, player):
        playerId = player.getId()
        buildings = self._getBuildableBuildings(playerId)
        if len(buildings) > 0: 
            request = {"action":"build", "options":buildings + [""]}
            choice = player.chooseAction(request)
            if choice in buildings:
                self._buyBuilding(playerId, choice)

    def getCurrentPlayerId(self):
        return self.playerIds[self.currentPlayerIndex]

    def _getPayOrder(self):
        i = self.currentPlayerIndex
        result = self.playerIds[i+1:] + self.playerIds[:i]
        result.reverse()
        return result

    def _calcIncome(self, player, roll):
        playerId = player.getId()
        # first red (commercial buildings, you'll pay for this)
        # also affected by shopping mall bonus
        for cardName, cardData in commercialCards.items():
            if roll in cardData["roll"]:
                basicAmount = cardData["amount"]
                for luckyBastardId in self._getPayOrder():
                    n = self.table.playerHasN(luckyBastardId, cardName)
                    shoppingmallBonus = 1 if self.table.playerHasN(luckyBastardId, cardName) else 0
                    if n > 0:
                        self._tryMoveCash(playerId, luckyBastardId, n * (basicAmount + shoppingmallBonus))

        # then green (you throw your own nr) (green is secondary + multipliers)
        #   regular secondary cards (bakery and convenience store)
        #   also affected by shoppingmall bonus
        for cardName, cardData in secondaryCards.items():
            if roll in cardData["roll"]:
                n = self.table.playerHasN(playerId, cardName)
                shoppingmallBonus = 1 if self.table.playerHasN(playerId, cardName) else 0
                if n > 0:
                    basicAmount = cardData["amount"]
                    self.table.gainCash(playerId, n * (basicAmount + shoppingmallBonus))

        # green bis
        #   multiplier cards (cheese factory, furniture factory and market)
        # not affected by shopping mall bonus
        for cardName, cardData in multiplierCards.items():
            if roll in cardData["roll"] and self.table.playerHasN(playerId, cardName):
                cofactors = cardData["cofactor"]
                n = sum([self.table.playerHasN(playerId, c) for c in cofactors])
                if n > 0:
                    self.table.gainCash(playerId, n * cardData["factor"])

        # then blue (anyone benefits from any throw)
        for cardName, cardData in primaryCards.items():
            if roll in cardData["roll"]:
                for anyPlayerId in self.playerIds:
                    n = self.table.playerHasN(anyPlayerId, cardName)
                    if n > 0:
                        self.table.gainCash(anyPlayerId, n * cardData["amount"])

        #purple not handled here as it needs player input

    def _tryMoveCash(self, sourceId, targetId, amount):
        sourceN = self.table.playerCredit[sourceId]
        targetN = self.table.playerCredit[targetId]
        actualAmount = min(amount, sourceN)
        if actualAmount > 0:
            self.table.transferCash(sourceId, targetId, actualAmount)

    def _getBuildableBuildings(self, playerId):
        # first landmarks not yet built (so the YesToAllPlayer favors landmarks)
        available =  set([b for b in landmarkCards.keys() if self.table.playerHasN(playerId, b) == 0])
        # add all building types available in the bank...
        available.update(self.table.availableBuildings())
        # ... excluding the major building type buildings allready build by player
        available.difference_update([b for b in majorCards.keys() if self.table.playerHasN(playerId, b) > 0])
        # return all these that the player can afford
        cash = self.table.playerCredit(playerId)
        return [b for b in available if cash >= allCards[b]["cost"]]

    def _buyBuilding(self, playerId, building):
        cost = allCards[building]["cost"]
        self.table.looseCash(playerId,cost)
        self.table.build(playerId, building)

class Player:
    def __init__(self, playerId):
        self.playerId = playerId
    def getId(self):
        return self.playerId
    def chooseAction(self, actionRequest):
        raise NotImplementedError()

class YesToAllBot(Player):
    # this is a most dumb bot, but better than the randombot!
    def chooseAction(self, actionRequest):
        debug(actionRequest)
        choice = actionRequest["options"][0]
        debug(choice)
        return choice

class RandomBot(Player):
    # this is the absolute baseline AI
    def chooseAction(self, actionRequest):
        debug(actionRequest)
        choice = random.choice(actionRequest["options"])
        debug(choice)
        return choice

class CafeBot(Player):
    # this bot favours buying cafes for some reason
    def chooseAction(self, actionRequest):
        debug(actionRequest)
        if "cafe" in actionRequest["options"]:
            choice = "cafe"
        else:
            choice = random.choice(actionRequest["options"])
        debug(choice)
        return choice

if __name__ == "__main__":
    random.seed(1)
    players = [YesToAllBot("YesBot"), CafeBot("CafeBot"),
               RandomBot("RandomBot1"), RandomBot("RandomBot2")]
    playerIds = [p.getId() for p in players]
    
    score = {p.getId():0 for p in players}
    for i in range(10):
        game = Game(players)
        game.play()
        score[game.getWinnerId()] += 1
        print "score = " + str(score)
