import json
import os
import shutil
import sys
from pathlib import Path
from pydantic import BaseModel


ENGINES_LIST_KEY = "engines.list"
KATAGO_PATH = "/opt/homebrew/bin/katago"
SABAKI_PATH = os.path.expanduser("~/Library/Application Support/Sabaki/")
SETTINGS_FILE = os.path.join(SABAKI_PATH, "settings.json")


class Engine(BaseModel):
    name: str = "katago"
    path: str = KATAGO_PATH
    args: str


def backup_file(filename):
    """Create a backup before modifying the settings file."""
    file_path = Path(filename)
    if file_path.exists():
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        shutil.copy(file_path, backup_path)
        print(f"Backup created: {backup_path}\n")


def setup_katago(config_path, model_path):
    """
    Updates the settings.json file with the correct KataGo paths.
    """
    print(f"Settings path: {SETTINGS_FILE}")
    backup_file(SETTINGS_FILE)

    try:
        with open(SETTINGS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    engine = Engine(
        args=f'gtp -config "{config_path}" -model "{model_path}"',
    )

    data[ENGINES_LIST_KEY] = [engine.model_dump()]

    with open(SETTINGS_FILE, "w") as file:
        json.dump(data, file, indent=2)

    print("Updated settings successfully!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 setup_katago.py <config_path> <model_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    model_path = sys.argv[2]

    print(f"Config path: {config_path}")
    print(f"Model path: {model_path}\n")

    setup_katago(config_path, model_path)
