from shiny import reactive

session_user = reactive.Value(None)        # Who's logged in
ui_mode = reactive.Value("login")          # "login" or "register"
active_deck = reactive.Value(None)         # Name of selected/open deck
card_update_counter = reactive.Value(0)    # Forces card list refresh
search_name_value = reactive.Value("")     # Card name search field
show_card_search = reactive.Value(False)   # Toggle card search view
choose_commander_stage = reactive.Value("closed")  # "closed", "first", "partner", "background"
commander_search_name = reactive.Value("")