import re

from colorama import Fore

from cards import Shoe
from constants import BJ_SETUP_DEFAULT, PLAYERS, PAYOUT, RE_SPLIT_ACES, SOFT17
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
            if player.plays:
                player.place_bet()

    def deal_cards(self):  # TODO: no hole card for dealer
        for player in self.players:
            if player.plays:
                for hand in player.hands:
                    hand.add_card(self.shoe.draw())
                    hand.add_card(self.shoe.draw())
                    hand.log = hand.__str__()
        self.dealer.hands[0].add_card(self.shoe.draw())
        self.dealer.hands[0].add_card(self.shoe.draw())
        self.dealer.hands[0].log = self.dealer.hands[0].__str__()

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
            new_hand = h.__class__()
            new_hand.bet = h.bet
            new_hand.start_bet = h.bet
            new_hand.add_card(h.cards.pop())
            new_hand.add_card(self.shoe.draw())
            new_hand.log = new_hand.__str__()

            h.add_card(self.shoe.draw())
            # h.log = h.__str__()

            p.hands.append(new_hand)
            p.bankroll -= h.bet

            # p.hands[-1].bet = h.bet
            # p.hands[-1].add_card(h.cards.pop())
            # h.add_card(self.shoe.draw())
            # p.hands[-1].add_card(self.shoe.draw())
            # h.log += f'{h.__str__()}'
            # p.hands[-1].log += f'{p.hands[-1].__str__()}'

            re_splitting_aces = RE_SPLIT_ACES.get(self.setup.get("rules").get('re-splitting aces'))
            # TODO: hitting split aces is not checked
            if h.cards[0].rank == 'A' and not re_splitting_aces:
                h.stand = True
                p.hands[-1].stand = True
            else:
                h.is_first_decision = True
                p.hands[-1].is_first_decision = True
                self.is_players = True

        def surrender():  # TODO: surrender
            pass

        def insurance():  # TODO: insurance
            pass

        for player in self.players:
            # print(player, end=': ')
            if player.plays:
                for hand in player.hands:
                    dealer_card = self.dealer.hands[0].cards[0]
                    setup = self.setup
                    num_of_hands = len(player)
                    bankroll = player.bankroll
                    action = hand.action(dealer_card, setup, num_of_hands, bankroll)
                    hand.log += f' ({action})'
                    # print(f'({action})')
                    # input()
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
        print(f'{self.dealer} {self.dealer.hands[0].log}')
        for player in self.players:
            print(player)
            for index, hand in enumerate(player.hands):
                # print(f'\t#{index + 1} {hand}')
                print(f'\t#{index + 1} bet: ${hand.start_bet} {hand.log} {hand.message}')

    def dealer_action(self):
        hit_17 = SOFT17.get(self.setup.get("rules").get('dealer hits on soft 17'))
        soft_17 = 17 if hit_17 else 16
        while self.dealer.hands[0].value <= soft_17:
            self.dealer.hands[0].log += f' (hit)'
            self.dealer.hands[0].add_card(self.shoe.draw())

    def payout(self):

        # win_blackjack_payout_condition = hand.is_blackjack and not dealer_hand.is_blackjack
        # print('win_bj:', win_blackjack_payout_condition, end=', ')
        # if win_blackjack_payout_condition:
        #     win_rate = hand.bet + hand.bet * PAYOUT.get(self.setup.get("rules").get('blackjack payout'))
        #     player.bankroll += win_rate
        #     self.dealer.bankroll -= win_rate
        #     hand.bet = 0
        #
        # win_payout_condition = hand.value <= 21 and not hand.is_blackjack and\
        #                        (dealer_hand.value < hand.value or 21 < dealer_hand.value)
        # print('win:', win_payout_condition, end=', ')
        # if win_payout_condition:
        #     win_rate = hand.bet + hand.bet
        #     player.bankroll += win_rate
        #     self.dealer.bankroll -= win_rate
        #     hand.bet = 0
        #
        # push_condition = hand.value == dealer_hand.value and hand.is_blackjack == dealer_hand.is_blackjack
        # print('push:', push_condition, end=', ')
        # if push_condition:
        #     player.bankroll += hand.bet
        #     hand.bet = 0
        #
        # loose_bj = not hand.is_blackjack and dealer_hand.is_blackjack
        # loose_dlr = hand.value < dealer_hand.value <= 21
        # loose_bust = hand.value > 21
        # loose_condition = loose_bj or loose_dlr or loose_bust
        # print('loose:', loose_condition, end=', ')
        # if loose_condition:
        #     self.dealer.bankroll += hand.bet
        #     hand.bet = 0

        def bet_lose():
            self.dealer.bankroll += hand.bet
            hand.message = f' lost ${hand.bet}'
            hand.bet = 0

        def bet_push():
            player.bankroll += hand.bet
            hand.message = f' pushed $0'
            hand.bet = 0

        def bet_win():
            win_rate = hand.bet
            hand.message = f' won ${win_rate}'
            player.bankroll += win_rate + hand.bet
            self.dealer.bankroll -= win_rate
            hand.bet = 0

        def bet_win_blackjack():
            win_rate = int(hand.bet * PAYOUT.get(self.setup.get("rules").get('blackjack payout')))
            hand.message = f' won ${win_rate}'
            player.bankroll += win_rate + hand.bet
            self.dealer.bankroll -= win_rate
            hand.bet = 0

        dealer_hand = self.dealer.hands[0]
        for player in self.players:
            if player.plays:
                for hand in player.hands:

                    if hand.value > dealer_hand.value:
                        if hand.value > 21:
                            bet_lose()
                        else:
                            bet_win()
                    elif hand.value == dealer_hand.value:
                        if hand.value > 21:
                            bet_lose()
                        elif hand.value == 21:
                            if hand.is_blackjack and not dealer_hand.is_blackjack:
                                bet_win_blackjack()
                            elif not hand.is_blackjack and dealer_hand.is_blackjack:
                                bet_lose()
                            else:
                                bet_push()
                        else:
                            bet_push()
                    else:
                        if hand.value > 21:
                            bet_lose()
                        elif hand.value == 21:
                            if hand.is_blackjack:
                                bet_win_blackjack()
                            else:
                                bet_win()
                        else:
                            if dealer_hand.value > 21:
                                bet_win()
                            else:
                                bet_lose()

    def reset_players(self):
        for player in self.players:
            player.reset()

    def play(self):

        # print(len(self.shoe.cards))

        # setting up the game
        self.setup_game()
        input()

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
            # print(self.dealer)
            # input()

            # asking the players for their actions
            self.is_players = True
            while self.is_players:
                self.is_players = False
                self.ask_for_actions()

            # opening the dealer's hand
            # dealing the dealer's hand to 17
            self.dealer_action()
            # print(self.dealer.hands[0], 'value:', self.dealer.hands[0].value)

            # comparing the hands and paying the players (small cycle end)
            self.payout()
            print()

            self.print_players()
            input()

            self.reset_players()
            self.dealer.reset()

            self.remove_winners()
            self.remove_losers()

        print("losers:", self.losers)
        print("winners:", self.winners)


if __name__ == "__main__":
    pass
