import random
import json

# Class representing a Card object
class Card:
    def __init__(self, suit, value):
        """Initialise a card with a suit and a value."""
        self.suit = suit
        self.value = value

    def __str__(self):
        """Return a human-readable string representation of the card."""
        return f"{self.value} of {self.suit}"

# Class representing a Player
class Player:
    def __init__(self, name):
        """Initialise a player with a name and a starting score of 0."""
        self.name = name
        self.score = 0

    def add_point(self):
        """Increase the player's score by 1."""
        self.score += 1

    def reset_score(self):
        """Reset the player's score to 0."""
        self.score = 0

# Main class for the Python Card War game
class PythonCardWar:
    def __init__(self):
        """Initialise the game with a shuffled deck and an empty player list."""
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.players = []

    def create_deck(self):
        """Create a standard deck of cards with two special Jokers."""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = list(range(2, 15))  # 2 to 14 (where 11 = Jack, 12 = Queen, etc.)
        # Create the deck and add two Joker cards with a unique effect
        deck = [Card(suit, value) for suit in suits for value in values]
        deck.append(Card("Special", "Joker"))
        deck.append(Card("Special", "Joker"))
        return deck

    def add_players(self):
        """Prompt players to enter their names and add them to the game."""
        for i in range(2):  # Two players for the game
            name = input(f"Please enter name for Player {i + 1}: ")
            self.players.append(Player(name))

    def play_round(self):
        """Conduct a single round of the game, applying special card rules."""
        if len(self.deck) < 2:
            print("Not enough cards to continue.")
            return False

        card1, card2 = self.deck.pop(), self.deck.pop()
        player1, player2 = self.players[0], self.players[1]

        print(f"{player1.name} drew {card1}, {player2.name} drew {card2}")

        # Handling special cards
        if card1.value == "Joker" or card2.value == "Joker":
            print("A Joker was drawn! Both players' scores are reset to 0!")
            player1.reset_score()
            player2.reset_score()
        elif card1.suit == "Hearts" and card1.value == 14:  # Ace of Hearts
            print(f"{player1.name} drew the Ace of Hearts and gets an extra point!")
            player1.add_point()
        elif card2.suit == "Hearts" and card2.value == 14:  # Ace of Hearts
            print(f"{player2.name} drew the Ace of Hearts and gets an extra point!")
            player2.add_point()
        else:
            # Regular round comparison
            if card1.value > card2.value:
                player1.add_point()
                print(f"{player1.name} wins this round ayy!")
            elif card2.value > card1.value:
                player2.add_point()
                print(f"{player2.name} wins this round ayy!")
            else:
                print("Welp it's a tie!")

        # Display scores after each round
        print(f"Scores: {player1.name}: {player1.score}, {player2.name}: {player2.score}")
        return True

    def save_game(self):
        """Save the game state to a file for future continuation."""
        game_state = {
            "deck": [(card.suit, card.value) for card in self.deck],
            "players": [{"name": player.name, "score": player.score} for player in self.players]
        }
        with open("game_save.json", "w") as file:
            json.dump(game_state, file)
        print("Game state saved successfully!")

    def load_game(self):
        """Load the game state from a file."""
        try:
            with open("game_save.json", "r") as file:
                game_state = json.load(file)
            self.deck = [Card(suit, value) for suit, value in game_state["deck"]]
            self.players = [Player(p["name"]) for p in game_state["players"]]
            for i, player in enumerate(self.players):
                player.score = game_state["players"][i]["score"]
            print("Game state loaded successfully!")
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")

    def play_game(self, rounds_limit):
        """Play the game for a given number of rounds or until the deck is tiredno."""
        self.add_players()
        round_counter = 0

        while round_counter < rounds_limit and self.play_round():
            round_counter += 1

        # Determine the winner based on the final scores
        if self.players[0].score > self.players[1].score:
            print(f"{self.players[0].name} is the overall winner!")
        elif self.players[1].score > self.players[0].score:
            print(f"{self.players[1].name} is the overall winner!")
        else:
            print("The game is a tie!")

if __name__ == "__main__":
    game = PythonCardWar()
    choice = input("Do you want to load a saved game? (yes/no): ").strip().lower()
    if choice == "yes":
        game.load_game()

    try:
        rounds_limit = int(input("Enter the number of rounds to play: "))
        game.play_game(rounds_limit)
    except ValueError:
        print("Invalid input. Please enter a valid number of rounds.")

    save_choice = input("Do you want to save the game? (yes/no): ").strip().lower()
    if save_choice == "yes":
        game.save_game()
