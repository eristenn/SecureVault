from encryption import encrypt_password, decrypt_password
from getpass import getpass
from datetime import datetime, timedelta
from strength import check_password_strength
import pyperclip
import shutil
import os
import sys


def resource_path(filename):

    if getattr(sys, "frozen", False):

        return os.path.join(
            os.path.dirname(sys.executable),
            filename
        )

    return os.path.join(
        os.path.dirname(__file__),
        filename
    )


VAULT_FILE = resource_path(
    "vault.txt"
)


def add_credential():
    website = input("Website: ")
    username = input("Username: ")
    password = getpass("Password: ")

    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

            for credential in credentials:
                stored_website, stored_username, _, _ = (
                    credential.strip().split("|")
                )

                if (
                    website.lower() == stored_website.lower()
                    and username.lower() == stored_username.lower()
                ):
                    print(
                        "Credential already exists."
                    )
                    return

    except FileNotFoundError:
        pass

    strength = check_password_strength(password)

    print(f"Password Strength: {strength}")

    encrypted_password = encrypt_password(password)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(VAULT_FILE, "a") as file:
        file.write(
            f"{website}|{username}|"
            f"{encrypted_password}|{timestamp}\n"
        )

    print("Credential saved securely.")


def view_credentials():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

            if not credentials:
                print("No credentials stored.")
                return

            reveal = input(
                "Reveal passwords? (y/n): "
            ).lower()

            print("\n=== Stored Credentials ===")

            for credential in credentials:
                website, username, encrypted_password, timestamp = (
                    credential.strip().split("|")
                )

                decrypted_password = decrypt_password(
                    encrypted_password
                )

                if reveal == "y":
                    display_password = decrypted_password
                else:
                    display_password = "*" * len(
                        decrypted_password
                    )

                credential_date = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M:%S"
                )

                password_age = (
                    datetime.now() - credential_date
                )

                warning_message = ""

                if password_age > timedelta(days=90):
                    warning_message = (
                        "WARNING: Password is older "
                        "than 90 days."
                    )

                print(f"""
Website: {website}
Username: {username}
Password: {display_password}
Date Added: {timestamp}
{warning_message}
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
            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            print(f"{index}. {website} ({username})")

        choice = int(
            input("\nEnter credential number to delete: ")
        )

        if choice < 1 or choice > len(credentials):
            print("Invalid selection.")
            return

        deleted_credential = credentials.pop(choice - 1)

        with open(VAULT_FILE, "w") as file:
            file.writelines(credentials)

        website, username, _, _ = (
            deleted_credential.strip().split("|")
        )

        print(
            f"Deleted credential for {website} ({username})"
        )

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

        search_term = input(
            "Search website or username: "
        ).lower()

        matches_found = False

        print("\n=== Search Results ===")

        for credential in credentials:
            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            if (
                search_term in website.lower()
                or search_term in username.lower()
            ):
                decrypted_password = decrypt_password(
                    encrypted_password
                )

                credential_date = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M:%S"
                )

                password_age = (
                    datetime.now() - credential_date
                )

                warning_message = ""

                if password_age > timedelta(days=90):
                    warning_message = (
                        "WARNING: Password is older "
                        "than 90 days."
                    )

                print(f"""
Website: {website}
Username: {username}
Password: {decrypted_password}
Date Added: {timestamp}
{warning_message}
------------------------
""")

                matches_found = True

        if not matches_found:
            print("No matching credentials found.")

    except FileNotFoundError:
        print("No vault file found.")


def copy_password():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

        if not credentials:
            print("No credentials stored.")
            return

        print("\n=== Stored Credentials ===")

        for index, credential in enumerate(credentials, start=1):
            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            print(f"{index}. {website} ({username})")

        choice = int(
            input(
                "\nSelect credential number "
                "to copy password: "
            )
        )

        if choice < 1 or choice > len(credentials):
            print("Invalid selection.")
            return

        selected_credential = credentials[choice - 1]

        (
            website,
            username,
            encrypted_password,
            timestamp
        ) = selected_credential.strip().split("|")

        decrypted_password = decrypt_password(
            encrypted_password
        )

        pyperclip.copy(decrypted_password)

        print(
            f"Password for {website} copied to clipboard."
        )

    except FileNotFoundError:
        print("No vault file found.")

    except ValueError:
        print("Invalid input.")


def export_backup():
    try:
        confirmation = input(
            "\nWARNING: Backup files contain "
            "sensitive encrypted credential data.\n"
            "Continue export? (y/n): "
        ).lower()

        if confirmation != "y":
            print("Backup export cancelled.")
            return

        backup_name = (
            f"vault_backup_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        shutil.copy(VAULT_FILE, backup_name)

        print(
            f"Encrypted backup created: {backup_name}"
        )

    except FileNotFoundError:
        print("No vault file found.")


def security_audit():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

        if not credentials:
            print("No credentials stored.")
            return

        total_credentials = len(credentials)
        weak_passwords = 0
        old_passwords = 0
        reused_passwords = 0

        password_list = []

        for credential in credentials:
            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            decrypted_password = decrypt_password(
                encrypted_password
            )

            password_list.append(
                decrypted_password
            )

            strength = check_password_strength(
                decrypted_password
            )

            if strength == "Weak":
                weak_passwords += 1

            credential_date = datetime.strptime(
                timestamp,
                "%Y-%m-%d %H:%M:%S"
            )

            password_age = (
                datetime.now() - credential_date
            )

            if password_age > timedelta(days=90):
                old_passwords += 1

        reused_passwords = (
            len(password_list)
            - len(set(password_list))
        )

        print("\n=== Vault Security Audit ===")

        print(
            f"Total Credentials: {total_credentials}"
        )

        print(
            f"Weak Passwords: {weak_passwords}"
        )

        print(
            f"Old Passwords (>90 days): "
            f"{old_passwords}"
        )

        print(
            f"Reused Passwords Detected: "
            f"{reused_passwords}"
        )

    except FileNotFoundError:
        print("No vault file found.")


def view_credentials_file():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

        if not credentials:
            return "No credentials stored."

        output = "\n=== Stored Credentials ===\n\n"

        for credential in credentials:
            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            decrypted_password = decrypt_password(
                encrypted_password
            )

            output += (
                f"Website: {website}\n"
                f"Username: {username}\n"
                f"Password: {decrypted_password}\n"
                f"Date Added: {timestamp}\n"
                f"------------------------\n\n"
            )

        return output

    except FileNotFoundError:
        return "No vault file found."

def add_credential_gui(
    website,
    username,
    password
):
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

            for credential in credentials:
                stored_website, stored_username, _, _ = (
                    credential.strip().split("|")
                )

                if (
                    website.lower() == stored_website.lower()
                    and username.lower() == stored_username.lower()
                ):
                    return "Credential already exists."

    except FileNotFoundError:
        pass

    encrypted_password = encrypt_password(password)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(VAULT_FILE, "a") as file:
        file.write(
            f"{website}|{username}|"
            f"{encrypted_password}|{timestamp}\n"
        )

    return "Credential saved securely."

def security_audit():

    try:

        with open(
            VAULT_FILE,
            "r"
        ) as file:

            credentials = file.readlines()

    except FileNotFoundError:

        return (
            "No vault data found."
        )

    weak_passwords = []
    reused_passwords = []
    password_list = []

    for credential in credentials:

        try:

            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            decrypted_password = decrypt_password(
                encrypted_password
            )

            password_list.append(
                (
                    website,
                    username,
                    decrypted_password
                )
            )

            # Weak password checks
            if (
                len(decrypted_password) < 8
                or decrypted_password.isalpha()
                or decrypted_password.isdigit()
            ):

                weak_passwords.append(
                    (
                        website,
                        username
                    )
                )

        except:
            continue

    # Reused password detection
    seen = {}

    for website, username, password in password_list:

        if password in seen:

            reused_passwords.append(
                (
                    website,
                    username
                )
            )

        else:

            seen[password] = (
                website,
                username
            )

    # Build results
    results = []

    results.append(
        "=== SECURITY AUDIT ===\n"
    )

    results.append(
        f"Weak Passwords Found: "
        f"{len(weak_passwords)}\n"
    )

    for website, username in weak_passwords:

        results.append(
            f"- {website} "
            f"({username})\n"
        )

    results.append("\n")

    results.append(
        f"Reused Passwords Found: "
        f"{len(reused_passwords)}\n"
    )

    for website, username in reused_passwords:

        results.append(
            f"- {website} "
            f"({username})\n"
        )

    return "".join(results)

def search_credentials(search_term):

    try:

        with open(
            VAULT_FILE,
            "r"
        ) as file:

            credentials = file.readlines()

    except FileNotFoundError:

        return (
            "No vault data found."
        )

    results = []

    for credential in credentials:

        try:

            website, username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            decrypted_password = decrypt_password(
                encrypted_password
            )

            if (
                search_term.lower() in website.lower()
                or search_term.lower() in username.lower()
            ):

                results.append(
                    f"Website: {website}\n"
                    f"Username: {username}\n"
                    f"Password: {decrypted_password}\n"
                    f"Date Added: {timestamp}\n\n"
                )

        except:
            continue

    if not results:

        return (
            "No matching credentials found."
        )

    return "".join(results)

def delete_credential(website, username):

    try:

        with open(
            VAULT_FILE,
            "r"
        ) as file:

            credentials = file.readlines()

    except FileNotFoundError:

        return (
            "Vault file not found."
        )

    updated_credentials = []

    deleted = False

    for credential in credentials:

        try:

            stored_website, stored_username, encrypted_password, timestamp = (
                credential.strip().split("|")
            )

            if (
                stored_website.lower() == website.lower()
                and stored_username.lower() == username.lower()
            ):

                deleted = True
                continue

            updated_credentials.append(
                credential
            )

        except:
            updated_credentials.append(
                credential
            )

    with open(
        VAULT_FILE,
        "w"
    ) as file:

        file.writelines(
            updated_credentials
        )

    if deleted:

        return (
            "Credential deleted successfully."
        )

    return (
        "Credential not found."
    )

def edit_credential(
    website,
    username,
    new_password
):

    try:

        with open(
            VAULT_FILE,
            "r"
        ) as file:

            credentials = file.readlines()

    except FileNotFoundError:

        return (
            "Vault file not found."
        )

    updated_credentials = []

    edited = False

    for credential in credentials:

        try:

            (
                stored_website,
                stored_username,
                encrypted_password,
                timestamp
            ) = credential.strip().split("|")

            if (
                stored_website.lower() == website.lower()
                and stored_username.lower() == username.lower()
            ):

                encrypted_password = (
                    encrypt_password(
                        new_password
                    )
                )

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                updated_credentials.append(
                    f"{stored_website}|"
                    f"{stored_username}|"
                    f"{encrypted_password}|"
                    f"{timestamp}\n"
                )

                edited = True

            else:

                updated_credentials.append(
                    credential
                )

        except:

            updated_credentials.append(
                credential
            )

    with open(
        VAULT_FILE,
        "w"
    ) as file:

        file.writelines(
            updated_credentials
        )

    if edited:

        return (
            "Credential updated successfully."
        )

    return (
        "Credential not found."
    )

