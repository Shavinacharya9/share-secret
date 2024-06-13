import hashlib
from cryptography.fernet import Fernet
import base64
import os

def hash_code(secret_code):
    return hashlib.sha256(secret_code.encode()).hexdigest()

def generate_key(secret_code):
    return base64.urlsafe_b64encode(hashlib.sha256(secret_code.encode()).digest())

def store_data(secret_code, data):
    try:
        hashed_code = hash_code(secret_code)
        key = generate_key(secret_code)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        
        with open("secret_code.txt", "w") as file:
            file.write(hashed_code)
        
        with open("protected_data.txt", "wb") as file:
            file.write(encrypted_data)
        
        return True
    except Exception as e:
        print(f"Error storing data: {e}")
        return False

def access_data(secret_code):
    try:
        hashed_code = hash_code(secret_code)
        with open("secret_code.txt", "r") as file:
            stored_hashed_code = file.read()
        
        if hashed_code == stored_hashed_code:
            key = generate_key(secret_code)
            fernet = Fernet(key)
            with open("protected_data.txt", "rb") as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            return decrypted_data
        else:
            return None
    except Exception as e:
        print(f"Error accessing data: {e}")
        return None

def modify_data(secret_code, new_data):
    try:
        hashed_code = hash_code(secret_code)
        with open("secret_code.txt", "r") as file:
            stored_hashed_code = file.read()
        
        if hashed_code == stored_hashed_code:
            key = generate_key(secret_code)
            fernet = Fernet(key)
            encrypted_new_data = fernet.encrypt(new_data.encode())
            
            with open("protected_data.txt", "wb") as file:
                file.write(encrypted_new_data)
            
            return True
        else:
            return False
    except Exception as e:
        print(f"Error modifying data: {e}")
        return False
