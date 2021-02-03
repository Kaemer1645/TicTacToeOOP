import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import QFile, QIODevice
from functools import partial

import numpy as np

class Main:
    def __init__(self):
        ui_file_name = "gui.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        if not self.window:
            print(loader.errorString())
            sys.exit(-1)
        self.window.show()

        self.turn = 0

        self.board = np.array([[0,0,0],
                                [0,0,0],
                                [0,0,0]])
        

        #buttons
        self.window.ox_1.clicked.connect(lambda:self.turns('1')) #tu musi byc lambda
        self.window.ox_2.clicked.connect(lambda:self.turns('2'))
        self.window.ox_3.clicked.connect(lambda:self.turns('3'))
        self.window.ox_4.clicked.connect(lambda:self.turns('4'))
        self.window.ox_5.clicked.connect(lambda:self.turns('5'))
        self.window.ox_6.clicked.connect(lambda:self.turns('6'))
        self.window.ox_7.clicked.connect(lambda:self.turns('7'))
        self.window.ox_8.clicked.connect(lambda:self.turns('8'))
        self.window.ox_9.clicked.connect(lambda:self.turns('9'))

        #reset
        self.window.pbReset.clicked.connect(lambda:self.reset())

        #set winner labels
        self.window.player1_points.setText("0")
        self.window.player2_points.setText("0")
        self.player_1_points = 0
        self.player_2_points = 0

    def turns(self, arg: str):
        nazwa='self.window.ox_'+arg
        exec (compile(nazwa+'.setCheckable(True)', "<string>", "exec"))
        if self.turn % 2 == 0:
            print('Player 1 turn')
            dudu = exec (compile(nazwa+'.setText("o")', "<string>", "exec"))
            exec (compile(nazwa+'.clicked.connect(dudu)', "<string>", "exec"))
            self.turn += 1

            if int(arg) >= 1 and int(arg) <=3:
                self.board[0][int(arg)-1] = 1
            if int(arg) >= 4 and int(arg) <= 6:
                self.board[1][int(arg)-4] = 1
            if int(arg) >= 7 and int(arg) <= 9:
                self.board[2][int(arg)-7] = 1
            #print(self.board)

            
        elif self.turn % 2 != 0:
            print('Player 2 turn')
            dadu = exec (compile(nazwa+'.setText("x")', "<string>", "exec"))
            exec (compile(nazwa+'.clicked.connect(dadu)', "<string>", "exec"))
            self.turn += 1

            if int(arg) >= 1 and int(arg) <=3:
                self.board[0][int(arg)-1] = 2
            if int(arg) >= 4 and int(arg) <= 6:
                self.board[1][int(arg)-4] = 2
            if int(arg) >= 7 and int(arg) <= 9:
                self.board[2][int(arg)-7] = 2
            #print(self.board)

        win = self.check_winner_rows(self.board)
        win2 = self.check_winner_diagonal(self.board)
        win3 = self.check_winner_diagonal_reverse(self.board)
        
    def reset(self):
        print('RESTART')
        for btns in range(1,10):
            nazwa='self.window.ox_'+str(btns)
            exec (compile(nazwa+'.setText("")', "<string>", "exec"))
            #self.window.player1_points.setText("0")
            #self.window.player2_points.setText("0")
            self.board = np.array([[0,0,0],
                                   [0,0,0],
                                   [0,0,0]])


    def check_winner_rows(self, matrix):
        print("")
        #print("I check who win the game")
        for i in range(3):
            set_rows = set(matrix[i])
            if len(set_rows) == 1 and matrix[0][i] != 0:
                if set_rows == {1}:
                    print("Player 1 won the game :)")
                    self.player_1_points += 1
                elif set_rows == {2}:
                    print("Player 2 won the game :)")
                    self.player_2_points += 1

        cols = np.transpose(matrix)
        for i in range(3):
            set_cols = set(cols[i])
            if len(set_cols) == 1 and matrix[0][i] != 0:
                if set_cols == {1}:
                    print("Player 1 won the game :)")
                    self.player_1_points += 1
                elif set_cols == {2}:
                    print("Player 2 won the game :)")
                    self.player_2_points += 1

        self.window.player1_points.setText(str(self.player_1_points))
        self.window.player2_points.setText(str(self.player_2_points))


    def check_winner_diagonal(self, matrix):
        diag = matrix.diagonal()
        #print('diag: ',diag)
        if set(diag) == {1}:
            print("Player 1 won the game :)")
            self.player_1_points += 1
        elif set(diag) == {2}:
            print("Player 2 won the game :)")
            self.player_2_points += 1

        self.window.player1_points.setText(str(self.player_1_points))
        self.window.player2_points.setText(str(self.player_2_points))

    def check_winner_diagonal_reverse(self, matrix):
        reverse_diag = np.diag(np.fliplr(matrix))
        #print('reverse diag: ',reverse_diag)
        if set(reverse_diag) == {1}:
            print("Player 1 won the game :)")
            self.player_1_points += 1
        elif set(reverse_diag) == {2}:
            print("Player 2 won the game :)")
            self.player_2_points += 1

        self.window.player1_points.setText(str(self.player_1_points))
        self.window.player2_points.setText(str(self.player_2_points))

if __name__ == "__main__":
    app = QApplication([])
    inst = Main()
    sys.exit(app.exec_())
