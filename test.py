#!/usr/bin/env python

import subprocess
import time

import gamemaster
import machiplayers

import botherder

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
    print "deploying 4 docker containers for contestants"
    ports = [2001,2002,2003,2004]
    containers = [botherder.ContainedAi(port) for port in ports]
    for c in containers:
        c.deploy()
    try:

        print "giving the containers a second to get started"
        time.sleep(10)
        players = [machiplayers.HTTPBot(
                        "bot_{}".format(str(p)),
                        "http://127.0.0.1:{}".format(str(p))
                    ) for p in ports ]

        if validateApi:
            with open("docs/api.schema.json","r") as f:
                apiSchema = json.loads(f.read())
            players = [ApiValidator(p, apiSchema) for p in players]

        playerIds = [p.getId() for p in players]
        score = {p.getId():0 for p in players}

        for i in range(5):
            game = gamemaster.Game(players)
            game.play()
            score[game.getWinnerId()] += 1

        print
        print "final score: {}".format(str(score))

    finally:
        print "destroying containers"
        for c in containers:
            c.destroy()
