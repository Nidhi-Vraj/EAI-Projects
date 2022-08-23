# Simple quintris program! v0.2
# D. Crandall, Sept 2021


import copy
import math
import pprint
from itertools import groupby

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time
import sys


class HumanPlayer:
    def get_moves(self, quintris):
        print(
            "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while True:
            c = get_char_keyboard()
            commands = {
                "b": quintris.left,
                "h": quintris.hflip,
                "n": quintris.rotate,
                "m": quintris.right,
                " ": quintris.down}
            commands[c]()


#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#

class EvalSuccessor:

    def __init__(self, board, base_touch, piece=""):
        self.board = board
        self.piece = piece
        self.base_touch = base_touch

        self.eval_score = self.get_heuristic()

    # calculates the current height of the board
    def height(self):
        c = 0
        for col in (self.board):
            if "x" in col:
                c = c + 1
        return c

    # calculates number of holes in the board

    def holes(self):
        c = 0
        for col in self.board:
            for id, col1 in enumerate(col):
                if (col1 == "x"):
                    c = c + abs((25 - id - (col.count("x"))))
                    break
        return c

    # calculates number of lines cleared after placing the piece

    def get_cleared_lines(self, x):
        self.count_clear_rows = 0
        for i in self.board:
            # CHECK X
            # IF ALL X THEN COUNT INC
            if all([True if "x" in i else False]):
                self.count_clear_rows += 1
            else:
                self.count_clear_rows -= 1

        return self.count_clear_rows

    # Reward if a piece touches the base of the board
    def touch_the_base(self):
        return self.board[-1].count('x')

        # return touch_the_base_list

    # Reward if a piece touches edges of the board
    def touch_the_edge(self):
        col_board = list(zip(self.make_str_to_list(self.board)))
        return  col_board[0].count('x') + col_board[-1].count('x')

    def filled_rows(self):
        c1 = []
        for col in self.board:
            c = c + col.count("x")
            c1.append(c)
        return max(c1)

    # Caluculate empty columns left in the board

    def pits(self):
        c = 0
        for col in self.board:
            if (col[0].count(" ") == len(self.board)):
                c = c + col.count(" ")
        return (c)

    # Get absolute difference between heights of columns in the board

    def bumpiness(self):
        c = 0
        for id, col in enumerate(self.board):
            if (id < len(self.board) - 1):
                c = c + \
                    (abs(self.board[id][0].count("x") - self.board[id + 1][0].count("x")))
        return (c)

    def make_str_to_list(self, str_list):
        board_fin = []
        for i in str_list:
            board = []
            for j in i:
                board.append(j)
            board_fin.append(board)
        return board_fin

    def rows_fill_percentage(self):
        x = 0
        c = 0
        for i in self.make_str_to_list(self.board):
            x = x + (i.count(x) * len(self.board) - c)
            c += 1
        return x / 25

    # get heuristic values for the current move
    def get_heuristic(self):
        
        h = 0
        h-= 3*(float(self.height()))
        h+= 10*(float(self.get_cleared_lines(self.board)))
        h-= 3*(float(self.holes()))
        h-= 3*(float(self.pits()))
        h-= 100*(float(self.bumpiness()))
        # h+= 200*(self.rows_fill_percentage())
        h+= 200*(self.touch_the_base())
        h+= 100*(self.touch_the_edge())
        return h

class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def __init__(self):
        self.piece_successors = []
        self.started = False

    def find_dups(self, each_possible_moves, some_rt):
        for move, state in each_possible_moves.items():
            if state == some_rt:
                return (True, len(move))
        return (False, None)

    def make_piece_successors(self,piece):
        # take current piece
        # find all rotations
        # find all flips
        # append to piece_successor_dict
        # for i in self.quintris.PIECES:
        i = piece
        each_possible = {}
        move = ""
        rt = i
        hrt = QuintrisGame.hflip_piece(i)
        each_possible.update({move: rt})
        is_in_dict, len_of_move = self.find_dups(each_possible, hrt)

        if is_in_dict:
            if len_of_move > len(move):
                each_possible.update({move + "h": hrt})
        else:
            each_possible.update({move + "h": hrt})
        for angle in [90, 180, 270]:
            move = move + "n"
            rt = QuintrisGame.rotate_piece(i, angle)
            hrt = QuintrisGame.hflip_piece(rt)

            is_in_dict, len_of_move = self.find_dups(each_possible, rt)

            if is_in_dict:
                if len_of_move > len(move):
                    each_possible.update({move: rt})
            else:
                each_possible.update({move: rt})

            is_in_dict, len_of_move = self.find_dups(each_possible, hrt)

            if is_in_dict:
                if len_of_move > len(move):
                    each_possible.update({move + "h": hrt})
            else:
                each_possible.update({move + "h": hrt})

        return each_possible

    # max -> successors and evalutaion for every successor
    # chance -> h
    # min
    # chance
    # max

    #
    def get_positions(self, board):
        board_cols = zip(*board)
        index_of_cols_list = []
        col_num = 0
        for col in board_cols:
            col_as_list = list(col)
            if 'x' in col_as_list:
                x_index = col_as_list.index('x')
                index_of_cols_list.append((col_num, x_index))

            else:
                index_of_cols_list.append((col_num, 25))
            col_num += 1
        return index_of_cols_list

    def board_successors(self, board, score, piece_all):
        #  this too shall pass

        piece, drop_row, drop_col = piece_all[0],piece_all[1],piece_all[2]
        board_successors_dict = {}

        positions = self.get_positions(self.make_str_to_list(board))
        temp_board = board

        # for orig_piece,each_possible in self.piece_successors:
        all_rots = self.make_piece_successors(piece)
        for move, piece_flip_or_rot in all_rots.items():
            current_row, current_col = len(piece_flip_or_rot), len(
                max(piece_flip_or_rot, key=len))

            for elem in positions:
                if not QuintrisGame.check_collision(
                        temp_board, 0, piece_flip_or_rot, elem[1] - current_row, elem[0]):

                    new_board, score = self.quintris.place_piece(
                        temp_board, score, piece_flip_or_rot, elem[1] - current_row, elem[0])
                    # base_touch_score = new_board[0][-1].count("x")- self.quintris.get_board()[-1].count("x")
                    base_touch_score = 0
                    if elem[0] < drop_col:
                        board_successors_dict.update(
                            {move + "b" * (drop_col - elem[0]): EvalSuccessor(new_board, piece, base_touch_score)})
                    elif elem[0] > drop_col:
                        board_successors_dict.update(
                            {move + "m" * (elem[0] - drop_col): EvalSuccessor(new_board, piece, base_touch_score)})
                    elif elem[0] == drop_col:
                        board_successors_dict.update(
                            {move: EvalSuccessor(new_board, piece, base_touch_score)})
        return board_successors_dict

    def make_str_to_list(self, str_list):
        board_fin = []
        for i in str_list:

            board = []
            for j in i:
                board.append(j)
            board_fin.append(board)
        return board_fin
    
    def get_moves(self, quintris):

        self.quintris = quintris
        succ = self.board_successors(
            self.quintris.get_board(),
            self.quintris.state[1],self.quintris.get_piece())

        move_score = -math.inf
        move = ""
        next_board  = ""

        next = {}
        for i in succ:
            move = i
            move_score = succ[i].eval_score
            next_board= succ[i].board

            x = self.board_successors(next_board,0,(self.quintris.next_piece,0,0))
            for j  in x:
                move_2 = j
                move_score_2 = x[j].eval_score
                next.update({(move,move_2):move_score+move_score_2})
        next = {k: v for k, v in sorted(next.items(), reverse=True,key=lambda item: item[1])}
        # pprint.pprint(next)
        # print(max(list(next.values())))
        # super simple current algorithm: just randomly move left, right, and
        # rotate a few times
        return list(next.keys())[0][0]

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
            # another super simple algorithm: just move piece to the least-full
            # column
            while True:
                time.sleep(0.1)

                board = quintris.get_board()
                piece = quintris.get_piece()
                # column_heights = [min([r for r in range(len(board) -
                #                                         1, 0, -
                #                                         1) if board[r][c] == "x"] +
                #                       [100, ]) for c in range(0, len(board[0]))]
                # index = column_heights.index(max(column_heights))
                moves = player.get_moves(quintris)
                for c in moves:
                    if c == 'b':
                        quintris.left()
                    elif c == 'm':
                        quintris.right()
                    elif c == 'n':
                        quintris.rotate()
                quintris.down()


###################
# main program
(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)
