VAULT_FILE = "vault.txt"


def add_credential():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    with open(VAULT_FILE, "a") as file:
        file.write(f"{website}|{username}|{password}\n")

    print("Credential saved.")


def view_credentials():
    try:
        with open(VAULT_FILE, "r") as file:
            credentials = file.readlines()

            if not credentials:
                print("No credentials stored.")
                return

            print("\n=== Stored Credentials ===")

            for credential in credentials:
                website, username, password = credential.strip().split("|")

                print(f"""
Website: {website}
Username: {username}
Password: {password}
------------------------
""")

    except FileNotFoundError:
        print("No vault file found.")
