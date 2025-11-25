# utils/password_hasher.py
import hashlib, os, binascii

class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    @staticmethod
    def verify(stored_password: str, provided_password: str) -> bool:
        if not stored_password or len(stored_password) < 65:
            return False
        salt = stored_password[:64].encode('ascii')
        stored_pwdhash = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_pwdhash
