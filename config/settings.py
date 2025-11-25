import os

# Path to this file (finance_manager/config)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the root project folder (finance_manager)
ROOT_DIR = os.path.dirname(BASE_DIR)

# Path to the data directory (finance_manager/data)
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Path to JSON files inside data/
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
