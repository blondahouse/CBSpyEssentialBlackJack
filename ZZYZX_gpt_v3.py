# Card class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"


# Deck Class
class Deck:
    suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
    values = [x + 1 for x in range(13)]

    def __init__(self):
        self.deck = []
        for suit in self.suits:
            for value in self.values:
                self.deck.append(Card(suit, value))


# Hand Class
class Hand:
    def __init__(self):
        self.hand = []

    def draw_from(self, deck):
        drawn_card = deck.deck.pop()
        self.hand.append(drawn_card)
        return drawn_card

    def total(self):
        total = 0
        for card in self.hand:
            if 1 <= card.value < 11:
                total += card.value
            elif card.value == 11 or card.value == 12 or card.value == 13:
                total += 10
            else:
                print("Ace value was encountered - it can take value 1 or 11")
                ace = int(input("Enter 1 or 11 as a value of Ace "))
                total += ace
        return total


# Player Class
class Player:
    def __init__(self):
        self.balance = 100
        self.total = 0
        self.bust = False
        self.blackjack = False

    def bet(self, amount):
        self.balance -= amount
        return self.balance

    def hit(self, deck):
        new_card = Hand().draw_from(deck)
        self.total = Hand().total()
        if 21 < self.total:
            self.bust = True
        elif self.total == 21:
            self.blackjack = True
        return new_card

    def draw(self, deck):
        card = Hand().draw_from(deck)
        self.total = Hand().total()
        return card
    # Dealer Class


class Dealer:
    def __init__(self):
        self.total = 0

    def hit(self, deck):
        new_card = Hand().draw_from(deck)
        self.total = Hand().total()
        return new_card
    # Game Class


class Game:
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer

    def play_game(self, player, dealer):
        # initial betting
        bet = int(input("How much do you want to bet? "))
        player.bet(bet)
        # player draws cards
        for _ in range(2):
            card = player.draw(deck)
            print(f"You have been dealt {card}")
        # setup completed
        while not self.player.bust and not self.player.blackjack:
            action = input("Do you want to hit or stand? Type 'hit' or 'stand' \n")
            if action == "hit":
                card = player.hit(deck)
                print(f"You have been dealt {card}")
            elif action == "stand":
                break
                # dealer's turn
        while self.dealer.total <= 16:
            card = self.dealer.hit(deck)
            print(f"Dealer has been dealt {card}")
        print(f"Dealer's total is {dealer.total}")
        print(f"Your total is {player.total}")
        # determining the winner
        if self.player.blackjack:
            print("Blackjack!! With 21, you win")
            player.balance += (bet * 2)
        elif self.player.bust:
            print("You busted!")
        elif self.dealer.total > 21:
            print("The dealer busted! You win!")
            player.balance += (bet * 2)
        elif self.dealer.total < player.total:
            print("Your total is higher than the dealers! You Win!")
            player.balance += (bet * 2)
        elif self.dealer.total > player.total:
            print("Your total is lower than the dealers! You Lose!")
        elif self.dealer.total == player.total:
            print("It's a tie! You get your bet back")
            player.balance += bet
        print(f"Your current balance is {player.balance}")


if __name__ == "__main__":
    deck = Deck()
    player = Player()
    dealer = Dealer()
    blackjack = Game(player, dealer)
    blackjack.play_game(player, dealer)
