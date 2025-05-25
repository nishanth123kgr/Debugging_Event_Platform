#!/bin/bash

# Install system dependencies (GCC is already available on Render)
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
