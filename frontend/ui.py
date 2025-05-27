from shiny import ui
from state import search_name_value
from utils import load_decks  # bovenaan als nodig
from state import session_user

# --- Login page layout ---
login_ui = ui.div(
    ui.h2("Login"),
    ui.input_text("username", "Username"),
    ui.input_password("password", "Password"),
    ui.input_action_button("login_btn", "Login"),
    ui.p(ui.a("No account? Register here", href="#", id="go_register")),
    ui.output_text("login_msg"),
    ui.output_text("card_error_msg"),
)

# --- Registration page layout ---
register_ui = ui.div(
    ui.h2("Register"),
    ui.input_text("new_username", "Choose a Username"),
    ui.input_password("new_password", "Choose a Password"),
    ui.input_password("confirm_password", "Confirm Password"),
    ui.input_action_button("register_btn", "Register"),
    ui.p(ui.a("Already have an account? Login", href="#", id="go_login")),
    ui.output_text("register_msg")
)

def card_search_ui():
    return ui.div(
        ui.h3("Add Filters"),

        ui.input_checkbox_group(
            "filter_mana_colors", "Mana colors",
            choices={
                "W": ui.HTML('<img src="/icons/W.svg" height="16px" title="White">'),
                "U": ui.HTML('<img src="/icons/U.svg" height="16px" title="Blue">'),
                "B": ui.HTML('<img src="/icons/B.svg" height="16px" title="Black">'),
                "R": ui.HTML('<img src="/icons/R.svg" height="16px" title="Red">'),
                "G": ui.HTML('<img src="/icons/G.svg" height="16px" title="Green">'),
                "C": ui.HTML('<img src="/icons/C.svg" height="16px" title="Colorless">')
            },
            inline=True
        ),

        ui.input_select(
            "filter_type",
            "Card Type",
            choices={
                "": "All",
                "artifact": "Artifact",
                "battle": "Battle",
                "conspiracy": "Conspiracy",
                "creature": "Creature",
                "dungeon": "Dungeon",
                "enchantment": "Enchantment",
                "instant": "Instant",
                "kindred": "Kindred",
                "land": "Land",
                "phenomenon": "Phenomenon",
                "plane": "Plane",
                "planeswalker": "Planeswalker",
                "scheme": "Scheme",
                "sorcery": "Sorcery",
                "vanguard": "Vanguard",
            }
        ),

        ui.input_text("filter_subtype", "Subtype contains"),
        ui.input_text("filter_flavor", "Flavor text contains"),

        ui.tags.p(
            {"style": "color: red; font-weight: bold; margin-top: 0.5em;"},
            ui.output_text("card_error_msg")
        ),

        ui.hr(),
        ui.output_ui("filtered_card_list")
    )

# --- Logged-in layout showing deck list ---
def logged_in_ui(username):
    return ui.div(
        ui.div(
            ui.input_action_button("logout_btn", "Logout"),
            style="text-align: right;"
        ),
        ui.h2(f"Welcome, {username}!"),
        ui.div(
            ui.input_text("deck_search", "🔍 Search Decks by Name"),
            ui.input_action_button("clear_search", "❌ Clear"),
            style="display: flex; gap: 8px; align-items: flex-end;"
        ),
        ui.output_ui("deck_list"),
        ui.hr(),
        ui.input_text("deck_name", "New Deck Name"),
        ui.input_action_button("create_deck", "Create Deck"),
    )

# --- Single deck view with card adding and back button ---
def deck_view_ui(deck_name):
    deck_data = load_decks(session_user.get()).get(deck_name, {})
    card_count = len(deck_data.get("cards", [])) + len(deck_data.get("commander", []))

    return ui.div(
        ui.h2(f"Deck: {deck_name} ({card_count}/100 cards)"),

        ui.output_ui("deck_card_list"),
        ui.hr(),

        ui.input_text("card_name", "Card Name"),

        ui.div(
            ui.input_action_button("add_card_btn", "Search cards"),
            ui.input_action_button("back_to_decks", "← Back to Deck List"),
            style="margin-top: 8px; display: flex; gap: 8px;"
        ),

        ui.output_text("commander_error_msg"),
        ui.hr(),

        ui.output_ui("card_search_view")
    )


# --- App root layout + JavaScript interactions ---
app_ui = ui.page_fluid(
    ui.tags.style("""
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px 10px;
            border-bottom: 1px solid #ddd;
            text-align: left;
            vertical-align: middle;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        a.toggle-fav {
            text-decoration: none;
            font-size: 16px;
        }
        a.open-deck {
            font-weight: 500;
            text-decoration: none;
        }
        a.delete-deck {
            color: red;
            text-decoration: none;
            font-weight: bold;
        }
    """),

    ui.tags.script("""
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('open-deck')) {
                const deckName = e.target.dataset.deck;
                Shiny.setInputValue('open_deck_name', deckName, {priority: 'event'});
            }
            if (e.target.classList.contains('delete-deck')) {
                const deckName = e.target.dataset.deck;
                if (confirm('Are you sure you want to delete this deck?')) {
                    Shiny.setInputValue('delete_deck', deckName, {priority: 'event'});
                }
            }
            if (e.target.classList.contains('delete-card')) {
                const card = e.target.dataset.card;
                Shiny.setInputValue('delete_card', card, {priority: 'event'});
            }
            if (e.target.id === 'go_register') {
                Shiny.setInputValue('switch_to_register', Math.random());
            }
            if (e.target.id === 'go_login') {
                Shiny.setInputValue('switch_to_login', Math.random());
            }
            if (e.target.classList.contains('toggle-fav')) {
                const deckName = e.target.dataset.deck;
                Shiny.setInputValue('toggle_favorite', deckName, {priority: 'event'});
            }
            if (e.target.id === 'clear_search') {
                const inputEl = document.querySelector('input[id$="deck_search"]');
                if (inputEl) {
                    inputEl.value = "";
                    Shiny.setInputValue('deck_search', "", {priority: 'event'});
                }
            }
            if (e.target.classList.contains('add-card-btn')) {
                const cardName = e.target.dataset.card;
                Shiny.setInputValue('add_selected_card', cardName, {priority: 'event'});
            }
        });

        Shiny.addCustomMessageHandler('clear_card_input', function(_) {
            const inputEl = document.querySelector('input[id$="card_name"]');
            if (inputEl) inputEl.value = "";
        });
    """),

    ui.output_ui("main_ui")
)
