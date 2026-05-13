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
