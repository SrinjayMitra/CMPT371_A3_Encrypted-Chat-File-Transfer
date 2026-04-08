from cryptography.fernet import Fernet

# 🔑 IMPORTANT: Replace this with your generated key
KEY = b'HOJfWpMllxQSn9cS8kSEUTEpr2XB734ZM07v2pA3mI0='

cipher = Fernet(KEY)

def encrypt(message):
    # If bytes, skip .encode()
    if isinstance(message, bytes):
        return cipher.encrypt(message)
    else:
        return cipher.encrypt(message.encode())

def decrypt(ciphertext: bytes) -> str:
    return cipher.decrypt(ciphertext)