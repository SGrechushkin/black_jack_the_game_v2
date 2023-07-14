from class_render1 import Deck
from class_render1 import Card
from class_render1 import Player
from class_render1 import Dealer
from class_render1 import Money
from class_render1 import PlayBoard
import turtle

# -*- coding: utf-8 -*-

money = Money(0, 1000)
game_on = True

while game_on:
    wn = turtle.Screen()
    wn.bgcolor("green")
    wn.setup(800, 600)
    wn.title("Play Board")
 
    if not game_on:
        wn.bye()

    def play_game():
        deck = Deck()
        deck.shuffle()
        play_board = PlayBoard(money)

        dealer = Dealer("Dealer", play_board)
        player = Player("Player", play_board)
        player.add_card(deck.deal_one())
        player.add_card(deck.deal_one())
        dealer.start_add_card(deck.deal_one())
        dealer.start_add_card(deck.deal_one())

        def play_again():
            play_again = turtle.textinput("Blackjack", "Do you want play_again? (y/n): ")
            if play_again.lower() == "y":
                return True
            else:
                game_on = False

        player.show_hand()
        amount =turtle.textinput(f"Blackjack", "You got " + str(money.balance) + " credits. Make your Bet: ")
        if int(amount) >= 0:
            money.bet(amount)
            play_board.render_money("Player")
        else:
             amount = int(turtle.textinput("Blackjack", "Make your Bet: "))

        while not player.has_lost():
            player.show_hand()
            choice = turtle.textinput("Blackjack", "Take another card? (y/n)") # ��� ���������� ����� � ²�Ͳ, ����� ������� ��� � ����� ����� ��� � ²����
            if choice.lower() == "y":
                player.add_card(deck.deal_one())
            else:
                break

        if player.has_lost():
            print(f"Player got over 21 and lost!")
            money.lose()
            return play_again()
        else:
           dealer.show_hand()
           while dealer.calculate_hand_value() <= player.calculate_hand_value():
                dealer.add_card(deck.deal_one())
                dealer.show_hand() 
           if dealer.calculate_hand_value() == 21:
                money.lose()
                print("Dealer got Black Jack!")
                return play_again()
           elif dealer.calculate_hand_value() > 21:
               money.win()
               print(f"Dealer got {dealer.calculate_hand_value()} and lost!")
               return play_again()
           else:
                if dealer.calculate_hand_value() > player.calculate_hand_value() and dealer.calculate_hand_value() <= 21:
                    money.lose()
                    print(f"{dealer.calculate_hand_value()} > {player.calculate_hand_value()} dealer wins!")
                    return play_again()
                elif player.calculate_hand_value() > dealer.calculate_hand_value() and player.calculate_hand_value() <= 21:
                    money.win()
                    print(f"{player.calculate_hand_value()} > {dealer.calculate_hand_value()} player wins!")
                    return play_again()
 
    game_on = play_game()
    wn.clear()




