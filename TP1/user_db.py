import json
import os
import hashlib

DB_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users: dict):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def create_user(username: str, password: str) -> bool:
    users = load_users()
    if username in users:
        print(f"User {username} already exists.")
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def verify_user(username: str, password: str) -> bool:
    users = load_users()
    hashed = hash_password(password)
    return users.get(username) == hashed