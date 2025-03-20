#!/usr/bin/env bash
# Description: Generate KataGo arguments for macOS based on Homebrew installation paths.

# Check if Homebrew is installed
if ! command -v brew >/dev/null 2>&1; then
    echo "Error: Homebrew is not installed."
    exit 1
fi

# Check if KataGo is installed
if ! brew list katago >/dev/null 2>&1; then
    echo "Error: KataGo is not installed."
    exit 1
fi

# Get the config file path
KATAGO_CONFIG=$(brew list --verbose katago | awk '/gtp_example.cfg/ {print $0; exit}')

# Get the model file path (first .gz file)
KATAGO_MODEL=$(brew list --verbose katago | awk '/\.gz$/ {print $0; exit}')

# Validate that both paths were found
if [[ -z "$KATAGO_CONFIG" ]]; then
    echo "Error: Could not find gtp_example.cfg."
    exit 1
fi

if [[ -z "$KATAGO_MODEL" ]]; then
    echo "Error: Could not find a model file (.gz)."
    exit 1
fi

python3 setup_katago.py "$KATAGO_CONFIG" "$KATAGO_MODEL"
