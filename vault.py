from encryption import encrypt_password, decrypt_password
from getpass import getpass
from datetime import datetime

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


def delete_credential():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

        if not credentials:
            print("No credentials stored.")
            return

        print("\n=== Stored Credentials ===")

        for index, credential in enumerate(credentials, start=1):
            website, username, encrypted_password = credential.strip().split("|")

            print(f"{index}. {website} ({username})")

        choice = int(input("\nEnter credential number to delete: "))

        if choice < 1 or choice > len(credentials):
            print("Invalid selection.")
            return

        deleted_credential = credentials.pop(choice - 1)

        with open(VAULT_FILE, "w") as file:
            file.writelines(credentials)

        website, username, _ = deleted_credential.strip().split("|")

        print(f"Deleted credential for {website} ({username})")

    except FileNotFoundError:
        print("No vault file found.")

    except ValueError:
        print("Invalid input.")


def search_credentials():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

        if not credentials:
            print("No credentials stored.")
            return

        search_term = input("Search website or username: ").lower()

        matches_found = False

        print("\n=== Search Results ===")

        for credential in credentials:
            website, username, encrypted_password = credential.strip().split("|")

            if (
                search_term in website.lower()
                or search_term in username.lower()
            ):
                decrypted_password = decrypt_password(encrypted_password)

                print(f"""
Website: {website}
Username: {username}
Password: {decrypted_password}
------------------------
""")

                matches_found = True

        if not matches_found:
            print("No matching credentials found.")

    except FileNotFoundError:
        print("No vault file found.")
