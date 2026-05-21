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
