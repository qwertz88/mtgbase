from typing import Optional
from datetime import date

class CardPrice:
    def __init__(
            self,
            price_id: int,
            card_id: int,
            price: float,
            currency: str = 'USD',
            vendor: Optional[str] = None,
            price_date: Optional[date] = None,
    ):
        self.price_id = price_id
        self.card_id = card_id
        self.price = price
        self.currency = currency
        self.vendor = vendor
        self.price_date = price_date or date.today()