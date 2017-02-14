from gamemaster import debug
import random
import requests,json

rnd = random.Random()
rnd.seed()

class MachiPlayer:
    def __init__(self, playerId):
        self.playerId = playerId

    def getId(self):
        return self.playerId

    def chooseAction(self, actionRequest):
        raise NotImplementedError()

class YesToAllBot(MachiPlayer):
    # this is a most dumb bot, but better than the randombot!
    def chooseAction(self, actionRequest):
        debug(actionRequest)
        choice = actionRequest["options"][0]
        debug(choice)
        return choice

class RandomBot(MachiPlayer):
    # this is the absolute baseline AI
    def chooseAction(self, actionRequest):
        debug(actionRequest)
        choice = random.choice(actionRequest["options"])
        debug(choice)
        return choice

class CafeBot(MachiPlayer):
    # this bot favours buying cafes for some reason
    def chooseAction(self, actionRequest):
        debug(actionRequest)
        if "cafe" in actionRequest["options"]:
            choice = "cafe"
        else:
            choice = random.choice(actionRequest["options"])
        debug(choice)
        return choice

class HTTPBot(MachiPlayer):
    def __init__(self, playerId, url):
        MachiPlayer.__init__(self, playerId)
        self.url = url

    def chooseAction(self, actionRequest):
        debug(actionRequest)
        response = requests.post(self.url, data = json.dumps(actionRequest))
        choice = response.text
        debug(choice)
        return choice

