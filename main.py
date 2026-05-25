from auth import (
    setup_master_password,
    verify_master_password,
    change_master_password
)

from generator import generate_password

from vault import (
    add_credential,
    view_credentials,
    delete_credential,
    search_credentials,
    copy_password,
    export_backup,
    security_audit
)


def menu():
    while True:
        print("\n==== SecureVault ====")
        print("1. Add Credential")
        print("2. View Credentials")
        print("3. Delete Credential")
        print("4. Search Credentials")
        print("5. Copy Password")
        print("6. Generate Password")
        print("7. Change Master Password")
        print("8. Export Encrypted Backup")
        print("9. Run Security Audit")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_credential()

        elif choice == "2":
            view_credentials()

        elif choice == "3":
            delete_credential()

        elif choice == "4":
            search_credentials()

        elif choice == "5":
            copy_password()

        elif choice == "6":
            length = int(
                input("Password length: ")
            )

            password = generate_password(length)

            print(
                f"\nGenerated Password:\n{password}"
            )

        elif choice == "7":
            change_master_password()

        elif choice == "8":
            export_backup()

        elif choice == "9":
            security_audit()

        elif choice == "10":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


setup_master_password()

if verify_master_password():
    print("Access Granted.")
    menu()
else:
    print("Access Denied.")
