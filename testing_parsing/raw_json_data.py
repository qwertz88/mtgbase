import json

def parse_mtg_data(json_file):
    # Load the JSON data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Get the 'data' section
    cards_data = data.get('data', None)

    # Check if 'data' is available
    if cards_data:
        # Inspect one of the sets, e.g., '10E'
        set_key = '10E'  # Change this to any valid set code from the list
        set_data = cards_data.get(set_key, None)

        if set_data:
            # Print the first few cards or details from this set to inspect
            print(f"First few items in the set '{set_key}':", list(set_data)[:5])
        else:
            print(f"No data found for set '{set_key}'.")
    else:
        print("No 'data' key found in the JSON.")

# Run the function to check the file structure
json_file = "/Users/sebastienderuyck/Downloads/allprintings-2.json"  # Replace with the correct path
parse_mtg_data(json_file)
