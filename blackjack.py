'''
Basic little Blackjack game with no regards to the advanced blackjack rules e.g. splitting.
Author: Timon Schell
Website: https://timonschell.com
'''

import random

suits = ('♥', '♦', '♠', '♣')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

def scroll_up() -> None:
    print("\n"*50)

class Card:
    def __init__(self, suit, rank) -> None:
        self.suit = suit
        self.rank = rank
        self.value = values[rank.title()]       
    def __str__(self):
        return self.rank+" of "+self.suit

class Deck:
    def __init__(self) -> None:
        self.all_cards = []
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
    def __init__(self, amount) -> None:
        self.amount = amount
        print(self.__str__())        

    def __str__(self) -> str:
        return 'You have $'+str(self.amount)+' in your account!'
    
    def add_money(self, amount)-> None:
        self.amount+=amount
        print(self.__str__())

    def subtract_money(self, amount) -> None:
        if self.amount < amount:
            print("Insufficient funds!")
            return
        self.amount-=amount
        print(self.__str__())

def show_cards(player_cards, dealer_cards, money_bet) -> None:
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

def check_cards(cards) -> (int,int):
    return_value = 0
    return_value_1 = 0
    for card in cards:
        if card.value == 11:            
            return_value_1 += 1
        else:
            return_value_1 += card.value
        return_value += card.value
    return (return_value, return_value_1)

def highest_under_21(cards) -> bool:
    return max(check_cards(cards)) if max(check_cards(cards)) < 22 else min(check_cards(cards))

def house_wins(player_cards, dealer_cards) -> bool:
    return highest_under_21(dealer_cards) > highest_under_21(player_cards)

scroll_up()
print('°~-Welcome to Jack Blacks Blackjack-~°')
card_deck = Deck()
player = Account(100)
game_on = True

while game_on:
    if len(card_deck.all_cards) < 20:
        print(len(card_deck.all_cards))
        card_deck = Deck()
        print('New deck of cards applied!')
        print(len(card_deck.all_cards))
    if player.amount == 0:
        print('Dude...get your broke ass out of here. As they say in bavaria: "Zupf di!"')
        game_on == False
        break

    player_cards = []
    dealer_cards = []
    money_bet = 0
    while True:
        money_bet = (input('How much do you want to bet?\n'))
        if money_bet.isdigit():            
            money_bet = int(money_bet)
            if money_bet > player.amount:
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
    
    player_cards.append(card_deck.deal_one())
    dealer_cards.append(card_deck.deal_one())
    player_cards.append(card_deck.deal_one())
    dealer_cards.append(card_deck.deal_one())

    show_cards(player_cards, [dealer_cards[0]], money_bet)

    push_on = True

    while push_on:
        if min(check_cards(player_cards))>21:
            print('You overreached 21 and lost!')            
            push_on = False
            break
        choice = (input('Do you want another card? (H for hit & S for stay)')).upper()
        if choice == "S":
            push_on = False
            break
        if choice == "H":
            player_cards.append(card_deck.deal_one())
            show_cards(player_cards, [dealer_cards[0]], money_bet)

    house_always_wins = True
    while house_always_wins:
        if min(check_cards(player_cards))>21:
            house_always_wins = False
            break
        if min(check_cards(dealer_cards))>21:
            show_cards(player_cards, dealer_cards, money_bet)
            print("The house overreached and lost!")
            player.add_money(2*money_bet)
            house_always_wins = False
            break        
        if house_wins(player_cards, dealer_cards):
            show_cards(player_cards, dealer_cards, money_bet)            
            print("The House wins and you lost")
            house_always_wins = False
            break
        dealer_cards.append(card_deck.deal_one())
        



            


    

    


