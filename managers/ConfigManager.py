import json
import os
import sys
import shutil
from utils.FileUtils import get_data_folder

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_persistent_data_folder():
    app_dir = os.path.join(os.path.expanduser("~"), ".OPALE")
    os.makedirs(app_dir, exist_ok=True)

    config_path = os.path.join(app_dir, "config.json")
    if not os.path.exists(config_path):
        try:
            default_config = resource_path("data/config.json")
            shutil.copy(default_config, config_path)
        except Exception:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"data_folder": app_dir}, f, indent=2, ensure_ascii=False)

    for name in ["opale.json", "tasks.json"]:
        path = os.path.join(app_dir, name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)

    return app_dir

def get_config_path():
    return os.path.join(get_persistent_data_folder(), "config.json")
