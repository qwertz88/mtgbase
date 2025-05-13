from marshmallow import Schema, fields

class CardSchema(Schema):
    # The name of the card (e.g. "Lightning Bolt")
    card_name = fields.Str(data_key="name", required=True)

    # The mana cost (e.g. "{2}{R}")
    card_mana_cost = fields.Str(data_key="manaCost")

    # Converted mana cost (e.g. 3)
    card_cmc = fields.Int(data_key="convertedManaCost")

    # Full type line (e.g. "Creature — Goblin Shaman")
    card_type = fields.Str(data_key="type")

    # Subtype portion (e.g. "Goblin Shaman") — extracted from type line
    card_subtype = fields.Method("get_subtype")

    # Rules text (e.g. "Deal 3 damage to any target.")
    card_text = fields.Str(data_key="text")

    # Power (e.g. "3") — stored as string because it could be "*", "X", etc.
    card_power = fields.Str()

    # Toughness (e.g. "2") — same reasoning as power
    card_toughness = fields.Str()

    # Loyalty (e.g. 5) — only relevant for planeswalkers
    card_loyalty = fields.Int()

    # Rarity of the card (e.g. "rare", "mythic")
    card_rarity = fields.Str()

    # URL to the card's image — we'll use Card Kingdom if available
    card_image_url = fields.Method("get_image_url")

    # Optional field if you want to store triggered abilities or similar separately
    card_ability = fields.Str(load_default=None)

    # --- Custom Field Methods ---

    def get_subtype(self, obj):
        """
        Extracts the subtype from the 'type' field, if it exists.
        Example: "Legendary Creature — Snake Samurai" → "Snake Samurai"
        """
        type_line = obj.get("type", "")
        parts = type_line.split("—")
        return parts[1].strip() if len(parts) > 1 else None

    def get_image_url(self, obj):
        """
        Returns a card image URL using purchase links (e.g. from Card Kingdom).
        Falls back to None if not found.
        """
        return obj.get("purchaseUrls", {}).get("cardKingdom")
