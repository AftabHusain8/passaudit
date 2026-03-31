"""
modules/hasher.py
────────────────────────────────────────────────────────────────
Stage 2 — Cryptographic Hashing Service
Author : Aftab Husain | CDAC PassAudit v2.0

Produces three hashes for every submitted password:
  • SHA-256  — fast, used for dictionary comparison
  • SHA-512  — wider digest, shown for educational comparison
  • bcrypt   — adaptive, work-factor based — production standard

Passwords are NEVER stored in plaintext at any stage.
"""

import hashlib
import bcrypt


def hash_password(password: str) -> dict:
    """
    Returns a dict with sha256, sha512, and bcrypt hashes
    of the given password string.
    """
    encoded = password.encode("utf-8")

    sha256_hash = hashlib.sha256(encoded).hexdigest()
    sha512_hash = hashlib.sha512(encoded).hexdigest()

    # bcrypt: work factor 12 (recommended for 2024+)
    # Each call generates a unique salt automatically
    bcrypt_hash = bcrypt.hashpw(encoded, bcrypt.gensalt(rounds=12)).decode("utf-8")

    return {
        "sha256": sha256_hash,
        "sha512": sha512_hash,
        "bcrypt": bcrypt_hash,
    }


def verify_bcrypt(password: str, hashed: str) -> bool:
    """Verify a password against a stored bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
