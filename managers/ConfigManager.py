import json
import os
import sys
import shutil
from utils.FileUtils import get_data_folder

DEFAULT_THEME = "style/blue.json"
APP_DIR_NAME = ".OPALE"
DEFAULT_APPEARANCE = "System"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_persistent_data_folder():
    app_dir = os.path.join(os.path.expanduser("~"), APP_DIR_NAME)
    os.makedirs(app_dir, exist_ok=True)

    config_path = os.path.join(app_dir, "config.json")
    if not os.path.exists(config_path):
        try:
            default_config = resource_path("data/config.json")
            shutil.copy(default_config, config_path)
        except Exception:
            # Création d'un config par défaut minimal
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"data_folder": app_dir, "theme_file": DEFAULT_THEME, "appearance" : DEFAULT_APPEARANCE}, f, indent=2, ensure_ascii=False)

    # Initialisation des fichiers vides s'ils n'existent pas
    for filename in ["opale.json", "tasks.json"]:
        path = os.path.join(app_dir, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)

    return app_dir

def get_config_path():
    return os.path.join(get_persistent_data_folder(), "config.json")

def load_config():
    path = get_config_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(config: dict):
    with open(get_config_path(), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_theme_file():
    config = load_config()
    return config.get("theme_file", DEFAULT_THEME)

def set_theme_file(theme_file):
    config = load_config()
    config["theme_file"] = theme_file
    save_config(config)

def get_theme_path():
    theme_file = get_theme_file()
    return resource_path(theme_file)

def get_appearance_mode():
    config = load_config()
    return config.get("appearance", DEFAULT_APPEARANCE)

def set_appearance_mode(mode):
    config = load_config()
    config["appearance"] = mode
    save_config(config)
