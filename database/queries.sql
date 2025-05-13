create table if not exists tbl_cards(
    card_id					serial primary key,
    card_name 				varchar(100) not null,
    card_mana_cost 			varchar(50) null,
    card_cmc 				integer null,          		-- converted mana cost
    card_type 				varchar(100) null,
	card_subtype 			varchar(100) null,
    card_text 				text null,
    card_power 				varchar(10) null,           -- Sometimes cards have symbols like '*' or combinations
    card_toughness 			varchar(10) null,           -- Same reason as power
    card_loyalty 			integer null,               -- Only for planeswalkers
    card_rarity 			varchar(20) null,
    card_image_url 			text null,
	card_ability			text null
);


create table if not exists tbl_card_prices (
    price_id    serial primary key,
    card_id     integer not null,
    price       numeric(10, 2) not null,
    currency    varchar(10) default 'USD',
    vendor      varchar(50),
    price_date  date default current_date,
    foreign key (card_id) references tbl_cards(card_id) on delete cascade
);



create table if not exists tbl_players (
    player_id           serial primary key,
    player_lastname     varchar(50) not null,
	player_firstname    varchar(50) not null
);


create table if not exists tbl_decks (
    deck_id     serial primary key,
    deck_name   varchar(100) not null,
    player_id   integer not null,
    foreign key (player_id) references tbl_players(player_id) on delete cascade
);


create table if not exists tbl_deck_cards (
    deck_card_id    serial primary key,
    deck_id         integer not null,
    card_id         integer not null,
    quantity        integer not null default 1,  -- Number of this card in the deck
    foreign key (deck_id) references tbl_decks(deck_id) on delete cascade,
    foreign key (card_id) references tbl_cards(card_id) on delete cascade,
    unique (deck_id, card_id) -- optional: prevent duplicate entries in one deck
);


select
    d.deck_id,
    d.deck_name,
    sum(dc.quantity * cp.price) as deck_value
from
    tbl_decks d
    join tbl_deck_cards dc on d.deck_id = dc.deck_id
    join tbl_card_prices cp on dc.card_id = cp.card_id
where
    d.deck_id = <your_deck_id>
group by
    d.deck_id, d.deck_name;




