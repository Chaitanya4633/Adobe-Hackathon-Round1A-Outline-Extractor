#!/bin/bash

# Adobe Hackathon Round 1A: PDF Outline Extractor
# Run script for Docker container execution

set -e  # Exit on any error

echo "Starting PDF Outline Extractor..."
echo "Input directory: /app/input"
echo "Output directory: /app/output"

# Check if input directory exists and has PDF files
if [ ! -d "/app/input" ]; then
    echo "Error: Input directory /app/input not found"
    exit 1
fi

# Count PDF files
pdf_count=$(find /app/input -name "*.pdf" -type f | wc -l)
echo "Found $pdf_count PDF file(s) to process"

if [ "$pdf_count" -eq 0 ]; then
    echo "Warning: No PDF files found in input directory"
    exit 0
fi

# Ensure output directory exists
mkdir -p /app/output

# Run the Python script
echo "Processing PDF files..."
python3 main.py

echo "PDF processing completed successfully!"
echo "Output files saved to /app/output"