import random
import os
class TicTacToe:

    ROWS = COLUMNS = 3

    def __init__(self) -> None:
        self._board = [' ']*10
        self._player1_marker = "" #either X or O
        self._player2_marker = "" #either X or O

        self.game_on = True

    @property
    def board(self):
        return self._board
    
    @property
    def player1_marker(self):
        return self._player1_marker
    
    @property
    def player2_marker(self):
        return self._player2_marker

    def player_input(self) -> None: 
        marker = input("Do you want to be X or O? ").upper().strip()
        flag = True

        # checking for correct input
        while flag:
            if marker not in ('X','O'):
                print("Wrong input!")
                marker = input("Do you want to be X or O? ").upper().strip()
            else: flag = False

        if marker == 'X':
            self._player1_marker, self._player2_marker = ('X','O')
        else: self._player1_marker, self._player2_marker = ('O','X')

    def display_board(self) -> None:
        for i in range((TicTacToe.COLUMNS*TicTacToe.ROWS),0,-3):
            print(' ' + self.board[i-2] + ' | ' + self.board[i-1] + ' | ' + self.board[i])
            #print seperator only if it is not the last row
            if i-2 != 1:
                print('-----------')

    def place_marker(self, marker:str, position:int) -> None:
        self.board[position] = marker

    def win_check(self,marker:str) -> bool:

        # row check
        for i in range(1,(TicTacToe.COLUMNS*TicTacToe.ROWS)+1,3):
            if self.board[i] == self.board[i+1] == self.board[i+2] == marker:
                return True
            
        #column check
        for i in range(1,(TicTacToe.COLUMNS)+1):
            if self.board[i] == marker and self.board[i+3] == marker and self.board[i+6] == marker:
                return True
            
        # diagonals check
        return ((self.board[1] == self.board[5] == self.board[9] == marker) or 
               (self.board[3] == self.board[5] == self.board[7] == marker))
    
    def space_check(self, position:int) -> bool:
        return self.board[position] == ' '
    
    @staticmethod
    def choose_first() -> str:
        choice = random.randint(1,2)
        if choice == 1:
            return ("Player 1","Player 2")
        else:
            return ("Player 2","Player 1")
        
    @staticmethod
    def replay() -> bool:
        flag = False
        while not flag:
            replay_choice = input("Do you want to play again? Press y for YES and n for NO: ")
            if replay_choice.lower().strip() == 'y':
                return True
            elif replay_choice.lower().strip() == 'n': return False
            else:
                print("Please enter a correct letter.")
        
    def full_board_check(self) -> bool:
        for i in range(1,(TicTacToe.COLUMNS*TicTacToe.ROWS)+1):
            if self.space_check(i):
                return False
        return True
    
    def player_choice(self,player_marker:str) -> None:
        flag = False
        while not flag:
            try:
                pos = int(input("Please choose a number from 1-9: "))
                if pos >0 and pos<10 and self.space_check(pos):
                    self.place_marker(player_marker,pos)
                    flag = True
                else:
                    print("That is an imposible move. Try again.")
            except ValueError:
                print("You didn't enter a number. Try again.")

    def win_msg(self,msg:str) -> None:
        os.system('cls')
        self.display_board()
        print(msg)
        self.game_on = False

    def game_round(self,turn_player:str) -> None:
        marker = self.player1_marker if turn_player == "Player 1" else self.player2_marker

        print(f"{turn_player}'s turn:")
        self.player_choice(marker)
        self.display_board()

        if self.win_check(marker):
            self.win_msg(f"Congradulations {turn_player}. You Won!")
        elif self.full_board_check():
            self.win_msg("The board is full so it is a draw.")

    def play(self) -> None:
        # clearing the screen
        os.system('cls')

        self.player_input()
        turns = self.choose_first()
        rotator = 0 #to help rotate through the turns

        while self.game_on:
            # clearing the screen
            os.system('cls')
            self.display_board()

            print(f"Player 1 is {self.player1_marker}, Player 2 is {self.player2_marker}")
            self.game_round(turns[rotator%len(turns)])
            rotator +=1

        # when the game is over ask the player if they want to restart
        if TicTacToe.replay():
            # reset some values
            self._board = [' ']*10
            self.game_on = True
            self.play()
        else: print("Thank you for playing")

if __name__ == "__main__":
    game = TicTacToe()
    game.play()

