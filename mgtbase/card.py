from typing import Optional

class Card:
    def __init__(
            self,
            card_id: int,
            card_name: str,
            card_mana_cost: Optional[str] = None,
            card_cmc: Optional[int] = None,
            card_type: Optional[str] = None,
            card_subtype: Optional[str] = None,
            card_text: Optional[str] = None,
            card_power: Optional[str] = None,
            card_toughness: Optional[str] = None,
            card_loyalty: Optional[int] = None,
            card_rarity: Optional[str] = None,
            card_image_url: Optional[str] = None,
            card_ability: Optional[str] = None,
    ):
        self.card_id = card_id
        self.card_name = card_name
        self.card_mana_cost = card_mana_cost
        self.card_cmc = card_cmc
        self.card_type = card_type
        self.card_subtype = card_subtype
        self.card_text = card_text
        self.card_power = card_power
        self.card_toughness = card_toughness
        self.card_loyalty = card_loyalty
        self.card_rarity = card_rarity
        self.card_image_url = card_image_url
        self.card_ability = card_ability