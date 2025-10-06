#!/bin/bash

# Build script for Render deployment
echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating application directories..."
mkdir -p uploads
mkdir -p generated
mkdir -p templates_img
mkdir -p static

# Set permissions
echo "Setting permissions..."
chmod 755 uploads
chmod 755 generated

echo "Build completed successfully!"
