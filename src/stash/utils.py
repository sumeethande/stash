import os
import json
from pathlib import Path
from datetime import datetime


# -------------------- GLOBALS TO SAVE CONFIG --------------------
CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "stash"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config() -> dict:

    '''
    Loads the configuration object from the JSON file
    '''

    if CONFIG_FILE.exists():
        with CONFIG_FILE.open() as config_file:
            return json.load(config_file)
    
    return {}

def save_config(config: dict) -> None:

    '''
    Saves the configuration object to the JSON file
    '''

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w") as config_file:
        json.dump(config, config_file, indent=2)

def create_unique_id(full_name:str, dob: datetime):

    '''
    Create a unique ID by combining full name and dob.
    Example: firstnamelastname_daymonthyear
    '''

    return full_name.replace(" ", "").lower() + "_" + str(dob.day) + str(dob.month) + str(dob.year) 