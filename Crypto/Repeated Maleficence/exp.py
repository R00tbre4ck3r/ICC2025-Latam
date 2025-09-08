import sys

KEY_LEN = 5
KNOWN_PREFIX = b"HTB{"

def read_ciphertext(path: str) -> bytes:
    with open(path, "r", encoding="utf-8") as f:
      mport sys


KEY_LEN = 5

KNOWN_PREFIX = b"HTB{"


def read_ciphertext(path: str) -> bytes:

    with open(path, "r", encoding="utf-8") as f:

        data = f.read().strip()

