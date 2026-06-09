"""SHA1 hashing — Minecraft clients use SHA1 to identify resource packs."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha1_hex(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def sha1_file(path: Path) -> str:
    """Return the lowercase SHA1 hex digest of a file's contents."""
    return sha1_hex(path.read_bytes())
