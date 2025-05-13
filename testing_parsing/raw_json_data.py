import json

def parse_mtg_data(json_file):
    # Load the JSON data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Assuming the cards are stored in a key like 'cards'
    cards = data.get('cards', data)  # Fall back to 'data' if 'cards' is not found

    # Print the type and structure of 'cards' to inspect
    print("Type of 'cards':", type(cards))
    print("First few items in 'cards':", list(cards)[:5])  # Print the first 5 items to inspect

# Run the function to check the file structure
json_file = "/Users/sebastienderuyck/Downloads/allprintings-2.json"  # Replace with the correct path
parse_mtg_data(json_file)
