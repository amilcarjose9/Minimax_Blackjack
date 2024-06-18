# Minimax_Blackjack
The motivation behind this project is to explore the application of artificial intelligence (AI) in strategic game scenarios, specifically Blackjack. The objective is to develop an AI that can evaluate the game's state and make decisions on betting and playing hands, aiming to maximize its chances of winning.

## Architecture
**Card Handling**: manage the deck of cards, dealing cards to players, and calculating the value of hands.
* Deck of cards initialized with suits, ranks, and values.
* initialize_deck() sets up the deck by generating all possible combinations of suits and ranks.
* deal_card() randomly selects a card from the deck and removes it, simulating card dealing.
* calculate_hand_value() computes the total value of a hand after adjusting the value of Aces if necessary

**Game Execution:** orchestrate the flow of the blackjack game and manage the interaction between players and the deck of cards.
* run_game_loop() and run_game_simulations() control the execution flow, allowing users to play single games or run multiple game simulations.
* Game outcomes are tracked and displayed to the user, including the total number of games played, player wins, dealer wins, and ties.

## Minimax player

**Input:** player's current hand, the dealer's current visible hand, remaining deck of cards.

**Evaluation Function:** estimate_win_probability()
* Estimates the probability of the player winning based on the current hand and the dealer's visible card.
* Simulates multiple scenarios where the dealer hits until their hand value is at least 17.
* Then it compares the player's current hand value with the average value the dealer achieves in these simulations.
* If the player's hand value is greater than this average dealer value, it returns 1, indicating a higher chance of winning, otherwise 0.

**Decision Making:**
* Calculates the win probability for hitting and standing by calling the estimate_win_probability() function twice:
  * Once with the player's hand after hitting (adding a random card from the remaining deck).
  * Once with the player's current hand (no additional cards).
* Returns 'hit' if the win probability for hitting is greater than the win probability for standing; otherwise returns 'stand'.

