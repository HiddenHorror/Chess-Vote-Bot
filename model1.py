import threading
from datetime import datetime, timezone, timedelta
import chess
import random
import re
from twitch_class_test import Twitch
import time
import berserk

EXTRATIME = 0* 1000 #Need to get rid of. dynamic time management
STANDARD = 30*1000 #Milliseconds to make a move if no increment defined
votes = []



class Game(threading.Thread):
    def __init__(self, client, twitch, client_games,game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.twitch = twitch
        self.client_games = client_games
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
        self.bot_name = client.account.get()["username"]
        self.is_white = self.bot_name == self.current_state["white"]["name"]
        self.time_last_move = client_games.export(game_id)["lastMoveAt"]

    def run(self):
        self.twitch.run()
        #For first time runnning we have to call the method because no gamestate is fired
        moves = self.current_state["state"]["moves"]
        if self.is_my_turn(moves):
            self.make_bot_move(moves)

        for event in self.stream:
            #TODO Game-Ending scenarios draw, lose, win
            if event["type"] == "gameState" and event["status"] == "started": #Sent when a move is played a draw is offered or the game end
                print("gameState")
                moves = event["moves"]
                if self.is_my_turn(moves):
                    self.make_bot_move(moves)
            elif event["type"] == "gameState" and event["status"] == "mate":
                if self.is_my_turn(moves):
                    self.twitch.write_twitch_bot_msg("You lost. Try harder next time ;-)")
                else:
                    self.twitch.write_twitch_bot_msg(f"Congratulations {self.twitch.channel}! You won.")
                    time.sleep(5)
            elif event["type"] == "gameState" and event["status"] == "resign":
                self.twitch.write_twitch_bot_msg("You resigned?")
            elif event["type"] == "gameState" and event["status"] == "aborted":
                self.twitch.write_twitch_bot_msg("You aborted the game?")
            elif event["type"] == "gameState" and event["status"] == "outoftime":
                if not self.is_my_turn(event["moves"]):
                    self.twitch.write_twitch_bot_msg("You ran out of time...?")
            #TODO status if time runs out?

            #
            #elif event["type"] == "chatLine" and event["username"] == self.client.account.get()["username"]:
                #self.handle_chat_line(event)


    def write_bot_msg(self, msg):
        self.client.bots.post_message(self.game_id, msg)


    # def handle_chat_line(self, chat_line):
    #     if chat_line["username"] != self.client.account.get()["username"]:
    #         votes.append((chat_line["text"], datetime.now(timezone.utc)))

    def update_board(self,board, move):
        uci_move = chess.Move.from_uci(move)
        board.push(uci_move)
        return board

    def isMove(self, msg):
        pattern = "[a-hA-H][1-8][a-hA-H][1-8]"
        if re.search(pattern, msg):
            votes.append((re.findall(pattern, msg)[0], datetime.now(timezone.utc)))
        else:
            print("Invalid move")

    def get_valid_votes(self,board,end_time):
        votes_in_time = self.twitch.get_twitch_chat(end_time)
        #votes_in_time = self.filter_tuples(votes,list(filter(lambda x: start_time <= x <= end_time, (y[1] for y in votes))))
        # TODO Define filter which checks for valid moves
        valid_moves = list(filter(lambda x: self.is_valid_move(board, x), (y for y in votes_in_time)))
        if valid_moves:
            print("valid moves = " + str(valid_moves))
        return valid_moves
        #self.filter_tuples(votes_in_time,valid_moves)

    def filter_tuples(self,lst_tup,lst):
        return [tup for tup in lst_tup if any(i in tup for i in lst)]

    def get_max_votes(self,votes):
        return max(votes, key=votes.count)

    def times_up(self):
        self.write_bot_msg("Time is up.")
#TODO Determine Vote Time depending on increment and current clock situation
    def get_vote_time(self):
        try:
            increment_time = self.current_state["clock"]["increment"]
        except TypeError:
            increment_time = STANDARD
        if increment_time == 0:
            return timedelta(milliseconds=self.current_state["clock"]["initial"]/50)
        else:
            return timedelta(milliseconds=increment_time + EXTRATIME)

#TODO is_valid_move
    def is_valid_move(self, board, move):
        board1 = chess.Board()
        for moves in board.split():
            board1 = self.update_board(board1, moves)
        return chess.Move.from_uci(move) in board1.legal_moves

    def is_my_turn(self, moves):
        # For the first move only check if we are white
        if len(moves) == 0:
            return self.is_white
        else:
            #because stream hasnt updated last move it is the other way as you'd expect
            return len(moves) % 2 == (1 if self.is_white else 0)


    def is_engine_move(self,game, moves):
        return game.is_white == self.is_white_to_move(game, moves)

    def is_white_to_move(self,game, moves):
        return len(moves) % 2 == (0 if game.white_starts else 1)
    def make_bot_move(self, moves):
        # self.write_bot_msg("Vote for my next turn!")
        vote_time_start = datetime.now(timezone.utc)
        vote_time_end = vote_time_start + self.get_vote_time()
        vote_time = (vote_time_end - vote_time_start).seconds
        # TODO Verhindern, dass Bot disonnected Funktioniert das wirklich so?
        self.twitch.send(self.twitch.socket, "PONG :tmi.twitch.tv")
        self.twitch.write_twitch_bot_msg(f"Vote for my next turn! You have {vote_time} seconds.")
        try:
            valid_votes = self.get_valid_votes(moves, vote_time_end)
            max_vote = self.get_max_votes(valid_votes)
        except ValueError:
            # make random move if no votes?
            board = chess.Board()
            for move in moves.split():
                board = self.update_board(board, move)
            max_vote = random.choice(list(board.legal_moves))
        try:
            print(max_vote)
            self.client.bots.make_move(self.game_id, max_vote)
        except berserk.exceptions.ResponseError:
            self.twitch.write_twitch_bot_msg(" Something went wrong. You resigned or I ran out of time. Cannot make a move.")
