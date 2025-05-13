import json
import os

# Path to the JSON file
file_path = os.path.expanduser('~/Downloads/UpgradesUnleashed_NEC.json')

# Load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Print the top-level keys of the JSON data to understand the structure
if isinstance(data, dict):
    print("Top-level keys:", data.keys())
else:
    print("The data is not a dictionary, it is a:", type(data))
