import requests

def get_scryfall_image_url(card_id):
    url = f"https://api.scryfall.com/cards/{card_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # For single-faced cards
        if 'image_uris' in data:
            return data['image_uris'].get('normal')
        # For double-faced cards
        elif 'card_faces' in data:
            return data['card_faces'][0]['image_uris'].get('normal')
    else:
        print(f"Error fetching card data: {response.status_code}")
    return None

# Your card's scryfall ID
scryfall_id = "7a5cd03c-4227-4551-aa4b-7d119f0468b5"
image_url = get_scryfall_image_url(scryfall_id)
print("Card image URL:", image_url)

