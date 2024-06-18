import random
from itertools import product

# Initialize the deck of cards
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

def initialize_deck():
    return list(product(suits, ranks))

def deal_card(deck):
    if deck:
        chosen_card = random.choice(deck)
        deck.remove(chosen_card)
        return chosen_card
    else:
        return None

def calculate_hand_value(hand):
    value = sum(values[card] for card in hand)
    num_aces = hand.count('Ace')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def minimax_agent(hand, dealer_hand, deck):
    dealer_visible_rank = dealer_hand[0][1]
    remaining_deck = [card for card in deck if card[1] not in hand and card not in dealer_hand]
    hit_win_prob = estimate_win_probability(hand + [random.choice(remaining_deck)[1]], dealer_visible_rank, remaining_deck)
    stand_win_prob = estimate_win_probability(hand, dealer_visible_rank, remaining_deck)
    return 'hit' if hit_win_prob > stand_win_prob else 'stand'

def estimate_win_probability(hand, dealer_visible, remaining_deck):
    player_current_value = calculate_hand_value(hand)
    if player_current_value > 21:
        return 0
    dealer_chances = 0
    simulations = 0
    for card_tuple in remaining_deck:
        card = card_tuple[1]
        simulated_dealer_hand = [dealer_visible, card]
        while calculate_hand_value(simulated_dealer_hand) < 17:
            next_card = deal_card(remaining_deck.copy())
            if next_card:
                simulated_dealer_hand.append(next_card[1])
        if calculate_hand_value(simulated_dealer_hand) <= 21:
            dealer_chances += calculate_hand_value(simulated_dealer_hand)
        simulations += 1
    dealer_average = dealer_chances / simulations if simulations else 0
    return 1 if player_current_value > dealer_average else 0

def simulate_blackjack_game(agent_player):
    deck = initialize_deck()
    player_hand = [deal_card(deck)[1] for _ in range(2)]
    dealer_hand = [deal_card(deck) for _ in range(2)]

    # Player's turn
    while calculate_hand_value(player_hand) < 21:
        action = agent_player(player_hand, dealer_hand, deck)
        if action == 'hit':
            player_hand.append(deal_card(deck)[1])
        else:
            break

    player_score = calculate_hand_value(player_hand)
    if player_score > 21:
        return "Dealer wins"

    # Dealer's turn
    dealer_hand_values = [card[1] for card in dealer_hand]
    while calculate_hand_value(dealer_hand_values) < 17:
        dealer_hand_values.append(deal_card(deck)[1])


    dealer_score = calculate_hand_value(dealer_hand_values)
    if dealer_score > 21:
        return "Player wins"
    elif player_score == dealer_score:
        return "Tie"
    elif player_score > dealer_score:
        return "Player wins"
    else:
        return "Dealer wins"

def run_game_simulations():
    amount = ''
    while not amount.isnumeric():
        amount = input("\nHow many simulations do you want the Minimax agent to run? (Input a number): ")
    amount = int(amount)
    agent_player = minimax_agent 
    games_played = amount
    player_wins = 0
    dealer_wins = 0
    ties = 0
    orignal_amount = amount
    
    while amount != 0:
        amount -= 1
        result = simulate_blackjack_game(agent_player)  
        # print(result)
        if result == "Player wins":
            player_wins += 1
        elif result == "Dealer wins":
            dealer_wins += 1
        else:
            ties += 1

    print(f"\nTotal games played: {games_played}")
    print(f"Player wins: {player_wins}")
    print(f"Dealer wins: {dealer_wins}")
    print(f"Ties: {ties}")

    print(f"Win-ratio: {player_wins/orignal_amount}")
    print(f"Loss-ratio: {dealer_wins/orignal_amount}")
    print(f"Tie-ratio: {ties/orignal_amount}\n")


def run_game_loop():
    choice = ''
    while choice != '1' and choice != '2':
        choice = input("Which agent should be the player? (1 for Minimax, 2 for User): ")
    if choice == '1':
        agent_player = minimax_agent 
    games_played = 0
    player_wins = 0
    dealer_wins = 0
    ties = 0

    while True:
        deck = initialize_deck()
        player_hand = [deal_card(deck)[1] for _ in range(2)]
        dealer_hand = [deal_card(deck) for _ in range(2)]
        player_usable_ace = 'Ace' in player_hand
        dealer_visible_card = dealer_hand[0][1]
        print("\nDealer's Visible Hand:", dealer_visible_card)
        print("Player's Hand:", player_hand)
        print("Total Sum:", calculate_hand_value(player_hand))
        print("Has Usable Ace:", player_usable_ace)

        # Player's turn
        while calculate_hand_value(player_hand) < 21:
            if choice == '1':
            # if agent_player == minimax_agent:
                action = agent_player(player_hand, dealer_hand, deck)
            else:
                while True:
                    action = input("Do you want to Hit or Stand? (hit/stand): ").lower()
                    if action == 'hit' or action == 'stand': break
            print("\nPlayer Action:", action.upper())
            if action == 'hit':
                player_hand.append(deal_card(deck)[1])
                print("\nPlayer's Hand:", player_hand)
                print("Total Sum:", calculate_hand_value(player_hand))
            else:
                break

        player_score = calculate_hand_value(player_hand)
        dealer_hand_values = [card[1] for card in dealer_hand]
        dealer_score = calculate_hand_value(dealer_hand_values)
        if player_score > 21:
            print("\nYou bust! Dealer wins.")
            print("Player's Final Hand:", player_hand)
            print("Dealer's Final Hand:", dealer_hand_values)
            print("Player's Score:", player_score)
            print("Dealer's Score:", dealer_score)
            dealer_wins += 1

        else: 
            # Dealer's turn
            while calculate_hand_value(dealer_hand_values) < 17:
                dealer_hand_values.append(deal_card(deck)[1])

            dealer_score = calculate_hand_value(dealer_hand_values)

            print("\nPlayer's Final Hand:", player_hand)
            print("Dealer's Final Hand:", dealer_hand_values)
            print("Player's Score:", player_score)
            print("Dealer's Score:", dealer_score)

            if dealer_score > 21:
                print("Player wins")
                player_wins += 1
            elif player_score == dealer_score:
                print("Tie")
                ties += 1
            elif player_score > dealer_score:
                print("Player wins")
                player_wins += 1
            else:
                print("Dealer wins")
                dealer_wins += 1

        games_played += 1

        if input("\nDo you want to start another game? (yes/no): ").lower() != 'yes':
            break

    print(f"\nTotal games played: {games_played}")
    print(f"Player wins: {player_wins}")
    print(f"Dealer wins: {dealer_wins}")
    print(f"Ties: {ties}\n")

def main():
    choice = ''
    while choice != '1' and choice != '2':
        choice = input("Which mode do you want to play (1 for Normal, 2 for Multi): ")
    if choice == '1':
       run_game_loop()
    else:
        run_game_simulations()

main()
