import socket
from pprint import pprint
import time
import re
from datetime import datetime, timezone, timedelta

start = datetime.now(timezone.utc)
end = datetime.now(timezone.utc) + timedelta(minutes=1)



CHANNELS = ["brainlighter","votebottest","stpeach","xintani_", "simply"]

def main():

    oauth = "oauth:84251sxafnzsz5ahdw5x121uwl8cif"
    nick_name = "votebotchess"
    channel = CHANNELS[0]
    addr = "irc.chat.twitch.tv"
    port = 6667
    msg_send = False
    sock = socket.socket()

    sock.connect((addr, port))
    send(sock, f"PASS {oauth}")
    send(sock, f"NICK {nick_name}")

    send(sock, f"JOIN #{channel}")

    pprint(recv(sock, 1024))
    while True:
        if not msg_send:
            send(sock,f"PRIVMSG #{channel} Test")
        data = recv(sock, 1024)
        pprint(data)



def parseMsgdata(msg):
    dat = msg.split(":")[2]
    index = dat.index("\r")
    return dat[0:index]

def isMove(msg):
    pattern = "[a-hA-H][1-8][a-hA-H][1-8]"
    if (re.search(pattern, msg)):
        votes.append((re.findall(pattern, msg)[0],datetime.now(timezone.utc)))
    else:
        print("Invalid move")

def send(sock, msg):
    sock.send(bytes(msg + "\n", "ASCII"))

def recv(sock, buff_size):
    return sock.recv(buff_size).decode("UTF-8")
if __name__ == '__main__':
    main()

# for line in readbuffer.split("\r\n"):
#     if line == "":
#         continue
#     if "PING :tmi.twitch.tv" in line:
#         print(line)
#         msgg = "PONG :tmi.twitch.tv\r\n".encode()
#         irc.send(msgg)
#         print(msgg)
#         continue
#GET https://id.twitch.tv/oauth2/authorize
#    ?client_id=<your client ID>
#    &redirect_uri=<your registered redirect URI>
#    &response_type=code
#    &scope=<space-separated list of scopes>
