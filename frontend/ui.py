from shiny import ui

# --- Login page layout ---
login_ui = ui.div(
    ui.h2("Login"),
    ui.input_text("username", "Username"),
    ui.input_password("password", "Password"),
    ui.input_action_button("login_btn", "Login"),
    ui.p(ui.a("No account? Register here", href="#", id="go_register")),
    ui.output_text("login_msg")  # ✅ output from logic.py
)

# --- Registration page layout ---
register_ui = ui.div(
    ui.h2("Register"),
    ui.input_text("new_username", "Choose a Username"),
    ui.input_password("new_password", "Choose a Password"),
    ui.input_action_button("register_btn", "Register"),
    ui.p(ui.a("Already have an account? Login", href="#", id="go_login")),
    ui.output_text("register_msg")  # ✅ output from logic.py
)

# --- Logged-in layout showing deck list ---
def logged_in_ui(username):
    return ui.div(
        # 🔒 Logout button top-right
        ui.div(
            ui.input_action_button("logout_btn", "Logout"),
            style="text-align: right;"
        ),
        # 👤 Welcome message
        ui.h2(f"Welcome, {username}!"),
        # 📋 List of decks (rendered from logic)
        ui.div(
            ui.input_text("deck_search", "🔍 Search Decks by Name"),
            ui.input_action_button("clear_search", "❌ Clear"),
            style="display: flex; gap: 8px; align-items: flex-end;"
        ),
        ui.output_ui("deck_list"),
        ui.hr(),
        # ➕ Create new deck (moved to bottom)
        ui.input_text("deck_name", "New Deck Name"),
        ui.input_action_button("create_deck", "Create Deck"),
    )

# --- Single deck view with card adding and back button ---
def deck_view_ui(deck_name):
    return ui.div(
        ui.h2(f"Deck: {deck_name}"),

        ui.input_text("card_name", "Card Name"),

        ui.div(
            ui.input_action_button("add_card_btn", "Add to Deck"),
            ui.input_action_button("add_commander_btn", "Add as Commander"),
            style="margin-top: 8px; display: flex; gap: 8px;"
        ),

        ui.output_text("commander_error_msg"),  # ✅ Add this to show errors

        ui.output_ui("card_list"),

        ui.hr(),

        ui.input_action_button("back_to_decks", "← Back to Deck List")
    )



# --- App root layout + JavaScript interactions ---
app_ui = ui.page_fluid(
    # ✅ Global deck table styling
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
            // ✅ Clear search logic — here!
            if (e.target.id === 'clear_search') {
                const inputEl = document.querySelector('input[id$="deck_search"]');
                if (inputEl) {
                    inputEl.value = "";
                    Shiny.setInputValue('deck_search', "", {priority: 'event'});
                }
            }
        });

        Shiny.addCustomMessageHandler('clear_card_input', function(_) {
            const inputEl = document.querySelector('input[id$="card_name"]');
            if (inputEl) inputEl.value = "";
        });
    """),

ui.output_ui("main_ui")  # ✅ dynamically renders login, register, deck list, or card view
)
