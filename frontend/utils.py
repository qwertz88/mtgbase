import os
import json
import pathlib
import re
from datetime import datetime
from dbmanager import DBManager
from shiny import ui

# === Path Configuration ===

# Define base project directory
BASE_DIR = pathlib.Path(__file__).resolve().parent

# Directory for application data
DATA_DIR = BASE_DIR / "data"

# JSON file for user credentials
USERS_FILE = DATA_DIR / "users.json"

# Directory containing decks per user
DECKS_DIR = DATA_DIR / "decks"

# Ensure data directories exist
os.makedirs(DECKS_DIR, exist_ok=True)

# Initialize users.json if it doesn't exist
if not USERS_FILE.exists():
    with open(USERS_FILE, "w") as file:
        json.dump({}, file)

# === Utility Functions ===

def mana_symbol_to_filename(symbol: str) -> str:
    """Convert mana symbol to corresponding filename."""
    if "/" in symbol:
        return symbol.replace("/", "").upper()
    elif symbol.isdigit():
        return symbol
    elif symbol.upper() in {"X", "Y", "Z"}:
        return f"C_{symbol.upper()}"
    return symbol.upper()

# === User Management ===

def load_users() -> dict:
    """Load user credentials from JSON file."""
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_users(users: dict) -> None:
    """Save user credentials to JSON file."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

# === Deck Management ===

def get_deck_file(username: str) -> pathlib.Path:
    """Return the deck file path for a given user."""
    return DECKS_DIR / f"{username}.json"

def load_decks(username: str) -> dict:
    """Load all decks for a given user. Auto-upgrade old formats if needed."""
    file_path = get_deck_file(username)
    try:
        with open(file_path, "r") as file:
            decks = json.load(file)
            if isinstance(decks, list):
                decks = {name: [] for name in decks}
                save_decks(username, decks)
            return decks
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_decks(username: str, decks: dict) -> None:
    """Save all decks of a user to file."""
    with open(get_deck_file(username), "w") as file:
        json.dump(decks, file)

def get_deck_cards(username: str, deck_name: str) -> list:
    """Get all cards from a specific deck."""
    decks = load_decks(username)
    if isinstance(decks.get(deck_name), dict):
        return decks[deck_name].get("cards", [])
    return decks.get(deck_name, [])

def add_card_to_deck(username: str, deck_name: str, card_name: str) -> None:
    """Add a card to a deck if it is not already present."""
    decks = load_decks(username)
    decks.setdefault(deck_name, {"cards": [], "commander": [], "updated_at": None})

    match = find_card_by_name(card_name)
    if not match:
        return

    existing_names = {c.get("name") for c in decks[deck_name]["cards"]}
    if card_name not in existing_names:
        decks[deck_name]["cards"].append(match)
        decks[deck_name]["updated_at"] = datetime.utcnow().isoformat()
        save_decks(username, decks)

# === Database Access ===

_password = os.environ.get("DB_PASSWORD")
_db = DBManager(dbname="mtgbase", user="postgres", password=_password)

def get_all_cards() -> list[dict]:
    """Fetch one version per card name from the database."""
    return _db.get_cards_by_name("")  # Empty search returns all distinct names

def find_card_by_name(name: str) -> dict | None:
    """Find a single unique card by name using DB directly."""
    return _db.get_cards_by_name(name)[0] if _db.get_cards_by_name(name) else None


# === UI Rendering ===

def render_mana_cost(mana_cost_str: str):
    """Render mana cost string into icon images."""
    if not mana_cost_str:
        return ""

    parts = mana_cost_str.replace("{", "").split("}")
    icons = [mana_symbol_to_filename(part) for part in parts if part]

    return ui.span(*[
        ui.img(
            src=f"/icons/{symbol}.svg",
            height="16px",
            style="vertical-align: middle; margin-right: 2px;",
            title=symbol
        ) for symbol in icons
    ])

def render_text_with_icons(text: str):
    """Replace mana symbols in card text with corresponding icons."""
    if not text:
        return ""

    text = (
        text.replace("â€”", "—")
            .replace("â€™", "’")
            .replace("\\n", "\n")
            .replace("\n", "<br>")
            .replace("â€¢", "*")
            .replace("âˆ’", "-")
    )

    def replace_symbol(match):
        symbol = match.group(1)
        filename = mana_symbol_to_filename(symbol)
        return f"<img src='/icons/{filename}.svg' title='{symbol}' height='16px' style='vertical-align: middle; margin-right: 2px;'/>"

    html = re.sub(r"\{([^}]+)\}", replace_symbol, text)
    return ui.HTML(html)

def render_card_list(cards: list, add_button_class: str = "add-card-btn"):
    """Render an HTML table of cards with add buttons."""
    headers = ui.tags.tr(
        ui.tags.th("Add"),
        ui.tags.th("Name"),
        ui.tags.th("Mana Cost"),
        ui.tags.th("Type(s)"),
        ui.tags.th("Text"),
    )

    rows = [
        ui.tags.tr(
            ui.tags.td(
                ui.tags.button("Add", class_=add_button_class, **{"data-card": card["name"]})
            ),
            ui.tags.td(card.get("name") or ""),
            ui.tags.td(str(int(card.get("manavalue"))) if card.get("manavalue") is not None else ""),
            ui.tags.td(" ".join((card.get("supertypes") or []) + (card.get("types") or []))),
            ui.tags.td(render_text_with_icons(card.get("text"))),
        ) for card in cards
    ]

    return ui.tags.table(
        {"style": "width: 100%; border-collapse: collapse; margin-top: 1em;"},
        headers,
        *rows
    )
def is_basic_land(card):
    return (
        "Land" in (card.get("types") or []) and
        "Basic" in (card.get("supertypes") or []) and
        card.get("name") in {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}
    )
