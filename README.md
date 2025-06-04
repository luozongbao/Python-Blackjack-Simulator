# Blackjack Simulator

A comprehensive blackjack simulation tool with perfect basic strategy, advanced betting systems, and detailed performance tracking including **Max Equity** and **Max Drawdown** analysis.

## Features

### Game Engine
- **Real card dealing** from actual shoe simulation
- **Multiple game styles**: American, European, and Macau
- **Configurable rules**: Dealer stands on soft/hard 17
- **Flexible deck count**: 1-8 decks with auto-shuffle or traditional dealing
- **Perfect basic strategy** with customizable modifications
- **Advanced splitting**: Up to 4 splits with doubling after split

### Betting System
- **Progressive betting strategy** with 3-level system
- **Dynamic score tracking** (-3 to 0 range)
- **Automatic level management** based on win/loss patterns
- **Bet amounts**: 1, 3, or 9 units based on current level

### Performance Tracking ⭐ **NEW**
- **Max Equity Tracking**: Monitors the highest equity point reached during simulation
- **Max Drawdown Analysis**: Tracks the largest decline from peak equity
- **Comprehensive statistics**: Win/loss rates, expected values, and profit analysis
- **Real-time monitoring**: Updated after every game outcome

## Usage

### Command Line Options

```bash
python blackjack_simulator.py [options]
```

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `-d, --dealer` | `s17`, `h17` | `s17` | Dealer rule: stand on all 17s or hit soft 17 |
| `-n, --decks` | `1-8` | `6` | Number of decks in shoe |
| `-s, --style` | `A`, `E`, `M` | `A` | Game style (American/European/Macau) |
| `-a, --shuffle` | `y`, `n` | `y` | Auto-shuffle every game or traditional 80% rule |
| `-g, --games` | `1-100000` | `10000` | Number of games to simulate |
| `-m, --splits` | `1-4` | `2` | Maximum number of splits allowed |

### Examples

```bash
# Basic simulation with default settings
python blackjack_simulator.py

# Quick test with 100 games
python blackjack_simulator.py -g 100

# European style with dealer hitting soft 17
python blackjack_simulator.py -s E -d h17

# Single deck, no auto-shuffle, maximum splits
python blackjack_simulator.py -n 1 -a n -m 4

# Large simulation for statistical analysis
python blackjack_simulator.py -g 50000
```

## Game Styles

### American (Default)
- Dealer receives 2 cards initially
- Checks for blackjack if showing 10 or Ace
- Standard hole card rules

### European
- Dealer receives 1 card initially
- **If dealer has blackjack**: Player loses ALL bets (original + doubles/splits)

### Macau
- Dealer receives 1 card initially  
- **If dealer has blackjack**: Player loses only original bet (doubles/splits returned)

## Betting Strategy

The simulator uses a sophisticated 3-level progressive betting system:

### Level Management
- **Level 1**: 1 unit bet
- **Level 2**: 3 unit bet  
- **Level 3**: 9 unit bet

### Score System
- **Win**: Score +1 (maximum 0)
- **Loss**: Score -1 (minimum -3)
- **Score -3**: Level up and reset score to 0
- **Level > 1 + Win at score 0**: Level down and reset score
- **Level 3 + Score -3**: Return to Level 1

## Performance Metrics

### Standard Tracking
- **Won Amount**: Profit only (excluding returned bets)
- **Lost Amount**: Total amount lost
- **Total Bet**: Cumulative betting volume
- **Win/Loss/Push Rates**: Game outcome percentages
- **Expected Values**: Return, loss, and overall expected value

### Sample Output

```
==================================================
BLACKJACK SIMULATION RESULTS
==================================================
Games Played: 10000
Games Won: 4321
Games Lost: 4567
Games Pushed: 1112

Final Equity: $-245.00
Total Amount Bet: $15,000.00
Total Amount Won (Profit): $4,321.00
Total Amount Lost: $4,566.00

Expected Return: 0.2881
Expected Loss: 0.3044
Expected Value: -0.0163

Final Betting System Status: Level: 2, Score: -1, Bet: 3
Win Rate: 43.21%
Push Rate: 11.12%
Loss Rate: 45.67%
```

## Strategy Details

### Basic Strategy
- **Perfect mathematical strategy** with one modification
- **No surrender** option available
- **Modified rule**: Hit on 15 and 16 against dealer 10 (overrides standard basic strategy)

### Splitting Rules
- Can split any pair
- Up to specified maximum splits (1-4)
- Can double down after splitting
- Aces receive only one card when split

## Technical Implementation

### Card Simulation
- **Real shoe mechanics** with actual card depletion
- **Accurate probability calculations** based on remaining cards
- **No suit tracking** (only values matter for blackjack)

### Equity Management
- **Starting equity**: $0.00
- **Bet deduction**: Immediate equity reduction on bet placement
- **Win addition**: Profit added to equity (excludes returned bet)
- **Max Equity/Drawdown**: Continuous tracking throughout simulation

## Requirements

- Python 3.6+
- No external dependencies required

## File Structure

```
blackjack_simulator.py    # Main simulation engine
README.md                 # This documentation
docs/
  requirements/
    Requirements.md       # Original requirements
    Detailed_Spec.md     # Detailed specifications
```

## Contributing

This simulator implements precise blackjack rules and mathematical strategies. When modifying:

1. Maintain perfect basic strategy accuracy
2. Preserve betting system logic
3. Ensure equity tracking remains accurate
4. Test with multiple game configurations

## License

This project is provided as-is for educational and analysis purposes.