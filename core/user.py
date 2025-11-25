# core/user.py
import uuid
from dataclasses import dataclass, field
from typing import List
from core.account import Account

@dataclass
class UserProfile:
    name: str
    email: str = ""
    phone: str = ""

@dataclass
class User:
    username: str
    password_hash: str
    profile: UserProfile
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    accounts: List[Account] = field(default_factory=list)

    def add_account(self, account: Account):
        self.accounts.append(account)
