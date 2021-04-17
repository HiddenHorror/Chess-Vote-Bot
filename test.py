import threading

from dotenv import load_dotenv
import os
import berserk
import socket
from model1 import Game
from twitch_class_test import Twitch


def is_white_to_move(game, moves):
    return len(moves) % 2 == (0 if game.white_starts else 1)


def is_engine_move(game, moves):
    return game.is_white == is_white_to_move(game, moves)

#Get API Token from .env file
BASE_URL = "https://lichess.org"
load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")


#start session
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)
game_id = 'QTxXIumt'
test = berserk.clients.Board(session, BASE_URL)
client_games = berserk.clients.Games(session,BASE_URL)
test2 = berserk.clients
#print(client_games.export(game_id)["lastMoveAt"])
#Twitch
sock = socket.socket()
twitch = Twitch(sock,"brainlighter")
twitch.run()
#game = Game(client, twitch, client_games,game_id)

#game.start()


#Twitch connection










# def is_white(game):
#     return game.botname == game.current_state["white"]["name"]
#
# def my_turn(game):
#     return len(game["moves"]) % 2 == (0 if is_white(game) else 1)

#print(client.bots.stream_game_state(game_id))
#print(is_white(game))

#print("current state is" + str(game.current_state))
#print(game.current_state["white"])


#QTxXIumt
#game = model.Game(initial_state, user_profile["username"], li.baseUrl, config.get("abort_time", 20))

#elif u_type == "gameState":
#game.state = upd
#moves = upd["moves"].split()






#client.bots.post_message(game_id, 'Prepare to loose')
client.bots.make_move(game_id, 'd1h5')