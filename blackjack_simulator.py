#!/usr/bin/env python3
"""
Blackjack Simulator with Perfect Strategy and Betting System
"""

import random
import argparse
from typing import List, Tuple, Dict, Optional
from enum import Enum
from dataclasses import dataclass


class GameStyle(Enum):
    AMERICAN = "A"
    EUROPEAN = "E"
    MACAU = "M"


class DealerRule(Enum):
    STAND_17 = "s17"  # Stand on all 17s
    HIT_SOFT_17 = "h17"  # Hit on soft 17


class Card:
    """Represents a playing card"""
    def __init__(self, value: int):
        self.value = value  # 1-13 (1=Ace, 11=Jack, 12=Queen, 13=King)
    
    def blackjack_value(self) -> int:
        """Returns the blackjack value of the card"""
        if self.value == 1:  # Ace
            return 11  # Will be adjusted for soft/hard later
        elif self.value > 10:  # Face cards
            return 10
        else:
            return self.value
    
    def __str__(self):
        if self.value == 1:
            return "A"
        elif self.value == 11:
            return "J"
        elif self.value == 12:
            return "Q"
        elif self.value == 13:
            return "K"
        else:
            return str(self.value)


class Hand:
    """Represents a blackjack hand"""
    def __init__(self):
        self.cards: List[Card] = []
        self.bet: int = 0
        self.doubled: bool = False
        self.split_from: Optional['Hand'] = None
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def get_value(self) -> Tuple[int, bool]:
        """Returns (value, is_soft) where is_soft means contains usable ace"""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.value == 1:  # Ace
                aces += 1
                total += 11
            else:
                total += card.blackjack_value()
        
        # Adjust for aces
        while total > 21 and aces > 0:
            total -= 10  # Convert ace from 11 to 1
            aces -= 1
        
        is_soft = aces > 0 and total <= 21
        return total, is_soft
    
    def is_blackjack(self) -> bool:
        """Check if hand is a natural blackjack"""
        return len(self.cards) == 2 and self.get_value()[0] == 21
    
    def is_busted(self) -> bool:
        """Check if hand is busted"""
        return self.get_value()[0] > 21
    
    def can_split(self) -> bool:
        """Check if hand can be split"""
        return len(self.cards) == 2 and self.cards[0].blackjack_value() == self.cards[1].blackjack_value()
    
    def can_double(self) -> bool:
        """Check if hand can be doubled"""
        return len(self.cards) == 2 and not self.doubled


class Shoe:
    """Represents a shoe of cards"""
    def __init__(self, num_decks: int, auto_shuffle: bool = True):
        self.num_decks = num_decks
        self.auto_shuffle = auto_shuffle
        self.cards: List[Card] = []
        self.dealt_cards = 0
        self.shuffle_threshold = int(num_decks * 52 * 0.8)  # 80% of cards
        self.shuffle()
    
    def shuffle(self):
        """Shuffle the shoe"""
        self.cards = []
        for _ in range(self.num_decks):
            for value in range(1, 14):  # 1-13 for each suit
                for _ in range(4):  # 4 suits
                    self.cards.append(Card(value))
        
        random.shuffle(self.cards)
        self.dealt_cards = 0
    
    def need_shuffle(self) -> bool:
        """Check if shoe needs shuffling"""
        if self.auto_shuffle:
            return len(self.cards) == 0
        else:
            return self.dealt_cards >= self.shuffle_threshold
    
    def deal_card(self) -> Card:
        """Deal a card from the shoe"""
        if len(self.cards) == 0:
            if self.auto_shuffle:
                self.shuffle()
            else:
                raise ValueError("No cards left in shoe")
        
        card = self.cards.pop()
        self.dealt_cards += 1
        return card


@dataclass
class GameStats:
    """Track game statistics"""
    won_amount: float = 0.0  # Profit only
    lost_amount: float = 0.0
    total_bet: float = 0.0
    won_games: int = 0
    lost_games: int = 0
    push_games: int = 0
    total_games: int = 0
    max_equity: float = 0.0  # Highest equity reached
    max_drawdown: float = 0.0  # Largest drop from peak
    min_equity: float = 0.0  # Lowest equity reached
    
    @property
    def expected_return(self) -> float:
        return self.won_amount if self.total_bet == 0 else self.won_amount / self.total_bet
    
    @property
    def expected_loss(self) -> float:
        return self.lost_amount if self.total_bet == 0 else self.lost_amount / self.total_bet
    
    @property
    def expected_value(self) -> float:        return (self.won_amount - self.lost_amount) if self.total_bet == 0 else (self.won_amount - self.lost_amount) / self.total_bet
    
    def update_equity_tracking(self, current_equity: float):
        """Update max equity, min equity, and max drawdown tracking"""
        # Update max equity if current equity is higher
        if current_equity > self.max_equity:
            self.max_equity = current_equity
        
        # Update min equity if current equity is lower
        if current_equity < self.min_equity:
            self.min_equity = current_equity
        
        # Calculate current drawdown from peak
        current_drawdown = self.max_equity - current_equity
        
        # Update max drawdown if current drawdown is larger
        if current_drawdown > self.max_drawdown:
            self.max_drawdown = current_drawdown


class BettingSystem:
    """Manages the betting progression system"""
    def __init__(self):
        self.level = 1
        self.score = 0
        self.base_unit = 1
    
    def get_bet_amount(self) -> int:
        """Get current bet amount based on level"""
        return 3 ** (self.level - 1) * self.base_unit
    
    def process_win(self):
        """Process a win according to betting strategy"""
        if self.level == 1 and self.score == 0:
            # Stay at level 1, score 0
            pass
        elif self.level > 1 and self.score == 0:
            # Level down and reset score
            self.level -= 1
            self.score = 0
        else:
            # Increase score but max at 0
            self.score = min(0, self.score + 1)
    
    def process_loss(self):
        """Process a loss according to betting strategy"""
        self.score = max(-3, self.score - 1)
        
        # Control level progression
        if self.score == -3:
            if self.level == 3:
                # Return to level 1
                self.level = 1
                self.score = 0
            else:
                # Level up and reset score
                self.level += 1
                self.score = 0
    
    def get_status(self) -> str:
        return f"Level: {self.level}, Score: {self.score}, Bet: {self.get_bet_amount()}"


class BasicStrategy:
    """Perfect basic strategy implementation"""
    
    @staticmethod
    def should_hit(player_hand: Hand, dealer_up_card: Card, can_double: bool = False) -> str:
        """
        Returns the optimal action: 'hit', 'stand', 'double', 'split'
        Modified strategy: hit on 15 and 16 against dealer 10
        """
        player_value, is_soft = player_hand.get_value()
        dealer_value = dealer_up_card.blackjack_value()
        
        # Check for splitting first
        if player_hand.can_split():
            return BasicStrategy._get_split_action(player_hand, dealer_value)
        
        # Soft hands (with usable ace)
        if is_soft:
            return BasicStrategy._get_soft_action(player_value, dealer_value, can_double)
        
        # Hard hands
        return BasicStrategy._get_hard_action(player_value, dealer_value, can_double)
    
    @staticmethod
    def _get_split_action(hand: Hand, dealer_value: int) -> str:
        """Get action for pairs"""
        card_value = hand.cards[0].blackjack_value()
        
        # Simplified split strategy
        if card_value in [1, 8]:  # Always split Aces and 8s
            return 'split'
        elif card_value == 10:  # Never split 10s
            return 'stand'
        elif card_value in [2, 3]:
            return 'split' if dealer_value in [2, 3, 4, 5, 6, 7] else 'hit'
        elif card_value == 4:
            return 'hit'  # Never split 4s
        elif card_value in [6, 7]:
            return 'split' if dealer_value in [2, 3, 4, 5, 6] else 'hit'
        elif card_value == 9:
            return 'split' if dealer_value in [2, 3, 4, 5, 6, 8, 9] else 'stand'
        else:
            return 'hit'
    
    @staticmethod
    def _get_soft_action(player_value: int, dealer_value: int, can_double: bool) -> str:
        """Get action for soft hands"""
        if player_value >= 19:
            return 'stand'
        elif player_value == 18:
            if dealer_value in [2, 7, 8]:
                return 'stand'
            elif dealer_value in [3, 4, 5, 6] and can_double:
                return 'double'
            else:
                return 'hit'
        elif player_value in [17, 16] and dealer_value in [3, 4, 5, 6] and can_double:
            return 'double'
        elif player_value in [15, 14] and dealer_value in [4, 5, 6] and can_double:
            return 'double'
        elif player_value == 13 and dealer_value in [5, 6] and can_double:
            return 'double'
        else:
            return 'hit'
    
    @staticmethod
    def _get_hard_action(player_value: int, dealer_value: int, can_double: bool) -> str:
        """Get action for hard hands with modified strategy"""
        if player_value >= 17:
            return 'stand'
        elif player_value == 16:
            # Modified: hit against dealer 10
            if dealer_value == 10:
                return 'hit'
            else:
                return 'stand' if dealer_value <= 6 else 'hit'
        elif player_value == 15:
            # Modified: hit against dealer 10
            if dealer_value == 10:
                return 'hit'
            else:
                return 'stand' if dealer_value <= 6 else 'hit'
        elif player_value in [13, 14]:
            return 'stand' if dealer_value <= 6 else 'hit'
        elif player_value == 12:
            return 'stand' if dealer_value in [4, 5, 6] else 'hit'
        elif player_value == 11:
            return 'double' if can_double else 'hit'
        elif player_value == 10:
            return 'double' if can_double and dealer_value <= 9 else 'hit'
        elif player_value == 9:
            return 'double' if can_double and dealer_value in [3, 4, 5, 6] else 'hit'
        else:
            return 'hit'


class BlackjackGame:
    """Main blackjack game engine"""
    
    def __init__(self, num_decks: int = 6, dealer_rule: DealerRule = DealerRule.STAND_17,
                 style: GameStyle = GameStyle.AMERICAN, auto_shuffle: bool = True,
                 max_splits: int = 2):
        self.shoe = Shoe(num_decks, auto_shuffle)
        self.dealer_rule = dealer_rule
        self.style = style
        self.max_splits = max_splits
        self.betting_system = BettingSystem()
        self.stats = GameStats()
        self.equity = 0.0
    
    def play_game(self) -> bool:
        """
        Play a single game of blackjack
        Returns True if we can continue playing, False if shoe needs shuffle
        """
        # Check if we need to shuffle before dealing
        if not self.shoe.auto_shuffle and self.shoe.need_shuffle():
            return False  # Signal that we need to shuffle
        
        # Place bet
        bet_amount = self.betting_system.get_bet_amount()
        self.equity -= bet_amount
        self.stats.total_bet += bet_amount
        
        # Deal initial cards
        player_hands = [Hand()]
        player_hands[0].bet = bet_amount
        dealer_hand = Hand()
        
        # Deal cards based on style
        if self.style == GameStyle.AMERICAN:
            # Deal 2 cards to player, 2 to dealer
            player_hands[0].add_card(self.shoe.deal_card())
            dealer_hand.add_card(self.shoe.deal_card())
            player_hands[0].add_card(self.shoe.deal_card())
            dealer_hand.add_card(self.shoe.deal_card())
        else:  # European or Macau
            # Deal 2 cards to player, 1 to dealer
            player_hands[0].add_card(self.shoe.deal_card())
            dealer_hand.add_card(self.shoe.deal_card())
            player_hands[0].add_card(self.shoe.deal_card())
        
        # Check for player blackjack
        player_has_blackjack = player_hands[0].is_blackjack()
        
        # American style: check for dealer blackjack early
        dealer_has_blackjack = False
        if self.style == GameStyle.AMERICAN:
            if dealer_hand.cards[0].blackjack_value() in [10, 11]:  # 10 or Ace
                # Peek at hole card
                if dealer_hand.is_blackjack():
                    dealer_has_blackjack = True
          # Handle blackjacks
        if player_has_blackjack and dealer_has_blackjack:
            # Push
            self.equity += bet_amount  # Return bet
            self.stats.push_games += 1
            self.stats.total_games += 1
            self.stats.update_equity_tracking(self.equity)
            return True
        elif player_has_blackjack:
            # Player wins 3:2
            winnings = bet_amount + (bet_amount * 1.5)
            self.equity += winnings
            self.stats.won_amount += bet_amount * 1.5  # Profit only
            self.stats.won_games += 1
            self.stats.total_games += 1
            self.betting_system.process_win()
            self.stats.update_equity_tracking(self.equity)
            return True
        elif dealer_has_blackjack:
            # Player loses
            self.stats.lost_amount += bet_amount
            self.stats.lost_games += 1
            self.stats.total_games += 1
            self.betting_system.process_loss()
            self.stats.update_equity_tracking(self.equity)
            return True
        
        # Play player hands
        active_hands = player_hands.copy()
        hand_index = 0
        
        while hand_index < len(active_hands):
            current_hand = active_hands[hand_index]
            
            # Play this hand
            while not current_hand.is_busted():
                action = BasicStrategy.should_hit(
                    current_hand, 
                    dealer_hand.cards[0], 
                    current_hand.can_double()
                )
                
                if action == 'stand':
                    break
                elif action == 'hit':
                    current_hand.add_card(self.shoe.deal_card())
                elif action == 'double':
                    if current_hand.can_double():
                        # Double the bet
                        double_bet = current_hand.bet
                        self.equity -= double_bet
                        self.stats.total_bet += double_bet
                        current_hand.bet += double_bet
                        current_hand.doubled = True
                        # Hit once
                        current_hand.add_card(self.shoe.deal_card())
                        break
                    else:
                        # Can't double, just hit
                        current_hand.add_card(self.shoe.deal_card())
                elif action == 'split':
                    if (current_hand.can_split() and 
                        len([h for h in active_hands if h.split_from == current_hand]) < self.max_splits):
                        # Create new hand
                        new_hand = Hand()
                        new_hand.bet = current_hand.bet
                        new_hand.split_from = current_hand
                        
                        # Move one card to new hand
                        new_hand.add_card(current_hand.cards.pop())
                        
                        # Deal new cards to both hands
                        current_hand.add_card(self.shoe.deal_card())
                        new_hand.add_card(self.shoe.deal_card())
                        
                        # Add bet for new hand
                        self.equity -= new_hand.bet
                        self.stats.total_bet += new_hand.bet
                        
                        # Add new hand to active hands
                        active_hands.append(new_hand)
                    else:
                        # Can't split, treat as hit
                        current_hand.add_card(self.shoe.deal_card())
            
            hand_index += 1
        
        # For European/Macau style, deal dealer's second card now
        if self.style in [GameStyle.EUROPEAN, GameStyle.MACAU]:
            dealer_hand.add_card(self.shoe.deal_card())
            
            # Check for dealer blackjack
            if dealer_hand.is_blackjack():
                dealer_has_blackjack = True
                
                # Handle losses based on style
                total_lost = 0
                for hand in active_hands:
                    if self.style == GameStyle.EUROPEAN:
                        # Lose all bets
                        total_lost += hand.bet
                    else:  # Macau
                        # Lose only original bet (not doubles/splits)
                        original_bet = self.betting_system.get_bet_amount()
                        total_lost += original_bet                        # Return the extra bets
                        extra_bet = hand.bet - original_bet
                        if extra_bet > 0:
                            self.equity += extra_bet
                            self.stats.total_bet -= extra_bet
                
                self.stats.lost_amount += total_lost
                self.stats.lost_games += 1
                self.stats.total_games += 1
                self.betting_system.process_loss()
                self.stats.update_equity_tracking(self.equity)
                return True
        
        # Play dealer hand (if no dealer blackjack)
        if not dealer_has_blackjack:
            while True:
                dealer_value, dealer_soft = dealer_hand.get_value()
                
                if dealer_value > 21:
                    break  # Dealer busted
                elif dealer_value > 17:
                    break  # Dealer stands
                elif dealer_value == 17:
                    if self.dealer_rule == DealerRule.STAND_17:
                        break  # Stand on all 17s
                    elif not dealer_soft:
                        break  # Stand on hard 17
                    # Otherwise hit on soft 17
                
                dealer_hand.add_card(self.shoe.deal_card())
        
        # Determine results for each hand
        dealer_value = dealer_hand.get_value()[0]
        dealer_busted = dealer_hand.is_busted()
        
        game_won = False
        game_lost = False
        game_pushed = False
        
        total_winnings = 0
        total_losses = 0
        
        for hand in active_hands:
            player_value = hand.get_value()[0]
            player_busted = hand.is_busted()
            
            if player_busted:
                # Player loses
                total_losses += hand.bet
                game_lost = True
            elif dealer_busted:
                # Player wins
                winnings = hand.bet * 2  # Return bet + equal win
                self.equity += winnings
                total_winnings += hand.bet  # Profit only
                game_won = True
            elif player_value > dealer_value:
                # Player wins
                winnings = hand.bet * 2  # Return bet + equal win
                self.equity += winnings
                total_winnings += hand.bet  # Profit only
                game_won = True
            elif player_value < dealer_value:
                # Player loses
                total_losses += hand.bet
                game_lost = True
            else:
                # Push
                self.equity += hand.bet  # Return bet
                game_pushed = True
        
        # Update statistics
        self.stats.won_amount += total_winnings
        self.stats.lost_amount += total_losses
          # Determine overall game result for betting system
        if game_won and not game_lost:
            self.stats.won_games += 1
            self.betting_system.process_win()
        elif game_lost and not game_won:
            self.stats.lost_games += 1
            self.betting_system.process_loss()
        else:
            self.stats.push_games += 1
            # No betting system change for push
        
        self.stats.total_games += 1
        
        # Update equity tracking
        self.stats.update_equity_tracking(self.equity)
        
        return True
    
    def run_simulation(self, num_games: int):
        """Run the full simulation"""
        games_played = 0
        
        while games_played < num_games:
            can_continue = self.play_game()
            games_played += 1
            
            if not can_continue:
                # Need to shuffle
                self.shoe.shuffle()
          # Display results
        self.display_results()
    
    def display_results(self):
        """Display simulation results"""
        print("\n" + "="*50)
        print("BLACKJACK SIMULATION RESULTS")
        print("="*50)
        
        print(f"Games Played: {self.stats.total_games}")
        print(f"Games Won: {self.stats.won_games}")
        print(f"Games Lost: {self.stats.lost_games}")
        print(f"Games Pushed: {self.stats.push_games}")
        print()
        
        print(f"Final Equity: ${self.equity:.2f}")
        print(f"Max Equity: ${self.stats.max_equity:.2f}")
        print(f"Min Equity: ${self.stats.min_equity:.2f}")
        print(f"Max Drawdown: ${self.stats.max_drawdown:.2f}")
        print(f"Total Amount Bet: ${self.stats.total_bet:.2f}")
        print(f"Total Amount Won (Profit): ${self.stats.won_amount:.2f}")
        print(f"Total Amount Lost: ${self.stats.lost_amount:.2f}")
        print()
        
        print(f"Expected Return: {self.stats.expected_return:.4f}")
        print(f"Expected Loss: {self.stats.expected_loss:.4f}")
        print(f"Expected Value: {self.stats.expected_value:.4f}")
        print()
        
        print(f"Final Betting System Status: {self.betting_system.get_status()}")
        print()
        
        win_rate = self.stats.won_games / self.stats.total_games * 100 if self.stats.total_games > 0 else 0
        push_rate = self.stats.push_games / self.stats.total_games * 100 if self.stats.total_games > 0 else 0
        loss_rate = self.stats.lost_games / self.stats.total_games * 100 if self.stats.total_games > 0 else 0
        
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Push Rate: {push_rate:.2f}%")
        print(f"Loss Rate: {loss_rate:.2f}%")


def main():
    """Main function to run the simulator"""
    parser = argparse.ArgumentParser(description='Blackjack Simulator')
    
    parser.add_argument('-d', '--dealer', choices=['s17', 'h17'], default='s17',
                        help='Dealer rule: s17 (stand all 17) or h17 (hit soft 17)')
    parser.add_argument('-n', '--decks', type=int, choices=range(1, 9), default=6,
                        help='Number of decks in shoe (1-8)')
    parser.add_argument('-s', '--style', choices=['A', 'E', 'M'], default='A',
                        help='Game style: A(merican), E(uropean), M(acau)')
    parser.add_argument('-a', '--shuffle', choices=['y', 'n'], default='y',
                        help='Auto shuffle: y(es) or n(o)')
    parser.add_argument('-g', '--games', type=int, choices=range(1, 10000001), default=10000,
                        help='Number of games to play (1-100000)')
    parser.add_argument('-m', '--splits', type=int, choices=range(1, 5), default=2,
                        help='Maximum number of splits allowed (1-4)')
    
    args = parser.parse_args()
    
    # Convert arguments
    dealer_rule = DealerRule.STAND_17 if args.dealer == 's17' else DealerRule.HIT_SOFT_17
    style = GameStyle(args.style)
    auto_shuffle = args.shuffle == 'y'
    
    print("Starting Blackjack Simulation...")
    print(f"Configuration: {args.decks} decks, {args.dealer}, {style.value} style, "
          f"auto-shuffle: {auto_shuffle}, {args.games} games, max splits: {args.splits}")
    print()
    
    # Create and run simulation
    game = BlackjackGame(
        num_decks=args.decks,
        dealer_rule=dealer_rule,
        style=style,
        auto_shuffle=auto_shuffle,
        max_splits=args.splits
    )
    
    game.run_simulation(args.games)


if __name__ == "__main__":
    main()
