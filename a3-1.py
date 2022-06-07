# a3.py
"""
Implement (in Python) a Tic-Tac-Toe playing program 
where a human can play against the computer, 
and the computer makes all its moves using random playouts as described below.
"""

import copy as cp
import random

MAX_PLAY = 3000

"""
display_board() function use to show the game board
"""
def display_board(map):
    for i in range(0,3):
        for j in range(0,3):
            print(map[i][j],end='')
            if j != 2:
                print(' | ', end='')
        if i != 2:
            print('\n----------')
    print()

"""
Helper function, help find unused places
idea is from:
https://blog.csdn.net/Jerry_1126/article/details/88924288
"""
def get_index(lst, item=0):
    return [index for (index,value) in enumerate(lst) if value == item]

"""
Then for each of the moves it does some number of random playouts. 
A random playout is when the computer simulates playing the game until it is over. 
During a random playout, the computer makes random moves for each player 
until a win, loss, or draw is reached. When a playout is done, the result (win, loss, or draw) 
is recorded, and then some more random playouts are done. After random playouts are done for 
all legal moves, it choses the move that resulted in the greatest number of wins (or least number of 
losses, or most number of wins + draws, etc. — whatever formula you find is the best way to make a 
decision based on these win/loss/draw statistics).
"""

def random_playout(board, state, human_symbol, ai_symbol, legal_position):
    wins = 0
    draws = 0
    losses = 0
    for i in range(MAX_PLAY):
        human_result = ai_result = 0
        simulation_board = cp.deepcopy(board)
        simulation_state = cp.deepcopy(state)
        simulation_game = Tic_Tac_Toe(simulation_board, human_symbol, ai_symbol, simulation_state)
        simulation_game.computer_move(legal_position)
        simulation_legal_move = get_index(simulation_game.get_state())
        whose_round = 'person'
        while True:
            simulation_legal_move = get_index(simulation_game.get_state())
            if len(simulation_legal_move) == 0:
                break
            if whose_round == 'person':
                human_chose = random.choice(simulation_legal_move)
                simulation_game.human_move(human_chose)
                whose_round = 'computer'
                human_result = simulation_game.judge_victory(human_symbol)
                if human_result == 2 :
                    break
            elif whose_round == 'computer':
                ai_chose = random.choice(simulation_legal_move)
                simulation_game.computer_move(ai_chose)
                whose_round = 'person'
                ai_result = simulation_game.judge_victory(ai_symbol)
                if ai_result == 2 :
                    break
        if ai_result == 2:
            wins += 1
        elif human_result == 2:
            losses += 1
        else:
            draws += 1
    return wins + draws


class Tic_Tac_Toe:
    """
    include all information about Tic Tac Toe games
    """

    def __init__(self, board, human_player, ai_player, state=None):
        self.board = board
        self.human = human_player
        self.computer = ai_player
        self.state = state or [0]*9
        
        # if end is True, means the game is done
        self.end = False
    
    def get_end(self):
        return self.end

    def get_board(self):
        return self.board
    
    def get_state(self):
        return self.state

    # This function output the winner message
    def winner(self):
        human_win = self.judge_victory(self.human)
        ai_win = self.judge_victory(self.computer)

        if human_win == 2:
            print(" You are Winner !")
            self.end = True
        elif ai_win == 2:
            print(" Computer are Winner !")
            self.end = True
        elif human_win == 1 or ai_win == 1:
            print(" Game Draw !")
            self.end = True

    def judge_victory(self,symbol):
        # Determine who wins or draws, 2 means win, 1 means draws

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == symbol \
                or self.board[0][i] == self.board[1][i] == self.board[2][i] == symbol:
                return 2
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol \
            or self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            return 2

        if 0 not in self.state:
            return 1

        return 0


        # if self.board[0][0] == symbol and self.board[0][1] == symbol and self.board[0][2] == symbol:
        #     return 2
        # elif self.board[0][0] == symbol and self.board[1][0] == symbol and self.board[2][0] == symbol:
        #     return 2
        # elif self.board[0][0] == symbol and self.board[1][1] == symbol and self.board[2][2] == symbol:
        #     return 2
        # elif self.board[0][1] == symbol and self.board[1][1] == symbol and self.board[2][1] == symbol:
        #     return 2
        # elif self.board[0][2] == symbol and self.board[1][2] == symbol and self.board[2][2] == symbol:
        #     return 2
        # elif self.board[0][2] == symbol and self.board[1][1] == symbol and self.board[2][0] == symbol:
        #     return 2
        # elif self.board[1][0] == symbol and self.board[1][1] == symbol and self.board[1][2] == symbol:
        #     return 2
        # elif self.board[2][0] == symbol and self.board[2][1] == symbol and self.board[2][2] == symbol:
        #     return 2
        # else:
        #     if 0 not in self.state :
        #         return 1
        #     else:
        #         return 0
    
    def human_move(self,position):
        self.board[position//3][position%3] = self.human
        # 1 means this position has already been used
        self.state[position] = 1

    def computer_move(self,position):
        self.board[position//3][position%3] = self.computer
        # 1 means this position has aleady been used
        self.state[position] = 1

    # choses the move that resulted in the most number of wins + draws
    def choses_move(self):
        # Record where computer can move.
        legal_moves = get_index(self.state)
        # Record the number of wins+draws at each location.
        num_WandD = []
        for i in range(len(legal_moves)):

            wins_Draws = random_playout(self.board,self.state,self.human,self.computer,legal_moves[i])
            num_WandD.append(wins_Draws)
        
        # the most wins and draws index is
        # print(num_WandD)
        index = num_WandD.index(max(num_WandD))
        return legal_moves[index]


def check_input(place, state):
    if place >= 0 and place <= 8 and state[place] == 0:
        return True
    return False

def play_a_new_game():
    print("Tic-Tac-Toe is a game played on a 3x3 grid. Players will fight against the computer.")
    print("Before starting the game, you need to select your own symbol in ‘X’ and ‘O’.")
    print("The'X' symbol is the first one, and the'O' symbol is the next one.")
    print("When one symbol on the game board is first connected horizontally, straightly, or diagonally, it wins.")
    print("The following is the game version, choose to specify the number to put down your symbol")
    print()

    # Set up the game board to display the game panel.
    game_board = { 0:[0,1,2],
                   1:[3,4,5],
                   2:[6,7,8]}
    display_board(game_board)
    print()
    # input_record use to record that position already has input
    # 0 means that this position is empty, 1 means that this position has 'X' or 'O'
    input_record = [0]*9
    # print(get_index(input_record))

    # Set who chooses 'X', 'X' is the first mover
    human_player = computer_player = None
    while True:
        human_player = input("Please select your game symbol from X & O : ").upper()
        if human_player == 'X':
            computer_player = 'O'
            break
        elif human_player == 'O':
            computer_player = 'X'
            break
        else:
            print("Wrong symbol, please select true symbol")
            continue
    # print(human_player)
    # print(computer_player)

    print()
    print("---Game Start---")
    print()
    new_game = Tic_Tac_Toe(game_board, human_player, computer_player, input_record)
    while True:
        if new_game.get_end():
            break

        print("Human symbol : ", human_player, " ; Computer symbol : ", computer_player)
        print()

        if human_player == 'X':
            human_place = int(input("Select the space you want to mark from [0,8] : "))
            if not check_input(human_place, new_game.get_state()):
                print("Invalid spaces. please enter again!")
                continue
            print()
            print("----------Your Move----------")
            new_game.human_move(human_place)
            display_board(new_game.get_board())
            print()
            new_game.winner()

            if new_game.get_end():
                break

            print()
            print("--------Computer Move--------")
            ai_place = new_game.choses_move()
            new_game.computer_move(ai_place)
            display_board(new_game.get_board())
            print()
            new_game.winner()
        else:
            print()
            print("--------Computer Move--------")
            ai_place = new_game.choses_move()
            new_game.computer_move(ai_place)
            display_board(new_game.get_board())
            print()
            new_game.winner()
            if new_game.get_end():
                break
            print()
            print("----------Your Move----------")
            human_place = int(input("Select the space you wnat to mark from [0,8] : "))
            if not check_input(human_place, new_game.get_state()):
                print("Invalid spaces. Please enter again!")
                continue
            new_game.human_move(human_place)
            display_board(new_game.get_board())
            print()
            new_game.winner()



if __name__ == '__main__':
    play_a_new_game()