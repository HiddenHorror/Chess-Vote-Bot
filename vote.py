#Test Api from https://python-lichess.readthedocs.io/en/latest/api.html
#Python chess https://github.com/niklasf/python-chess
#Beserk https://github.com/rhgrant10/berserk
#import threading
from model1 import Game
from dotenv import load_dotenv
import os
import berserk
import socket
from twitch_class_test import Twitch


#Get API Token from .env file
load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")
BASE_URL = "https://lichess.org"
#TODO extract Valid User-IDs to sperate files txt

VALID_LICHESS_USERS = []
VALID_TWITCH_USERS = []

with open("User_IDs.txt", "r") as f:
    next(f)
    for line in f:
        VALID_LICHESS_USERS.append(line.split(",")[0].strip())
        VALID_TWITCH_USERS.append(line.split(",")[1].strip())
    f.close()


#VALID_USERS = list(zip(VALID_LICHESS_USERS, VALID_TWITCH_USERS))

#start session
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)
client_games = berserk.clients.Games(session,BASE_URL)
#base_client = berserk.clients.BaseClient(session)
#Required for authorization with oauth2 to abort or resign games
#board = berserk.clients.Board(session, BASE_URL)


def get_twitch_user_id(lichess_name):
    if lichess_name in VALID_LICHESS_USERS:
        index = VALID_LICHESS_USERS.index(lichess_name)
        return VALID_TWITCH_USERS[index]
    else:
        return ''


def get_lichess_user_id(event):
    if client.account.get()["username"] == client_games.export(event["game"]["id"])["players"]["white"]["user"]["name"]:
        return client_games.export(event["game"]["id"])["players"]["black"]["user"]["name"]
    else:
        return client_games.export(event["game"]["id"])["players"]["white"]["user"]["name"]


def is_valid_user(user):
    return user != ''

#Accept Challenges
#TODO Check if its a Problem if more than one challenge
for event in client.bots.stream_incoming_events():
    #TODO Accept every challenge abort game after start if user-ids are not defined. Therefore oauth2 authorization is required
    if event['type'] == "challenge" and event["challenge"]["challenger"]["name"] in VALID_LICHESS_USERS:
        client.bots.accept_challenge(event['challenge']['id'])
    elif event['type'] == 'challenge' and event["challenge"]["challenger"]["name"] not in VALID_LICHESS_USERS:
        client.bots.decline_challenge(event['challenge']['id'])

    elif event['type'] == "gameStart":
        game_id = event['game']['id']
        sock = socket.socket()
        twitch_user_id = get_twitch_user_id(get_lichess_user_id(event))
        print(twitch_user_id)
        twitch = Twitch(sock, twitch_user_id)
        client.bots.post_message(game_id, f"Hi there {get_lichess_user_id(event)}.\n Good luck!")
        #TODO authorization with oauth2 to be able to abort or resign games
        #berserk.clients.Board.abort_game(board,game_id)
        game = Game(client, twitch, client_games, game_id)
        print(game.game_id)
        game.start()




