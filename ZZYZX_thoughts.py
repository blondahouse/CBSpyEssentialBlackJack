# Welcome message
# - input user nickname
# - input user bankroll
# - convert to chips
# - setup the game
#
# Start Game (Loop)
# Get player bet (input)
# Build & shuffle deck
# Deal cards for player and dealer
# Show both player cards and one dealer card
# Calculate the value of player cards
# If the value is equal to 21 - player wins
# Else - get player decision (stand, hit, double, surrender)
#
# Rules:
# basic
# - blackjack payout (default 3:2) | options - 1:1, 6:5, 3:2, 2:1
# - player's blackjack wins immediately (default True) | options True, False
# - dealing shoe - decks (default 4) | options -  1, 2, 4, 6, 8
# - cut-card used
# - players (default 3: player, bot and dealer) | options 2 to 8
# - player positions (default 1) | options 1, 2, 3
# - bet range (default $10 to $10000) | options - any
# - soft 17 (default hit) | options hit, stand
#
# optional
# - hole card (default True) | options True, False
# - double down rule - only one extra card allowed, only available as the first decision, if player have enough chips
# - double down restrictions (default None) | options None, 9 through 11, 10 or 11 (“American/European Reno Rule”)
# - splitting rule - allowed only if player have enough chips to split
# - split options (default None) |
#           options None, same rank, no ace splits, split after hit, split any 16, No 4/5/10 splits
# - doubling after split (default True) | options True, False
# - re-splitting (default up to 4 hands) | options up to 4 hands | None | Unlimited
# - blackjack after split (default False) | options True, False
# - hitting split aces (default False) | options True, False (not available if no ace splits checked)
# - re-splitting split aces (default False) | options True, False (not available if no ace splits checked)
# - surrender (default late) | options None, early, late (late possible only with hole card)
# - insurance (default ace) | options ace, ace or 10 value card
# insurance payout: 2:1
# insurance limit: 0.5 bet
#
# - original bets only "OBO" (default True) | options True, False
# - dealer wins on a tie (default False) | options True, False
#
#
# - back betting (play behind) - not allowed | multiplayer required
#
# Chips:
# $1 - White
# $5 - Red
# $25 - Green
# $50 - Blue
# $100 - Black
# $500 - Purple
# $1000 - Orange (Yellow)
# $5000 - Brown
#
# -------------------------------------------------------------------------------------------------------------------- #
# Blackjack setup: {
# Bases: {
# base #1:          {type: human,       nickname: Taylor Parry,             bankroll: $500}
# base #2:          {type: bot,         nickname: Charlie Duncan,           bankroll: $500}
# base #3:          {type: bot,         nickname: John White,               bankroll: $500}
# base #4:          {type: bot,         nickname: Jamie Read,               bankroll: $500}
# base #5:          {type: bot,         nickname: Daniel Ramirez,           bankroll: $500}
# base #6:          {type: bot,         nickname: Peter Hartman,            bankroll: $500}
# base #7:          {type: bot,         nickname: Leonel Waller,            bankroll: $500}
# }
# Rules: {
# bet range: $10 to $10 000                                 dealing shoe: 4 decks
# blackjack payout: 3:2                                     cut-card: used
# soft 17: hit                                              hole card: used
# split restrictions: None                                  double restrictions: None
# re-split: up to 4 hands                                   tie condition: push
# re-splitting aces: not allowed                            original bets only: True
# double after split: allowed                               surrendering: not allowed
# hitting split aces: not allowed                           insurance: ace or 10 value card
# }
# Confirm                                                   Exit
# -------------------------------------------------------------------------------------------------------------------- #
# Blackjack game:       Dealer's hand:                  totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
#
# Taylor Parry/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
# Charlie Duncan/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
# John White/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
# Jamie Read/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
# Daniel Ramirez/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
# Peter Hartman/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
# Leonel Waller/ bank: $500
#       hand #1:        bet: $100       ins: $0         totals: 17      cards: ♥10-♠7-♣J-♦2-♦A
#
#                                                           Exit
# -------------------------------------------------------------------------------------------------------------------- #
# nicknames =
# {"#1": "Taylor", "#2": "Charlie", "#3": "John", "#4": "Jamie", "#5": "Daniel", "#6": "Peter", "#7": "Leonel"}
# bankrolls = {"#1": 100, "#2": 200, "#3": 500, "#4": 1000, "#5": 2000, "#6": 5000, "#7": 10000}

# blackjack_setup = {
#     "Bases": {"#1": BASE, "#2": BASE, "#3": BASE, "#4": BASE, "#5": BASE, "#6": BASE, "#7": BASE},
#     "Rules": {
#         "payout": {"#1": "1:1", "#2": "6:5", "#3!": "3:2", "#4": "2:1"},
#         "shoe": {"#1": "1 deck", "#2": "2 decks", "#3!": "4 decks", "#4": "6 decks", "#5": "8 decks"},
#         "cut-card": {"#1!": "used", "#2": "not used"},
#         "hole card": {"#1!": "used", "#2": "not used"},
#         "soft 17": {"#1!": "hit", "#2": "stand"},
#         "split restrictions": {"#1!": "None", "#2": "same rank only", "#3": "no ace", "#4": "no 4/5/10"},
#         "double restrictions": {"#1!": "None", "#2": "9/10/11 only", "#3": "10/11 only"},
#         "re-split": {"#1": "None", "#2!": "up to 4 hands", "#3": "unlimited"},
#         "re-splitting aces": {"#1": "allowed", "#2!": "not allowed"},
#         "double after split": {"#1!": "allowed", "#2": "not allowed"},
#         "hitting split aces": {"#1": "allowed", "#2!": "not allowed"},
#         "original bets only": {"#1!": "True", "#2!": "False"},
#         "tie condition": {"#1!": "push", "#2": "dealer wins"},
#         "surrendering": {"#1!": "not allowed", "#2": "early", "#3": "late"},
#         "insurance": {"#1!": "10/11", "#2": "11"}
#     }
# }
# ♠♣♥♦
def clear_screen():
    pass


def print_setup():
    pass


if __name__ == "__main__":
    # Blackjack setup
    while True:
        clear_screen()
        print_setup()
        pass
