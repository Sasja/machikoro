#!/usr/bin/env python

import subprocess
import time

import gamemaster
import machiplayers

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

    playerIds = [p.getId() for p in players]
    score = {p.getId():0 for p in players}
    for i in range(20):
        game = gamemaster.Game(players)
        game.play()
        score[game.getWinnerId()] += 1

    print
    print "final score: {}".format(str(score))

    print "killing bot {}".format(botcommand)
    popen.kill()
