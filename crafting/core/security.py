import base64
import os 
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_100,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_contetn(content: str, password: str) -> str:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fermet = Fernet(key)
    encrypted_bytes = fermet.encrypt(content.encode())
    return base64.b64encode(salt + encrypted_bytes).decode("utf-8")

def decrypt_content(encrypted_data: str, password: str) -> str:
    try:
        combined = base64.b64decode(encrypted_data.encode("utf-8"))
        salt = combined[:16]
        encrypted_bytes = combined[16:]
        key = _derive_key(password, salt)
        fermet = Fernet(key)
        return fermet.decrypt(encrypted_bytes).decode("utf-8")
    except (InvalidToken, Exception):
        raise ValueError("Hatalı parola veya bozulmuş veri!")
    
