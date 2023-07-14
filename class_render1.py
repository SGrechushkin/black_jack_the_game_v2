
import random
import tkinter as tk
import turtle
suits = ('\u2665', '\u2666', '\u2660', '\u2663')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
render_rank = {'Two':"2", 'Three':"3", 'Four':"4", 'Five':"5", 'Six':"6", 'Seven':"7", 'Eight':"8", 
            'Nine':"9", 'Ten':"10", 'Jack':"J", 'Queen':"Q", 'King':"K", 'Ace':"A"}
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':[1,11]}

class Card:
    #Creating cards
    def __init__(self,suit, rank):
        self.suit = suit
        self.rank = rank
        self.render_rank = render_rank[rank]
        self.values= values[rank]
    def __str__(self):
        return self.rank + " of " + self.suit
    #Rendering cards
    def render(self, x, y, pen):
        pen.penup()
        pen.goto(x, y)
        pen.color("white")
        pen.goto(x-100, y+250)
        pen.pendown()
        pen.goto(x-50, y+250)
        pen.goto(x-50, y+175)
        pen.goto(x-100, y+175)
        pen.goto(x-100, y+250)
        pen.penup()
        #Draw rank in the top corner
        pen.color("white")
        pen.goto(x-96, y+232)
        pen.pendown()
        pen.write(self.render_rank, False, font =("Courier New", 13, "normal"))
        pen.penup()
        pen.goto(x-96, y+218)
        pen.pendown()
        pen.write(self.suit, False, font =("Courier New", 13, "normal"))
        pen.penup()
        #Draw suit in the middle
        pen.goto(x-82, y+195)
        pen.pendown()
        pen.write(self.suit, False, font =("Courier New", 25, "normal"))
        pen.penup()
           
class Deck:
    #Creating deck
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
    #Deck shuffle
    def shuffle(self):
        random.shuffle(self.all_cards)
    #Grabbing one card
    def deal_one(self):
        return self.all_cards.pop()


class Player:
    #Creating Player
    def __init__(self, name,play_board):
        self.name = name
        self.hand  = []
        self.play_board = play_board

    def add_card(self, card):
        self.hand.append(card)
        self.play_board.render_card_Player(self.name, card) #working

    def show_hand(self):
        self.play_board.render_hand(self.name, self.hand)
        print(f"{self.name}'s hand value {self.calculate_hand_value()}:")
        for card in self.hand:
            print(f"{card}, card value: {card.values}")

    def calculate_hand_value(self):
        hand_value = 0
        num_aces = 0

        for card in self.hand:
            if card.rank == 'Ace':
                num_aces += 1
            else:
                hand_value += card.values

        for _ in range(num_aces):
            if hand_value + values['Ace'][1] <= 21:
                hand_value += values['Ace'][1]
            else:
                hand_value += values['Ace'][0]

        return hand_value


    def has_lost(self):
        return self.calculate_hand_value() > 21
        play_again = input("Do you want play_again? (y/n): ")
        if play_again == 'y':
            game_on = True
        else:
            game_on = False
    
    def __str__(self):
        return self.calculate_hand_value

class Dealer:
    #Creating dealer
    def __init__(self, name, play_board):
        self.name = name
        self.hand = []
        self.play_board = play_board

    def start_add_card(self, card):
        self.hand.append(card)

    def add_card(self, card):
        self.hand.append(card)
        self.play_board.render_card_Dealer(self.name, card)

    def show_hand(self):
        self.play_board.render_hand(self.name, self.hand)
        print(f"Dealer's hand value {self.calculate_hand_value()}:")
        for card in self.hand:
            print(f"{card}, card value: {card.values}")
            if self.name == "Dealer" and len(self.hand) <=2:
                self.play_board.render_card_Dealer(self.name, card)


    def calculate_hand_value(self):
        hand_value = 0
        num_aces = 0

        for card in self.hand:
            if card.rank == 'Ace':
                num_aces += 1
            else:
                hand_value += card.values

        for _ in range(num_aces):
            if hand_value + values['Ace'][1] <= 21:
                hand_value += values['Ace'][1]
            else:
                hand_value += values['Ace'][0]

        return hand_value

    def has_lost(self):
        return self.calculate_hand_value() > 21
        play_again = input("Do you want play_again? (y/n): ")
        if play_again == 'y':
            game_on = True
        else:
            game_on = False

class Money:
    def __init__(self,bank,balance):
        self.bank = bank
        self.balance = balance
    def __str__(self):
        return f"Payer balance: {self.balance}", f"Bank balance: {self.bank}"
    def win(self):
        self.balance = self.balance + self.bank
        print(f"You win: {self.bank}! Payer balance: {self.balance}")
    def lose(self):
        self.bank = 0
        print(f"You lose! Payer balance: {self.balance}")
    def bet(self,amount):
        if int(amount) <= self.balance:
            self.balance = self.balance - int(amount)
            self.bank = int(amount)*2
            print(f"Bet Accepted {amount}")
            print(f"Your balance {self.balance}")
        else:
            print("Funds Unavailable!")
            pass

class PlayBoard:
    def __init__(self, money):
        self.money = money
        self.card_positions = {
            "Player": (-200, -200),  # Позиція тексту гравця
            "Dealer": (-200, +230),  # Позиція тексту дилера
        }
        self.hand_positions = {
            "Player": (+46, -435),  # Позиція карт гравця
            "Dealer": (+46, 0),  # Позиція карт дилера
        }
        self.game_positions = {
            "Player": (-0, -0),  # Позиція тексту гравця
           
        }
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.hideturtle()
        self.hit_button = None

    def render_money(self, Player):
        position = self.card_positions[Player]
        x,y = position[0], position[1] +23
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        #self.pen.clear()
        self.pen.write(f"Balance: {self.money.balance}", False, font=("Courier New", 13, "normal"))
        self.pen.penup()
        self.pen.goto(-300, 0)
        self.pen.pendown()
        self.pen.write(f"Bank: {self.money.bank}", False, font=("Courier New", 13, "normal"))

    def render_card_Player(self, Player, card):
        position = self.hand_positions[Player]
        x, y = position[0], position[1]
        card.render(x, y, self.pen)
        self.hand_positions[Player] = (x + 55, y)  # Збільшуємо значення x на 50 одиниць для наступної карти

    def render_card_Dealer(self, player_name, card):
        position = self.hand_positions[player_name]
        x, y = position[0], position[1]
        if player_name == "Dealer":
            card.render(x, y, self.pen)
        self.hand_positions[player_name] = (x + 55, y)  # Збільшуємо значення x на 50 одиниць для наступної карти"""

    def render_hand(self, player_name, hand):
        position = self.card_positions[player_name]
        #sore = self.calculate_hand_value(player_name)
        x, y = position[0], position[1]
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.write(f"{player_name}'s hand: ", False, font=("Courier New", 13, "normal"))
        #self.pen.write(score)
        self.pen.penup()
        y -= 30
        for card in hand:
            self.pen.goto(x, y)
            self.pen.pendown()
            self.pen.write(str(card), False, font=("Courier New", 13, "normal"))
            self.pen.penup()
            y -= 20

class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = 100
        self.height = 50

    def draw(self):
        turtle.penup()
        turtle.goto(self.x, self.y)
        turtle.pendown()
        turtle.setheading(0)
        turtle.fillcolor("white")
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(self.width)
            turtle.left(90)
            turtle.forward(self.height)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()
        turtle.goto(self.x + self.width / 2, self.y + self.height / 2)
        turtle.write(self.text, align="center", font=("Arial", 12, "normal"))

    def is_clicked(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height







