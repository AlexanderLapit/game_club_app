import hashlib
import hmac
import os

class Security:
    @staticmethod
    def hash_password(password: str, salt: bytes = None) -> str:
        if salt is None:
            salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt.hex() + pwd_hash.hex()

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        if len(stored_password) < 32:
            return False
        salt_hex = stored_password[:32]
        stored_hash = stored_password[32:]
        try:
            salt = bytes.fromhex(salt_hex)
        except ValueError:
            return False
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000).hex()
        return hmac.compare_digest(pwd_hash, stored_hash)