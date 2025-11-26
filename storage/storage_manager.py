# storage/storage_manager.py
import json, os
from config.settings import USERS_FILE, DATA_DIR
from core.user import User, UserProfile
from core.transaction import Transaction

class StorageManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)     # ensure data folder exists

        # Create users.json if missing
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    # --------------------------
    # USER FILES
    # --------------------------
    def save_users(self, users: list):
        arr = []
        for u in users:
            # convert User objects → dictionary to store as JSON
            arr.append({
                "id": u.id,
                "username": u.username,
                "password_hash": u.password_hash,
                "profile": {
                    "name": u.profile.name,
                    "email": u.profile.email,
                    "phone": u.profile.phone
                }
            })

        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(arr, f, indent=2)

    def load_users(self):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            arr = json.load(f)

        users = []
        for item in arr:
            # recreate UserProfile object from stored data
            profile = UserProfile(
                item["profile"].get("name", ""),
                item["profile"].get("email", ""),
                item["profile"].get("phone", "")
            )
            # recreate User object
            u = User(
                item["username"],
                item["password_hash"],
                profile,
                id=item["id"]
            )
            users.append(u)

        return users

    
    def get_user_tx_file(self, user_id):
        return os.path.join(DATA_DIR, f"transactions_{user_id}.json")   # each user has a separate transaction file

    def load_transactions(self, user_id):
        path = self.get_user_tx_file(user_id)

        # Create file if it doesn't exist
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f)
            return []

        with open(path, "r", encoding="utf-8") as f:
            arr = json.load(f)

        txs = []
        for item in arr:
            try:
                # convert saved transaction dict → Transaction object
                txs.append(
                    Transaction(
                        item["amount"],
                        item["category"],
                        item["ttype"],
                        note=item.get("note", ""),
                        date=item.get("date"),
                        id=item.get("id")
                    )
                )
            except:
                continue

        return txs

    def save_transactions(self, user_id, transactions):
        path = self.get_user_tx_file(user_id)

        arr = []
        for t in transactions:
            # convert Transaction objects → dict for JSON storage
            arr.append({
                "id": t.id,
                "amount": t.amount,
                "category": t.category,
                "ttype": t.ttype,
                "note": t.note,
                "date": t.date
            })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(arr, f, indent=2)
