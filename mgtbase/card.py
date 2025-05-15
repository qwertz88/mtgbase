from typing import Optional
from pydantic import BaseModel

class Card(BaseModel):
    card_id: Optional[int] = None  # Optional for new card
    card_name: str
    card_mana_cost: Optional[str] = None
    card_cmc: Optional[int] = None
    card_type: Optional[str] = None
    card_subtype: Optional[str] = None
    card_text: Optional[str] = None
    card_power: Optional[str] = None
    card_toughness: Optional[str] = None
    card_loyalty: Optional[int] = None
    card_rarity: Optional[str] = None
    card_image_url: Optional[str] = None
    card_ability: Optional[str] = None


class Cards:
    def __init__(self):
        self.cards:list[tuple] = []

    def add_card(self, card: Card):
        # Convert card to a tuple of its values and add to the list
        self.cards.append(tuple(card.model_dump().values()))

    def get_all_cards(self) -> list[tuple]:
        return self.cards


def main():
    deck = Cards()
    card1 = Card(card_name="Some Card", card_mana_cost="1G", card_cmc=2)
    card2 = Card(card_name="Another Card", card_mana_cost="2R", card_cmc=3)
    deck.add_card(card1)
    deck.add_card(card2)
    print(deck.get_all_cards())

if __name__ == "__main__":
    main()