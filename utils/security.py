from cryptography.fernet import Fernet
import os

# Ключ можно генерировать один раз и сохранить в .env
def get_cipher():
    key = os.getenv("SECRET_KEY")
    if not key:
        raise ValueError("SECRET_KEY не найден в .env")
    return Fernet(key.encode())

def encrypt_text(text: str) -> str:
    cipher = get_cipher()
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    cipher = get_cipher()
    return cipher.decrypt(token.encode()).decode()
