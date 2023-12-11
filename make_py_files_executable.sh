#!/bin/bash

# Find all .py files in current directory and its subdirectories
py_files=$(find . -type f -name "*.py")

# Loop through each .py file and set executable permissions
for file in $py_files; do
    chmod +x "$file"
done

echo "Executable permissions set for all .py files"

