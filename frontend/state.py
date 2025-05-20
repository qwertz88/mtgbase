from shiny import reactive

session_user = reactive.Value(None)       # Who's logged in
ui_mode = reactive.Value("login")         # "login" or "register"
active_deck = reactive.Value(None)        # Name of selected/open deck
card_update_counter = reactive.Value(0)  # 💬 Forces card list refresh
