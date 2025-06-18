#!/bin/bash
set -euo pipefail

echo "🔍 Checking Python environment..."

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "🧪 Creating virtual environment..."
  python3 -m venv venv
else
  echo "✅ Virtual environment already exists."
fi

# Step 2: Install dependencies silently and suppress pip's version notice
if [ ! -f "venv/.deps_installed" ]; then
  echo "📦 Installing Python dependencies..."
  PIP_DISABLE_PIP_VERSION_CHECK=1 venv/bin/pip install --quiet -r requirements.txt
  touch venv/.deps_installed
  echo "✅ Dependencies installed."
else
  echo "📦 Dependencies already installed. Skipping..."
fi

# Step 3: Run the project
echo "🚀 Launching your project..."
echo "------------------------------------------------------------------------"
echo ""
venv/bin/python -B Project/main.py