#!/bin/bash

# Step 1: Initialize the SQLite database
echo "Initializing SQLite database..."
python3 init_db.py

# Step 2: Create the static/qr/ directory
echo "Creating static/qr/ directory..."
mkdir -p static/qr

# Step 3: Start the Flask server
echo "Starting Flask server..."
python3 app.py
