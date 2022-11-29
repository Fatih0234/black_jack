

"""Blackjack also known as 21"""

import random, sys

# Set up the constans:

HEARTS   = chr(9829)
DIAMONDS = chr(9830)
SPADES   = chr(9824)
CLUBS    = chr(9827)

BACKSIDE = "backside"


def main():
     print("""Blackjack, by Fatih Karahan 
     
     Rules:
          Try to get as close to 21 without going over. 
          Kings, Queens, and Jacks are worth 10 points.
          Aces are worth 1 or 11 points.
          Cards 2 through 10 are worth their face value.
          (H)it to take another card.
          (S)tand to stop taking cards.
          On your first play, you can (D)ouble down to increase your bet
          but must hit exactly one more time before standing.
          In case of a tie, the bet is returned to the player.
          The dealer stops hitting at 17.""")
     money = 5000

     while True: # main game loop.
          # Check if the player has money or not.
          if money <= 0:
               print("You are brokie right now.")
               print("Good thing though, you didin't play with real money :)")
               sys.exit()

          bet = get_bet(money)

          deck = get_deck()
          dealer_hand = [deck.pop(), deck.pop()]
          player_hand = [deck.pop(), deck.pop()]
          # print(deck)
          # Take a look at player's actions

          while True:

               display_cards(player_hand, dealer_hand, False)

               if get_hand_value(player_hand) >= 21:
                    break

               # Look at player's move
               move = get_move(player_hand, money-bet)

               if move == "D":
                    additional_bet = get_bet(min(bet, money-bet))
                    bet += additional_bet
                    print(f"Bet increased to {bet}")
                    print("Bet: ", bet)

               if move in ("H", "D"):
                    #We will have to take additional card.

                    new_card = deck.pop()
                    rank, suit = new_card
                    print(f"You drew {rank} of {suit}")

                    player_hand.append(new_card)

                    if get_hand_value(player_hand) > 21:
                         continue
               if move in ("S", "D"):
                    break
          
          # Take a look at dealer's actions.

          if get_hand_value(player_hand) < 21:
               while get_hand_value(dealer_hand) < 17:
                    print("Dealer hits...")
                    dealer_hand.append(deck.pop())
                    display_cards(player_hand, dealer_hand, False)

                    if get_hand_value(dealer_hand) > 21:
                         break
                    input("Press enter for next...")
                    print()

          # Show the final results.

          display_cards(player_hand, dealer_hand, True)
          dealer_value = get_hand_value(dealer_hand)
          player_value = get_hand_value(player_hand)

          if player_value == 21 and dealer_hand != 21:
               print(f"You won {bet*1.5}, congrats!")
               money += bet*1.5

          elif player_value > 21:
               print(f"You busted! you lost {bet}")
               money -= bet 
          elif dealer_value > 21:
               print(f"You won! {bet}")
               money += bet

          elif player_value < 21 and player_value > dealer_value:
               print("You won")
               money += bet 
          elif player_value == dealer_value:
               print("It is a tie. You money got backed to you.")
               
          else:
               print("You lost!")
               money -= bet
          
          input('Press Enter to continue...')
          print('\n\n')
          
                                 


def get_deck():
     deck = []
     for suit in (SPADES, HEARTS, DIAMONDS, CLUBS):
          for rank in range(2,11):
               deck.append((str(rank), suit))
          for rank in ("K", "J", "Q", "A"):
               deck.append((str(rank), suit))

     random.shuffle(deck)
     return deck

def get_bet(max_money):

     while True: # keep iterating till you get a valid answer.
          bet = input(f"how much money do you want to put in (1-{max_money}, QUIT), > ")

          if bet == "QUIT":
               sys.exit()
          if not bet.isdecimal():
               continue
          if int(bet) <= max_money:
               return int(bet)


def display_cards(player_hand, dealer_hand, show_dealer_hand):

     if show_dealer_hand:
          print(f"DEALER: {get_hand_value(dealer_hand)}")
          display_hand(dealer_hand)

     else:
          print("DEALER: ???")
          display_hand([BACKSIDE] + dealer_hand[1:])

     print("PLAYER:", get_hand_value(player_hand))
     display_hand(player_hand)
     



def get_hand_value(cards):
     value = 0 
     number_of_aces = 0
     
     for card in cards:
          rank = card[0]
          if rank == "A":
               number_of_aces += 1
          elif rank in ("J", "K", "Q"):
               
               value += 10
          else:
               value += int(rank)

     # Handling the aces
     value += number_of_aces
     for i in range(number_of_aces):
        if value + 10 <= 21:
            value += 10
     return value
def display_hand(cards):

     rows = ["", "", "", "", ""]

     
     # print(f"This is all the cards: {cards}")
     for i, card in enumerate(cards):
          rows[0] += " ___ "
          # print(card)
          if card == BACKSIDE:
               rows[1] += "|## |"
               rows[2] += "|###|"
               rows[3] += "|_##|"

          else:
               # print(card)
               # print(type(card))
               # print(cards)
               rank, suit = card
               rows[1] += "|{} |".format(rank.ljust(2))
               rows[2] += "| {} |".format(suit)
               rows[3] += "|_{}|".format(rank.rjust(2, "_"))
     # print(f"All the rows => {rows}")
     for row in rows:
          print(row)


def get_move(player_hand, max_money):

     moves = ["(H)itting", "(S)taying"]

     if max_money > 0 and len(player_hand) == 2:
          moves.append("(D)oubling")

     txt = ", ".join(moves) 
     move = input(txt + "> ").upper()

     if move in ("H", "S"):
          return move
     
     if move == "D" and "(D)oubling" in moves:
          return move


if __name__ == "__main__":
     main()