from datetime import datetime
import json
import os
from utils.FileUtils import get_data_folder
from model.Task import Task

TASKS_JSON_PATH = os.path.join(get_data_folder(), "tasks.json")

def load_tasks():
    try:
        with open(TASKS_JSON_PATH, "r", encoding="utf-8") as f:
            return [Task.from_dict(item) for item in json.load(f)]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=2, ensure_ascii=False)

def finish_open_tasks(tasks):
    now_iso = datetime.now().isoformat(timespec='minutes')
    for task in tasks:
        if task.endDate is None:
            task.endDate = datetime.fromisoformat(now_iso)
    return tasks


def delete_tasks_between(start_date, end_date):
    try:
        with open(TASKS_JSON_PATH, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        return 0

    filtered_tasks = [
        t for t in tasks
        if not (t.get("date") and start_date <= datetime.fromisoformat(t["date"].replace("Z", "+00:00")) <= end_date)
    ]

    deleted_count = len(tasks) - len(filtered_tasks)
    with open(TASKS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(filtered_tasks, f, indent=2, ensure_ascii=False)

    return deleted_count

def update_task(updated_task):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == updated_task["id"]:
            t.update(updated_task)
            break
    save_tasks(tasks)
