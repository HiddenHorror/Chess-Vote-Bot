import chess
import random
import re

# moves = 'e2e3 a7a6 f1e2 a6a5 f2f3 a5a4 h2h3 b7b6 d2d3 d7d5 e2f1 b8c6 b1c3 d5d4 e3d4 c6d4 c3e4 c7c5 d1d2 e7e5 e1d1 f8d6 f3f4 d8h4 g2g3 h4g3 g1e2 c8f5 e2g3 b6b5 f1g2 d6b8 d2f2 a8a7 f2f1 g7g6 b2b3 b8d6 h1g1 a7b7 c2c3 b7b8'
board = chess.Board()
#
#
def update_board(board, move):
    uci_move = chess.Move.from_uci(move)
    board.push(uci_move)
    return board
#
#
# moves_split = moves.split()
# for move in moves.split():
#     board = update_board(board, move)
#
#
def is_valid_move(board, move):
    for moves in board.split():
        board = update_board(board, moves)
        return chess.Move.from_uci(move) in board.legal_moves
#
# print(random.choice(list(board.legal_moves)))
#board.legal_moves.random.choice()

def extractMove(msg):
    pattern = "[a-hA-H]7[a-hA-H]8[qrnb]|[a-hA-H][1-8][a-hA-H][1-8]"
    moves = []
    for el in msg:
        if re.search(pattern, el):
            moves.append(re.findall(pattern, el)[0].lower())
    return moves

msg1 = ["e7e8q"]
print(extractMove(msg1))

# channel = "xintani_"
# a = f"PRIVMSG #{channel} : "
# b = 4
# c = "Geht des {b}"
# d = f"PRIVMSG #{channel} : {c}"
# print(d)

#my_list = [f"test", f"test{b}"]
#tests = [a + x for x in my_list]
#print(tests)

#msg = ["hallo", "a2a4", "b2b4", "totalA1A8"]
#move = extractMove(msg)
#print(move)


#print(chess.Move.from_uci(board.legal_moves) in board.legal_moves)

