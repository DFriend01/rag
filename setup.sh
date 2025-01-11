#!/bin/bash
set -e

# Install Ollama CLI tool
if [ -z "$(which ollama)" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
    echo "Ollama tool at $(which ollama)"
fi

# Create python virtual environment
if [ -z  "$(dpkg -l | grep 'python3-virtualenv')" ]; then
    echo "python3-virutalenv missing, installing package"
    sudo apt update && sudo apt install -y python3-virtualenv
fi

if [ ! -d venv/ ]; then
    echo "Creating python virtual environment"
    python3 -m venv venv
fi

# Install python dependencies
echo "Installing python dependencies"
source venv/bin/activate
python -m pip install --upgrade pip && python -m pip install -r requirements.txt
deactivate
