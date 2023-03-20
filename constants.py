from random import randrange
from faker import Faker


def bankrolls():
    while True:
        yield "$" + str(randrange(MIN_BANKROLL, 100000, 100))


def nicknames():
    fake = Faker('en_US')
    while True:
        yield fake.name()


MIN_BANKROLL = 100
MIN_BET = 10

SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
          '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
          'Q': 10, 'K': 10, 'A': 11}

PLAYERS = {"#1": "human", "#2": "bot random strategy ", "#3": "bot basic strategy", "#4": "None"}

PAYOUT = {"1:1": 1.0, "6:5": 1.2, "3:2": 1.5, "2:1": 2.0}
SHOE = {"1 deck": 1, "2 decks": 2, "4 decks": 4, "6 decks": 6, "8 decks": 8}
CUT_CARD = {"used": True, "not used": False}
HOLE_CARD = {"used": True, "not used": False}
SOFT17 = {"True": True, "False": False}
# SPLIT_RESTRICTIONS = {"None": False, "same rank only": "same rank only",
#                       "no ace": "no ace", "no 4/5/10": "no 4/5/10"}
SPLIT_ACES = {"allowed": True, "not allowed": False}
SPLIT_4510 = {"allowed": True, "not allowed": False}
SPLIT_NS10 = {"True": True, "False": False}
# SPLIT_ANY = {"allowed": True, "not allowed": False}
# DOUBLE_RESTRICTIONS = {"None": False, "9/10/11 only": "9/10/11 only", "10/11 only": "10/11 only"}
DOUBLE_91011 = {"True": True, "False": False}
DOUBLE_1011 = {"True": True, "False": False}
# DOUBLE_ANY = {"allowed": True, "not allowed": False}

# RE_SPLIT = {"None": False, "4 hands": "4 hands", "unlimited": "unlimited"}
RE_SPLIT_UNLIMITED = {"allowed": True, "not allowed": False}
RE_SPLIT_UP_TO_4H = {"allowed": True, "not allowed": False}
RE_SPLIT_ACES = {"allowed": True, "not allowed": False}

DOUBLE_AFTER_SPLIT = {"allowed": True, "not allowed": False}
HITTING_SPLIT_ACES = {"allowed": True, "not allowed": False}
OBO = {"True": True, "False": False}
TIE = {"True": True, "False": False}
# SURRENDERING = {"not allowed": False, "early": "early", "late": "late"}
EARLY_SURRENDER = {"True": True, "False": False}
LATE_SURRENDER = {"True": True, "False": False}
INSURANCE_10 = {"allowed": True, "not allowed": False}

BJ_SETUP_DEFAULT = {
    "bases": {
        "base #1": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())},
        "base #2": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())},
        "base #3": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())},
        "base #4": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())},
        "base #5": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())},
        "base #6": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())},
        "base #7": {"player": PLAYERS.get("#3"), "nickname": next(nicknames()),
                    "bankroll": next(bankrolls())}
    },
    "rules": {
        "blackjack payout": list(PAYOUT)[2],
        "dealing shoe": list(SHOE)[3],
        "dealer hits on soft 17": list(SOFT17)[0],
        "shoe cut-card": list(CUT_CARD)[0],
        "dealer hole card": list(HOLE_CARD)[0],
        "insurance on 10": list(INSURANCE_10)[0],

        # "double restrictions": list(DOUBLE_RESTRICTIONS)[0],
        # "double any value": list(DOUBLE_ANY)[0],
        "double only on hard 10/11": list(DOUBLE_1011)[1],  # True/False, False/True, False/False
        "double only on hard 9/10/11": list(DOUBLE_91011)[1],  # True/False, False/True, False/False

        # "surrendering limits": list(SURRENDERING)[0],
        "early surrender": list(EARLY_SURRENDER)[1],  # True/False, False/True, False/False
        "late surrender": list(LATE_SURRENDER)[1],  # True/False, False/True, False/False

        # "split restrictions": list(SPLIT_RESTRICTIONS)[0],
        # "split any pair": list(SPLIT_ANY)[0],  # parent rule
        "split aces": list(SPLIT_ACES)[0],

        "split 4/5/10": list(SPLIT_4510)[0],  # True/Any False/False
        "split only same rank": list(SPLIT_NS10)[1],  # True/Any False/False

        # "re-split limit": list(RE_SPLIT)[1],
        "re-split unlimited": list(RE_SPLIT_UNLIMITED)[1],  # True/False/Any False/True/Any False/False/False
        "re-split up to 4 hands": list(RE_SPLIT_UP_TO_4H)[0],  # True/False/Any False/True/Any False/False/False
        "re-splitting aces": list(RE_SPLIT_ACES)[1],  # True/False/Any False/True/Any False/False/False

        "double after split": list(DOUBLE_AFTER_SPLIT)[0],
        "hitting split aces": list(HITTING_SPLIT_ACES)[1],
        "original bets only": list(OBO)[1],
        "dealer wins ties": list(TIE)[1]
    }
}

# Hand actions
HIT = "hit"
STAND = "stand"
DOUBLE = "double"
SPLIT = "split"
SURRENDER = "surrender"
INSURANCE = "insurance"

if __name__ == '__main__':
    print(type(list(DOUBLE_1011)[1]))
