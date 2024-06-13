import getpass
import hashlib
from cryptography.fernet import Fernet
import base64

# Function to hash the secret code
def hash_code(secret_code):
    return hashlib.sha256(secret_code.encode()).hexdigest()

# Function to generate a key based on the secret code
def generate_key(secret_code):
    return base64.urlsafe_b64encode(hashlib.sha256(secret_code.encode()).digest())

# Function to store the secret code and data
def store_secret_code_and_data():
    secret_code = getpass.getpass("Enter a secret code: ")
    hashed_code = hash_code(secret_code)
    data = input("Enter the data you want to protect: ")
    
    key = generate_key(secret_code)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    
    # Store hashed secret code in a text file
    with open("secret_code.txt", "w") as file:
        file.write(hashed_code)
    
    # Store encrypted data in a binary file
    with open("protected_data.txt", "wb") as file:
        file.write(encrypted_data)
    
    print("Secret code and data stored securely.")

# Function to verify the secret code and access data
def verify_secret_code_and_access_data():
    secret_code = getpass.getpass("Enter your secret code to access the data: ")
    hashed_code = hash_code(secret_code)
    
    try:
        with open("secret_code.txt", "r") as file:
            stored_hashed_code = file.read()
    except FileNotFoundError:
        print("Error: No secret code stored. Please store a secret code first.")
        return
    
    if hashed_code == stored_hashed_code:
        key = generate_key(secret_code)
        fernet = Fernet(key)
        
        try:
            with open("protected_data.txt", "rb") as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            print("Access granted. Here is the protected data:")
            print(decrypted_data)
        except Exception as e:
            print(f"Access denied. Decryption failed: {e}")
    else:
        print("Access denied. Incorrect secret code.")

# Function to modify the protected data
def modify_protected_data():
    secret_code = getpass.getpass("Enter your secret code to modify the data: ")
    hashed_code = hash_code(secret_code)
    
    try:
        with open("secret_code.txt", "r") as file:
            stored_hashed_code = file.read()
    except FileNotFoundError:
        print("Error: No secret code stored. Please store a secret code first.")
        return
    
    if hashed_code == stored_hashed_code:
        key = generate_key(secret_code)
        fernet = Fernet(key)
        
        try:
            with open("protected_data.txt", "rb") as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            print("Access granted. Here is the current protected data:")
            print(decrypted_data)
            new_data = input("Enter the new data to protect: ")
            encrypted_new_data = fernet.encrypt(new_data.encode())
            
            with open("protected_data.txt", "wb") as file:
                file.write(encrypted_new_data)
            
            print("Data modified successfully.")
        except Exception as e:
            print(f"Access denied. Decryption failed: {e}")
    else:
        print("Access denied. Incorrect secret code.")

# Main code
if __name__ == "__main__":
    print("1. Store a new secret code and data")
    print("2. Access protected data")
    print("3. Modify protected data")
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == "1":
        store_secret_code_and_data()
    elif choice == "2":
        verify_secret_code_and_access_data()
    elif choice == "3":
        modify_protected_data()
    else:
        print("Invalid choice.")
