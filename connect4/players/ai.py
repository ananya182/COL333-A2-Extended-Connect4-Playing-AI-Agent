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
        #function to simulate the board for the next player

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
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column)
                raise Exception(err)
# -------------------------------------------------------------------------------------------------------------------------------- 
    def eval_function(self, state, no_of_moves): 
        #The evaluation and heuristics for minimax are defined in this function

        initial_heuristic = 0 #initial/trivial heuristic
        board = state[0]
        num_popouts=state[1]
        n,m = np.shape(state[0])
        board_size = n*m
        points_plyer = get_pts(self.player_number,state[0])
        points_oppnt = get_pts((self.player_number*2)%3, state[0])

        heuristic = initial_heuristic

        if board_size > 40:
            importance = 0.5
        else:
            importance = 0.25

        if(no_of_moves > (n*m*3)//4): #central columns heuristic
            #Dealing with the important columns, which aid in getting score on both sides of the board
            imp_columns = [i for i in range((m//2) - 1,(m//2) + 1 + 1)] #central columns
            count_imp_cols = 0

            for col in imp_columns:
                for elem in board[:,col]:
                    if(elem == self.player_number):
                        count_imp_cols += 1
            
            heuristic += count_imp_cols*(no_of_moves**importance) #adding the central columns heuristic

        if(no_of_moves > (n*m)//4 and no_of_moves < (n*m*5)//6): #popout heuristic
            pop_out_heuristic = 4*num_popouts[self.player_number].get_int() 
            #the lesser the no. of popouts the better it is for player one,
            #as otherwise in the end it would be forced to play sub-optimal popout moves
            heuristic -= pop_out_heuristic #adding the pop_out heuristic
            if(self.player_number == 2):
                heuristic += pop_out_heuristic 
            #however for player 2, the popout heuristics doesn't matter as it is not forced
            # to play and exhaust it's pop out moves in the end.

        if(no_of_moves < (n*m)//2): #Weighted points heuristic
        #Since at the later stage of the game we should focus more on preventing the opponent from scoring
        #and in the initial stages of the game focus more on getting our points as there is nothing to prevent
            start_heuristic =  points_plyer - 2*points_oppnt
            heuristic += start_heuristic
        else:
            later_heuristic = 2*points_plyer - points_oppnt
            heuristic += later_heuristic

        ratio_state = max(15,(n*m)//2) 
        #initially the points_oppnt is not big enough to consider ratios and start working with it
        #however in the later stages of the game, we should focus more on maximizing the winning ratio

        if(no_of_moves < ratio_state): #ratio_absolute heuristic
            return heuristic/points_oppnt
        else:
            return heuristic
    
    def min_value(self, state, player_num, depth, limit, alpha, beta, start, no_of_moves):
        #simulating the min_node, the min_agent
        try:
            if depth >= limit: #if the depth limit is reached, return the value determined using the evaluation function
                return self.eval_function(state, no_of_moves)
        
            valid_actions = get_valid_actions((self.player_number*2)%3, state)
            min_val = np.inf
            
            for play_move in valid_actions: #Basic implementation of the min node of the minimax algorithm

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, (self.player_number*2)%3, is_pop, board_new, num_popout_new) #simulating the board for player 2's move
                state_new = (board_new,num_popout_new)

                cur_val = self.max_value(state_new, self.player_number, depth+1, limit, alpha, beta, start, no_of_moves-1) #simulating the move of the next player

                if cur_val=="exception":
                    raise Exception
                    
                if(self.time-(time.time() - start) < 0.3): 
                    #dealing with time, i.e to stop our execution if the time remaining is less than 0.3 secs
                    raise Exception                       

                min_val = min(min_val, cur_val)

                if(min_val == cur_val): #implementing alpha beta pruning
                    beta = min(min_val, beta)
                if beta <= alpha: #alpha beta pruning
                    return min_val
       
            return min_val

        except Exception as e:
            return "exception"

    def max_value(self, state, player_num, depth, limit, alpha, beta, start, no_of_moves):
        #simulating the max_node, the max_agent
        try:
            if depth >= limit: 
                #if the depth limit is reached, return the value determined using the evaluation function
                return self.eval_function(state,no_of_moves)
    
            valid_actions = get_valid_actions(player_num, state) #maximizing for our own player
            max_val = -1 * np.inf
            
            for play_move in valid_actions:  #Basic implementation of the max node of the minimax algorithm

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, player_num, is_pop, board_new, num_popout_new)
                state_new = (board_new,num_popout_new)

                cur_val = self.min_value(state_new, self.player_number, depth+1, limit, alpha, beta, start, no_of_moves - 1)

                if cur_val=="exception":
                        raise Exception
                    
                if(self.time-(time.time() - start) < 0.3):
                    #dealing with time, i.e to stop our execution if the time remaining is less than 0.3 secs
                    raise Exception
                
                max_val = max(cur_val, max_val)

                if(cur_val == max_val): #implementing alpha beta pruning
                    alpha = max(max_val, alpha)
                if alpha >= beta: #alpha beta pruning
                    return max_val
                      
            return max_val

        except Exception as e:
            return "exception"    

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
        limit = 0

        board, num_popout = state
        no_of_moves = np.count_nonzero(board == 0)
        total_moves = no_of_moves + num_popout[1].get_int() + num_popout[2].get_int()

        while True: 
            #implementing iterative deepening i.e increasing the limit till which search takes place by 1 
            #in each iteration and limiting this depth to the total no of moves that are still possible in the game
            #to prevent unnecessary calculations

            limit += 1
            
            try :
                if limit > total_moves:
                    raise Exception

                min_val = -1 * np.inf

                for play_move in valid_actions: 
                    # simulating the agent as a max node which maximizes its utility function
                    
                    (act_column,is_pop) = play_move
                    board, num_popout = state
                    board_new = copy.deepcopy(board)
                    num_popout_new = copy.deepcopy(num_popout)

                    self.simulate_board(act_column, self.player_number, is_pop, board_new, num_popout_new)
                    state_new = board_new, num_popout_new

                    new_min = self.min_value(state_new, self.player_number, 1, limit, -np.inf, np.inf, start, total_moves)
                    
                    if new_min=="exception":
                        raise Exception
                    
                    if(self.time-(time.time() - start)< 0.3):
                        #dealing with time, i.e to stop our execution if the time remaining is less than 0.3 secs
                        raise Exception

                    if self.player_number not in board[:,act_column] and is_pop and True in valid_actions[:,1]:
                        continue
                        #if all the cells in the columns are of opposite players, then there is no point in poping from that
                        #as the other agent can simply move again in that column, thus we would be wasting our popout move
                        #Hence, avoiding that, except for when all the moves left with us are popout moves
                    
                    elif new_min > min_val: #max utility finding
                        opt_action_curr = play_move
                        min_val = new_min
                    
                #if this depth could be completed
                opt_action = opt_action_curr
                min_val = new_min
            
            except Exception as e :
                end = time.time()
                return opt_action

        end = time.time()

        return opt_action #returning the optimal action
# --------------------------------------------------------------------------------------------------------------------------------
    def eval_function_expectimax(self, state, player_num):
        #The evaluation and heuristics for minimax are defined in this function

        initial_heuristic = 0 #the initial/trivial heuristic
        board = state[0]
        num_popouts=state[1]
        n,m = np.shape(state[0])
        board_size = n*m
        points_plyer = get_pts(self.player_number,state[0])
        points_oppnt = get_pts((self.player_number*2)%3, state[0])

        if(board_size < 35): 
            #greedily playing on a smaller board size as in 
            #it the random player has very less prob. of gaining points
            heuristic += 3*points_plyer - points_oppnt
        else:
            #playing safe in case of larger boards as in this case the random player has very less 
            #prob of stopping our connect fours, and so we should focus more on stopping the connect fours
            #of the other random agent
            heuristic += points_plyer - 3*points_oppnt

        return heuristic

    def max_value_expectimax(self, state, player_num, depth, limit, alpha, beta, start):
        #simulating the max_node, the max_agent
        try:
            if depth >= limit: 
                #if the depth limit is reached, return the value determined using the evaluation function
                return self.eval_function_expectimax(state,player_num)
    
            valid_actions = get_valid_actions(player_num, state) #maximizing for our own player
            max_val = -1 * np.inf
            
            for play_move in valid_actions: #Basic implementation of the max node of the expectimax algorithm

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, player_num, is_pop, board_new, num_popout_new)
                #simulating the board for the move of the current player
                state_new = (board_new,num_popout_new)

                cur_val = self.do_player_move_random(state_new, self.player_number, depth+1, limit, alpha, beta, start) 

                if cur_val=="exception":
                        raise Exception
                    
                if(self.time-(time.time() - start)< 0.3):
                        #dealing with time, i.e to stop our execution if the time remaining is less than 0.3 secs
                        raise Exception
                
                max_val = max(cur_val, max_val) #finding the max value from all its childrens

            return max_val

        except Exception as e:
            return "exception"
            
    def do_player_move_random(self, state, player_num, depth, limit, alpha, beta, start):
        #simulating a random node in the expectimax algorithm
        try:

            if depth >= limit:
                #if the depth limit is reached, return the value determined using the evaluation function
                return self.eval_function_expectimax(state,player_num)

            valid_actions = get_valid_actions((player_num*2)%3, state)
            board, num_popouts = state
            cumulative_benefit = 0

            for play_move in valid_actions: #Basic implementation of the random node of the minimax algorithm

                (act_column,is_pop) = play_move
                board, num_popout = state
                board_new = copy.deepcopy(board)
                num_popout_new = copy.deepcopy(num_popout)

                self.simulate_board(act_column, (player_num*2)%3, is_pop, board_new, num_popout)
                #simulating the board for the current agent
                state_new = board_new, num_popout_new

                cur_val = self.max_value_expectimax(state_new, self.player_number, depth+1, limit, alpha, beta, start) 

                if cur_val=="exception":
                    raise Exception
                        
                if(self.time-(time.time() - start) < 0.3):
                    #dealing with time, i.e to stop our execution if the time remaining is less than 0.3 secs
                    raise Exception
                    
                cumulative_benefit += cur_val #summing all the benefits

            return cumulative_benefit/len(valid_actions) 
            #returning the adjusted cumulative benefit i.e multiplying with the prob. of each move

        except Exception as e:
            return "exception"

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
            #implementing iterative deepening i.e increasing the limit till which search takes place by 1 
            #in each iteration and limiting this depth to the total no of moves that are still possible in the game
            #to prevent unnecessary calculations
            limit += 1
            
            try :
                if limit > total_moves:
                    raise Exception

                min_val = -1 * np.inf

                for play_move in valid_actions:
                    # simulating the agent as a max node which maximizes its utility function

                    (act_column,is_pop) = play_move
                    board, num_popout = state
                    board_new = copy.deepcopy(board)
                    num_popout_new = copy.deepcopy(num_popout)

                    self.simulate_board(act_column, self.player_number, is_pop, board_new, num_popout_new) 
                    # simulating the board for the player's move
                    state_new = board_new, num_popout_new

                    cumulative_benefit = self.do_player_move_random(state_new, self.player_number, 0, limit, -np.inf, np.inf, start)
                    # making the search tree 

                    if cumulative_benefit == "exception":
                        raise Exception
                    
                    if(self.time-(time.time() - start)< 0.3):
                        #dealing with time, i.e to stop our execution if the time remaining is less than 0.3 secs
                        raise Exception

                    if(cumulative_benefit > min_val): #max expected utility finding
                        opt_action_curr = play_move
                        min_val = cumulative_benefit

                #if this depth could be completed
                opt_action = opt_action_curr

            except Exception as e :
                end = time.time()
                return opt_action

        
        end = time.time()

        return opt_action #returning the optimal action
# --------------------------------------------------------------------------------------------------------------------------------
