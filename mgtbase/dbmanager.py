import os
import psycopg2
from card import Card

class DBManager:
    """
    Database manager for interacting with a PostgreSQL database containing card information.

    Provides methods to retrieve all cards, selected card data, and cards matching a given name
    from the 'cards' table. Handles database connection and cleanup.

    Parameters
    ----------
    dbname : str
        Name of the database to connect to.
    user : str
        Database user name.
    password : str
        Password for the database user.
    host : str, optional
        Host address of the PostgreSQL server (default is 'localhost').
    port : str, optional
        Port number for the PostgreSQL server (default is '5432').

    Attributes
    ----------
    conn : psycopg2.extensions.connection
        Active connection to the PostgreSQL database.

    Methods
    -------
    get_all_cards() -> list[Card]
        Retrieve all card records and return them as a list of `Card` objects.
    get_selected_card_data() -> list[dict]
        Retrieve selected fields for all cards as a list of dictionaries.
    get_cards_by_name(text: str) -> list[dict]
        Retrieve card records matching a given name (case-insensitive, English only).
    close()
        Close the database connection.
    """

    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.autocommit = True

    def get_all_cards(self) -> list[Card]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM cards;")
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            cards = []
            for row in rows:
                data = dict(zip(columns, row))
                cards.append(Card(**data))
            return cards

    def get_selected_card_data(self) -> list[dict]:
        query = """
                SELECT
                    name,
                    colorIdentity,
                    colorIndicator,
                    flavorText,
                    keywords,
                    manaCost,
                    manavalue,
                    originalType,
                    power,
                    rarity,
                    subtypes,
                    text,
                    toughness,
                    types,
                    id,
                    uuid
                FROM cards; \
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def get_cards_by_name(self, text: str) -> list[dict]:
        query = """
                SELECT DISTINCT ON (name)
                    name,
                    colorIdentity,
                    colorIndicator,
                    flavorText,
                    keywords,
                    manaCost,
                    manavalue,
                    originalType,
                    power,
                    rarity,
                    subtypes,
                    text,
                    toughness,
                    types,
                    id,
                    uuid
                FROM cards
                WHERE name ILIKE %s
                  AND language = 'English'
                ORDER BY name, id; \
                """
        param = f"%{text}%"
        with self.conn.cursor() as cur:
            cur.execute(query, (param,))
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def close(self):
        self.conn.close()

# Example usage:
def all_cards_full():
    mtgbase = "mtgbase"
    postgres = "postgres"
    password = os.environ.get("DB_PASSWORD")

    db = DBManager(
        dbname=mtgbase,
        user=postgres,
        password=password
    )
    cards = db.get_all_cards()
    for card in cards:
        print(card)
    db.close()


def all_cards_short():
    mtgbase = "mtgbase"
    postgres = "postgres"
    password = os.environ.get("DB_PASSWORD")

    db = DBManager(
        dbname=mtgbase,
        user=postgres,
        password=password
    )

    selected_data = db.get_selected_card_data()
    for data in selected_data:
        print(data)
    db.close()


def all_cards_name():
    mtgbase = "mtgbase"
    postgres = "postgres"
    password = os.environ.get("DB_PASSWORD")

    db = DBManager(
        dbname=mtgbase,
        user=postgres,
        password=password
    )

    cards = db.get_cards_by_name("opt")
    for card in cards:
        print(card)
    db.close()


if __name__ == '__main__':
    #all_cards_full()
    #all_cards_short()
    all_cards_name()