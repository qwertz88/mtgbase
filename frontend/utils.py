import os
import json
import pathlib
import re
from datetime import datetime
from dbmanager2 import DBManager2
from shiny import ui

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
    decks.setdefault(deck_name, {"cards": [], "commander": [], "updated_at": None})

    # Zoek volledige kaart in database
    cards_db = get_all_cards()
    match = next((c for c in cards_db if c.get("name") == card_name), None)
    if not match:
        return

    # Vermijd duplicaten
    if all(c.get("name") != card_name for c in decks[deck_name]["cards"]):
        decks[deck_name]["cards"].append(match)
        decks[deck_name]["updated_at"] = datetime.utcnow().isoformat()
        save_decks(username, decks)


# utils.py
_password = os.environ.get("DB_PASSWORD")
_db = DBManager2(dbname="mtgbase", user="postgres", password=_password)

def get_all_cards() -> list[dict]:
    # Get only selected card info for the UI
    return _db.get_selected_card_data()

from shiny import ui

from shiny import ui

def render_mana_cost(mana_cost_str):
    if not mana_cost_str:
        return ""
    parts = mana_cost_str.replace("{", "").split("}")

    icons = []

    for part in parts:
        if not part:
            continue

        # Hybride mana: {W/U} → WU.svg
        if "/" in part:
            icons.append(part.replace("/", "").upper())

        # Numeriek mana: {0}–{20} → gebruik direct 0.svg, 1.svg, ...
        elif part.isdigit():
            icons.append(part)  # toon bv. "5.svg"

        # X/Y/Z → als C_X.svg
        elif part.upper() in {"X", "Y", "Z"}:
            icons.append(f"C_{part.upper()}")

        # Alles standaard: bv. W, U, B, R, G, C
        else:
            icons.append(part.upper())

    return ui.span(*[
        ui.img(
            src=f"/icons/{symbol}.svg",
            height="16px",
            style="vertical-align: middle; margin-right: 2px;",
            title=symbol
        )
        for symbol in icons
    ])

def render_text_with_icons(text):
    if not text:
        return ""

    # Fix common encoding issues
    text = (
        text.replace("â€”", "—")  # em dash
            .replace("â€™", "’")  # apostrophe
            .replace("\\n", "\n")  # literal "\n" to newline
            .replace("\n", "<br>")  # actual linebreaks to HTML
    )

    def replace_symbol(match):
        symbol = match.group(1)
        if "/" in symbol:
            filename = symbol.replace("/", "").upper()
        elif symbol.isdigit():
            filename = symbol
        elif symbol.upper() in {"X", "Y", "Z"}:
            filename = f"C_{symbol.upper()}"
        else:
            filename = symbol.upper()

        return f"<img src='/icons/{filename}.svg' title='{symbol}' height='16px' style='vertical-align: middle; margin-right: 2px;'/>"

    html = re.sub(r"\{([^}]+)\}", replace_symbol, text)
    return ui.HTML(html)


