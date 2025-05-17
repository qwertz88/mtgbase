import os
import psycopg2
from card import Card

class DBManager2:
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
                    id,
                    loyalty,
                    manaCost,
                    manavalue,
                    name,
                    power,
                    rarity,
                    subtypes,
                    text,
                    toughness,
                    type,
                    types
                FROM cards; \
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def close(self):
        self.conn.close()

# Example usage:
def test1():
    mtgbase = "mtgbase2"
    postgres = "postgres"
    password = os.environ.get("DB_PASSWORD")

    db = DBManager2(
        dbname=mtgbase,
        user=postgres,
        password=password
    )
    cards = db.get_all_cards()
    for card in cards:
        print(card)
    db.close()


def test2():
    mtgbase = "mtgbase2"
    postgres = "postgres"
    password = os.environ.get("DB_PASSWORD")

    db = DBManager2(
        dbname=mtgbase,
        user=postgres,
        password=password
    )

    selected_data = db.get_selected_card_data()
    for data in selected_data:
        print(data)
    db.close()


if __name__ == '__main__':
    #test1()
    test2()