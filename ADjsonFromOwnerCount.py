import json

# Load the data from the JSON file
with open('nerdStonesAddressCounts.json', 'r') as file:
    data = json.load(file)

# Filter and reformat the data
filtered_data = [ 
    {
        "dogecoin_address": entry['address']
    } 
    for entry in data if entry['count'] >= 1  ##Change to filter number of tokers in wallets.  
]

# Create the output structure
output = {"cujoNFTairDropList": filtered_data}

# Save the output to a new JSON file
with open('oneOrMoreADlist.json', 'w') as file:
    json.dump(output, file, indent=4)

print("Filtered data has been saved to 'FilteredAddressCounts.json'.")
