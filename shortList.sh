#!/bin/bash

# Ask the user for the number of letters
read -p "Enter the number of letters: " num_letters

# Ask the user for the path to the .txt file
read -p "Enter the path to the .txt file: " file_path

# Check if the file exists
if [[ ! -f "$file_path" ]]; then
  echo "The file does not exist. Please check the path and try again."
  exit 1
fi

# Extract the filename and extension
base_name=$(basename "$file_path" .txt)
dir_name=$(dirname "$file_path")

# Create a new file name with "_short.txt"
output_file="${dir_name}/${base_name}_short.txt"

# Filter words with the specified letter count and save to the new file
grep -E "^[a-zA-Z]{$num_letters}$" "$file_path" > "$output_file"

# Let the user know the operation is complete
echo "Words with $num_letters letters have been saved to $output_file"
