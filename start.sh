#!/bin/bash
# Start the Weather Scene Generator backend
cd "$(dirname "$0")/backend"

echo "=== Weather Scene Generator ==="
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python3 main.py
