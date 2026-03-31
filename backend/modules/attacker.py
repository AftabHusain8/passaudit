"""
modules/attacker.py
────────────────────────────────────────────────────────────────
Stage 3 — Dictionary Attack Engine
Author : Aftab Husain | CDAC PassAudit v2.0

Simulates how real-world attackers crack passwords:

  1. Exact match          — direct SHA-256 comparison
  2. Case-insensitive     — checks lowercase variant
  3. Leet-speak reversal  — decodes @→a, 0→o, 1→i, 3→e, $→s, 5→s
  4. Common mutations     — strips trailing digits (pass1 → pass)
  5. Wordlist file        — loads from wordlist.txt if present

The engine is intentionally limited to educational simulation.
A real attack would use GPU-accelerated cracking with rainbow
tables and millions of entries (e.g., rockyou.txt).
"""

import hashlib
import os
import re

# ── Built-in wordlist (extended) ─────────────────────────────────────────────
# In production: replace with a file load of rockyou.txt or similar

BUILTIN_WORDS = [
    # Top 50 most common passwords (NCSC / HaveIBeenPwned 2024)
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "baseball",
    "iloveyou", "monkey", "letmein", "football", "shadow", "master",
    "666666", "qwertyuiop", "123321", "mustang", "1234567890", "michael",
    "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000",
    "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer",
    "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", "harley",
    "batman", "andrew", "tigger", "sunshine", "iloveyou1", "charlie",
    "aa123456", "donald", "password1", "qwerty123", "zxcvbn",

    # Common patterns
    "abc123", "admin", "admin123", "root", "toor", "login", "welcome",
    "passw0rd", "p@ssword", "p@ssw0rd", "pass", "guest", "test",
    "demo", "user", "changeme", "default", "temp", "secret",
    "access", "hello", "hello123", "mypassword", "pass123", "pass1234",

    # Keyboard walks
    "qwerty1", "qwerty12", "asdf", "asdfghjkl", "1q2w3e", "1q2w3e4r",
    "zaq12wsx", "!qaz2wsx",

    # Name-based common
    "jessica", "ashley", "bailey", "passw0rd1", "abc", "password2",
    "thomas", "daniel", "george", "computer", "samsung", "manchester",

    # India-specific common passwords
    "india", "india123", "india@123", "cdac", "pune", "mumbai",
    "delhi", "bangalore", "hyderabad", "chennai", "kolkata",
    "aftab", "husain", "password@123", "Admin@123", "Welcome@1",
    "Pass@1234", "Test@123", "Admin@1234",

    # Number sequences
    "11111111", "22222222", "33333333", "99999999", "10203040",
    "13579", "24680", "112233", "998877",

    # Common with years
    "password2023", "password2024", "admin2024", "pass2024",
]


def _load_wordlist_file() -> list:
    """Load extra words from wordlist.txt if it exists beside main.py."""
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "wordlist.txt"),
        os.path.join(os.getcwd(), "wordlist.txt"),
    ]
    for path in paths:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return [line.strip() for line in f if line.strip()]
    return []


# Build combined wordlist and pre-hash it
_file_words = _load_wordlist_file()
WORDLIST    = list(dict.fromkeys(BUILTIN_WORDS + _file_words))  # deduplicated

# SHA-256 hash → original word mapping
_HASH_MAP: dict[str, str] = {
    hashlib.sha256(w.encode()).hexdigest(): w for w in WORDLIST
}

# ── Leet-speak decoder ────────────────────────────────────────────────────────

_LEET_TABLE = str.maketrans({
    "@": "a", "4": "a",
    "0": "o",
    "1": "i", "!": "i",
    "3": "e",
    "$": "s", "5": "s",
    "+": "t", "7": "t",
    "9": "g",
    "8": "b",
    "|": "l",
})


def _decode_leet(password: str) -> str:
    return password.translate(_LEET_TABLE)


def _trailing_digits_strip(password: str) -> str:
    """Pass123  →  Pass"""
    return re.sub(r"\d+$", "", password)


# ── Main attack function ──────────────────────────────────────────────────────

def dictionary_attack(password: str, sha256_hash: str) -> dict:
    """
    Attempts to crack the password using:
      1. Exact match against pre-hashed wordlist
      2. Lowercase variant
      3. Leet-speak decoded variant
      4. Trailing-digit-stripped variant

    Returns a result dict with cracked status, matched word (if any),
    and wordlist size.
    """

    candidates = {
        "exact":          password,
        "lowercase":      password.lower(),
        "leet_decoded":   _decode_leet(password.lower()),
        "stripped":       _trailing_digits_strip(password),
        "stripped_lower": _trailing_digits_strip(password.lower()),
    }

    for variant_name, candidate in candidates.items():
        h = hashlib.sha256(candidate.encode()).hexdigest()
        if h in _HASH_MAP:
            matched = _HASH_MAP[h]
            label   = matched if variant_name == "exact" else f"{matched} ({variant_name})"
            return {
                "cracked":      True,
                "word":         label,
                "wordlist_size": len(WORDLIST),
            }

    return {
        "cracked":       False,
        "word":          None,
        "wordlist_size": len(WORDLIST),
    }
