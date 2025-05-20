create table if not exists cards (
	id                      SERIAL PRIMARY KEY,
	artist                  TEXT,
	artistIds               TEXT,
	asciiName               TEXT,
	attractionLights        TEXT,
	availability            TEXT,
	boosterTypes            TEXT,
	borderColor             TEXT,
	cardParts               TEXT,
	colorIdentity           TEXT,
	colorIndicator          TEXT,
	colors                  TEXT,
	defense                 TEXT,
	duelDeck                TEXT,
	edhrecRank              INTEGER,
	edhrecSaltiness         FLOAT,
	faceConvertedManaCost   FLOAT,
	faceFlavorName          TEXT,
	faceManaValue           FLOAT,
	faceName                TEXT,
	finishes                TEXT,
	flavorName              TEXT,
	flavorText              TEXT,
	frameEffects            TEXT,
	frameVersion            TEXT,
	hand                    TEXT,
	hasAlternativeDeckLimit BOOLEAN,
	hasContentWarning       BOOLEAN,
	hasFoil                 BOOLEAN,
	hasNonFoil              BOOLEAN,
	isAlternative           BOOLEAN,
	isFullArt               BOOLEAN,
	isFunny                 BOOLEAN,
	isGameChanger           BOOLEAN,
	isOnlineOnly            BOOLEAN,
	isOversized             BOOLEAN,
	isPromo                 BOOLEAN,
	isRebalanced            BOOLEAN,
	isReprint               BOOLEAN,
	isReserved              BOOLEAN,
	isStarter               BOOLEAN,
	isStorySpotlight        BOOLEAN,
	isTextless              BOOLEAN,
	isTimeshifted           BOOLEAN,
	keywords                TEXT,
	language                TEXT,
	layout                  TEXT,
	leadershipSkills        TEXT,
	life                    TEXT,
	loyalty                 TEXT,
	manaCost                TEXT,
	manaValue               FLOAT,
	name                    TEXT,
	number                  TEXT,
	originalPrintings       TEXT,
	originalReleaseDate     TEXT,
	originalText            TEXT,
	originalType            TEXT,
	otherFaceIds            TEXT,
	power                   TEXT,
	printings               TEXT,
	promoTypes              TEXT,
	rarity                  TEXT,
	rebalancedPrintings     TEXT,
	relatedCards            TEXT,
	securityStamp           TEXT,
	setCode                 TEXT,
	side                    TEXT,
	signature               TEXT,
	sourceProducts          TEXT,
	subsets                 TEXT,
	subtypes                TEXT,
	supertypes              TEXT,
	text                    TEXT,
	toughness               TEXT,
	type                    TEXT,
	types                   TEXT,
	uuid                    VARCHAR(36) NOT NULL,
	variations              TEXT,
	watermark               TEXT
);

CREATE INDEX cards_uuid ON cards(uuid);


-- create table if not exists tbl_cards(
--     card_id					serial primary key,
--     card_name 				varchar(100) not null,
--     card_mana_cost 			varchar(50) null,
--     card_cmc 				integer null,          		-- converted mana cost
--     card_type 				varchar(100) null,
-- 	card_subtype 			varchar(100) null,
--     card_text 				text null,
--     card_power 				varchar(10) null,           -- Sometimes cards have symbols like '*' or combinations
--     card_toughness 			varchar(10) null,           -- Same reason as power
--     card_loyalty 			integer null,               -- Only for planeswalkers
--     card_rarity 			varchar(20) null,
--     card_image_url 			text null,
-- 	card_ability			text null
-- );
--
--
-- create table if not exists tbl_card_prices (
--     price_id    serial primary key,
--     card_id     integer not null,
--     price       numeric(10, 2) not null,
--     currency    varchar(10) default 'USD',
--     vendor      varchar(50),
--     price_date  date default current_date,
--     foreign key (card_id) references tbl_cards(card_id) on delete cascade
-- );
--
--
--
-- create table if not exists tbl_players (
--     player_id           serial primary key,
--     player_lastname     varchar(50) not null,
-- 	player_firstname    varchar(50) not null
-- );
--
--
-- create table if not exists tbl_decks (
--     deck_id     serial primary key,
--     deck_name   varchar(100) not null,
--     player_id   integer not null,
--     foreign key (player_id) references tbl_players(player_id) on delete cascade
-- );
--
--
-- create table if not exists tbl_deck_cards (
--     deck_card_id    serial primary key,
--     deck_id         integer not null,
--     card_id         integer not null,
--     quantity        integer not null default 1,  -- Number of this card in the deck
--     foreign key (deck_id) references tbl_decks(deck_id) on delete cascade,
--     foreign key (card_id) references tbl_cards(card_id) on delete cascade,
--     unique (deck_id, card_id) -- optional: prevent duplicate entries in one deck
-- );