from shiny import reactive, render, ui
import humanize
from datetime import datetime
from layout import Page
from ui import login_ui, register_ui, logged_in_ui, deck_view_ui
from utils import (
    load_users, save_users,
    load_decks, save_decks,
    get_deck_cards, add_card_to_deck
)
from state import session_user, ui_mode, active_deck, card_update_counter

# 🧠 Reactive values to show login/register feedback
login_msg_val = reactive.Value("")
register_msg_val = reactive.Value("")

commander_error_val = reactive.Value("")

# 🔄 Load user data once on startup
USERS = load_users()

TAG_ORDER = [
    "commander", "artifact", "battle", "conspiracy", "creature", "dungeon",
    "enchantment", "instant", "kindred", "land", "phenomenon", "plane",
    "planeswalker", "scheme", "sorcery", "vanguard"
]

def get_card_type(card_name, commander_names):
    if card_name in commander_names:
        return "commander"
    # naive logic — improve later if needed
    card_name_lc = card_name.lower()
    for tag in TAG_ORDER:
        if tag != "commander" and tag in card_name_lc:
            return tag
    return "other"


# 🔁 Utility: trigger deck/card list UI to refresh
def trigger_update():
    card_update_counter.set(card_update_counter.get() + 1)


# ✂️ Utility: safely strip text inputs
def get_clean_input(input, name):
    return input[name]().strip()


# 📦 Utility: save decks and trigger UI update
def update_decks_and_refresh(username, decks):
    save_decks(username, decks)
    trigger_update()


# ⏱️ Utility: format "updated_at" timestamps into "2 minutes ago"
def format_updated(updated_at):
    if not updated_at:
        return ""
    try:
        dt = datetime.fromisoformat(updated_at)
        return f"(updated {humanize.naturaltime(datetime.utcnow() - dt)})"
    except Exception:
        return ""


# 🚀 Main reactive server logic
def server(input, output, session):
    # Text feedback messages for login and register
    @output
    @render.text
    def login_msg():
        return login_msg_val.get()

    @output
    @render.text
    def register_msg():
        return register_msg_val.get()

    # Main UI router: switches between login/register or deck view
    @output
    @render.ui
    def main_ui():
        user = session_user.get()
        deck = active_deck.get()
        if not user:
            return Page.build_view("Login", login_ui) if ui_mode.get() == "login" else Page.build_view("Register",
                                                                                                       register_ui)
        if deck:
            return Page.build_view(f"Deck: {deck}", deck_view_ui(deck))
        return Page.build_view("Your Decks", logged_in_ui(user))

    # List decks with buttons to open/delete
    @output
    @render.ui
    def deck_list():
        username = session_user.get()
        _ = card_update_counter.get()
        if not username:
            return ui.div()

        decks = load_decks(username)
        search = input.deck_search().lower().strip() if "deck_search" in input else ""

        # Filter based on search
        filtered = {
            name: data for name, data in decks.items()
            if search in name.lower()
        }

        header = ui.tags.tr(
            ui.tags.th(""),  # ⭐
            ui.tags.th("Name"),
            ui.tags.th("Colors"),
            ui.tags.th("Commander"),
            ui.tags.th("Last Updated"),
            ui.tags.th("")  # ❌
        )

        rows = []
        for deck in sorted(filtered, key=lambda d: (not filtered[d].get("favorite", False), d.lower())):
            deck_data = filtered[deck]

            rows.append(ui.tags.tr(
                ui.tags.td(
                    ui.a("⭐" if deck_data.get("favorite") else "☆",
                         href="#", class_="toggle-fav",
                         title="Unmark favorite" if deck_data.get("favorite") else "Mark as favorite",
                         **{"data-deck": deck})
                ),
                ui.tags.td(
                    ui.a(deck,
                         href="#", class_="open-deck",
                         title="Open deck",
                         **{"data-deck": deck})
                ),
                ui.tags.td(*[
                    ui.img(src=f"/icons/{color}.svg",
                           height="16px",
                           style="vertical-align: middle; margin-right: 2px;",
                           title=color)
                    for color in deck_data.get("colors", [])
                ]),
                ui.tags.td(" | ".join(deck_data.get("commander", [])) if deck_data.get("commander") else "—"),
                ui.tags.td(format_updated(deck_data.get("updated_at"))),
                ui.tags.td(
                    ui.a("❌", href="#", class_="delete-deck",
                         title="Delete deck",
                         **{"data-deck": deck})
                )
            ))

        return ui.div(
            ui.h4("📃 Your Decks:"),
            ui.tags.table(
                {"style": "width: 100%; border-collapse: collapse;"},
                header,
                *rows
            )
        )

    # List cards in the selected deck
    @output
    @render.ui
    def card_list():
        _ = card_update_counter.get()
        username, deck = session_user.get(), active_deck.get()
        if not username or not deck:
            return ui.div()

        decks = load_decks(username)
        deck_data = decks.get(deck, {})
        all_cards = deck_data.get("cards", [])
        commander_cards = deck_data.get("commander", [])

        # Group cards by type
        from collections import defaultdict
        grouped = defaultdict(list)

        # Include commanders in display
        for card in commander_cards:
            grouped["commander"].append(card)

        for card in all_cards:
            card_type = get_card_type(card, commander_cards)
            grouped[card_type].append(card)

        # Build UI by ordered tags
        sections = []
        for tag in TAG_ORDER:
            cards = grouped.get(tag)
            if not cards:
                continue

            sections.append(ui.h4(tag.capitalize()))
            sections.append(
                ui.tags.ul(*[
                    ui.tags.li(
                        ui.span(card + " "),
                        ui.a("❌", href="#", class_="delete-card", **{"data-card": card})
                    )
                    for card in sorted(cards)
                ])
            )

        return ui.div(*sections)

    # Mode switch: login <-> register
    @reactive.effect
    @reactive.event(input.switch_to_register)
    def switch_to_register():
        ui_mode.set("register")

    @reactive.effect
    @reactive.event(input.switch_to_login)
    def switch_to_login():
        ui_mode.set("login")

    # Handle user login
    @reactive.effect
    @reactive.event(input.login_btn)
    async def handle_login():
        username = get_clean_input(input, "username")
        password = get_clean_input(input, "password")
        if username in USERS and USERS[username] == password:
            session_user.set(username)
            active_deck.set(None)
        else:
            login_msg_val.set("❌ Invalid username or password")

    # Handle user registration
    @reactive.effect
    @reactive.event(input.register_btn)
    async def handle_register():
        new_user = get_clean_input(input, "new_username")
        new_pass = get_clean_input(input, "new_password")

        if not new_user or not new_pass:
            register_msg_val.set("❌ Please fill in all fields.")
            return

        if new_user in USERS:
            register_msg_val.set("❌ Username already exists.")
            return

        USERS[new_user] = new_pass
        save_users(USERS)
        save_decks(new_user, {})
        session_user.set(new_user)
        active_deck.set(None)

    # Handle logout
    @reactive.effect
    @reactive.event(input.logout_btn)
    async def handle_logout():
        session_user.set(None)
        active_deck.set(None)

    # Create a new deck and optionally activate it
    @reactive.effect
    @reactive.event(input.create_deck)
    def handle_create_deck():
        username = session_user.get()
        deck_name = get_clean_input(input, "deck_name")
        if not username or not deck_name:
            return

        decks = load_decks(username)
        if deck_name not in decks:
            decks[deck_name] = {
                "cards": [],
                "commander": "",  # 👈 NEW field
                "updated_at": datetime.utcnow().isoformat()
            }
            update_decks_and_refresh(username, decks)

        active_deck.set(deck_name)

    # Set active deck when user opens one
    @reactive.effect
    @reactive.event(input.open_deck_name)
    def open_deck():
        active_deck.set(input.open_deck_name())

    # Return to deck list view
    @reactive.effect
    @reactive.event(input.back_to_decks)
    def back_to_decks():
        active_deck.set(None)

    # Delete a deck from the user's list
    @reactive.effect
    @reactive.event(input.delete_deck)
    def delete_deck():
        username = session_user.get()
        deck_to_delete = input.delete_deck()
        if not username or not deck_to_delete:
            return

        decks = load_decks(username)
        if deck_to_delete in decks:
            del decks[deck_to_delete]
            update_decks_and_refresh(username, decks)
            if active_deck.get() == deck_to_delete:
                active_deck.set(None)

    # Add a card to the active deck
    @reactive.effect
    @reactive.event(input.add_card_btn)
    async def add_card():
        username, deck = session_user.get(), active_deck.get()
        card = get_clean_input(input, "card_name")
        if username and deck and card:
            add_card_to_deck(username, deck, card)
            trigger_update()
            await session.send_custom_message("clear_card_input", {})

    # Toggle favorite on decks
    @reactive.effect
    @reactive.event(input.toggle_favorite)
    def toggle_favorite():
        username = session_user.get()
        deck = input.toggle_favorite()
        if not username or not deck:
            return

        decks = load_decks(username)
        if deck in decks:
            decks[deck]["favorite"] = not decks[deck].get("favorite", False)
            save_decks(username, decks)
            trigger_update()

    # Remove a card from the active deck
    @reactive.effect
    @reactive.event(input.delete_card)
    def delete_card():
        username, deck = session_user.get(), active_deck.get()
        card_to_delete = input.delete_card()

        if username and deck and card_to_delete:
            decks = load_decks(username)
            if deck in decks:
                deck_data = decks[deck]
                changed = False

                # Remove from normal cards
                if "cards" in deck_data and card_to_delete in deck_data["cards"]:
                    deck_data["cards"].remove(card_to_delete)
                    changed = True

                # Remove from commanders
                if "commander" in deck_data and card_to_delete in deck_data["commander"]:
                    deck_data["commander"].remove(card_to_delete)
                    changed = True

                if changed:
                    save_decks(username, decks)
                    trigger_update()

    @reactive.effect
    @reactive.event(input.add_commander_btn)
    def add_commander():
        username, deck = session_user.get(), active_deck.get()
        card = get_clean_input(input, "card_name")

        if not username or not deck or not card:
            return

        decks = load_decks(username)
        deck_data = decks.get(deck)

        if deck_data:
            # 🛠 Fix: ensure commander is a list
            commander_data = deck_data.get("commander", [])
            if isinstance(commander_data, str):
                commander_data = [commander_data] if commander_data else []

            if card in commander_data:
                return  # avoid duplicates

            if len(commander_data) >= 2:
                commander_error_val.set("⚠️ You can only have 2 commanders.")
                return

            commander_data.append(card)
            deck_data["commander"] = commander_data
            commander_error_val.set("")  # ✅ Clear error
            update_decks_and_refresh(username, decks)

    @output
    @render.text
    def commander_error_msg():
        return commander_error_val.get()
