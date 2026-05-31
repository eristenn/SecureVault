import hashlib
import os
import sys
import time
from getpass import getpass


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


MASTER_PASSWORD_FILE = resource_path(
    "master.hash"
)

MAX_ATTEMPTS = 3
LOCKOUT_TIME = 30


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def setup_master_password():

    if not os.path.exists(
        MASTER_PASSWORD_FILE
    ):

        password = getpass(
            "Create a master password: "
        )

        hashed_password = hash_password(
            password
        )

        with open(
            MASTER_PASSWORD_FILE,
            "w"
        ) as file:

            file.write(
                hashed_password
            )

        print(
            "Master password created."
        )


def verify_master_password(password):

    try:

        with open(
            MASTER_PASSWORD_FILE,
            "r"
        ) as file:

            stored_password = (
                file.read().strip()
            )

        hashed_password = hash_password(
            password
        )

        return (
            hashed_password
            == stored_password
        )

    except FileNotFoundError:

        return False


def verify_master_password_terminal():

    with open(
        MASTER_PASSWORD_FILE,
        "r"
    ) as file:

        stored_password = (
            file.read().strip()
        )

    attempts = 0

    while attempts < MAX_ATTEMPTS:

        password = getpass(
            "Enter master password: "
        )

        hashed_password = hash_password(
            password
        )

        if (
            hashed_password
            == stored_password
        ):

            return True

        attempts += 1

        remaining = (
            MAX_ATTEMPTS
            - attempts
        )

        print(
            f"Incorrect password. "
            f"{remaining} attempts remaining."
        )

    print(
        f"\nToo many failed attempts."
        f"\nAccess locked for "
        f"{LOCKOUT_TIME} seconds."
    )

    time.sleep(LOCKOUT_TIME)

    return False


def change_master_password():

    with open(
        MASTER_PASSWORD_FILE,
        "r"
    ) as file:

        stored_password = (
            file.read().strip()
        )

    current_password = getpass(
        "Enter current master password: "
    )

    current_hash = hash_password(
        current_password
    )

    if current_hash != stored_password:

        print(
            "Current password is incorrect."
        )

        return

    new_password = getpass(
        "Enter new master password: "
    )

    confirm_password = getpass(
        "Confirm new master password: "
    )

    if new_password != confirm_password:

        print(
            "Passwords do not match."
        )

        return

    new_hash = hash_password(
        new_password
    )

    with open(
        MASTER_PASSWORD_FILE,
        "w"
    ) as file:

        file.write(new_hash)

    print(
        "Master password updated successfully."
    )