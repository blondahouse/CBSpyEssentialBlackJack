class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # comparing two cards
    def __cmp__(self, other):
        # check the suits
        if self.suit > other.suit:
            return 1
        if self.suit < other.suit:
            return -1
        # check the ranks
        if self.rank > other.rank:
            return 1
        if self.rank < other.rank:
            return -1
        # otherwise they are equal
        return 0


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    # shuffle the cards
    def shuffle(self):
        import random
        random.shuffle(self.cards)

    # deal a card from the deck
    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = False

    def add_card(self, card):
        self.cards.append(card)
        # calculate value
        if card.rank > 9:
            self.value += 10
        elif card.rank == 1:
            self.value += 11
            self.ace = True  # track ace
        else:
            self.value += card.rank

    # adjust value with ACE as 1 when needed
    def adjust_ace(self):
        while self.value > 21 and self.ace:
            self.value -= 10
            self.ace = False


# Player Class
class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []

    # A method to add a card to the player's hand
    def draw_card(self, card):
        self.hand.append(card)

    # A method to show what cards the player has
    def show_hand(self):
        print(f"{self.name}'s Hand: {self.hand}")


# Dealer Class
class Dealer:
    def __init__(self):
        self.hand = []

    # A method to add a card to the dealer's hand
    def draw_card(self, card):
        self.hand.append(card)

    # A method to show what cards the dealer has
    def show_hand(self):
        print(f"Dealer's Hand: {self.hand}")


# Game Class
class Game:
    def __init__(self):
        self.deck = []
        self.player = None
        self.dealer = Dealer()

    # A method to initialize the game
    def start_game(self, player):
        self.player = player
        self.deal_cards()

    # A method to deal cards
    def deal_cards(self):
        self.player.draw_card(self.deck.pop())
        self.dealer.draw_card(self.deck.pop())
        self.player.draw_card(self.deck.pop())
        self.dealer.draw_card(self.deck.pop())

    # A method to show the cards
    def show_cards(self):
        self.player.show_hand()
        self.dealer.show_hand()
