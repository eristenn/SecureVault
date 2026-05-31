from cryptography.fernet import Fernet
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


KEY_FILE = resource_path(
    "vault.key"
)


def load_key():

    if not os.path.exists(
        KEY_FILE
    ):

        key = Fernet.generate_key()

        with open(
            KEY_FILE,
            "wb"
        ) as file:

            file.write(key)

    with open(
        KEY_FILE,
        "rb"
    ) as file:

        return file.read()


key = load_key()

cipher = Fernet(
    key
)


def encrypt_password(password):

    return cipher.encrypt(
        password.encode()
    ).decode()


def decrypt_password(encrypted_password):

    return cipher.decrypt(
        encrypted_password.encode()
    ).decode()