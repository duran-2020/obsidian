"""
Author: Dan
Title: Obsidian

Description:
This Python script provides an encryption tool that allows the user to encrypt and decrypt messages using 
the Fernet encryption algorithm from the cryptography library. The program presents a menu-driven interface 
with the following options:

1. Encrypt a message:
   - Prompts the user to enter a message.
   - Generates a random encryption key.
   - Encrypts the message using the key and displays the key and encrypted message.

2. Decrypt a message:
   - Prompts the user to enter the encryption key and encrypted message.
   - Decrypts the message using the key and displays the decrypted message.

3. Open encrypted file:
   - Attempts to open the 'encrypted_data.txt' file, which stores the encrypted information.

4. Exit:
   - Exits the program.

The script uses the cryptography library's Fernet implementation to handle the encryption and decryption operations. 
The encrypted information, including the key, encrypted message, and timestamp, is saved to the 'encrypted_data.txt' file. 
Error handling is included to handle decryption failures due to an invalid key or corrupted data.

By providing an intuitive menu interface, this script offers a user-friendly way to perform encryption and decryption 
tasks and allows easy management of encrypted data.
"""

import os
import datetime
import subprocess
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def generate_key():
    # Generate a cryptographically secure random number as the encryption key
    key = os.urandom(32)
    encoded_key = base64.urlsafe_b64encode(key)
    return encoded_key

def derive_key_from_passphrase(passphrase):
    # Derive a key from the passphrase using PBKDF2
    salt = os.urandom(16)  # Generate a random salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())
    encoded_key = base64.urlsafe_b64encode(key)
    return encoded_key

def encrypt_message(message, key):
    # Create Fernet cipher object using the key
    cipher = Fernet(key)

    # Encrypt the message using the encrypt method
    encrypted_message = cipher.encrypt(message)

    return encrypted_message

def save_to_file(key, encrypted_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_number = get_entry_number() + 1
    with open('encrypted_data.txt', 'a') as file:
        file.write(f"--- Entry #{entry_number} ---\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Key: {key.decode()}\n")
        file.write(f"Encrypted message: {encrypted_message.decode()}\n")
        file.write("\n")
        print("Encrypted information saved to 'encrypted_data.txt'.")

def decrypt_message(encrypted_message, key):
    try:
        # Create Fernet cipher object using the key
        cipher = Fernet(key)

        # Decrypt the message
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message, 'green'  # Pass the color parameter

    except InvalidToken:
        print("Invalid key or corrupted data. Decryption failed.")
        return None, None  # Return None for both decrypted_message and color

def get_entry_number():
    with open('encrypted_data.txt', 'r') as file:
        lines = file.readlines()
        return len(lines) // 5

def open_encrypted_file():
    try:
        subprocess.run(['open', 'encrypted_data.txt'], check=True)
    except subprocess.CalledProcessError:
        print("Failed to open the encrypted file.")


art = """

 ██████╗ ██████╗ ███████╗██╗██████╗ ██╗ █████╗ ███╗   ██╗
██╔═══██╗██╔══██╗██╔════╝██║██╔══██╗██║██╔══██╗████╗  ██║
██║   ██║██████╔╝███████╗██║██║  ██║██║███████║██╔██╗ ██║
██║   ██║██╔══██╗╚════██║██║██║  ██║██║██╔══██║██║╚██╗██║
╚██████╔╝██████╔╝███████║██║██████╔╝██║██║  ██║██║ ╚████║
 ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                                                    
                                                         
"""

def main():
    # Get the active count of entries
    active_count = get_entry_number()

    # ASCII header
    print(art)

    # Display the active count to the user
    print(f"\nActive Count of Entries: {active_count}\n")

    # Display the program menu options and collect user input
    while True:
        print("--- Menu ---")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Open encrypted file")
        print("4. Exit")
        choice = input("Enter your choice (1, 2, 3, or 4): ")

        if choice == '1':
            # Ask user to enter a message
            message = input("Enter a message: ").encode('utf-8')  # Convert input to bytes

            # Encryption
            print("\nSelect key generation method:")
            print("1. Random key")
            print("2. Passphrase-based key derivation")
            key_choice = input("Enter your choice (1 or 2): ")

            if key_choice == '1':
                # Random key generation
                key = generate_key()
            elif key_choice == '2':
                # Passphrase-based key derivation
                passphrase = input("Enter a passphrase: ")
                key = derive_key_from_passphrase(passphrase)
            else:
                print("Invalid choice. Returning to the main menu.")
                continue

            encrypted_message = encrypt_message(message, key)

            print("\n[Encryption Successful]")
            print("Key:", key.decode())
            print("Encrypted message:", encrypted_message.decode())

            # Save encrypted information to a file
            save_to_file(key, encrypted_message)

        elif choice == '2':
            # Ask user to enter the key and encrypted message
            key = input("Enter the encryption key: ").encode('utf-8')  # Convert input to bytes
            encrypted_message = input("Enter the encrypted message: ").encode('utf-8')  # Convert input to bytes

            # Decryption
            decrypted_message, color = decrypt_message(encrypted_message, key)

            if decrypted_message is not None:
                print("\n[Decryption Successful]")
                if color == 'green':
                    print("\033[92mDecrypted message:\033[0m", decrypted_message.decode('utf-8'))
                else:
                    print("Decrypted message:", decrypted_message.decode('utf-8'))

        elif choice == '3':
            # Open the file holding the encrypted credentials
            open_encrypted_file()

        elif choice == '4':
            print("\nExiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")

# Call the main function
if __name__ == '__main__':
    main()
