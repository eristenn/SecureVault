from auth import setup_master_password, verify_master_password
from generator import generate_password


def menu():
    while True:
        print("\n==== SecureVault ====")
        print("1. Add Credential")
        print("2. View Credentials")
        print("3. Generate Password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("Feature coming soon.")

        elif choice == "2":
            print("Feature coming soon.")

        elif choice == "3":
            password = generate_password()
            print(f"\nGenerated Password:\n{password}")

        elif choice == "4":
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
