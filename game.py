if __name__ == "__main__":
    pass
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
# - decks (default 4) | options -  1, 2, 4, 6, 8
# - players (default 3: player, bot and dealer) | options 2 to 8
# - player positions (default 1) | options 1, 2, 3
# - bet range (default $10 to 10000) | options - any
# - soft 17 (default hit) | options hit, stand
#
# optional
# - hole card (default True) | options True, False
# - double down rule - only one extra card allowed, only available as the first decision
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
