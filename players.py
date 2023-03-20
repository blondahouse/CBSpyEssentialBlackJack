from constants import MIN_BET, SPLIT_NS10, DOUBLE_AFTER_SPLIT, DOUBLE_1011, DOUBLE_91011, SPLIT_ACES, SPLIT_4510, \
    RE_SPLIT_UNLIMITED, RE_SPLIT_UP_TO_4H, RE_SPLIT_ACES, EARLY_SURRENDER, LATE_SURRENDER, INSURANCE_10
from strategy import BASIC_STRATEGY


class Account:
    def __init__(self, name, bankroll):
        self.name = name
        self.start_bankroll = bankroll
        self.bankroll = bankroll
        self.hands = []
        self.plays = True

    def __repr__(self):
        return f'{self.name} start: ${self.start_bankroll} current: ${self.bankroll}'

    def __str__(self):
        return f'{self.name} start: ${self.start_bankroll} current: ${self.bankroll}'

    def __len__(self):
        return len(self.hands)

    def reset(self):
        hand_class = self.hands[0].__class__
        self.hands = []
        self.hands.append(hand_class())


class Dealer(Account):
    def __init__(self, name, bankroll):
        super().__init__(name, bankroll)
        self.hands.append(DealerHand())
    #
    # def __repr__(self):
    #     return f'{self.name} start ${self.start_bankroll} current ${self.bankroll} ' \
    #            f'hand {self.hands[0]}'
    #
    # def __str__(self):
    #     return f'{self.name} start ${self.start_bankroll} current ${self.bankroll} ' \
    #            f'hand {self.hands[0]}'


class Player(Account):
    def __init__(self, name, bankroll, hand_class):
        super().__init__(name, bankroll)
        self.hands.append(hand_class())

    def place_bet(self):
        basic_bet = round(self.bankroll * 0.1)
        if basic_bet > MIN_BET:
            self.bankroll -= basic_bet
            self.hands[0].bet += basic_bet
            self.hands[0].start_bet += basic_bet
        else:
            self.bankroll -= MIN_BET
            self.hands[0].bet += MIN_BET
            self.hands[0].start_bet += MIN_BET


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.soft = False
        self.stand = False
        self.log = ''

    def __repr__(self):
        string = f''
        for card in self.cards:
            string += f'{card}'
            if card is not self.cards[-1]:
                string += f', '
        string += f' v: {self.value}'
        return string

    def __str__(self):
        string = f'cards: '
        for card in self.cards:
            string += f'{card}'
            if card != self.cards[-1]:
                string += f', '
        string += f' v: {self.value}'
        return string

    def __len__(self):
        return len(self.cards)

    def add_card(self, card):

        def calculate_value():
            self.value = 0
            self.aces = 0
            self.soft = False
            # calculate hard value
            for c in self.cards:
                if c.rank != 'A':
                    self.value += c.value
                else:
                    self.aces += 1
            for c in self.cards:
                if c.rank == 'A':
                    if self.value + 10 + self.aces > 21:
                        self.value += 1
                    else:
                        self.value += 11
                        self.soft = True

        self.cards.append(card)
        calculate_value()
        if self.__len__() >= 2:
            self.log += f' {card.__str__()} v: {self.value}'
        if self.is_bust():
            self.stand = True

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value == 21

    def is_bust(self):
        return self.value > 21

    # def is_21(self):
    #     return self.value == 21


class DealerHand(Hand):
    def __init__(self):
        super().__init__()
        self.split = False
        self.is_active = True
        self.is_first_decision = True


class PlayerHand(Hand):
    def __init__(self):
        super().__init__()


class BotRandomStrategyHand(Hand):
    def __init__(self):
        super().__init__()


class BotBasicStrategyHand(Hand):
    def __init__(self):
        super().__init__()
        self.bet = 0
        self.start_bet = 0
        self.split = False
        self.stand = False
        self.is_first_decision = True
        self.log = ''
        self.message = ''

    def is_splittable(self, setup):
        split_ns10 = SPLIT_NS10.get(setup.get("rules").get("split only same rank"))
        if split_ns10:
            return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
        else:
            return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value

    def action(self, dealer_card, setup, num_of_hands, bankroll):
        available_actions = ["stand"]
        if self.stand:
            return "stand"
        else:
            available_actions.append("hit")

            if bankroll >= self.bet:
                # double down
                das = DOUBLE_AFTER_SPLIT.get(setup.get("rules").get("double after split"))
                das = not (self.split and not das)
                reno_eu = DOUBLE_1011.get(setup.get("rules").get("double only on hard 10/11"))
                reno_eu = not (not 9 <= self.value <= 11 and reno_eu)
                reno_us = DOUBLE_91011.get(setup.get("rules").get("double only on hard 9/10/11"))
                reno_us = not (not 10 <= self.value <= 11 and reno_us)
                if das and reno_eu and reno_us and self.is_first_decision:
                    available_actions.append("double")

                # split
                split_aces = SPLIT_ACES.get(setup.get("rules").get("split aces"))
                split_aces = not (not split_aces and self.aces)
                split_4510 = SPLIT_4510.get(setup.get("rules").get("split 4/5/10"))
                split_4510 = not (not split_4510 and self.cards[0].value in (4, 5, 10))
                re_split_unlimited = RE_SPLIT_UNLIMITED.get(setup.get("rules").get("re-split unlimited"))
                re_split_up_to4 = RE_SPLIT_UP_TO_4H.get(setup.get("rules").get("re-split up to 4 hands"))
                re_split_unlimited = not (not re_split_unlimited and not re_split_up_to4)
                re_split_up_to4 = not (re_split_up_to4 and num_of_hands >= 4)
                re_split_aces = RE_SPLIT_ACES.get(setup.get("rules").get("re-splitting aces"))
                re_split_aces = not (self.split and not re_split_aces)
                if self.is_splittable(setup) and self.is_first_decision and split_aces and split_4510 and \
                        re_split_aces and re_split_unlimited and re_split_up_to4:
                    available_actions.append("split")

            # surrender
            early_surrender = EARLY_SURRENDER.get(setup.get("rules").get("early surrender"))
            late_surrender = LATE_SURRENDER.get(setup.get("rules").get("late surrender"))
            surrender = early_surrender or late_surrender
            if surrender and self.is_first_decision:
                available_actions.append("surrender")

            # insurance
            insurance = INSURANCE_10.get(setup.get("rules").get("insurance on 10"))
            insurance = dealer_card.value == 11 or dealer_card.value == 10 and insurance
            if insurance:
                available_actions.append("insurance")

            # get advice from basic strategy
            # print(self, self.value, dealer_card, available_actions, end='')
            if self.is_splittable(setup):
                if self.aces:
                    advice = "split"
                else:
                    advice = BASIC_STRATEGY['pair'][self.value][dealer_card.value]
            else:
                if not self.soft:
                    advice = BASIC_STRATEGY['hard'][self.value][dealer_card.value]
                else:
                    advice = BASIC_STRATEGY['soft'][self.value][dealer_card.value]

            # divide composited advice and check if it is in available actions
            if "/" in advice:
                advice = advice.split("/")
                for a in advice:
                    if a in available_actions:
                        # print(a)
                        return a
            else:
                if advice in available_actions:
                    # print(advice)
                    return advice


if __name__ == '__main__':
    p = Player("BotBS", 1000, BotBasicStrategyHand)
    # print(p.hands[0].cards)
    # p.hands[0].add_card(Card('H', 'A'))
    # print(p.hands[0].cards)
    h = p.hands[0].__class__
    print(h())
    p.hands.append(BotBasicStrategyHand())
    print(len(p))
    print(BASIC_STRATEGY['hard'][5][2])
