import json
import os

# Path to the JSON file
file_path = os.path.expanduser('~/Downloads/UpgradesUnleashed_NEC.json')

# Load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Print the raw JSON data (or a portion if it's too large)
print(json.dumps(data, indent=4))

# Optionally, inspect the keys of the JSON data to understand its structure
if isinstance(data, list):
    for item in data:
        print("Item keys:", item.keys())
else:
    print("Data keys:", data.keys())
