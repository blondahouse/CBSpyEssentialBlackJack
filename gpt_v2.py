# This is an example of a Blackjack game in Python
from random import shuffle


# Classes
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(value, suit) for suit in suits for value in values]

    def __repr__(self):
        return f"Deck of {self.count()} cards"

    def count(self):
        return len(self.cards)

    def _deal(self, num):
        count = self.count()
        actual = min([count, num])
        if count == 0:
            raise ValueError("All cards have been dealt")
        cards = self.cards[-actual:]
        self.cards = self.cards[:-actual]
        return cards

    def deal_card(self):
        return self._deal(1)[0]

    def deal_hand(self, hand_size):
        return self._deal(hand_size)

    def shuffle(self):
        if self.count() < 52:
            raise ValueError("Only full decks can be shuffled")
        shuffle(self.cards)
        return self


# Set up the game
deck = Deck()
deck.shuffle()
player_hand = deck.deal_hand(2)
dealer_hand = deck.deal_hand(2)


# Play the game
# Score the hands
# The highest score of a single round of Blackjack is 21.
# A hand with one card with a value of 11 is called a blackjack or natural.
def score_hand(hand):
    # Calculate the total score of all cards in the list
    # Only one ace can have the value 11, and this will be reduced to 1 if the hand
    # would otherwise exceed 21
    score = 0
    ace = False
    for card in hand:
        if card.value == 'A':
            ace = True
        elif card.value in ('J', 'Q', 'K'):
            score += 10
        else:
            score += int(card.value)
    if ace and score <= 11:
        score += 11
    elif ace and score > 11:
        score += 1
    return score


# Take hits
def hit(deck, hand):
    single_card = deck.deal_card()
    hand.append(single_card)
    return hand


# Visualize the current hands
def show_some(player, dealer):
    print("\nDealer Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer Hand:", *player_hand, sep='\n ')


def show_all(player, dealer):
    print("\nDealer Hand:", *dealer_hand, sep='\n ')
    print("Dealer Score:", score_hand(dealer_hand))
    print("\nPlayer Hand:", *player_hand, sep='\n ')
    print("Player Score:", score_hand(player_hand))


# Handle end of game scenarios
while True:
    print("\nPlayer Score:", score_hand(player_hand))
    player_choice = input("Do you want to [H]it or [S]tand? ")
    if player_choice.lower() == 'h':
        hit(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if score_hand(player_hand) > 21:
            print("Player busts!")
            break
    elif player_choice.lower() == 's':
        while score_hand(dealer_hand) < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)
        if score_hand(dealer_hand) > 21:
            print("Dealer busts!")
            break
        elif score_hand(player_hand) == score_hand(dealer_hand):
            print("It's a tie!")
        elif score_hand(player_hand) > score_hand(dealer_hand):
            print("You win!")
        else:
            print("Dealer wins!")
        break
