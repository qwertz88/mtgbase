from shiny import reactive

# 👤 Holds the username of the currently logged-in user (or None if not logged in)
session_user = reactive.Value(None)

# 🔀 Controls whether the UI is in "login" or "register" mode
ui_mode = reactive.Value("login")

# 📘 Tracks the currently active (opened) deck name
active_deck = reactive.Value(None)

# 🔄 Trigger to refresh card-related UI; increment to force a re-render
card_update_counter = reactive.Value(0)

# 🔍 Stores the card name filter input for search fields
search_name_value = reactive.Value("")

# 🔎 Boolean flag: should the card search interface be shown?
show_card_search = reactive.Value(False)

# 🧙 Controls the stage of the commander selection flow
# "closed" → hidden, "first" → first commander, "partner"/"background" → second commander
choose_commander_stage = reactive.Value("closed")

# 🧭 Filter input for searching commanders by name
commander_search_name = reactive.Value("")
