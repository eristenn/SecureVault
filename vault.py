from encryption import encrypt_password, decrypt_password
from getpass import getpass

VAULT_FILE = "vault.txt"


def add_credential():
    website = input("Website: ")
    username = input("Username: ")
    password = getpass("Password: ")

    encrypted_password = encrypt_password(password)

    with open(VAULT_FILE, "a") as file:
        file.write(f"{website}|{username}|{encrypted_password}\n")

    print("Credential saved securely.")


def view_credentials():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

            if not credentials:
                print("No credentials stored.")
                return

            print("\n=== Stored Credentials ===")

            for credential in credentials:
                website, username, encrypted_password = credential.strip().split("|")

                decrypted_password = decrypt_password(encrypted_password)

                print(f"""
Website: {website}
Username: {username}
Password: {decrypted_password}
------------------------
""")

    except FileNotFoundError:
        print("No vault file found.")
