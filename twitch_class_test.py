
from pprint import pprint
import time
import re
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os




class Twitch:
    def __init__(self, socket, channel):
        self.socket = socket
        self.channel = channel
        self.address = "irc.chat.twitch.tv"
        self.oauth = self.get_twitch_token()
        self.port = 6667
        self.nickname = "votebotchess"

    def run(self):
        # Connect with twitch
        try:
            self.socket.connect((self.address, self.port))
            self.send(self.socket, f"PASS {self.oauth}")
            self.send(self.socket, f"NICK {self.nickname}")
            self.send(self.socket, f"JOIN #{self.channel}")
        #already connected?
        #TODO check if it's the right connection else abort game
        except OSError:
            pass

    def write_twitch_bot_msg(self, msg):
        try:
            self.send(self.socket, f"PRIVMSG #{self.channel} : " + msg)
        except ConnectionAbortedError:
            self.run()
            self.send(self.socket, f"PRIVMSG #{self.channel} : " + msg)

    def get_twitch_token(self):
        # Get Twitch Token
        #TODO oauth2 authorization code to get Token
        #https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-authorization-code-flow

        load_dotenv()
        return os.environ.get("OAUTH")

    def recv(self,socket, buff_size):
        return socket.recv(buff_size).decode("UTF-8")

    def send(self,socket, msg):
        try:
            socket.send(bytes(msg + "\n", "ASCII"))
        except ConnectionAbortedError:
            self.run()
            socket.send(bytes(msg + "\n", "ASCII"))

    def parseMsgdata(self, msg):
        dat = msg.split(":")[2]
        index = dat.index("\r")
        return dat[0:index]

    #TODO Check if valid move combine this method with isMove method
    def get_twitch_chat(self, endtime):

        msgs = []
        while datetime.now(timezone.utc) < endtime:
            try:
                data = self.recv(self.socket, 1024)
            except ConnectionAbortedError:
                self.run()
                data = self.recv(self.socket, 1024)
            try:
                msgs.append(self.parseMsgdata(data))
            except:
                pass

        return self.extractMove(msgs)

    def extractMove(self, msg):
        pattern = "[a-hA-H][1-8][a-hA-H][1-8]"
        moves = []
        for el in msg:
            if re.search(pattern, el):
                moves.append(re.findall(pattern, el)[0].lower())
        return moves



# for line in readbuffer.split("\r\n"):
#     if line == "":
#         continue
#     if "PING :tmi.twitch.tv" in line:
#         print(line)
#         msgg = "PONG :tmi.twitch.tv\r\n".encode()
#         irc.send(msgg)
#         print(msgg)
#         continue

