select
    d.deck_id,
    d.deck_name,
    sum(dc.quantity * cp.price) as deck_value
from
    tbl_decks d
    join tbl_deck_cards dc on d.deck_id = dc.deck_id
    join tbl_card_prices cp on dc.card_id = cp.card_id
where
    d.deck_id = 1
group by
    d.deck_id, d.deck_name;