import json
import os
from utils.FileUtils import get_data_folder

OPALE_JSON_PATH = os.path.join(get_data_folder(), "opale.json")


def load_opale_titles():
    try:
        with open(OPALE_JSON_PATH, "r", encoding="utf-8") as f:
            opale_list = json.load(f)
        return { str(item["id"]): item.get("title", f"Opale {item['id']}") for item in opale_list }
    except FileNotFoundError:
        return {}

def load_opale():
    try:
        with open(OPALE_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def add_opale_line(title):
    opale_list = load_opale()

    new_id = max([item["id"] for item in opale_list], default=0) + 1
    opale_list.append({"id": new_id, "title": title})

    with open(OPALE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(opale_list, f, indent=2, ensure_ascii=False)

def load_opale_list():
    try:
        with open(OPALE_JSON_PATH, "r", encoding="utf-8") as f:
            opale_list = json.load(f)
        return [(str(item["id"]), item.get("title", f"Opale {item['id']}")) for item in opale_list]
    except FileNotFoundError:
        return []
