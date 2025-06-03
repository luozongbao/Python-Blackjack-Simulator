# Blackjack Simulator - Detailed Specification

## Command Line Options
- `d`: Dealer rules - s17 (stand on all 17+) or h17 (stand on hard 17+) [default: s17]
- `n`: Number of decks in shoe - 1 to 8 [default: 6]
- `s`: Game style - A (American), E (European), M (Macau) [default: A]
- `a`: Shuffle - y (auto shuffle every game), n (shuffle when 80% dealt) [default: y]
- `g`: Number of games - 1 to 100000 [default: 10000]
- `s`: Max splits allowed - 1 to 4 [default: 2]

## Game Styles
- **American**: Dealer gets 2 cards, checks for blackjack if showing 10/A
- **European**: Dealer gets 1 card initially, if dealer has blackjack player loses ALL bets (original + doubles/splits)
- **Macau**: Dealer gets 1 card initially, if dealer has blackjack player loses only original bet

## Card Values
- Ace: 1 or 11 (soft/hard)
- Face cards (J, Q, K): 10
- Number cards: face value

## Player Strategy
- Perfect basic strategy EXCEPT:
  - No surrender allowed
  - Hit on 15 and 16 against dealer 10 (overrides basic strategy)
- Splitting: Can split any pair, up to specified limit, can double after split

## Betting Strategy
Starting: Level 1, Score 0, Bet 1 unit

### Score Management
- Win: Score +1, but max score is 0 (cannot go above 0)
- Loss: Score -1, min score is -3

### Level Management
- When score reaches -3: Reset score to 0, Level = Level + 1, Bet = 3^(Level-1) units
- When Level > 1 AND win at score 0: Level = Level - 1, reset score to 0
- When Level 3 AND score reaches -3: Return to Level 1, score 0
- When Level 1 AND win at score 0: Stay at Level 1, score 0 (no score increase)

### Bet Amounts by Level
- Level 1: 1 unit (3^0)
- Level 2: 3 units (3^1)
- Level 3: 9 units (3^2)

## Tracking Requirements
- Won amount (profit only, excluding original bet)
- Lost amount
- Total bet amount
- Won games count
- Lost games count
- Push games count
- Total games count
- Expected Return
- Expected Loss
- Expected Value
- Display all results in console

## Technical Requirements
- Real shoe simulation with actual card dealing
- No suit generation needed (only card values matter)
- Player starts with 0 equity
- Each bet subtracts from equity, each win adds profit to equity
