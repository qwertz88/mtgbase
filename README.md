# mtgbase
Magic The Gathering Base

Creating a DB of all the existing cards in Magic The Gathering.
The DB will be created in postgresql
This DB will contain:
- Name
- Mana cost
- Colors
- Card types (e.g., Creature, Instant)
- Subtypes (e.g., Elf, Wizard)
- Power / Toughness
- Rarity
- Set / Expansion
- Abilities / Rules text
- Converted mana cost (CMC)
- Loyalty (for planeswalkers)
- Is legendary?
- Is token?
- Is spell or permanent?
- Price

Finally the total value of a deck will be determined

Players own certain decks / cards

## Following libraries should be installed:
- pydantic
- psycopg2
- shiny
- shinyswatch
- humanize

## Creating Environmental Variables
### Windows
- Open the Start menu, type “Environment Variables”, and select “Edit the system environment variables.”
- Click `Environment Variables`
- Under “User variables for  ”, click “New…”
    - Variable name: `DB_PASSWORD`
    - Variable value: `<your password>`
- Click OK.


