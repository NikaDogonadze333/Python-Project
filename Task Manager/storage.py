import json
import os
from models import Task

DATA_FILE = "tasks_data.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            tasks = []
            for item in raw_data:
                task = Task(
                    title=item["title"],
                    description=item["description"],
                    deadline=item["deadline"],
                    priority=item["priority"],
                    project=item.get("project", "General"),
                    status=item.get("status", "pending")
                )
                tasks.append(task)
            return tasks
    except (json.JSONDecodeError, Exception):
        return []

def save_tasks(tasks):
    data = [task.to_dict() for task in tasks]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)