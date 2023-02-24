import os
import binascii


def generate_token(size: int = 40) -> str:
    return binascii.hexlify(os.urandom(size)).decode()
