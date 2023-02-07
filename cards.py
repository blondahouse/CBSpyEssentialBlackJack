import random

from constants import SUITS, RANKS, VALUES, SHOE


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES.get(rank)

    def __repr__(self):
        return f'{self.rank}{self.suit}'

    def __str__(self):
        return f'{self.rank}{self.suit}'


class CutCard(Card):
    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        self.value = 0

    def __repr__(self):
        return f'XX'

    def __str__(self):
        return f'XX'


class Shoe:
    def __init__(self, setup):
        self.decks = SHOE.get(setup.get("rules").get("dealing shoe"))
        self.cards = []
        # self.build()
        # self.shuffle(setup)
        self.reshuffle = True

    def __len__(self):
        return len(self.cards)

    def clear(self):
        self.cards = []

    def build(self):
        for i in range(self.decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(suit, rank))

    def shuffle(self, setup):
        self.clear()
        self.build()
        cut_card = setup.get("rules").get("cut-card")
        random.shuffle(self.cards)
        if cut_card:
            position = range(15, len(self.cards) - 16) if self.decks <= 2 else range(78, len(self.cards) - 79)
            position = random.choice(position)
            self.cards.insert(position, CutCard('XX', 'XX'))
            self.reshuffle = False
        else:
            self.reshuffle = True

    def draw(self):
        card = self.cards.pop()
        if isinstance(card, CutCard):
            card = self.cards.pop()
            self.reshuffle = True
        return card
