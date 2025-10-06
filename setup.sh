#!/bin/bash

echo "Setting up Kairos 2025 Badge Generator..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

echo "Setup complete! Now run ./run.sh to start the application"
