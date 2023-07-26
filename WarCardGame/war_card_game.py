from collections import namedtuple
import random
import os
import time
import csv

class WarGame:

    """War card game with the 3 cards variantion for war and only the red suits.
    The given name will be the name of the csv file with records of how the game went."""

    _SUITS = ["Diamond","Hearts"]
    _RANKS = {"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"10":9,
              "J":10,"Q":11,"K":12,"A":13}
    _NUM_OF_CARDS = 26
    
    def __init__(self,name) -> None:

        #check that name is not empty or None
        if not len(name) or not name:
            raise ValueError("Name cannot be empty!")
        
        #csv file
        self.name = name
        self.csv_file_name = (f"{os.path.dirname(__file__)}\\game_records\\") + f"{self.name}.csv"
        self.create_csv()

        #deck
        self._deck = []
        self._create_deck()

        #cards for each player
        self._player1_cards = []
        self._player2_cards = []
        self._deal_cards()

        #won stack for each player
        self._player1_won_stack = []
        self._player2_won_stack = []

        self.game_on = True
    
    @property
    def deck(self):
        return self._deck
    
    @property
    def player1_cards(self):
        return self._player1_cards
    
    @property
    def player2_cards(self):
        return self._player2_cards
    
#<----------------DECK FUNCTIONS-------------------------------------------------->  

    def _create_deck(self) -> None:
        card = namedtuple("Card", "suit rank")
        for rank,value in (WarGame._RANKS).items():
            for suit in WarGame._SUITS:
                self._deck.append(card(suit=suit,rank={rank:value}))

    # shuffle the deck and give each player half of the cards
    def _deal_cards(self) -> None:
        random.shuffle(self.deck)
        self._player1_cards = self.deck[:WarGame._NUM_OF_CARDS//2]
        self._player2_cards = self.deck[WarGame._NUM_OF_CARDS//2:]

#<----------------CSV FILE FUNCTIONS-------------------------------------------------->  

    def create_csv(self) -> None:

        with open(self.csv_file_name,'w',encoding='utf-8') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(("Player 1 total cards","Player 2 total cards","Player 1 card","Player 2 card","Winner","War")) #field headers

    def add_round_to_csv(self,msg:list) -> None:
        """ The msg should contain in order: "Player 1 total cards","Player 2 total cards","Player 1 card","Player 2 card","Winner","War"""
        with open(self.csv_file_name,'a',encoding='utf-8') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(msg)

#<----------------CARD FUNCTIONS--------------------------------------------------> 

    # pop a card at certain index
    def reveal_card(self,player:list,index:int) -> namedtuple:
        return player.pop(index)
    
    #returns the string representation of a card plus its value
    @staticmethod
    def str_card_and_value(card: namedtuple) -> tuple:

        """ Returns (string, int) """

        card_rank = list(card.rank.items())

        return (f"{card_rank[0][0]} of {card.suit}", card_rank[0][1])
    
    #a function to change to the selected player's win stack
    def change_to_win_stack(self,player:str) -> None:

        if player == "player1":
            if not len(self._player1_won_stack):
                print(f"Player 1 doesn't have enought cards to continue!\nPlayer 2 wins!")
                time.sleep(2)
                self.game_on = False
                return
            self._player1_cards.extend(self._player1_won_stack)
            self._player1_won_stack = []
        else:
            if not len(self._player2_won_stack):
                print(f"Player 2 doesn't have enought cards to continue!\nPlayer 1 wins!")
                time.sleep(2)
                self.game_on = False
                return
            self._player2_cards.extend(self._player2_won_stack)
            self._player2_won_stack = []

#<----------------PLAY FUNCTIONS-------------------------------------------------->      
    def check_turn_winner(self,player1_card:namedtuple,player2_card:namedtuple,
                          continuing_card_index:int,war:bool = False,
                          player1_face_down_cards:list = [],player2_face_down_cards:list = []) -> None:

        #get the str representation and the value of the cards
        player1_card_rank = WarGame.str_card_and_value(player1_card)
        player2_card_rank = WarGame.str_card_and_value(player2_card)

        print("\n")

        print(f"Player 1: {player1_card_rank[0]}")
        print(f"Player 2: {player2_card_rank[0]}")

        #calculations for the csv file
        player1_total_cards = len(self.player1_cards)+len(self._player1_won_stack)+len(player1_face_down_cards) if war else len(self.player1_cards)+len(self._player1_won_stack)+1+len(player1_face_down_cards)
        player2_total_cards = len(self.player2_cards)+len(self._player2_won_stack)+len(player2_face_down_cards) if war else len(self.player2_cards)+len(self._player2_won_stack)+1+len(player2_face_down_cards)
        
        #if player 1's card is higher
        if player1_card_rank[1] > player2_card_rank[1]:
            print("Player 1's card is higher. Thus he gets the cards.")
            #append result to csv
            self.add_round_to_csv([player1_total_cards, 
                                   player2_total_cards,
                                   player1_card_rank[0], player2_card_rank[0],"Player 1",str(False)])
            #if this was a war round, remove/append multiple cards
            if war:
                self.war_round_card_removal("player1",player1_face_down_cards,player2_face_down_cards)
            else:
                #add the won card
                self._player1_won_stack.append(player2_card)
                #move winner's card also to the end of the stack
                self._player1_won_stack.append(player1_card)

        #if player 2's card is higher
        elif player1_card_rank[1] < player2_card_rank[1]:
            print("Player 2's card is higher. Thus he gets the cards.")
            #append result to csv
            self.add_round_to_csv([player1_total_cards, 
                                   player2_total_cards,
                                   player1_card_rank[0], player2_card_rank[0],"Player 2",str(False)])
            #if this was a war round, remove/append multiple cards
            if war:
                self.war_round_card_removal("player2",player1_face_down_cards,player2_face_down_cards)
            else:
                self._player2_won_stack.append(player1_card)
                self._player2_won_stack.append(player2_card)
        # last option is war
        else:
            print("WAR!")
            self.add_round_to_csv([player1_total_cards, 
                                   player2_total_cards,
                                   player1_card_rank[0], player2_card_rank[0],"None",str(True)])
            self.war(player1_card,player2_card,continuing_card_index)
        time.sleep(2)
        #after continue playing
        self.play()
    
    def war_round_card_removal(self,winner:str,player1_face_down_cards:list,player2_face_down_cards:list) -> None:
        time.sleep(2)

        # if winner is player 1, add both face down stacks to his win stack
        if winner == "player1":

            self._player1_won_stack +=(player2_face_down_cards)
            self._player1_won_stack +=(player1_face_down_cards)

        # if winner is player 2, add both face down stacks to his win stack
        else:

            self._player2_won_stack += (player2_face_down_cards)
            self._player2_won_stack += (player1_face_down_cards)

        time.sleep(2)
        # war is over so continue playing
        self.play()

    def war(self,player1_card:namedtuple,player2_card:namedtuple,continuing_card_index:int) -> None:
        # keep track of how many cards are displayed
        # start from index + 3 than the previously revealed card

        continuing_card_index += 3

        # add the cards that started the war to the face down stacks
        player1_face_down_cards = [player1_card]
        player2_face_down_cards = [player2_card]

        # add the top 3 cards of the deck + the 4th card,that is later used for comparison, to the face down stack
        # be wary of if a player needs to change to their win stack
        for _ in range(continuing_card_index+1):
            try:
                player1_face_down_cards.append(self._player1_cards.pop(0))
            # if no cards left in the stack, change to win stack
            except IndexError:
                self.change_to_win_stack("player1")
                #if the game_on has changed that means a player does not have enough cards to continue and the other player gets all the cards
                if not self.game_on:
                    self._player2_won_stack.extend(player1_face_down_cards)
                    self._player2_won_stack.extend(player2_face_down_cards) 
                    return

            try:
                player2_face_down_cards.append(self._player2_cards.pop(0))
            # if no cards left in the stack, change to win stack
            except IndexError:
                self.change_to_win_stack("player2")
                #if the game_on has changed that means a player does not have enough cards to continue
                if not self.game_on:
                    self._player1_won_stack.extend(player1_face_down_cards)
                    self._player1_won_stack.extend(player2_face_down_cards) 
                    return

        #the continious index should be back to 0
        continuing_card_index = 0

        # the face up card for comparison is actually the last card in the new face down stack
        self.check_turn_winner(player1_face_down_cards[-1],player2_face_down_cards[-1],continuing_card_index,
                               war = True,player1_face_down_cards=player1_face_down_cards,player2_face_down_cards=player2_face_down_cards)

    # main play function    
    def play(self) -> None:

        while self.game_on:
            #keeping track of which index of the cards needs to be popped
            continuing_card_index = 0

            #if one of the players has no cards change to their win stack
            if not len(self.player1_cards) and len(self._player1_won_stack):
                print("Player 1 changed to won stack!")
                self.change_to_win_stack("player1")
            
            if not len(self.player2_cards) and len(self._player2_won_stack):
                print("Player 2 changed to won stack!")
                self.change_to_win_stack("player2")
                
            print("Player 1 total cards: ",len(self._player1_cards) + len(self._player1_won_stack))
            print("Player 2 total cards: ",len(self._player2_cards) + len(self._player2_won_stack))
            #if a player has all the cards they win
            if (len(self.player1_cards) + len(self._player1_won_stack) == WarGame._NUM_OF_CARDS or len(self.player2_cards) + len(self._player2_won_stack) == WarGame._NUM_OF_CARDS):
                winner = "Player 1" if len(self.player1_cards) + len(self._player1_won_stack) == WarGame._NUM_OF_CARDS  else "Player 2"
                print(f"{winner} has all the cards and wins!")
                self.add_round_to_csv([len(self._player1_cards) + len(self._player1_won_stack),len(self._player2_cards) + len(self._player2_won_stack),
                                       "None", "None", winner, str(False)])
                time.sleep(2)
                self.game_on = False
                break
                
            #next round

            #pop the first card of the list
            player1_card = self.reveal_card(self.player1_cards,continuing_card_index)
            player2_card = self.reveal_card(self.player2_cards,continuing_card_index)

            # check who wins the turn
            self.check_turn_winner(player1_card,player2_card,continuing_card_index)

if __name__ == "__main__":
    game = WarGame("game3")
    game.play()


