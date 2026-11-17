import json
import os
from models import Client, Admin

DATA_FILE = "atm_data.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        default_admin = Admin("admin", "admin123")
        save_users([default_admin])
        return [default_admin]

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            users = []
            for item in raw_data:
                if item["role"] == "admin":
                    users.append(Admin(item["username"], item["password"]))
                else:
                    users.append(Client(item["username"], item["password"], item["balance"], item["loans"]))
            return users
    except (json.JSONDecodeError, Exception):
        return []

def save_users(users):
    data = [user.to_dict() for user in users]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)