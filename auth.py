import hashlib
import os
import time
from getpass import getpass

MASTER_PASSWORD_FILE = "master.hash"

MAX_ATTEMPTS = 3
LOCKOUT_TIME = 30


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def setup_master_password():
    if not os.path.exists(MASTER_PASSWORD_FILE):
        password = getpass(
            "Create a master password: "
        )

        hashed_password = hash_password(password)

        with open(MASTER_PASSWORD_FILE, "w") as file:
            file.write(hashed_password)

        print("Master password created.")


def verify_master_password():
    with open(MASTER_PASSWORD_FILE, "r") as file:
        stored_password = file.read()

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        password = getpass(
            "Enter master password: "
        )

        hashed_password = hash_password(password)

        if hashed_password == stored_password:
            return True

        attempts += 1

        remaining = MAX_ATTEMPTS - attempts

        print(
            f"Incorrect password. "
            f"{remaining} attempts remaining."
        )

    print(
        f"\nToo many failed attempts."
        f"\nAccess locked for {LOCKOUT_TIME} seconds."
    )

    time.sleep(LOCKOUT_TIME)

    return False
