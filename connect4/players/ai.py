import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

    def simulate_board(self, column: int, player_num: int, is_popout: bool = False):
    
        board, num_popouts = self.state
        print("Next move : Player:",player_num,"Column:",column,"Is_pop:",is_popout)

        if not is_popout:
            if 0 in board[:, column]:
                for row in range(1, board.shape[0]):
                    update_row = -1
                    if board[row, column] > 0 and board[row - 1, column] == 0:
                        update_row = row - 1
                    elif row == board.shape[0] - 1 and board[row, column] == 0:
                        update_row = row
                    if update_row >= 0:
                        board[update_row, column] = player_num
                        self.c.itemconfig(self.gui_board[column][update_row], fill=self.colors[self.current_turn + 1])
                        break
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column, is_popout)
                raise Exception(err)
        else:
            if 1 in board[:, column] or 2 in board[:, column]:
                for r in range(board.shape[0] - 1, 0, -1):
                    board[r, column] = board[r - 1, column]
                    self.c.itemconfig(self.gui_board[column][r], fill=self.colors[
                        board[r, column]])  # this needs to be tweaked
                board[0, column] = 0
                self.c.itemconfig(self.gui_board[column][0], fill=self.colors[0])
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column)
                raise Exception(err)
            num_popouts[player_num].decrement()
        
        print("\n", board, "\n")
        s = ""
        s += f'Player 1 Score: {get_pts(1, self.state[0])}\n'
        s += f'Player 2 Score: {get_pts(2, self.state[0])}\n'
        s += "-"*25
        s += "\n"
        print(s)

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        # raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """

        # Do the rest of your implementation here

        valid_actions = get_valid_actions(self.player_number, state)

        # for (act,is_pop) in valid_actions:
        #     board, num_popout = state
        #     board_new = copy.deepcopy(board)
        #     if(!is_pop):
        #         board
        #     state.
    

        action, is_popout = random.choice(valid_actions)

        return action, is_popout

        # raise NotImplementedError('Whoops I don\'t know what to do')
