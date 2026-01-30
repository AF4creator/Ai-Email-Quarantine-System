from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY not set in environment")

fernet = Fernet(FERNET_KEY)

def encrypt_imap_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_imap_password(enc_password: str) -> str:
    return fernet.decrypt(enc_password.encode()).decode()
