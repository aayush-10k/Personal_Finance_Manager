# core/user.py
import uuid
from dataclasses import dataclass, field
from typing import List
from core.account import Account

@dataclass
class UserProfile:
    name: str
    email: str = ""
    phone: str = ""                      # optional profile fields

@dataclass
class User:
    username: str
    password_hash: str                   # store password in hashed form
    profile: UserProfile
    id: str = field(default_factory=lambda: str(uuid.uuid4()))   # auto-generated unique user ID
    accounts: List[Account] = field(default_factory=list)        # multiple accounts per user allowed

    def add_account(self, account: Account):
        self.accounts.append(account)    # link account to the user
