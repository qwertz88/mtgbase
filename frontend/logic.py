from shiny import reactive, render, ui
import humanize
from datetime import datetime
from layout import Page
from ui import login_ui, register_ui, logged_in_ui, deck_view_ui, card_search_ui
from utils import (
    load_users, save_users,
    load_decks, save_decks,
    get_all_cards, add_card_to_deck, render_mana_cost, render_text_with_icons, render_card_list, find_card_by_name
)
from state import session_user, ui_mode, active_deck, card_update_counter, choose_commander_stage,commander_search_name

# 🧠 Reactive values to show login/register feedback
login_msg_val = reactive.Value("")
register_msg_val = reactive.Value("")
card_error_val = reactive.Value("")
commander_error_val = reactive.Value("")

# 🔄 Load user data once on startup
USERS = load_users()

TAG_ORDER = [
    "commander", "artifact", "battle", "conspiracy", "creature", "dungeon",
    "enchantment", "instant", "kindred", "land", "phenomenon", "plane",
    "planeswalker", "scheme", "sorcery", "vanguard"
]

def get_card_type(card_data, commander_names):
    name = card_data.get("name", "")
    if name in commander_names:
        return "commander"

    types_field = card_data.get("types")
    if not types_field:
        return "other"

    # Zorg dat types altijd een lijst is
    if isinstance(types_field, str):
        types_field = [t.strip() for t in types_field.split(",")]

    # Match met de eerste tag uit TAG_ORDER die in types voorkomt
    for tag in TAG_ORDER:
        if tag.lower() in [t.lower() for t in types_field]:
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
        confirm_password = get_clean_input(input, "confirm_password")

        if not new_user or not new_pass or not confirm_password:
            register_msg_val.set("❌ Please fill in all fields.")
            return

        if new_pass != confirm_password:
            register_msg_val.set("❌ Passwords do not match.")
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
        show_card_search.set(False)  # 👈 Close card search view

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
    async def handle_add_card_and_show_list():
        username, deck = session_user.get(), active_deck.get()
        card = get_clean_input(input, "card_name")

        search_name_value.set(card)
        show_card_search.set(True)

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
                if "cards" in deck_data:
                    before = len(deck_data["cards"])
                    deck_data["cards"] = [c for c in deck_data["cards"] if c.get("name") != card_to_delete]
                    changed |= len(deck_data["cards"]) < before

                # Remove from commanders
                if "commander" in deck_data:
                    before = len(deck_data["commander"])
                    deck_data["commander"] = [c for c in deck_data["commander"] if c.get("name") != card_to_delete]
                    changed |= len(deck_data["commander"]) < before

                if changed:
                    save_decks(username, decks)
                    trigger_update()

    @output
    @render.text
    def commander_error_msg():
        return commander_error_val.get()

    # Track whether we're showing search view
    show_card_search = reactive.Value(False)
    search_name_value = reactive.Value("")

    @output
    @render.ui
    def filtered_card_list():
        name_filter = search_name_value.get() or ""
        type_filter = input.filter_type() or ""
        flavor_filter = input.filter_flavor() or ""
        subtype_filter = input.filter_subtype() or ""
        mana_filter = input.filter_mana_colors() or []

        cards = get_all_cards()

        def matches(card):
            name_ok = name_filter.lower() in (card.get("name") or "").lower()

            # --- Type ---
            card_types = card.get("types", [])
            if isinstance(card_types, str):
                card_types = [t.strip() for t in card_types.split(",")]
            type_ok = not type_filter or type_filter.lower() in [t.lower() for t in card_types]

            # --- Subtype ---
            subtype_ok = subtype_filter.lower() in (card.get("subtypes") or "").lower()

            # --- Flavor text ---
            flavor_ok = flavor_filter.lower() in (card.get("text") or "").lower()

            # --- Mana color check ---
            mana_cost = card.get("manacost") or ""
            mana_cost_pips = {p.strip("{}") for p in mana_cost.split("}") if "{" in p}

            # --- Manavalue ---
            mana_range = input.filter_mana_range() if "filter_mana_range" in input else (0, 15)

            mana_value = card.get("cmc") or card.get("manavalue") or 0
            mana_ok = mana_range[0] <= mana_value <= mana_range[1]

            if mana_filter:
                def is_colorless(pip):
                    return pip == "C" or pip.isdigit()

                if "C" in mana_filter:
                    if not any(is_colorless(p) for p in mana_cost_pips):
                        return False

                color_filter = set(mana_filter) - {"C"}
                if color_filter and not any(pip in color_filter for pip in mana_cost_pips):
                    return False

            return name_ok and type_ok and flavor_ok and subtype_ok and mana_ok

        filtered = [card for card in cards if matches(card)]

        headers = ui.tags.tr(
            ui.tags.th("Add"),
            ui.tags.th("Name"),
            ui.tags.th("Mana Cost"),
            ui.tags.th("Mana Value"),
            ui.tags.th("Type(s)"),
            ui.tags.th("Subtypes"),
            ui.tags.th("Power"),
            ui.tags.th("Toughness"),
            ui.tags.th("Text"),
            ui.tags.th("Rarity"),
        )

        rows = [
            ui.tags.tr(
                ui.tags.td(
                    ui.tags.button("Add", class_="add-card-btn", **{"data-card": card["name"]})
                ),
                ui.tags.td(card.get("name") or ""),
                ui.tags.td(render_mana_cost(card.get("manacost"))),
                ui.tags.td(str(int(card.get("cmc") or card.get("manavalue") or 0))),
                ui.tags.td(
                    " ".join(
                        filter(None, [
                            " ".join(card.get("supertypes", [])) if isinstance(card.get("supertypes"),
                                                                               list) else card.get("supertypes") or "",
                            " ".join(card.get("types", [])) if isinstance(card.get("types"), list) else card.get(
                                "types") or ""
                        ])
                    )
                ),
                ui.tags.td(card.get("subtypes") or ""),
                ui.tags.td(card.get("power") or ""),
                ui.tags.td(card.get("toughness") or ""),
                ui.tags.td(render_text_with_icons(card.get("text"))),
                ui.tags.td(card.get("rarity") or "")
            )
            for card in filtered
        ]

        return ui.tags.table(
            {"style": "width: 100%; border-collapse: collapse; margin-top: 1em;"},
            headers,
            *rows
        )

    @reactive.effect
    @reactive.event(input.add_commander_btn)
    def handle_add_commander():
        search_name_value.set(input.card_name())
        show_card_search.set(True)

        username, deck = session_user.get(), active_deck.get()
        card_name = get_clean_input(input, "card_name")

        if not username or not deck or not card_name:
            return

        decks = load_decks(username)
        deck_data = decks.get(deck)

        if deck_data:
            commander_data = deck_data.get("commander", [])
            if isinstance(commander_data, str):
                commander_data = [commander_data] if commander_data else []

            # Fetch full card info
            cards_db = get_all_cards()
            match = next((c for c in cards_db if c.get("name") == card_name), None)
            if not match:
                return

            if any(c.get("name") == card_name for c in commander_data):
                return  # avoid duplicates

            if len(commander_data) >= 2:
                commander_error_val.set("⚠️ You can only have 2 commanders.")
                return

            commander_data.append(match)
            deck_data["commander"] = commander_data
            commander_error_val.set("")  # ✅ Clear error
            update_decks_and_refresh(username, decks)

    @output
    @render.ui
    def deck_card_list():
        deck_data = current_deck_data()  # 👈 Reactively tracks deck + card changes
        if not deck_data:
            return ui.div()

        all_cards = deck_data.get("cards", [])
        commander_cards = deck_data.get("commander", [])

        from collections import defaultdict
        grouped = defaultdict(list)

        for card in commander_cards:
            grouped["commander"].append(card)

        for card in all_cards:
            card_type = get_card_type(card, [c["name"] for c in commander_cards])
            grouped[card_type].append(card)

        # Sort each group by mana value (cmc)
        for tag in grouped:
            grouped[tag] = sorted(grouped[tag], key=lambda c: c.get("cmc") or c.get("manavalue") or 0)

        sections = []
        for tag in TAG_ORDER:
            cards = grouped.get(tag)
            if not cards:
                continue

            sections.append(ui.h4(f"{tag.capitalize()} ({len(cards)})"))
            sections.append(
                ui.tags.ul(*[
                    ui.tags.li(
                        ui.span(card["name"] + " "),
                        ui.HTML(render_mana_cost(card.get("manacost"))),
                        ui.a("❌", href="#", class_="delete-card", **{"data-card": card["name"]})
                    )
                    for card in cards
                ])
            )

        return ui.div(
            *[
                ui.div(  # Each section is a grid item
                    ui.h4(f"{tag.capitalize()} ({len(cards)})"),
                    ui.tags.ul(*[
                        ui.tags.li(
                            ui.span(card["name"] + " "),
                            ui.HTML(render_mana_cost(card.get("manacost"))),
                            ui.a("❌", href="#", class_="delete-card", **{"data-card": card["name"]})
                        )
                        for card in cards
                    ])
                )
                for tag in TAG_ORDER
                if (cards := grouped.get(tag))
            ],
            style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; align-items: start;"
        )

    @output
    @render.ui
    def card_search_view():
        return card_search_ui() if show_card_search.get() else ui.div()

    @reactive.effect
    @reactive.event(input.add_selected_card)
    def _():
        deck = active_deck.get()
        card_name = input.add_selected_card()
        if deck and card_name:
            decks = load_decks(session_user.get())
            deck_data = decks[deck]

            # Duplicate check
            if any(c.get("name") == card_name for c in deck_data.get("cards", [])):
                card_error_val.set("⚠️ This card is already in your deck.")
                return
            else:
                card_error_val.set("")

            # Get full card data
            cards_db = get_all_cards()
            match = next((c for c in cards_db if c.get("name") == card_name), None)

            if match:
                deck_data["cards"].append(match)
                save_decks(session_user.get(), decks)
                card_update_counter.set(card_update_counter.get() + 1)

    @output
    @render.text
    def deck_title():
        # 👇 Explicitly make this reactive
        _ = card_update_counter.get()
        deck = active_deck.get()
        if not deck:
            return ""

        decks = load_decks(session_user.get())
        deck_data = decks.get(deck, {})
        count = len(deck_data.get("cards", [])) + len(deck_data.get("commander", []))
        return f"Deck: {deck} ({count}/100 cards)"

    @output
    @render.text
    def card_error_msg():
        return card_error_val.get()

    @reactive.effect
    @reactive.event(input.card_name)
    def sync_card_name_to_search():
        if show_card_search.get():
            search_name_value.set(input.card_name())

    @reactive.calc
    def current_deck_data():
        _ = card_update_counter.get()
        username = session_user.get()
        deck = active_deck.get()

        if not username or not deck:
            return {}

        decks = load_decks(username)
        return decks.get(deck, {})

    @output
    @render.text
    def deck_card_counter():
        _ = card_update_counter.get()
        deck = active_deck.get()
        if not deck:
            return ""

        decks = load_decks(session_user.get())
        deck_data = decks.get(deck, {})
        count = len(deck_data.get("cards", [])) + len(deck_data.get("commander", []))
        return f"{count}/100 cards"

    @reactive.effect
    @reactive.event(input.choose_commander_btn)
    def show_commander_picker():
        choose_commander_stage.set("first")
        show_card_search.set(False)  # hide regular search

    @output
    @render.ui
    def commander_search_view():
        stage = choose_commander_stage.get()
        if stage == "closed":
            return ui.div()

        name_filter = commander_search_name.get().lower().strip()
        cards = get_all_cards()

        if stage == "first":
            filtered = [
                card for card in cards
                if "Legendary" in (card.get("supertypes") or []) and (
                        "Creature" in (card.get("types") or []) or
                        ("Planeswalker" in (card.get("types") or []) and "can be your commander" in (
                                card.get("text") or "").lower())
                )
            ]
        elif stage == "partner":
            filtered = [
                card for card in cards
                if "Legendary" in (card.get("supertypes") or []) and
                   "Creature" in (card.get("types") or []) and
                   "partner" in (card.get("text") or "").lower()
            ]
        elif stage == "background":
            filtered = [
                card for card in cards
                if "Legendary" in (card.get("supertypes") or []) and
                   "Enchantment" in (card.get("types") or [])
            ]
        else:
            filtered = []

        if name_filter:
            filtered = [card for card in filtered if name_filter in card["name"].lower()]

        return ui.div(
            render_card_list(filtered, add_button_class="add-commander-choice")
        )

    @reactive.effect
    @reactive.event(input.commander_search_name)
    def commander_search():
        commander_search_name.set(input.commander_search_name())

    @reactive.effect
    @reactive.event(input.commander_choice)
    def handle_commander_choice():
        card_name = input.commander_choice()
        username, deck = session_user.get(), active_deck.get()

        if not username or not deck or not card_name:
            return

        decks = load_decks(username)
        deck_data = decks.get(deck)
        if not deck_data:
            return

        commander_data = deck_data.get("commander", [])
        if isinstance(commander_data, str):
            commander_data = [commander_data] if commander_data else []

        cards_db = get_all_cards()
        match = next((c for c in cards_db if c.get("name") == card_name), None)
        if not match:
            return

        # Avoid duplicates
        if any(c.get("name") == card_name for c in commander_data):
            return

        if len(commander_data) >= 2:
            commander_error_val.set("⚠️ You can only have 2 commanders.")
            return

        commander_data.append(match)
        deck_data["commander"] = commander_data
        commander_error_val.set("")
        update_decks_and_refresh(username, decks)

