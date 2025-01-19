#!/bin/bash

# Prompt the user for input
read -p "Enter the desired word length: " number
read -p "Enter the path to the .txt file: " file

# Validate inputs
if [[ ! -f "$file" ]]; then
    echo "Error: File not found!"
    exit 1
fi
if ! [[ "$number" =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid number!"
    exit 1
fi

# Generate output filename
output_file="${file%.txt}_short.txt"

# Filter and save words with the specified length
grep -oE "\b[[:alnum:]]{$number}\b" "$file" > "$output_file"

# Confirm completion
echo "Filtered words saved to $output_file"
