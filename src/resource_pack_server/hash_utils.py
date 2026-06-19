"""SHA1 hashing — Minecraft clients use SHA1 to identify resource packs."""

import hashlib
from pathlib import Path


def sha1_hex(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def sha1_file(path: Path) -> str:
    """Return the lowercase SHA1 hex digest of a file's contents."""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
