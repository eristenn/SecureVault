def add_credential():
    website = input("Website: ")
    username = input("Username: ")
    password = getpass("Password: ")
    import pyperclip

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
                "\nSelect credential number to copy password: "
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
