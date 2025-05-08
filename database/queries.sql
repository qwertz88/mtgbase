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
