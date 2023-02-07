from random import random








class Game:
    def __init__(self, bj_setup):
        self.bj_setup = bj_setup
        self.shoe = Shoe(bj_setup.get("rules").get("dealing shoe"))
        self.dealer = Dealer("Dealer", 0)
        self.players = []
        for i in range(1, 8):
            base = bj_setup.get("bases").get(f"base #{i}")
            if base.get("player") == "yes":
                self.players.append(Player(base.get("nickname"), base.get("bankroll")))

    def __repr__(self):
        return f'Game({self.bj_setup})'

    def __str__(self):
        return f'Game({self.bj_setup})'

    def __len__(self):
        return len(self.players)

    def __getitem__(self, item):
        return self.players[item]

    def __setitem__(self, key, value):
        self.players[key] = value

    def __delitem__(self, key):
        del self.players[key]

    def deal(self):
        for i in range(2):
            for player in self.players:
                player.hand.append(self.shoe.draw())
            self.dealer.hand.append(self.shoe.draw())

    def hit(self, player):
        player.hand.append(self.shoe.draw())

    def hit_or_stand(self, player):
        while True:
            x = input(f'Hit or Stand? Enter h or s: ')
            if x[0].lower() == 'h':
                self.hit(player)
            elif x[0].lower() == 's':
                print("Player Stands. Dealer's Turn")
                break
            else:
                print("Sorry, please try again.")
                continue
            break

    def show_some(self):
        print("\nDealer's Hand:")
        print(" <card hidden>")
        print('', self.dealer.hand[1])
        print("\nPlayer's Hand:", *self.players[0].hand, sep='\n ')
        print(f"Player's Hand =", self.players[0].hand.value)

    def show_all(self):
        print("\nDealer's Hand:", *self.dealer.hand, sep='\n ')
        print(f"Dealer's Hand =", self.dealer.hand.value)


if __name__ == "__main__":
    pass
