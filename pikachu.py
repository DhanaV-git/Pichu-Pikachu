#
# pikachu.py : Play the game of Pikachu
#
# srichala-nvveer-bkavuri
#
# Based on skeleton code by D. Crandall, March 2021
#
import sys
import time
from copy import deepcopy


def parse_board(board, N):

    grid = [[None for _ in range(N)] for _ in range(N)]

    for n in range(N):
        for m in range(N):
            grid[n][m] = board[n*N + m]
    return grid


class Pikatchu:

    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.N = len(board)
        self.other = {"w": "b", "b": "w"}

    def successors(self):
        """ returns every possible next step from the current board """

        # forward direction
        adv = {"w": "bB", "b": "wW", "W": "bB", "B": "wW"}
        fd = {"w": 1, "b": -1}
        steps = ((0, 1), (0, -1), (fd[self.player], 0))

        for n, row in enumerate(self.board):
            for m, piece in enumerate(row):

                # skip non pieces
                if piece.lower() != self.player:
                    continue

                # a pichu
                if piece.islower():

                    for (x, y) in steps:

                        # move the piece to empty space
                        if min(n+x, m+y) >= 0 and max(n+x, m+y) < self.N \
                                and self.board[n+x][m+y] == ".":

                            new_board = deepcopy(self.board)
                            new_board[n][m] = "."

                            # convert into a pikachu
                            if (n+x == self.N-1 and player == "w") or \
                                    (n+x == 0 and player == "b"):
                                new_board[n+x][m+y] = piece.upper()
                            else:
                                new_board[n+x][m+y] = piece

                            yield (Pikatchu(new_board, self.other[self.player]), ((n, m), (n+x, m+y)))

                        elif min(n+2*x, m+2*y) >= 0 and max(n+2*x, m+2*y) < self.N \
                            and self.board[n+x][m+y] in adv[self.player] \
                                and self.board[n+2*x][m+2*y] == ".":

                            new_board = deepcopy(self.board)
                            new_board[n][m] = "."
                            new_board[n+x][m+y] = "."

                            # convert into a pikachu
                            if (n+2*x == self.N-1 and player == "w") or \
                                    (n+2*x == 0 and player == "b"):
                                new_board[n+2*x][m+2*y] = piece.upper()
                            else:
                                new_board[n+2*x][m+2*y] = piece

                            yield (Pikatchu(new_board, self.other[self.player]), ((n, m), (n+2*x, m+2*y)))

                # a pikachu
                else:
                    for (x, y) in ((1, 0), (-1, 0), (0, 1), (0, -1)):

                        u, v = n, m
                        capture = False
                        encounter = 0

                        # boundary check
                        while min(u+x, v+y) >= 0 and max(u+x, v+y) < self.N \
                            and not capture:

                            # piece of our player is in the way
                            if self.board[u+x][v+y].lower() == self.player:
                                break

                            # move to empty space
                            elif self.board[u+x][v+y].lower() == ".":

                                new_board = deepcopy(self.board)
                                new_board[n][m] = "."
                                new_board[u+x][v+y] = piece

                                yield (Pikatchu(new_board,
                                                self.other[self.player]),
                                       ((n, m), (u+x, v+y)))

                            # capture adversary
                            elif self.board[u+x][v+y].lower() in adv[self.player] \
                                and min(u+2*x, v+2*y) >= 0 and max(u+2*x, v+2*y) < self.N:

                                encounter += 1

                                if self.board[u+2*x][v+2*y] == "." and encounter < 2:

                                    capture = True

                                    # use all possible landings
                                    for i in range(2, self.N):

                                        if min(u+i*x, v+i*y) >= 0 \
                                          and max(u+i*x, v+i*y) < self.N \
                                            and self.board[u+i*x][v+i*y] == ".":

                                            new_board = deepcopy(self.board)
                                            new_board[n][m] = "."
                                            new_board[u+x][v+y] = "."

                                            new_board[u+i*x][v+i*y] = piece

                                            yield (Pikatchu(new_board,
                                                            self.other[self.player]),
                                                   ((n, m), (u+i*x, v+i*y)))

                                        else:
                                            break

                            # increment the position
                            u += x
                            v += y

    def fitness(self, player, pika_weight=3):
        """
        returns the score of the board with
        respect to the current player
        """

        pieces = "".join("".join(row) for row in self.board)

        # positive score
        team = (pieces.count(player) +
                pieces.count(player.upper()) * pika_weight)

        # negative score
        adversary = (pieces.count(self.other[player]) +
                     pieces.count(self.other[player].upper()) * pika_weight)

        # a win
        # if adversary == 0:
        #     return float("inf")

        # a loss
        # if team == 0:
        #     return -float("inf")

        return team - adversary

    def num_adv(self, player):

        pieces = "".join("".join(row) for row in self.board).lower()
        num = pieces.count(self.other[player])

        return num

    def __str__(self):
        return "".join("".join(row) for row in self.board)


def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


def maximum_score_ahead(board, player, num_moves=3):

    # base case
    if num_moves == 0:
        return board.fitness(player)

    # recursive case
    vals = [maximum_score_ahead(next_board, player, num_moves-1) for
            next_board, _ in board.successors()]

    return max(vals)


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!

    board = parse_board(board, N)
    pika = Pikatchu(board, player)

    # produce all possible boards one step ahead
    # and chose the one that highest score
    highest = -float("inf")

    for _next, (old, new) in pika.successors():

        # look K move ahead (default is 3)
        num = pika.num_adv(player)
        score = maximum_score_ahead(_next, player, num_moves=min(3, num-1))

        # update best score and yield board
        if score >= highest:
            highest = score

            line = (f"Move piece at row {old[0]+1} column {old[1]+1}" +
                    f" to row {new[0]+1} column {new[1]+1}.\n" +
                    "New board:\n" + _next.__str__())
            yield line


if __name__ == "__main__":
    if len(sys.argv) != 5:
       raise Exception("Usage: pikachu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv

    N = int(N)
    timelimit = int(timelimit)

    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player +
          " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
        # print(board_to_string(new_board, N))
