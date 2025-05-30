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

        ui.input_slider(
            "filter_mana_range", "Mana Value",
            min=0, max=15, value=(0, 15)
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
        ui.input_text("filter_flavor", "Text contains"),

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
    return ui.div(
        ui.div(
            [
                ui.h2(ui.output_text("deck_title")),
                ui.div(
                    [
                        ui.span(
                            ui.output_text("deck_card_counter"),
                            style="font-size: 1.2rem; font-weight: bold;"
                        ),
                        ui.input_action_button("back_to_decks", "← Back to Deck List"),
                    ],
                    style="display: flex; gap: 1rem; align-items: center;"
                )
            ],
            style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"
        ),

        # 🎛️ Add Commander and Add Card section side by side
        ui.div(
            {
                "style": "display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; margin-bottom: 1rem;"
            },

            # 🎯 Left column: Commander input
            ui.div(
                ui.input_text("commander_search_name", ui.tags.strong("Commander Name"), value=""),
                ui.input_action_button("choose_commander_btn", "Choose Commander"),
                ui.tags.p(
                    ui.output_text("commander_error_msg"),
                    style="color: red; font-weight: 500; margin-top: 0.3rem;"
                ),
                style="flex: 1;"
            ),

            # 🧩 Right column: Card input + back button
            ui.div(
                ui.input_text("card_name", ui.tags.strong("Card name"), value=search_name_value.get()),

                ui.div(
                    ui.input_action_button("add_card_btn", "Search cards"),
                    style="margin-top: 8px; display: flex; gap: 8px;"
                ),
                ui.tags.p(
                    ui.output_text("card_error_msg"),
                    style="color: red; font-weight: 500; margin-top: 0.3rem;"
                ),
                style="flex: 1;"
            ),
        ),

        # 📦 Current deck card list
        ui.output_ui("deck_card_list"),

        # 🔍 Commander and card search results (only one shown at a time)
        ui.output_ui("commander_search_view"),
        ui.output_ui("card_search_view")
    )


# --- App root layout + JavaScript interactions ---
app_ui = ui.page_fluid(
    ui.tags.style(""" 
        /* your CSS here */
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

            // 👇 Commander card selector
            if (e.target.classList.contains('add-commander-choice')) {
                const cardName = e.target.dataset.card;
                Shiny.setInputValue('commander_choice', cardName, {priority: 'event'});
            }
        });

        Shiny.addCustomMessageHandler('clear_card_input', function(_) {
            const inputEl = document.querySelector('input[id$="card_name"]');
            if (inputEl) inputEl.value = "";
        });
    """),  # 👈 This comma is critical

    ui.output_ui("main_ui")  # 👈 This must be inside the page_fluid
)
