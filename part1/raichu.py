#
# raichu.py : Play the game of Raichu
#
# UserIds- adisoni-nsadhuva-svaddi, Names- Aditi Soni, Nidhi Sadhuvala, Sriniavas Vaddi
#
# Based on skeleton code by D. Crandall, Oct 2021

import string
import sys
import heapq as hq
import time
from datetime import datetime


class Position:
    def __init__(self, n, occupied_by, row, col, was_jumped_on="", weight=0):
        self.row = row
        self.col = col
        self.index = n
        self.occupied_by = occupied_by
        self.score = 0
        self.was_jumped_on = was_jumped_on

    def __str__(self):
        return "Postion {} {} occupied by {} - at index {}".format(
            self.row, self.col, self.occupied_by, self.index)

    def __hash__(self):
        return hash("{}-{}-{}".format(self.row, self.col, self.occupied_by))

    def __eq__(self, other):
        if self.row == other.row and self.col == other.col:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other


class Position_Taker:

    def __str__(self):
        return self.alphabet

    def __init__(self, alphabet, row, col, n, index, board):
        """

        :param alphabet:
        :param row:
        :param col:
        :param n:
        :param index:
        :param board:
        """

        self.definite_moves = []
        self.index = index
        self.board = board
        self.row = row
        self.col = col
        self.n = n

        # For each pokemon:
        # Getting its 1- name, 2- weight, 3- max-steps that it can take considering normal moves and when it can jump over an opponent piece,
        # 4- pokemons that it can jump over, 5- if it can evolve into a Raichu and 6-all possible successor moves whether there is a jumpover pieve in the way or not

        self.pokemons = {".": {"name": "Empty"},
                         "w": {"name": "White Pichu",
                               "weight": 3,
                               "max_steps": 1,
                               "jump-over": "b",
                               "evolve": "@",
                               "possible_moves": [(+1, -1), (+2, -2), (+1, +1), (+2, +2)],
                               },
                         "W": {"name": "White Pikachu",
                               "max_steps": 2,
                               "weight": 5,
                               "jump-over": "b,B",
                               "evolve": "@",
                               "possible_moves": [(0, +1), (0, +2), (0, +3), (0, -1), (0, -2), (0, -3), (1, 0), (2, 0),
                                                  (3, 0)],
                               },
                         "b": {"name": "Black Pichu",
                               "max_steps": 1,
                               "jump-over": "w",
                               "weight": 3,
                               "evolve": "$",
                               "possible_moves": [(-1, -1), (-2, -2), (-1, +1), (-2, +2)]},
                         "B": {"name": "Black Pikachu",
                               "max_steps": 2,
                               "weight": 5,
                               "jump-over": "w,W",
                               "evolve": "$",
                               "possible_moves": [(0, +1), (0, +2), (0, +3), (0, -1), (0, -2), (0, -3), (-1, 0),
                                                  (-2, 0), (-3, 0)]},
                         "@": {"name": "White Raichu",
                               "max_steps": n - 1,
                               "weight": 9,
                               "jump-over": "b,B,$",
                               "possible_moves": []},
                         "$": {"name": "Black Raichu",
                               "max_steps": n - 1,
                               "weight": 9,
                               "jump-over": "w,W,@",
                               "possible_moves": []},
                         }
        self.alphabet = alphabet

        if self.alphabet != ".":

            self.can_jump = False
            self.name = self.pokemons[alphabet]
            self.cannot_jump = False
            self.is_white = False
            self.pieces_on_my_way = 0
            self.max_steps = self.pokemons[self.alphabet]["max_steps"]

            if self.alphabet in "@$":
                self.pokemons[self.alphabet]["possible_moves"] = self.raichu_moves()
            else:
                self.make_definite_moves()

    def __hash__(self):
        return hash("{}-{}-{}".format(self.row, self.col, self.alphabet))

    # pokemon jumps to capture its opponent possible jump over pieces
    # Using jumpover - pichus can jumpover oppoenent's pichus, pikachus can jump over opponent's pichus and pikachus and raichus can jump over opponent's pichu, pikachus and raichus
    def check_raichu_jump(self, possible_moves, can_jump=False, was_jumped_on=""):
        data_pokemon = self.pokemons[self.alphabet]
        for r, c in possible_moves:
            move = self.get_pos_for_rc(r, c, self.n, self.board)
            if move.occupied_by == "." and can_jump:
                move.was_jumped_on = was_jumped_on
                self.definite_moves.append(move)
            elif move.occupied_by == "." and not can_jump:
                self.definite_moves.append(move)
            else:
                if move.occupied_by in data_pokemon["jump-over"] and (
                        not can_jump):
                    was_jumped_on = move
                    can_jump = True
                else:
                    break

    def __eq__(self, other):
        if self.row == other.row and self.col == other.col and self.alphabet == other.alphabet:
            return True
        else:
            return False

    # check if pieces not going out of bounds
    def check_bound(self, row, col, N):
        if (row < N and row >= 0) and (col < N and col >= 0):
            return True
        else:
            return False

    # check successors for Raichu
    def raichu_moves(self):

        possible_moves = []

        # check raichu move down the row
        for i in range(self.row + 1, self.n):
            possible_moves.append((i, self.col))
        self.check_raichu_jump(possible_moves)

        # check raichu moves up the row
        possible_moves = []
        for i in range(self.row - 1, -1, -1):
            possible_moves.append((i, self.col))
        self.check_raichu_jump(possible_moves)

        # check raichu moves on right columns
        possible_moves = []
        for i in range(self.col + 1, self.n):
            possible_moves.append((self.row, i))
        self.check_raichu_jump(possible_moves)

        # check raichu moves on left columns
        possible_moves = []
        for i in range(self.col - 1, -1, -1):
            possible_moves.append((self.row, i))
        self.check_raichu_jump(possible_moves)

        # check raichu moves for antidiagonal upwards
        possible_moves = []
        i = self.row
        j = self.col
        while i > 0 and j > 0:
            possible_moves.append((i - 1, j - 1))
            i -= 1
            j -= 1
        self.check_raichu_jump(possible_moves)

        # check raichu moves for antidiagonal downwards
        possible_moves = []
        i = self.row
        j = self.col
        while i < self.n - 1 and j < self.n - 1:
            possible_moves.append((i + 1, j + 1))
            i += 1
            j += 1
        self.check_raichu_jump(possible_moves)

        # check raichu moves for diagonal upwards
        possible_moves = []
        i = self.row
        j = self.col
        while i > 0 and j < self.n - 1:
            possible_moves.append((i - 1, j + 1))
            i -= 1
            j += 1
        self.check_raichu_jump(possible_moves)

        # check raichu for diagonals downwards
        possible_moves = []
        i = self.row
        j = self.col
        while (i > 0 and i < self.n - 1) and (j < self.n - 1 and j > 0):
            possible_moves.append((i + 1, j - 1))
            i += 1
            j -= 1
        self.check_raichu_jump(possible_moves)

    # if not out of bounds
    # if has empty spaces till max_steps
    # if yes, append it to possible moves
    # and skip the max_step+1 and continue to another direction
    # if has a piece in between
    # can this be jumped_over
    # if yes, append it to possible moves
    # if has more than one pieces

    def get_pos_for_rc(self, r, c, n, board):
        return Position(r * n + c, board[r * n + c], r, c)

    def make_definite_moves(self):

        data_pokemon = self.pokemons[self.alphabet]
        upper_bound = self.n - \
                      1 if self.alphabet in "@$" else data_pokemon["max_steps"] + 1

        for i in range(0, len(data_pokemon["possible_moves"]), upper_bound):
            can_jump = False
            was_jumped_on = ""
            max_steps = data_pokemon["max_steps"]
            counter = 0
            while counter < max_steps:
                try:
                    r, c = data_pokemon["possible_moves"][counter + i]
                    if self.check_bound(self.row + r, self.col + c, self.n):
                        move = self.get_pos_for_rc(
                            self.row + r, self.col + c, self.n, self.board)
                        if move.occupied_by == "." and can_jump:
                            move.was_jumped_on = was_jumped_on
                            self.definite_moves.append(move)
                        elif move.occupied_by == "." and not can_jump:
                            self.definite_moves.append(move)
                        else:
                            if move.occupied_by in data_pokemon["jump-over"] and (
                                    not can_jump):
                                was_jumped_on = move
                                can_jump = True
                                if self.alphabet not in "@$":
                                    max_steps += 1
                            else:
                                break
                    counter += 1
                except BaseException:
                    # print("Going out of bounds")
                    counter += 1

    # evolve pokemons - only for Pichu and Pikachu
    def evolve(self):
        return self.pokemons[self.alphabet]["evolve"]


class Board:

    def __init__(self, board, N, player):

        # {Position : Position_Taker}
        self.board_positions = []
        self.board = board
        self.board_positions_dumb = {}
        self.player = player
        self.pieces = {"w": "wW@", "b": "bB$"}
        self.diff_top = 0
        self.n = N
        for i in range(0, len(board)):
            self.board_positions.append(
                Position_Taker(
                    board[i], i // N, i %
                              N, N, i, self.board))
        for x in range(len(self.board_positions)):
            i = self.board_positions[x]
            if (i.row == 0 or i.row == i.n - 1) and i.alphabet in "wWbB":
                self.board_positions[x] = self.evolve(i)
                self.board = "".join([j.alphabet for j in self.board_positions])
        self.white_pieces = []
        self.black_pieces = []
        for j in self.board_positions:
            if j.alphabet in "wW@":
                self.white_pieces.append(j)
            elif j.alphabet in "bB$":
                self.black_pieces.append(j)
            else:
                continue
        self.terminal_state = False

        if len(self.white_pieces) == 0 or len(self.black_pieces) == 0:
            self.terminal_state = True

    def __str__(self):
        return self.board

    def __lt__(self, other):
        return self.evaluation() < other.evaluation()

    def __gt__(self, other):
        return self.evaluation() > other.evaluation()

    def __le__(self, other):
        return self.evaluation() <= other.evaluation()

    def __ge__(self, other):
        return self.evaluation() >= other.evaluation()

    def __eq__(self, other):
        return True if self.evaluation() == other.evaluation() else False

    def move(self, p: Position_Taker):
        pass

    def evolve(self, p: Position_Taker):
        if p.index // p.n == p.n - 1 and p.alphabet in "wW":
            p = Position_Taker(p.evolve(), p.row, p.col, p.n, p.index, p.board)
        if p.index // p.n == 0 and p.alphabet in "bB":
            p = Position_Taker(p.evolve(), p.row, p.col, p.n, p.index, p.board)
        return p

    # Evaluation function - uses heuristic to decide on successor moves
    def evaluation(self):

        c = 0

        for i in self.board_positions:
            if i.definite_moves == [] and i.alphabet in self.pieces[self.player]:
                c += 1

        wc = {}
        bc = {}
        white_cumulative_height = 0
        black_cumulative_height = 0

        for i in self.board_positions:
            if i.alphabet in "wW@":
                white_cumulative_height += i.col
            elif i.alphabet in "bB$":
                black_cumulative_height += i.col

        for i in "wW@":
            wc.update({i: self.board.count(i)})
        for i in "bB$":
            bc.update({i: self.board.count(i)})
        cost = 10 * (wc["w"] - bc["b"]) + 15 * \
               (wc["W"] - bc["B"]) + 50 * (wc["@"] - bc["$"])
        if self.player == "w":
            return cost + white_cumulative_height  # - (self.diff_top)
        else:
            return (-1 * (cost - black_cumulative_height))  # - (self.diff_top)


def new_boards(b: Board, N, player):
    new_boards_array = []
    for i in b.board_positions:
        if i.alphabet in b.pieces[player]:
            # print(b)
            for j in i.definite_moves:
                new_dumb_board = list(b.board)
                new_dumb_board[i.index], new_dumb_board[j.index] = new_dumb_board[j.index], new_dumb_board[i.index]

                # print("New board after moving {}  from {} to  {} which has {}".format(board[i.index],i.index,j.index,board[j.index]))
                # print(board_to_string("".join(new_dumb_board),N))
                try:
                    new_dumb_board[j.was_jumped_on.index] = "."

                except Exception as e:
                    c = 0
                finally:
                    b_n = Board("".join(new_dumb_board), N, player)
                    if player == "w" and i.alphabet in "wW":
                        # b_n.diff_top = i.row - b_n.n
                        b_n.diff_top = (b_n.n - i.row) * 5
                    elif player == "b" and i.alphabet in "bB":
                        b_n.diff_top = (i.row) * 5
                    new_boards_array.append(b_n)
                    # print("**********************************************************************")
                    # print(b_n)
                    # print("**********************************************************************")

    return new_boards_array


# Implement Minmax with Alpha Beta pruning

# get minimumum value among all successors
# Beta value acts as bound for MIN nodes

def minvalue(successor: Board, alpha_val, beta_val, depth_level, player, depth_limit, N, timelimit):
    depth_level += 1
    if depth_level == depth_limit or successor.terminal_state:
        return successor.evaluation()
    else:
        if (player == "w"):
            oppositeplayer = "b"
        else:
            oppositeplayer = "w"
        maxsuccessors = new_boards(successor, N, oppositeplayer)
        for maxsucc in maxsuccessors:
            beta_val = min(
                beta_val,
                maxvalue(
                    maxsucc,
                    alpha_val,
                    beta_val,
                    depth_level,
                    player,
                    depth_limit,
                    N, timelimit))
            if alpha_val >= beta_val:
                return beta_val
        return beta_val


# get maximum values among all successors
# Alpha value acts as bound for MAX nodes

def maxvalue(successor, alpha_val, beta_val, depth_level, player, depth_limit, N, timelimit):
    depth_level += 1
    if depth_level == depth_limit or successor.terminal_state:
        return successor.evaluation()
    else:
        minsuccessors = new_boards(successor, N, player)
        for minsucc in minsuccessors:
            alpha_val = max(
                alpha_val,
                minvalue(
                    minsucc,
                    alpha_val,
                    beta_val,
                    depth_level,
                    player,
                    depth_limit,
                    N, timelimit))
            if alpha_val >= beta_val:
                return alpha_val
        return alpha_val


# get min-max decision - action leading to state of successor that maximizes the MIN values
def min_max(board, player, N, depth_level, timelimit):
    succ = new_boards(board, N, player)
    if succ == []:
        sys.exit(0)
    max_heap_beta = []
    defaultBetaValue = 100000000
    defaultAlphaValue = -10000000
    for minsucc in succ:
        hq.heappush(
            max_heap_beta,
            (minvalue(
                minsucc,
                defaultAlphaValue,
                defaultBetaValue,
                0,
                player,
                depth_level,
                N, timelimit) * -1,
             minsucc))
    # print(hq.heappop(max_heap_beta)[1].evaluation())
    return hq.heappop(max_heap_beta)[1]


def board_to_string(board, N):
    return "\n".join(board[i:i + N] for i in range(0, len(board), N))


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    depth_level = 1
    board = Board(board, N, player)
    while True:
        yield min_max(board, player, N, depth_level, timelimit)
        # at incrementing depth levels
        depth_level += 2


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
