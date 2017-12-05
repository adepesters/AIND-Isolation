"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    y_own, x_own = game.get_player_location(player)
    y_opp, x_opp = game.get_player_location(game.get_opponent(player))
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    #return float(own_moves + ((y_own - y_opp)**2 + (x_own - x_opp)**2) - 2 *opp_moves)
    return float(own_moves + (y_own - y_opp)**2 + (x_own - x_opp)**2 - 2 *opp_moves)
    
def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
   
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
        
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2 * opp_moves)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
        
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))    

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float(own_moves - (h - y)**2 - (w - x)**2 - 2 *opp_moves)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
            
        default_move = (-1, -1)
        
        self.depth = depth
                
        #print('current depth at beginning: '+str(self.depth))
        
        #for m in game.get_legal_moves():
        #        print('possible move: ' + str(m))
        #        print('score: '+str(self.score(game, game.active_player)))
        
        def terminal_test(game):
           
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            return not bool(game.get_legal_moves())
        
        # def depth_reached(depth):
#             if self.time_left() < self.TIMER_THRESHOLD:
#                 raise SearchTimeout()
#             self.depth = depth
#             return self.depth == 0
        
        def min_value(game, updated_depth):
           
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if terminal_test(game):
                return float("inf")
            #print('updated depth ' + str(updated_depth))
            if updated_depth == 0:
                #print('final depth reached during min: '+ str(updated_depth))
                #print(self.score(game, self))
                #print(game.to_string())
                return self.score(game, self)
            v = float("inf")
            updated_depth -= 1
           # for m in game.get_legal_moves():
           #     print('possible move: ' + str(m))
           #     print('score: '+str(self.score(game.forecast_move(m), game.active_player)))
            for m in game.get_legal_moves():
                #print('entered in min')
                #print('current game')
                #print(game.to_string())
                #print(m)
                #print('current v value at min: ' + str(v))
                v = min(v, max_value(game.forecast_move(m), updated_depth))
            return v

        def max_value(game, updated_depth):
            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if terminal_test(game):
                return float("-inf")
            if updated_depth == 0:
                #print('final depth reached during max: '+ str(updated_depth))
                #print(self.score(game, self))
                #print(game.to_string())
                return self.score(game, self)
            v = float("-inf")
            updated_depth -= 1
          #  for m in game.get_legal_moves():
          #      print('possible move: ' + str(m))
          #      print('score: '+str(self.score(game.forecast_move(m), game.active_player)))
            for m in game.get_legal_moves():
                #print('entered in max')
                #print('current game')
                #print(game.to_string())
                #print(m)
                #print('current v value at max: ' + str(v))
                v = max(v, min_value(game.forecast_move(m), updated_depth))
            return v
        
        def minimax_decision(game):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            best_score = float("-inf")
            best_move = default_move
         #   print(game.active_player)
         #   print(game.get_legal_moves())
            for m in game.get_legal_moves():
                updated_depth = self.depth - 1
                #print('updated depth ' + str(updated_depth))
                #print('evaluating first move: ' + str(m))
                v = min_value(game.forecast_move(m), updated_depth)
                #print('current v value at beginning: ' + str(v))
                if v > best_score:
                    best_score = v
                    best_move = m
            #print('best move: '+str(best_move))
         #   print(game.to_string())
            ######## added this to counter forfeits
            # if best_move == (-1, -1):
#                 legal_moves = game.get_legal_moves()
#                 if not legal_moves:
#                     best_move = (-1, -1)
#                 else: 
#                     best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]
            #########
            return best_move
        
        return minimax_decision(game)
        
        #legal_moves = game.get_legal_moves()
        #return legal_moves[1]
        

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        # self.time_left = time_left
# 
#         # TODO: finish this function!
#         raise NotImplementedError
        
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_next_move = (-1, -1)
        
        iterative_depth = 1
        
        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                #print('new depth')
                #print(iterative_depth)
                #print('new move')
                #print(best_next_move)
                best_next_move = self.alphabeta(game, iterative_depth, self, self)
                iterative_depth += 1

            except SearchTimeout:
                
                #print('final depth')
                #print(iterative_depth)
                #print('final move')
                #print(best_next_move)
                return best_next_move
                #return self.alphabeta(game, iterative_depth, self, self)
                #pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        #return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        default_move = (-1, -1)
        
        self.depth = depth
        
        def terminal_test(game):
           
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            return not bool(game.get_legal_moves())
        
        def min_value(game, updated_depth, alpha, beta):
           
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if terminal_test(game):
                return float("inf")
            if updated_depth == 0:
                return self.score(game, self)
            v = float("inf")
            updated_depth -= 1
            for m in game.get_legal_moves():
                v = min(v, max_value(game.forecast_move(m), updated_depth, alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        def max_value(game, updated_depth, alpha, beta):
            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if terminal_test(game):
                return float("-inf")
            if updated_depth == 0:
                return self.score(game, self)
            v = float("-inf")
            updated_depth -= 1
            for m in game.get_legal_moves():
                v = max(v, min_value(game.forecast_move(m), updated_depth, alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        
        def alpha_beta_decision(game):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            best_score = float("-inf")
            best_move = default_move
            alpha = float('-inf')
            beta = float('inf')
            for m in game.get_legal_moves():
                updated_depth = self.depth - 1
                v = min_value(game.forecast_move(m), updated_depth, alpha, beta)
                if v > best_score:
                    best_score = v
                    best_move = m
               # if v >= beta:
               #     best_score = v
               #     best_move = m
                alpha = max(alpha, v)
            ######## added this to counter forfeits
            # if best_move == (-1, -1):
#                 legal_moves = game.get_legal_moves()
#                 if not legal_moves:
#                     best_move = (-1, -1)
#                 else: 
#                     best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]
            #########
            return best_move
        
        return alpha_beta_decision(game)
        
################################## not necessary after that

# ############
# 
# from isolation import Board
# 
# class RandomPlayer():
#     """Player that chooses a move randomly."""
# 
#     def get_move(self, game, time_left):
#         """Randomly select a move from the available legal moves.
# 
#         Parameters
#         ----------
#         game : `isolation.Board`
#             An instance of `isolation.Board` encoding the current state of the
#             game (e.g., player locations and blocked cells).
# 
#         time_left : callable
#             A function that returns the number of milliseconds left in the
#             current turn. Returning with any less than 0 ms remaining forfeits
#             the game.
# 
#         Returns
#         ----------
#         (int, int)
#             A randomly selected legal move; may return (-1, -1) if there are
#             no available legal moves.
#         """
#         legal_moves = game.get_legal_moves()
#         if not legal_moves:
#             return (-1, -1)
#         return legal_moves[random.randint(0, len(legal_moves) - 1)]
# 
# class HumanPlayer():
#     """Player that chooses a move according to user's input."""
# 
#     def get_move(self, game, time_left):
#         """
#         Select a move from the available legal moves based on user input at the
#         terminal.
# 
#         **********************************************************************
#         NOTE: If testing with this player, remember to disable move timeout in
#               the call to `Board.play()`.
#         **********************************************************************
# 
#         Parameters
#         ----------
#         game : `isolation.Board`
#             An instance of `isolation.Board` encoding the current state of the
#             game (e.g., player locations and blocked cells).
# 
#         time_left : callable
#             A function that returns the number of milliseconds left in the
#             current turn. Returning with any less than 0 ms remaining forfeits
#             the game.
# 
#         Returns
#         ----------
#         (int, int)
#             The move in the legal moves list selected by the user through the
#             terminal prompt; automatically return (-1, -1) if there are no
#             legal moves
#         """
#         legal_moves = game.get_legal_moves()
#         if not legal_moves:
#             return (-1, -1)
# 
#         print(game.to_string()) #display the board for the human player
#         print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))
# 
#         valid_choice = False
#         while not valid_choice:
#             try:
#                 index = int(input('Select move index:'))
#                 valid_choice = 0 <= index < len(legal_moves)
# 
#                 if not valid_choice:
#                     print('Illegal move! Try again.')
# 
#             except ValueError:
#                 print('Invalid index! Try again.')
# 
#         return legal_moves[index]
# 
# 
# # create an isolation board (by default 7x7)
# player1 = HumanPlayer()
# player2 = AlphaBetaPlayer(score_fn=custom_score)
# #player2 = MinimaxPlayer(search_depth = 10)
# #player2 = RandomPlayer()
# game = Board(player1, player2)
# 
# # place player 1 on the board at row 2, column 3, then place player 2 on
# # the board at row 0, column 5; display the resulting board state.  Note
# # that the .apply_move() method changes the calling object in-place.
# game.apply_move((2, 3))
# game.apply_move((0, 5))
# print(game.to_string())
# 
# # players take turns moving on the board, so player1 should be next to move
# assert(player1 == game.active_player)
# 
# # get a list of the legal moves available to the active player
# print(game.get_legal_moves())
# 
# # get a successor of the current state by making a copy of the board and
# # applying a move. Notice that this does NOT change the calling object
# # (unlike .apply_move()).
# 
# # new_game = game.forecast_move((1, 1))
# # assert(new_game.to_string() != game.to_string())
# # print("\nOld state:\n{}".format(game.to_string()))
# # print("\nNew state:\n{}".format(new_game.to_string()))
# 
# # play the remainder of the game automatically -- outcome can be "illegal
# # move", "timeout", or "forfeit"
# winner, history, outcome = game.play(time_limit=20000)
# print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
# print(game.to_string())
# print("Move history:\n{!s}".format(history))
# 
# 
# 
