from ftplib import MAXLINE
import random
import copy
import time
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

    def simulate_board(self, column: int, player_num: int, is_popout: bool, board, num_popouts):

        # print("Next move : Player:",player_num,"Column:",column,"Is_pop:",is_popout)

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
                        # print("New board", board)
                        break
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column, is_popout)
                raise Exception(err)
        else:
            if 1 in board[:, column] or 2 in board[:, column]:
                for r in range(board.shape[0] - 1, 0, -1):
                    board[r, column] = board[r - 1, column]
                board[0, column] = 0
                num_popouts[player_num].decrement()
                # print("New board", board)
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column)
                raise Exception(err)
# -------------------------------------------------------------------------------------------------------------------------------- 
    def eval_function(self, state, player_num, s):

        # if s=="min":
        #     #print("eval : ", get_pts(player_num,state[0]) - get_pts((player_num*2)%3, state[0]))
        #     return get_pts(player_num,state[0]) - get_pts((player_num*2)%3, state[0]) 
        # else:
        #     #print("eval : ", get_pts((player_num*2)%3, state[0]) - get_pts(player_num,state[0]))
        #     return get_pts((player_num*2)%3, state[0]) - get_pts(player_num,state[0])
        return get_pts(player_num,state[0]) - get_pts((player_num*2)%3, state[0]) 
    
    def min_value(self, state, player_num, depth, limit, alpha, beta, start):
        try:
            if depth >= limit:
                return self.eval_function(state, self.player_number, "min")
        
            valid_actions = get_valid_actions((player_num*2)%3, state) #player 2 moves now
            min_val = np.inf
            
            for play_move in valid_actions:

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, (player_num*1)%3, is_pop, board_new, num_popout_new) #simulating the board for player 2's move
                state_new = (board_new,num_popout_new)

                cur_val = self.max_value(state_new, self.player_number, depth+1, limit, alpha, beta, start) #simulating the move of the next player
                if cur_val=="exception":
                    raise Exception
                    
                if(self.time-(time.time() - start)< 0.1):
                    raise Exception                       
    
                # print(cur_val)
                
                min_val = min(min_val, cur_val)
                beta = min(min_val, beta)
                if beta <= alpha: #alpha beta pruning
                    return min_val
                
            #print("min:",min)        
            return min_val

        except Exception as e:
            return "exception"

    def max_value(self, state, player_num, depth, limit, alpha, beta, start):

        try:
            if depth >= limit:
                return self.eval_function(state,player_num,"max")
    
            valid_actions = get_valid_actions(player_num, state) #maximizing for our own player
            max_val = -1 * np.inf
            
            for play_move in valid_actions:

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, player_num, is_pop, board_new, num_popout_new)
                state_new = (board_new,num_popout_new)

                cur_val = self.min_value(state_new, self.player_number, depth+1, limit, alpha, beta, start) 
                if cur_val=="exception":
                        raise Exception
                    
                if(self.time-(time.time() - start)< 0.1):
                        raise Exception
                
                max_val = max(cur_val, max_val)
                alpha = max(max_val, alpha)
                if alpha >= beta: #alpha beta pruning
                    return max_val
                
            #print("max",max)        
            return max_val

        except Exception as e:
            return "exception"    

    def terminal_test(self, state, player_num):
        valid_actions = get_valid_actions((player_num*2)%3, state)
        if(len[valid_actions]==1):
            return True

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
        start = time.time()

        valid_actions = get_valid_actions(self.player_number, state)
        min_val = -1 * np.inf
        opt_action = valid_actions[0]
        limit = 1

        board, num_popout = state
        no_of_moves = np.count_nonzero(board==0)
        total_moves = no_of_moves + num_popout[1].get_int() + num_popout[2].get_int()

        while True:
            limit += 1
            
            try :
                if limit>total_moves:
                    raise Exception

            # for limit in range(5):

                min_val = -1 * np.inf

                for play_move in valid_actions:
                    
                    (act_column,is_pop) = play_move
                    board, num_popout = state
                    board_new = copy.deepcopy(board)
                    num_popout_new = copy.deepcopy(num_popout)

                    self.simulate_board(act_column, self.player_number, is_pop, board_new, num_popout_new)
                    state_new = board_new, num_popout_new


                    new_min = self.min_value(state_new, self.player_number, 0, limit, -np.inf, np.inf, start)
                    
                    if new_min=="exception":
                        raise Exception
                    
                    if(self.time-(time.time() - start)< 0.1):
                        raise Exception
                    
                    if  new_min > min_val:
                        opt_action_curr = play_move
                        min_val = new_min
                    # print("New min:", new_min)
                    # print(play_move)
                    
                #if this depth could be completed
                opt_action = opt_action_curr
                min_val = new_min
            
            except Exception as e :
                end = time.time()
                print("limit:", limit)
                print(opt_action, "Time :", round(end - start,6),"secs")
                return opt_action

        
        end = time.time()
        print(opt_action, "Time :", round(end - start,6),"secs")

        return opt_action
        #print("Score difference for player 1:",Score_ai - Score_random)
    

        # raise NotImplementedError('Whoops I don\'t know what to do')
# --------------------------------------------------------------------------------------------------------------------------------
    def eval_function_expectimax(self, state, player_num, s):

        # if s=="min":
        #     #print("eval : ", get_pts(player_num,state[0]) - get_pts((player_num*2)%3, state[0]))
        #     return get_pts(player_num,state[0]) - get_pts((player_num*2)%3, state[0]) 
        # else:
        #     #print("eval : ", get_pts((player_num*2)%3, state[0]) - get_pts(player_num,state[0]))
        #     return get_pts((player_num*2)%3, state[0]) - get_pts(player_num,state[0])
        return get_pts(player_num,state[0]) - get_pts((player_num*2)%3, state[0])

    def max_value_expectimax(self, state, player_num, depth, limit, alpha, beta, start):

        try:
            if depth >= limit:
                return self.eval_function_expectimax(state,player_num,"max")
    
            valid_actions = get_valid_actions(player_num, state) #maximizing for our own player
            max_val = -1 * np.inf
            
            for play_move in valid_actions:

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, player_num, is_pop, board_new, num_popout_new)
                state_new = (board_new,num_popout_new)

                cur_val = self.do_player_move_random(state_new, self.player_number, depth+1, limit, alpha, beta, start) 

                if cur_val=="exception":
                        raise Exception
                    
                if(self.time-(time.time() - start)< 0.1):
                        raise Exception
                
                max_val = max(cur_val, max_val)
                # alpha = max(max_val, alpha)
                # if alpha >= beta: #alpha beta pruning
                #     return max_val
                
            #print("max",max)        
            return max_val

        except Exception as e:
            return "exception"
            
    def do_player_move_random(self, state, player_num, depth, limit, alpha, beta, start):

        try:

            if depth >= limit:
                return self.eval_function_expectimax(state,player_num,"max")

            valid_actions = get_valid_actions((player_num*2)%3, state)
            board, num_popouts = state
            cumulative_benefit = 0

            for play_move in valid_actions:

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, (player_num*2)%3, is_pop, board_new, num_popout)
                state_new = board_new, num_popout_new

                cur_val = self.max_value_expectimax(state_new, self.player_number, depth+1, limit, alpha, beta, start) 

                if cur_val=="exception":
                    raise Exception
                        
                if(self.time-(time.time() - start)< 0.1):
                    raise Exception
                    
                cumulative_benefit += cur_val

            # print("Benefit cumulative for player 2:",cumulative_benefit)

            return cumulative_benefit/len(valid_actions)

        except Exception as e:
            return "exception"
                # if(self.player_number == 1):
                #     Score_random = get_pts(2, board_new)
                # else:
                #     Score_random = get_pts(1, board_new)

                # cumulative_benefit += Score_ai - 2*Score_random

                # if Score_ai==0:
                #     percentage=cumulative_benefit
                # else:
                #     percentage=cumulative_benefit/Score_ai

            # print("Percent margin cumulative for player 2:",percentage*100)
            # if(Score_ai - Score_random > cmax):
            #     opt_action, opt_is_pop = act_column, is_pop

        # action, is_popout = random.choice(valid_actions)
        # action, is_popout =  opt_action, opt_is_pop
    
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
        start = time.time()

        valid_actions = get_valid_actions(self.player_number, state)
        min_val = -1 * np.inf
        opt_action = valid_actions[0]
        limit = 0

        board, num_popout = state
        no_of_moves = np.count_nonzero(board == 0)
        total_moves = no_of_moves + num_popout[1].get_int() + num_popout[2].get_int()

        while True:
            limit += 1
            
            try :
                # print("limit:", limit)
                if limit > total_moves:
                    # print(limit, total_moves)
                    raise Exception

                min_val = -1 * np.inf

                for play_move in valid_actions:

                    (act_column,is_pop) = play_move
                    board, num_popout = state
                    board_new = copy.deepcopy(board)
                    num_popout_new = copy.deepcopy(num_popout)

                    self.simulate_board(act_column, self.player_number, is_pop, board_new, num_popout_new)
                    state_new = board_new, num_popout_new

                    cumulative_benefit = self.do_player_move_random(state_new, self.player_number, 0, limit, -np.inf, np.inf, start)

                    if cumulative_benefit == "exception":
                        raise Exception
                    
                    if(self.time-(time.time() - start)< 0.1):
                        raise Exception

                    Score_random = get_pts((self.player_number*2)%3, board_new)

                    # print("Score difference for player 1:",cumulative_benefit - Score_random)

                    if Score_random == 0 :
                        Score_random = 1

                    # if(cumulative_benefit/Score_random > min_val):
                    #     opt_action_curr = play_move
                    #     min_val = cumulative_benefit/Score_random
                    # print(play_move, cumulative_benefit)

                    if(cumulative_benefit > min_val):
                        opt_action_curr = play_move
                        min_val = cumulative_benefit

                # action, is_popout =  opt_action, opt_is_pop
                # time.sleep(1)
                #if this depth could be completed
                opt_action = opt_action_curr
                # min_val = 

            except Exception as e :
                end = time.time()
                print("limit:", limit)
                print(opt_action, "Time :", round(end - start,6),"secs")
                return opt_action

        
        end = time.time()
        print(opt_action, "Time :", round(end - start,6),"secs")

        return opt_action

        # raise NotImplementedError('Whoops I don\'t know what to do')
# --------------------------------------------------------------------------------------------------------------------------------
