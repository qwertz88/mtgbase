import os
import json
import pathlib
from datetime import datetime

# 💬 File and folder paths
# BASE_DIR points to the folder containing this file
BASE_DIR = pathlib.Path(__file__).resolve().parent

# DATA_DIR will hold all application data (users + decks)
DATA_DIR = BASE_DIR / "data"

# USERS_FILE stores all login credentials as JSON: {username: password}
USERS_FILE = DATA_DIR / "users.json"

# DECKS_DIR contains one .json file per user with their deck data
DECKS_DIR = DATA_DIR / "decks"

# Create the decks folder if it doesn't exist
os.makedirs(DECKS_DIR, exist_ok=True)

# Initialize an empty users.json file if it doesn't exist
if not USERS_FILE.exists():
    with open(USERS_FILE, "w") as file:
        json.dump({}, file)

# 💬 Load/save user credentials
# Reads all registered users
def load_users():
    with open(USERS_FILE, "r") as file:
        return json.load(file)

# Saves the current state of user credentials
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

# 💬 Each user's decks are stored in a JSON dict: {deck_name: [cards]}

# Returns the path to a user's deck file
def get_deck_file(username):
    return os.path.join(DECKS_DIR, f"{username}.json")

# Loads all decks for a given user
# If old format (list) is found, it converts to dict and saves
def load_decks(username):
    file_path = get_deck_file(username)
    try:
        with open(file_path, "r") as file:
            decks = json.load(file)
            if isinstance(decks, list):  # legacy support
                decks = {name: [] for name in decks}
                save_decks(username, decks)
            return decks
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Saves all decks for a user
# Format: {deck_name: [card1, card2, ...]}
def save_decks(username, decks):
    with open(get_deck_file(username), "w") as file:
        json.dump(decks, file)

# 💬 Get all cards in one deck
def get_deck_cards(username, deck_name):
    decks = load_decks(username)
    if isinstance(decks.get(deck_name), dict):
        return decks[deck_name].get("cards", [])
    return decks.get(deck_name, [])

# 💬 Add a card to a deck if it's not already in it

def add_card_to_deck(username, deck_name, card_name):
    decks = load_decks(username)
    decks.setdefault(deck_name, {"cards": [], "updated_at": None})
    if card_name and card_name not in decks[deck_name]["cards"]:
        decks[deck_name]["cards"].append(card_name)
        decks[deck_name]["updated_at"] = datetime.utcnow().isoformat()
        save_decks(username, decks)
