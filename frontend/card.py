from typing import Optional
from pydantic import BaseModel

class Card(BaseModel):
    id: Optional[int] = None
    artist: Optional[str] = None
    artistIds: Optional[str] = None
    asciiName: Optional[str] = None
    attractionLights: Optional[str] = None
    availability: Optional[str] = None
    boosterTypes: Optional[str] = None
    borderColor: Optional[str] = None
    cardParts: Optional[str] = None
    colorIdentity: Optional[str] = None
    colorIndicator: Optional[str] = None
    colors: Optional[str] = None
    defense: Optional[str] = None
    duelDeck: Optional[str] = None
    edhrecRank: Optional[int] = None
    edhrecSaltiness: Optional[float] = None
    faceConvertedManaCost: Optional[float] = None
    faceFlavorName: Optional[str] = None
    faceManaValue: Optional[float] = None
    faceName: Optional[str] = None
    finishes: Optional[str] = None
    flavorName: Optional[str] = None
    flavorText: Optional[str] = None
    frameEffects: Optional[str] = None
    frameVersion: Optional[str] = None
    hand: Optional[str] = None
    hasAlternativeDeckLimit: Optional[bool] = None
    hasContentWarning: Optional[bool] = None
    hasFoil: Optional[bool] = None
    hasNonFoil: Optional[bool] = None
    isAlternative: Optional[bool] = None
    isFullArt: Optional[bool] = None
    isFunny: Optional[bool] = None
    isGameChanger: Optional[bool] = None
    isOnlineOnly: Optional[bool] = None
    isOversized: Optional[bool] = None
    isPromo: Optional[bool] = None
    isRebalanced: Optional[bool] = None
    isReprint: Optional[bool] = None
    isReserved: Optional[bool] = None
    isStarter: Optional[bool] = None
    isStorySpotlight: Optional[bool] = None
    isTextless: Optional[bool] = None
    isTimeshifted: Optional[bool] = None
    keywords: Optional[str] = None
    language: Optional[str] = None
    layout: Optional[str] = None
    leadershipSkills: Optional[str] = None
    life: Optional[str] = None
    loyalty: Optional[str] = None
    manaCost: Optional[str] = None
    manaValue: Optional[float] = None
    name: Optional[str] = None
    number: Optional[str] = None
    originalPrintings: Optional[str] = None
    originalReleaseDate: Optional[str] = None
    originalText: Optional[str] = None
    originalType: Optional[str] = None
    otherFaceIds: Optional[str] = None
    power: Optional[str] = None
    printings: Optional[str] = None
    promoTypes: Optional[str] = None
    rarity: Optional[str] = None
    rebalancedPrintings: Optional[str] = None
    relatedCards: Optional[str] = None
    securityStamp: Optional[str] = None
    setCode: Optional[str] = None
    side: Optional[str] = None
    signature: Optional[str] = None
    sourceProducts: Optional[str] = None
    subsets: Optional[str] = None
    subtypes: Optional[str] = None
    supertypes: Optional[str] = None
    text: Optional[str] = None
    toughness: Optional[str] = None
    type: Optional[str] = None
    types: Optional[str] = None
    uuid: str
    variations: Optional[str] = None
    watermark: Optional[str] = None

class Cards:
    def __init__(self):
        self.cards: list[Card] = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_all_cards(self) -> list[Card]:
        return self.cards

def main():
    deck = Cards()
    card1 = Card(uuid="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", name="Some Card", manaCost="1G", manaValue=2)
    card2 = Card(uuid="yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy", name="Another Card", manaCost="2R", manaValue=3)
    deck.add_card(card1)
    deck.add_card(card2)
    for card in deck.get_all_cards():
        print(card.model_dump())

if __name__ == "__main__":
    main()