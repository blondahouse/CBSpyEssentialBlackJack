import re

from colorama import Fore

from cards import Shoe
from constants import BJ_SETUP_DEFAULT, PLAYERS, PAYOUT
from players import Dealer, Player, PlayerHand, BotRandomStrategyHand, BotBasicStrategyHand


class Game:
    def __init__(self):
        self.setup = BJ_SETUP_DEFAULT
        self.players = []
        self.dealer = Dealer('Dealer', 0)
        self.shoe = Shoe(self.setup)
        self.bases = self.setup.get("bases")
        self.is_players = True
        self.losers = []
        self.winners = []

    def setup_game(self):
        def highlight(text, color):
            return f'{color}{text}{Fore.RESET}'

        def print_bases():
            print('bases:')

            def width(key):
                w = 0
                for d in self.bases.values():
                    t = len(d.get(key).strip())
                    w = t if w < t else w
                return w

            for base, setting in self.bases.items():
                print(f'\t{base + " " * 3}', end='')
                for i, (prop, value) in enumerate(setting.items()):
                    code = base[0].upper() + base[-1].upper() + prop[0].upper()
                    code = highlight(code, Fore.YELLOW)
                    c = width(prop)
                    symbols = c + 3 if i < len(setting) - 1 else c
                    print(f'{code} {prop}: {value: <{symbols}}', end='')
                print(f'')
            print()

        def print_rules():
            print('rules:')

            items = []
            for i, (rule, option) in enumerate(self.setup.get("rules").items()):
                rl_symbols = max(map(lambda x: len(x), self.setup.get("rules").keys())) + 1
                op_symbols = max(map(lambda x: len(x), self.setup.get("rules").values()))
                text = f'R{i + 1:02} '
                text = highlight(text, Fore.YELLOW)
                text += f'{rule: <{rl_symbols}}  {option: <{op_symbols}}'
                items.append(text)

            text_to_print = ''
            for row in range(abs(-len(items) // 2)):
                text_to_print += f'\t{items[row]}'
                shift = row + abs(-len(items) // 2)
                if shift <= len(items) - 1:
                    text_to_print += f'    {items[shift]}'
                text_to_print += f'\n'
            print(text_to_print)

        print_bases()
        print_rules()

    def create_players(self):
        for base in self.bases.values():
            nickname = base.get("nickname")
            bankroll = base.get("bankroll")
            bankroll = int(re.sub(r'\D', '', bankroll))
            if base.get("player") == PLAYERS.get("#1"):
                self.players.append(Player(nickname, bankroll, PlayerHand))
            if base.get("player") == PLAYERS.get("#2"):
                self.players.append(Player(nickname, bankroll, BotRandomStrategyHand))
            if base.get("player") == PLAYERS.get("#3"):
                self.players.append(Player(nickname, bankroll, BotBasicStrategyHand))

    def remove_losers(self):
        for index, player in enumerate(self.players):
            if player.bankroll <= 100:
                self.losers.append(self.players.pop(index))

    def remove_winners(self):
        for index, player in enumerate(self.players):
            if player.bankroll >= player.start_bankroll * 2:
                self.winners.append(self.players.pop(index))

    # def create_dealer(self):
    #     self.dealer = Dealer('Dealer', 0)

    def ask_for_bets(self):
        for player in self.players:
            player.place_bet()

    def deal_cards(self):  # TODO: no hole card for dealer
        for player in self.players:
            for hand in player.hands:
                hand.add_card(self.shoe.draw())
                hand.add_card(self.shoe.draw())
        self.dealer.hands[0].add_card(self.shoe.draw())
        self.dealer.hands[0].add_card(self.shoe.draw())

    def ask_for_actions(self):  # TODO: check if the dealer has blackjack

        def hit(h):
            h.add_card(self.shoe.draw())
            h.is_first_decision = False
            if not h.stand:
                self.is_players = True

        def stand(h):
            h.stand = True

        def double(p, h):
            p.bankroll -= h.bet
            h.bet *= 2
            h.add_card(self.shoe.draw())
            h.is_first_decision = False
            h.stand = True

        def split(p, h):
            p.hands.append(h.__class__())
            p.bankroll -= h.bet
            p.hands[-1].bet = h.bet
            p.hands[-1].add_card(h.cards.pop())
            p.hands[-1].add_card(self.shoe.draw())
            h.add_card(self.shoe.draw())

            if h.cards[0].rank == 'A' and not self.setup.get("rules").get('re-splitting aces'):
                h.stand = True
                p.hands[-1].stand = True
            else:
                h.is_first_decision = True
                p.hands[-1].is_first_decision = True

        def surrender():  # TODO: surrender
            pass

        def insurance():  # TODO: insurance
            pass

        for player in self.players:
            for hand in player.hands:
                dealer_card = self.dealer.hands[0].cards[0]
                setup = self.setup
                num_of_hands = len(player)
                bankroll = player.bankroll
                action = hand.action(dealer_card, setup, num_of_hands, bankroll)
                match action:
                    case 'hit':
                        hit(hand)
                    case 'stand':
                        stand(hand)
                    case 'double':
                        double(player, hand)
                    case 'split':
                        split(player, hand)
                    case 'surrender':
                        surrender()
                    case 'insurance':
                        insurance()

    def print_players(self):
        for player in self.players:
            print(player, end=': ')
            for hand in player.hands:
                print(hand)

    def dealer_action(self):
        soft_17 = 17 if self.setup.get("rules").get('dealer hits on soft 17') else 16
        while self.dealer.hands[0].value <= soft_17:
            self.dealer.hands[0].add_card(self.shoe.draw())

    def payout(self):
        for player in self.players:
            for hand in player.hands:
                dealer = self.dealer.hands[0]

                win_blackjack_payout_condition = hand.is_blackjack and not dealer.is_blackjack
                if win_blackjack_payout_condition:
                    win_rate = hand.bet + hand.bet * PAYOUT.get(self.setup.get("rules").get('blackjack payout'))
                    player.bankroll += win_rate
                    self.dealer.bankroll -= win_rate
                    hand.bet = 0

                win_payout_condition = hand.value <= 21 and (dealer.value < hand.value or dealer.value > 21)
                if win_payout_condition:
                    win_rate = hand.bet + hand.bet
                    player.bankroll += win_rate
                    self.dealer.bankroll -= win_rate
                    hand.bet = 0

                push_condition = hand.value == dealer.value and hand.is_blackjack == dealer.is_blackjack
                if push_condition:
                    player.bankroll += hand.bet
                    hand.bet = 0

                loose_bj = not hand.is_blackjack and dealer.is_blackjack
                loose_dlr = hand.value < dealer.value <= 21
                loose_bust = hand.value > 21
                loose_condition = loose_bj or loose_dlr or loose_bust
                if loose_condition:
                    self.dealer.bankroll += hand.bet
                    hand.bet = 0

            player.reset()

    def play(self):

        # print(len(self.shoe.cards))

        # setting up the game
        self.setup_game()

        # creating the players
        self.create_players()

        while len(self.players):
            # shuffling the shoe (big cycle)
            if self.shoe.reshuffle:
                self.shoe.shuffle(self.setup)

            # asking the players for their bets (small cycle)
            self.ask_for_bets()

            # dealing the cards
            self.deal_cards()

            # asking the players for their actions
            while self.is_players:
                self.is_players = False
                self.ask_for_actions()
                self.print_players()

            # opening the dealer's hand
            # dealing the dealer's hand to 17
            self.dealer_action()
            # print(self.dealer.hands[0], 'value:', self.dealer.hands[0].value)

            # comparing the hands and paying the players (small cycle end)
            self.payout()

            self.remove_winners()
            self.remove_losers()

        print("losers:", self.losers)
        print("winners:", self.winners)


if __name__ == "__main__":
    pass
