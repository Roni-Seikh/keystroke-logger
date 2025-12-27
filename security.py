from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())

def decrypt_data(data: bytes) -> str:
    return cipher.decrypt(data).decode()
