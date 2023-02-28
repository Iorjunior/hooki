import os
import string
import secrets
import binascii

def generate_token(size: int = 40) -> str:
    return binascii.hexlify(os.urandom(size)).decode()


def generate_passwork(size: int = 15) -> str:
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars

    password = ''

    for i in range(size):
        password += ''.join(secrets.choice(alphabet))

    return password