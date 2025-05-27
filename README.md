# # Magic: The Gathering Deck Manager
A modern web app for searching cards, creating decks, and managing collections for Magic: The Gathering, powered by Python, PostgreSQL, and [Shiny for Python](https://shiny.posit.co/py/).

## Features

- **User Authentication:** Register and log in securely.
- **Deck Management:**
    - Create, delete, and rename decks.
    - Organize decks per user (persistent storage for all your decks).

- **Card Search & Filtering:**
    - Search for Magic: The Gathering cards from an extensive database.
    - Filter by card name, type, mana color, subtype, and flavor text.
    - Add regular cards and commanders to your decks.

- **Intuitive Web UI:**
    - Elegant, Bootstrap-styled interface with interactive elements.
    - Deck list, deck detail view, and card adding interfaces.

- **Persistent Storage:**
    - PostgreSQL backend for card data.
    - JSON-based user and deck storage for quick access and flexibility.

- **Mana & Card Icon Rendering:**
    - In-app rendering of Magic mana and set icons for improved readability.

- **Session Management:**
    - See your decks when logged in, and securely log out.

## Tech Stack
- **Python 3.13+**
- **[Shiny for Python](https://shiny.posit.co/py/):** for interactive web application frontend and backend logic.
- **PostgreSQL:** for card data storage.
- **psycopg2:** for PostgreSQL connectivity.
- **JSON Data Storage:** for user accounts and individual decks.
- **Jinja2, Pandas, NumPy:** for potential data manipulation and future extensions

## Getting Started
### 1. Prerequisites
- Python 3.13 or newer (recommend using [conda](https://docs.conda.io/) or [venv](https://docs.python.org/3/library/venv.html))
- PostgreSQL database running locally (with Magic: The Gathering card data imported)

### 2. Install Required Dependencies
Activate your Python environment (e.g., `conda activate YOUR_ENV`) and run:
```
conda install psycopg2 pandas numpy click jinja2 pyyaml requests pytest six pytz
```

### 3. Database Setup
- Create a PostgreSQL database named `mtgbase`.
- Import the `cards` schema (see ). `create_tables.sql`
- Populate the `cards` table with MTG card data (sources such as [MTGJSON.com](https://mtgjson.com/) or similar).

### 4. Configuration
Set your database password as an environment variable:

Shell:
```
export DB_PASSWORD=your_db_password
```

On Windows:
```
set DB_PASSWORD=your_db_password
```
or
```
- Open the Start menu, type “Environment Variables”, and select “Edit the system environment variables.”
- Click `Environment Variables`
- Under “User variables for  ”, click “New…”
    - Variable name: `DB_PASSWORD`
    - Variable value: `<your password>`
- Click OK.
```

### 5. Running the App
In your project root, launch the app:

Shell:
```
python app.py
```

This will start the Shiny app and mount `/icons` for all necessary SVG mana/card icons.

## Project Structure

```
.
├── app.py             # App entry point
├── ui.py              # UI layouts (login, deck views, card search)
├── logic.py           # Server logic and reactive flows
├── dbmanager.py       # PostgreSQL connection & card queries
├── card.py            # Card data models
├── utils.py           # Deck/user file handling, utility functions
├── state.py           # Shared global state (sessions, UI mode, etc)
├── hash.py            # Password hashing
├── layout.py          # Theme & layout helpers
├── create_tables.sql  # Database schema (cards table)
├── icons/             # SVG mana/card symbols (for UI rendering)
└── data/
    ├── users.json     # User credentials (auto-created)
    └── decks/         # Per-user deck lists (one JSON per user)
```


## Usage Highlights
- **Login/Register:**
Register a new user or login with an existing account.
- **Deck List:**
After login, view, search, or create new decks.
- **Deck Details:**
Open a deck to add cards, commanders, or review contents.
- **Card Search:**
Use filters (mana color, type, flavor, name) to find and add cards to your deck.
- **Persistency:**
All data (users, decks) is stored under the `data/` folder and card data in PostgreSQL.

## Security Notes
- Passwords are stored **hashed** (not plain text) using SHA-256.
- User data and decks are stored in private `data/` subfolders.

## Customization & Theming
- Theme can be adjusted by modifying the `theme.css` in the project root.
- The app supports [Bootstrap's Flatly theme](https://bootswatch.com/flatly/).

## Contributing
Pull requests and issues are welcome! All new features should have accompanying documentation and, where practical, tests.


## License

[MIT](LICENSE)

## Acknowledgements
- [MTGJSON](https://mtgjson.com/) for open card data
- [Posit Shiny for Python](https://shiny.posit.co/py/) for the UI framework
