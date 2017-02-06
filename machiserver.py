#!/usr/bin/env python
import random
import pprint

def debug(message):
    print message
    pass

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

class Game:
    def __init__(self, players):
        assert len(players) == 4
        self.players = {p.getId():p for p in players}
        assert(len(self.players) == len(set(self.players))) # check for duplicates
        self.gameState = GameState([p.getId() for p in players])

    def play(self):
        while self.gameState.winnerId() == None:
            player = self.players[self.gameState.getCurrentPlayerId()]

            debug(pprint.pformat(self.gameState.data))
            debug("========== starting turn " + str(self.gameState.currentTurnNr) + " ==========")
            debug("-> " + self.gameState.getCurrentPlayerId() + "'s turn")

            roll = self.rollPhase(player)
            self.gameState.calcIncome(roll)

            self.satanPhase(player, roll) #will only do smth on roll == 6
            self.buildPhase(player)

            self.gameState.nextTurn()

    def rollPhase(self, player):
        playerId = player.getId()
        ndice = 1
        if self.gameState.playerOwnsN(playerId, "trainstation") > 0:
            request = {"action":"ndice", "options":["1","2"]}
            choice = player.chooseAction(request)
            if choice == "2":
                ndice = 2
        roll = sum([random.randint(1,6) for i in range(ndice)])
        debug("rolled " + str(roll))
        if self.gameState.playerOwnsN(playerId, "radiotower") > 0:
            request = {"action":"reroll", "lastroll":roll, "options":["y","n"]}
            choice = player.chooseAction(request)
            if choice == "y":
                roll = sum([random.randint(1,6) for i in range(ndice)])
                debug("rerolled " + str(roll))
        return roll

    def satanPhase(self, player, roll):
        if roll == 6:
            playerId = player.getId()
            if self.gameState.playerOwnsN(playerId, "stadium") > 0:
                for dupee in self.gameState.getPayOrder():
                    self.gameState.tryMoveCash(dupee, playerId, 2)

            if self.gameState.playerOwnsN(playerId, "tvstation") > 0:
                orderedOtherIds = self.gameState.getPayOrder()  # same relative order for everyone
                accounts = [(p,self.gameState.data["cash"][p]) for p in orderedOtherIds]
                playersWithCash = [p for p,amount in accounts if amount > 0]
                if playersWithCash:
                    request = {"action":"steal", "options":playersWithCash + [""]}
                    choice = player.chooseAction(request)
                    if choice != "":
                        assert(choice in playersWithCash)
                        self.gameState.tryMoveCash(choice, playerId, 5)

            if self.gameState.playerOwnsN(playerId, "businesscenter") > 0:
                orderedOtherIds = self.gameState.getPayOrder()  # same relative order for everyone
                tradableCards = ( set(allCards.keys())
                                - set(landmarkCards.keys())
                                - set(majorCards.keys())) #TODO rules? no major buildings?
                cities = self.gameState.data["city"]

                # tradewho
                playersWithTradableCards = \
                    [otherPlayerId for otherPlayerId in orderedOtherIds
                                   if tradableCards.intersection(cities[otherPlayerId])]
                if playersWithTradableCards:
                    request = {"action":"tradewho", "options":playersWithTradableCards + [""]}
                    victim = player.chooseAction(request)
                    if victim != "":
                        assert(victim in playersWithTradableCards)
                        # tradewhat
                        tradeWhatOptions = list(tradableCards.intersection(cities[victim]))
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
                                self.gameState.swapBuildings(playerId, given, victim, stolen)

    def buildPhase(self, player):
        playerId = player.getId()
        buildings = self.gameState.getAffordableBuildings(playerId)
        if len(buildings) > 0: 
            request = {"action":"buid", "options":buildings + [""]}
            choice = player.chooseAction(request)
            if choice in buildings:
                self.gameState.build(playerId, choice)

class GameState:
    def __init__(self, playerIds):
        assert len(players) == 4
        assert(len(playerIds) == len(set(playerIds))) # check for duplicates
        self.currentPlayerIndex = 0
        self.currentTurnNr = 0
        self.playerIds = playerIds
        self.data = {}
        # TODO figure out right figures
        self.data["buildingbank"] = {
            "wheatfield"        :6,
            "ranch"             :6,
            "forest"            :6,
            "mine"              :6,
            "appleorchard"      :6,
            "bakery"            :6,
            "conveniencestore"  :6,
            "cheesefactory"     :6,
            "furniturefactory"  :6,
            "market"            :6,
            "cafe"              :6,
            "restaurant"        :6,
            "stadium"           :4,
            "tvstation"         :4,
            "businesscenter"    :4
            }
        self.data["city"] = {}
        self.data["cash"] = {}
        for playerId in playerIds:
            self.data["city"][playerId] = \
                1 * ["wheatfield"] + \
                1 * ["bakery"]
            self.data["cash"][playerId] = 3

    def getCurrentPlayerId(self):
        return self.playerIds[self.currentPlayerIndex]

    def winnerId(self):
        winners = []
        for playerId,city in self.data["city"].items():
            if all([landmark in city for landmark in landmarkCards.keys()]):
                winners.append(playerId)
        assert(len(winners) < 2) # two winners are not possible without having one first
        return None if len(winners) == 0 else winners[0]

    def playerOwnsN(self, playerId, building):
        return self.data["city"][playerId].count(building)

    def getPayOrder(self):
        i = self.currentPlayerIndex
        result = self.playerIds[i+1:] + self.playerIds[:i]
        result.reverse()
        return result

    def calcIncome(self, roll):
        #TODO work out, apply multipliers
        playerId = self.getCurrentPlayerId()
        # first red (commercial buildings, you'll pay for this)
        for cardName, cardData in commercialCards.items():
            if roll in cardData["roll"]:
                for luckyBastardId in self.getPayOrder():
                    n = self.playerOwnsN(luckyBastardId, cardName)
                    if n > 0:
                        self.tryMoveCash(playerId, luckyBastardId, n * cardData["amount"])

        # then green (you throw your own nr) (green is secondary + multipliers)
        # regular secondary cards
        for cardName, cardData in secondaryCards.items():
            if roll in cardData["roll"]:
                n = self.playerOwnsN(playerId, cardName)
                if n > 0:
                    self.playerGainsCash(playerId, n * cardData["amount"])

        # multiplier cards (cheese factory, furniture factory and market)
        for cardName, cardData in multiplierCards.items():
            # these card effects do not stack up with multiples TODO: check rules
            if roll in cardData["roll"] and self.playerOwnsN(playerId, cardName):
                cofactors = cardData["cofactor"]
                n = sum([self.playerOwnsN(playerId, c) for c in cofactors])
                if n > 0:
                    self.playerGainsCash(playerId, n * cardData["factor"])

        # then blue (anyone benefits from any throw)
        for cardName, cardData in primaryCards.items():
            if roll in cardData["roll"]:
                for anyPlayerId in self.playerIds:
                    n = self.playerOwnsN(anyPlayerId, cardName)
                    if n > 0:
                        self.playerGainsCash(anyPlayerId, n * cardData["amount"])

        #purple not handled here as it needs player input

    def tryMoveCash(self, sourceId, targetId, amount):
        sourceN = self.data["cash"][sourceId]
        targetN = self.data["cash"][targetId]
        actualAmount = min(amount, sourceN)
        self.data["cash"][sourceId] = sourceN - actualAmount
        self.data["cash"][targetId] = targetN + actualAmount
        debug(sourceId + " pays " + str(actualAmount) + " to " + targetId)

    def playerGainsCash(self, playerId, amount):
        currentN = self.data["cash"][playerId]
        self.data["cash"][playerId] = currentN + amount
        debug(playerId + " gets " + str(amount) + " from the bank")

    def swapBuildings(self, playerIdA, buildingA, playerIdB, buildingB):
        cityA = self.data["city"][playerIdA]
        cityB = self.data["city"][playerIdB]
        assert(buildingA in cityA and buildingB in cityB)
        cityA.remove(buildingA)
        cityB.remove(buildingB)
        cityA.append(buildingB)
        cityB.append(buildingA)
        debug(playerIdA + " trades its " + buildingA + " with " + playerIdB + "'s " + buildingB)

    def nextTurn(self):
        debug("==========  ending turn " + str(self.currentTurnNr) + "  ==========")
        self.currentTurnNr += 1
        self.currentPlayerIndex = ( self.currentPlayerIndex + 1 ) % len(self.playerIds)

    def getAffordableBuildings(self, playerId):
        result = []
        cash = self.data["cash"][playerId]
        # first landmarks not yet built (so the YesToAllPlayer favors landmarks)
        for cardName,cardData in landmarkCards.items():
            if cash >= cardData["cost"] and not self.playerOwnsN(playerId, cardName) > 0:
                result.append(cardName)
        # now add buildings in the bank
        #TODO should we check against building 2 tvstations and such?
        available = [building for building,n in self.data["buildingbank"].items() if n > 0]
        result += [b for b in available if cash >= allCards[b]["cost"]]

        return result

    def build(self, playerId, building):
        if building in landmarkCards.keys():
            assert(self.playerOwnsN(playerId, building) == 0)
        else:
            nInBank = self.data["buildingbank"][building]
            assert(nInBank > 0)
            self.data["buildingbank"][building] = nInBank - 1
        self.data["city"][playerId].append(building)

        cash = self.data["cash"][playerId]
        cost = allCards[building]["cost"]
        assert(cash >= cost)
        self.data["cash"][playerId] = cash - cost
        debug(playerId + " builds a " + building)

class Player:
    def __init__(self, playerId):
        self.playerId = playerId
    def getId(self):
        return self.playerId
    def chooseAction(self, actionRequest):
        raise NotImplementedError()

class YesToAllBot(Player):
    # this is a most dumb bot
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
    random.seed()
    players = [YesToAllBot("YesBot"), CafeBot("CafeBot"),
               RandomBot("RandomBot1"), RandomBot("RandomBot2")]
    
    score = {p.getId():0 for p in players}
    for i in range(1):
        game = Game(players)
        game.play()
        winnerId = game.gameState.winnerId()
        print winnerId + " wins!"
        score[winnerId] += 1

    print score
