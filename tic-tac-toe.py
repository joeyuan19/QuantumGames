from math import exp
from random import random

def distance(v,u):
    return sum((vi-ui)**2 for vi,ui in zip(v,u))**.5

def probability(v,u):
    return exp(-(distance(v,u)**2))

class InvalidMoveException(Exception):
    pass

class TieGameException(Exception):
    pass

def get_proper_input():
    while True:
        try:
            row,col = map(int,input('Move: ').strip().split())
            return row,col
        except ValueError: 
            print("Invalid choice.  Please try again.  Give your move")
            print("in the form: 'row col', with a space in the middle e.g.")
            print("move: 0 0")

class Board(object):
    def __init__(self):
        self.board = [[' ' for i in range(3)] for j in range(3)]
        self.symbols = ['x','o']
        self.winner = None

    def get_winner(self):
        return self.winner

    def print_board(self):
        i = 0
        print('  ' + '  '.join(str(i)+' ' for i in range(3)))
        for row in self.board:
            print(str(i) + ' ' + '| '.join(i+' ' for i in row))
            if i < 2:
                print('  ' + ' '.join('-'*5))
            i += 1

    def randomize_move(self,origin_row,origin_col):
        psi = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == ' ':
                    psi.append((probability((origin_row,origin_col),(r,c)),(r,c)))
        N = sum(i[0] for i in psi)
        psi = [(i[0]/N,i[1]) for i in psi]
        psi = sorted(psi,key=lambda x: x[0])
        #print('Given:',origin_row,origin_col)
        #print('PSI:',psi)
        r = random()
        P = 0
        for p,move in psi:
            P += p
            if r < P:
                break
        #print('Chosen',move)
        return move

    def get_columns(self):
        return [[row[col] for row in self.board] for col in range(3)]

    def get_diagonals(self):
        return [
            [self.board[i][i] for i in range(3)],
            [self.board[2-i][i] for i in range(3)]
        ]
    
    def move(self,row,col,symbol):
        if self.board[row][col] == ' ':
            row,col = self.randomize_move(row,col)
            self.board[row][col] = symbol
        else:
            raise InvalidMoveException()

    def check_win(self):
        if all(all(i != ' ' for i in row) for row in self.board):
            raise TieGameException()
        for symbol in self.symbols:
            for row in self.board:
                if all(i == symbol for i in row):
                    self.winner = symbol
                    return True
            for col in self.get_columns():
                if all(i == symbol for i in col):
                    self.winner = symbol
                    return True
            for dia in self.get_diagonals():
                if all(i == symbol for i in dia):
                    self.winner = symbol
                    return True
        return False


print('Welcome to quantum tic-tac-toe!')
print('')
print('Choose the square you would like to try and play')
print('Your move gets randomly placed into free squares')
print('with decreasing probability  from the square you')
print('choose. i.e. if you choose the upper left corner')
print('')
print('Enter your moves as "row col", e.g')
print('Move: 0 0')
print('For the upper left corner')
print('')
print('ctrl-c to quit at any time')
b = Board()

p1 = True
try:
    while not b.check_win():
        b.print_board()
        if p1:
            print("x's turn")
            sym = 'x'
        else:
            print("o's turn")
            sym = 'o'
        row,col = get_proper_input()
        while True:
            try:
                b.move(row,col,sym)
                break
            except InvalidMoveException:
                print("Space ("+str(row)+","+str(col)+") is already taken.  Pick another move")
                row,col = get_proper_input()
        p1 = not p1

    b.print_board()
    print("Winner:",b.get_winner())
except TieGameException:
    print("Tie Game")


