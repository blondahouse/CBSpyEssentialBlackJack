from itertools import product
import random

from const import SUITS, RANKS


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # self.value = value

    def show_card(self):
        print(f'{self.rank} of {self.suit}')


class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()
        self.shuffle_deck()

    def build_deck(self):
        for suit, rank in product(SUITS, RANKS):
            # if rank == "Ace":
            #     value = 11
            # elif rank.isdigit():
            #     value = int(rank)
            # else:
            #     value = 10
            self.cards.append(Card(suit=suit, rank=rank))

    def show_deck(self):
        for card in self.cards:
            card.show_card()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        # calculate value of hand
        if card.rank == "Ace":
            self.aces += 1
        self.value += card.value
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def get_value(self):
        return self.value
