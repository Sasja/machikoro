from gamemaster import debug
import random
import socket
import requests,json

# todo handle errors and timeouts

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

class TCPBot(MachiPlayer):
    def __init__(self, playerId, host, port):
        MachiPlayer.__init__(self, playerId)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
    def __del__(self):
        self.sock.close()
    def _mysend(self, msg):
        assert("\n" not in msg)
        msg += "\n"
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
    def _myreceive(self):
        buff = ""
        while True:
            char = self.sock.recv(1)
            if char == '':
                raise RuntimeError("socket connection broken")
            elif char == "\n":
                break
            else:
                buff += char
        return buff
    def chooseAction(self, actionRequest):
        debug(json.dumps(actionRequest))
        self._mysend(json.dumps(actionRequest))
        response = self._myreceive()
        return response
    
