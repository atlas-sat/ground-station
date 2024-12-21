#!/bin/bash

file1="data.wav"
file2="output.wav"

# Check if both files exist
if [ ! -f "$file1" ]; then
    echo "File $file1 does not exist."
    exit 1
fi

if [ ! -f "$file2" ]; then
    echo "File $file2 does not exist."
    exit 1
fi

# Compare the files and log the differences
if cmp "$file1" "$file2"; then
    echo "The files are identical."
else
    echo "The files are different."
    diff "$file1" "$file2" > differences.log
    echo "Differences have been logged to differences.log"
fi
