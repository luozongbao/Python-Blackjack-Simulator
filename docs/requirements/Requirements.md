
1. Write Python Code simulating Blackjack game with 
    - options
        - d: s17, h17 (dealer stand on all 17 and above, dealer stand on hard 17 and above [optional:s17])
        - n: 1 - 8 (number of deck in shoes [optiona:6])
        - s: A, E, M (style American, European, Macau [Optional:A])
            - American (Default): Dealt two cards (Dealer Check for Blackjack after dealt 2 cards and faceup card is showing 10)
            - European: Dealt one card.  On dealer has blackjack, lose all original bet and the double and splits money if dealer has blackjack 
            - Macau: Dealt one card. On dealer has blackjack, lose only original bet
        - a: y, n (y: Auto Shuffle Machine: Shuffle every new game [optional:y] n: deal from the shoe until it exceeds 80% then shuffle on the next new game)
        - g: 1-100000 (number of game plays [optional:10000])
        - s: 1-4 (number of split up to [optional:2])
    - create real shoes and deal real cards, dont need to generate suites
2. simulate a player start equity with 0 money each bet subtract from the equity each win + to equity.  Play with perfect Blackjack strategy (standard card values: A=1/11, face cards=10, numbers=face value), but no surrender, hit on 15, and 16 against dealer 10. Player playing with betting strategy as follow
    - suppose score 0 and level 1 and bet 1 unit
    - every win score +1 max 0 (score can never go above 0), if lose score -1 min -3
    - if score reaches -3 reset score to 0, and set level = level +1 and bet = 3^(level-1) unit
    - if on level more than 1 if won at score 0 already then level = level-1 and reset score to 0
    - if level 3 and score reaches -3 return to level 1 score 0
    - if at level 1 and won at score 0 stays at level 1 score 0 (does not go to score +1)
    - Splitting: Can split any pair, can split up to specified limit, can double down on split hands
    - European style clarification: lose ALL bets (original + double/split money) when dealer has blackjack
3. Track status won amount (actually won: profit only, not include original bet), lose amount, total bet, Final Equity, Max Equity, Min Equity, Max Drawdown, Max Strategy level  won games, lose games, push games, total games, Expected Return, Expected Loss, Expected Value. Display results in console. 