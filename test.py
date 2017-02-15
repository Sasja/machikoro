#!/usr/bin/env python

import subprocess
import time

import gamemaster
import machiplayers

import json
from jsonschema import validate

validateApi = True

class ApiValidator:
    def __init__(self, bot, apiSchema):
        self.bot = bot
        self.apiSchema = apiSchema
    def getId(self):
	return self.bot.getId()
    def chooseAction(self, actionRequest):
	validate(actionRequest, apiSchema)
        return self.bot.chooseAction(actionRequest)

if __name__ == "__main__":

    botcommand = "bottemplate/pythonmachibot.py"
    print "starting bot {}".format(botcommand)
    popen = subprocess.Popen(
        botcommand,
        env = {"MACHI_IP":"127.0.0.1", "MACHI_PORT":"1234"} )
    print "giving the process a second to get started"
    time.sleep(1)

    players = [
        machiplayers.YesToAllBot("YesBot"),
        machiplayers.CafeBot("CafeBot"),
        machiplayers.RandomBot("RandomBot"),
        machiplayers.HTTPBot("HTTPBot", "http://127.0.0.1:1234")
        ]

    if validateApi:
        with open("docs/api.schema.json","r") as f:
            apiSchema = json.loads(f.read())
        players = [ApiValidator(p, apiSchema) for p in players]

    playerIds = [p.getId() for p in players]
    score = {p.getId():0 for p in players}
    for i in range(3):
        game = gamemaster.Game(players)
        game.play()
        score[game.getWinnerId()] += 1

    print
    print "final score: {}".format(str(score))

    print "killing bot {}".format(botcommand)
    popen.kill()
