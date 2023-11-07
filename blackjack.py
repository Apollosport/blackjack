'''
Basic little Blackjack game with no regards to the advanced blackjack rules e.g. splitting.
Author: Timon Schell
Website: https://timonschell.com
'''

import random

suits: dict = ('♥', '♦', '♠', '♣')
ranks: dict = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values: dict = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

def scroll_up() -> None:
    print("\n"*50)

class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit:str = suit
        self.rank:str = rank
        self.value: int = values[rank.title()]       
    def __str__(self):
        return self.rank+" of "+self.suit

class Deck:
    def __init__(self) -> None:
        self.all_cards: list = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
        self.shuffle()
        
    def shuffle(self) -> None:
        random.shuffle(self.all_cards)

    def deal_one(self) -> Card:
        return self.all_cards.pop()
    
class Account:
    def __init__(self, amount: int) -> None:
        self.amount: int = amount
        print(self.__str__())        

    def __str__(self) -> str:
        return 'You have $'+str(self.amount)+' in your account!'
    
    def add_money(self, amount: int)-> None:
        self.amount+=amount
        print(self.__str__())

    def subtract_money(self, amount: int) -> None:
        if self.amount < amount:
            print("Insufficient funds!")
            return
        self.amount-=amount
        print(self.__str__())

class Hand:
    def __init__(self) -> None:
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card: Card)-> None:
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces+=1

    def return_value(self)-> int :
        while self.value > 21 and self.aces:
            self.value-= 10
            self.aces-=1
        return self.value
    
def show_cards(player_cards: [Card], player_value: int, dealer_cards: [Card], money_bet: int) -> None:
    scroll_up()
    print(f"You got ${money_bet} riding on this!")
    print("The House has: ", end = '')

    for card in dealer_cards:
        print(card,end = '. ')
    print("\n")

    print("You have: ", end = '')
    for card in player_cards:
        print(card,end = '. ')
    print("\n")
    print(f"Current maximum card value: {player_value}")

scroll_up()
print('°~-Welcome to Jack Blacks Blackjack-~°')
card_deck = Deck()
player = Account(100)
game_on: bool = True

while game_on:
    if len(card_deck.all_cards) < 20:
        card_deck = Deck()
        print('New deck of cards applied!')
    if player.amount == 0:
        print('Dude...get your broke ass out of here. As they say in bavaria: "Zupf di!"')
        game_on == False
        break

    player_cards = Hand()
    dealer_cards = Hand()
    money_bet: int = 0
    while True:
        money_bet = (input('How much do you want to bet?\n'))
        if money_bet.isdigit():            
            money_bet = int(money_bet)
            if money_bet > player.amount:
                scroll_up()
                print("Insufficient funds!!!")
                print(player)
                money_bet = 0
            if money_bet > 0: 
                player.subtract_money(money_bet)
                print(f'You bet ${money_bet}!')      
                break
            else:
                print(f"Please enter a number from $1 to ${player.amount}!")
        else:
            print(f"Please enter a number from $1 to ${player.amount}!")
    
    player_cards.add_card(card_deck.deal_one())
    dealer_cards.add_card(card_deck.deal_one())
    player_cards.add_card(card_deck.deal_one())
    dealer_cards.add_card(card_deck.deal_one())

    show_cards(player_cards.cards, player_cards.return_value(), [dealer_cards.cards[0]], money_bet)

    push_on: bool = True

    while push_on:
        if player_cards.return_value()>21:        
            print('You overreached 21 and lost!')            
            push_on = False
            break
        choice = (input('Do you want another card? (H for hit & S for stay)')).upper()
        if choice[0] == "S":
            push_on = False
            break
        if choice[0] == "H":
            player_cards.add_card(card_deck.deal_one())
            show_cards(player_cards.cards, player_cards.return_value(), [dealer_cards.cards[0]], money_bet)
    
    house_always_wins = True
    while house_always_wins:
        if player_cards.return_value()>21:
            house_always_wins = False
            break
        if dealer_cards.return_value()>21:
            show_cards(player_cards.cards, player_cards.return_value(), dealer_cards.cards, money_bet)
            print("The house overreached and lost!")
            player.add_money(2*money_bet)
            house_always_wins = False
            break        
        if dealer_cards.return_value()>player_cards.return_value():
            show_cards(player_cards.cards, player_cards.return_value(), dealer_cards.cards, money_bet)
            print("The House wins and you lost")
            house_always_wins = False
            break
        dealer_cards.add_card(card_deck.deal_one())
        



            


    

    


