import json

# Function to load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to save data to a text file, with each address followed by the count
def save_to_text(data, filename):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item['address']} {item['count']}\n")

# Function to sort JSON data by the 'count' field
def sort_json(data):
    return sorted(data, key=lambda x: x['count'], reverse=True)

# Main function to handle the workflow
def process_json(input_file, output_file):
    # Load data
    data = load_json(input_file)
    
    # Sort data
    sorted_data = sort_json(data)
    
    # Save sorted data to text file
    save_to_text(sorted_data, output_file)

# Example usage
if __name__ == "__main__":
    input_file = 'AddressCounts.json'  # Path to the input JSON file
    output_file = 'leaderboard.txt'  # Path to the output text file
    process_json(input_file, output_file)
