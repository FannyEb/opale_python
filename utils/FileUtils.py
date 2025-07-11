import os
import json
import sys
import shutil

APP_FOLDER_NAME = ".OPALE"

def resource_path(relative_path):
    """
    PyInstaller place les données dans un dossier temporaire sys._MEIPASS.
    Sinon on prend le chemin courant.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_persistent_data_folder():
    home_dir = os.path.expanduser("~")
    data_dir = os.path.join(home_dir, APP_FOLDER_NAME)
    os.makedirs(data_dir, exist_ok=True)

    # Créer config.json par défaut si inexistant
    config_path = os.path.join(data_dir, "config.json")
    if not os.path.exists(config_path):
        # Tente de copier depuis ressources packagées (utile pour PyInstaller)
        try:
            default_config = resource_path("data/config.json")
            shutil.copy(default_config, config_path)
        except Exception:
            # sinon créer minimal
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"data_folder": data_dir}, f, indent=2, ensure_ascii=False)

    # Pareil pour opale.json
    opale_path = os.path.join(data_dir, "opale.json")
    if not os.path.exists(opale_path):
        with open(opale_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    # Pareil pour tasks.json
    tasks_path = os.path.join(data_dir, "tasks.json")
    if not os.path.exists(tasks_path):
        with open(tasks_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    return data_dir


def get_data_folder():
    return get_persistent_data_folder()
