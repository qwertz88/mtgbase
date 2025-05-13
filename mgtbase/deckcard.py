
class DeckCard:
    def __init__(
            self,
            deck_card_id: int,
            deck_id: int,
            card_id: int,
            quantity: int = 1,
    ):
        self.deck_card_id = deck_card_id
        self.deck_id = deck_id
        self.card_id = card_id
        self.quantity = quantity