import os
import json

DEFAULT_DATA_FOLDER = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(DEFAULT_DATA_FOLDER,"data", "config.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Erreur lecture config.json:", e)
    return {}

def get_data_folder():
    path = load_config().get("data_folder")
    print("Chemin du dossier de données:", load_config())
    if path and os.path.isdir(path):
        return path
    return os.path.join(DEFAULT_DATA_FOLDER, "data")
