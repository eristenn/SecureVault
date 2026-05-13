import hashlib
import os
from getpass import getpass

MASTER_PASSWORD_FILE = "master.hash"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def setup_master_password():
    if os.path.exists(MASTER_PASSWORD_FILE):
        return

    print("=== First Time Setup ===")
    password = getpass("Create a master password: ")

    hashed = hash_password(password)

    with open(MASTER_PASSWORD_FILE, "w") as f:
        f.write(hashed)

    print("Master password created.\n")


def verify_master_password():
    password = getpass("Enter master password: ")

    hashed = hash_password(password)

    with open(MASTER_PASSWORD_FILE, "r") as f:
        stored_hash = f.read()

    return hashed == stored_hash
