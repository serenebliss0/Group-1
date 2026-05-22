import json
from pathlib import Path

SESSION_FILE = Path(__file__).resolve().parent / "session.json"


def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"current_user": username}, f)


def load_session():
    if not SESSION_FILE.exists():
        return None

    with open(SESSION_FILE, "r") as f:
        data = json.load(f)

    return data.get("current_user")


def clear_session():
    with open(SESSION_FILE, "w") as f:
        json.dump({"current_user": None}, f)