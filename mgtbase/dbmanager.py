import os
import psycopg2
from typing import Optional
from psycopg2.extras import RealDictCursor
from mgtbase.card import Cards, Card


class DBManager:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.autocommit = False  # use transactions
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert_player(self, firstname: str, lastname: str) -> int:
        # Try to find the player first
        self.cur.execute(
            "SELECT player_id FROM tbl_players WHERE player_firstname=%s AND player_lastname=%s",
            (firstname, lastname)
        )
        player = self.cur.fetchone()
        if player:
            return player['player_id']
        # Insert if not found
        self.cur.execute(
            "INSERT INTO tbl_players (player_firstname, player_lastname) VALUES (%s, %s) RETURNING player_id",
            (firstname, lastname)
        )
        return self.cur.fetchone()['player_id']

    def insert_deck(self, deck_name: str, player_id: int) -> int:
        # To prevent duplicate deck names for one player: adjust uniqueness rules if needed
        self.cur.execute(
            "INSERT INTO tbl_decks (deck_name, player_id) VALUES (%s, %s) RETURNING deck_id",
            (deck_name, player_id)
        )
        return self.cur.fetchone()['deck_id']

    def insert_card(self, card_data: dict) -> int:
        # Try to find card with same name (policy may differ for your dataset)
        self.cur.execute(
            "SELECT card_id FROM tbl_cards WHERE card_name = %s",
            (card_data["card_name"],)
        )
        card = self.cur.fetchone()
        if card:
            return card["card_id"]

        # All fields in Card model, except optional card_id
        self.cur.execute(
            """INSERT INTO tbl_cards (
                card_name, card_mana_cost, card_cmc, card_type, card_subtype,
                card_text, card_power, card_toughness, card_loyalty, card_rarity,
                card_image_url, card_ability
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               RETURNING card_id""",
            (
                card_data.get("card_name"),
                card_data.get("card_mana_cost"),
                card_data.get("card_cmc"),
                card_data.get("card_type"),
                card_data.get("card_subtype"),
                card_data.get("card_text"),
                card_data.get("card_power"),
                card_data.get("card_toughness"),
                card_data.get("card_loyalty"),
                card_data.get("card_rarity"),
                card_data.get("card_image_url"),
                card_data.get("card_ability"),
            )
        )
        return self.cur.fetchone()["card_id"]

    def insert_deck_card(self, deck_id: int, card_id: int, quantity: int = 1):
        # Insert or update quantity (idempotent)
        self.cur.execute(
            """
            INSERT INTO tbl_deck_cards (deck_id, card_id, quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (deck_id, card_id) DO UPDATE SET quantity = EXCLUDED.quantity
            """,
            (deck_id, card_id, quantity)
        )

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()








def main():
    mtgbase="mtgbase2"
    postgres="postgres"
    password = os.environ.get("DB_PASSWORD")

    if not password:
        # Fail fast with a clear error message
        raise ValueError(
            "No database password supplied. Please set the DB_PASSWORD environment variable:\n"
            "Windows: set DB_PASSWORD=your_password\n"
            "Linux/Mac: export DB_PASSWORD=your_password")

    db = DBManager(
        dbname=mtgbase,
        user=postgres,
        password=password
    )
    try:
        # Example data (from your example)
        player_firstname, player_lastname = "John", "Doe"
        deck_name = "Awesome Deck"
        deck = Cards()
        card1 = Card(card_name="Some Card", card_mana_cost="1G", card_cmc=2)
        card2 = Card(card_name="Another Card", card_mana_cost="2R", card_cmc=3)
        deck.add_card(card1)
        deck.add_card(card2)
        all_cards = deck.get_all_cards()

        player_id = db.insert_player(player_firstname, player_lastname)
        deck_id = db.insert_deck(deck_name, player_id)
        for card_tuple in all_cards:
            # Your Cards.add_card uses tuple(card.model_dump().values())
            card_fields = Card.model_validate(dict(zip(Card.model_fields.keys(), card_tuple)))
            card_id = db.insert_card(card_fields.model_dump())
            db.insert_deck_card(deck_id, card_id, quantity=1)

        db.commit()
        print("Deck sent successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

