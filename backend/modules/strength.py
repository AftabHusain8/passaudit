"""
modules/strength.py
────────────────────────────────────────────────────────────────
Stage 1 — Password Strength Analysis
Author : Aftab Husain | CDAC PassAudit v2.0

Evaluates a password across multiple dimensions and assigns:
  • A numeric score  (0 – 100)
  • A level label    (Very Weak / Weak / Medium / Strong / Excellent)
  • Password entropy in bits
  • Detailed checks dictionary
  • Actionable feedback list
  • A strong-password hint
"""

import re
import math
import string

# ── Entropy helpers ───────────────────────────────────────────────────────────

def _charset_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password): size += 26
    if re.search(r"[A-Z]", password): size += 26
    if re.search(r"\d",    password): size += 10
    if re.search(r"[^a-zA-Z0-9]", password): size += 32
    return max(size, 1)


def _entropy(password: str) -> float:
    cs = _charset_size(password)
    return round(len(password) * math.log2(cs), 2)


# ── Patterns to penalise ─────────────────────────────────────────────────────

SEQUENCE_PATTERNS = re.compile(
    r"(0123|1234|2345|3456|4567|5678|6789|7890"
    r"|abcd|bcde|cdef|defg|efgh|fghi|ghij|hijk|ijkl|jklm|klmn|lmno|mnop"
    r"|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz"
    r"|qwerty|asdf|zxcv|qazwsx|1q2w3e)",
    re.IGNORECASE,
)

REPEAT_PATTERN   = re.compile(r"(.)\1{2,}")
KEYBOARD_WALK    = re.compile(r"(qwerty|asdfgh|zxcvbn|!@#\$%\^)", re.IGNORECASE)
COMMON_WORDS     = ["password", "passw0rd", "admin", "login", "welcome", "letmein"]


# ── Main analysis function ────────────────────────────────────────────────────

def analyze_strength(password: str) -> dict:
    length       = len(password)
    has_upper    = bool(re.search(r"[A-Z]", password))
    has_lower    = bool(re.search(r"[a-z]", password))
    has_digit    = bool(re.search(r"\d", password))
    has_special  = bool(re.search(r"[^A-Za-z0-9]", password))
    has_sequence = bool(SEQUENCE_PATTERNS.search(password))
    has_repeat   = bool(REPEAT_PATTERN.search(password))
    has_keyboard = bool(KEYBOARD_WALK.search(password))
    has_common   = any(w in password.lower() for w in COMMON_WORDS)
    all_same_case = password.isalpha() and (password.isupper() or password.islower())
    all_digits   = password.isdigit()

    score    = 0
    feedback = []

    # ── Length scoring (max 30 pts)
    if length >= 20:    score += 30
    elif length >= 16:  score += 25
    elif length >= 12:  score += 20
    elif length >= 10:  score += 15
    elif length >= 8:   score += 10
    elif length >= 6:   score += 5
    else:
        score += 2
        feedback.append("Use at least 8 characters — longer is always stronger.")

    if length < 12:
        feedback.append(f"Current length {length} — aim for 12+ characters.")

    # ── Character class scoring (max 40 pts)
    if has_upper:   score += 10
    else:           feedback.append("Add uppercase letters (A–Z) to increase complexity.")

    if has_lower:   score += 10
    else:           feedback.append("Add lowercase letters (a–z).")

    if has_digit:   score += 10
    else:           feedback.append("Include at least one number (0–9).")

    if has_special: score += 10
    else:           feedback.append("Add special characters like !@#$%^&*() for major strength gains.")

    # ── Entropy bonus (max 10 pts)
    entropy = _entropy(password)
    if entropy >= 60:   score += 10
    elif entropy >= 40: score += 6
    elif entropy >= 25: score += 3

    # ── Penalties (up to -30 pts)
    if has_sequence:
        score -= 12
        feedback.append("Avoid predictable sequences: 1234, abcd, qwerty, etc.")

    if has_repeat:
        score -= 8
        feedback.append("Avoid repeating characters (aaa, 111…).")

    if has_keyboard:
        score -= 8
        feedback.append("Avoid keyboard walk patterns: qwerty, asdfgh, zxcvbn.")

    if has_common:
        score -= 15
        feedback.append("Remove common words like 'password', 'admin', 'login'.")

    if all_same_case:
        score -= 5
        feedback.append("Mix uppercase and lowercase — don't use all-caps or all-lowercase.")

    if all_digits:
        score -= 10
        feedback.append("Avoid passwords made entirely of digits.")

    # ── Clamp score
    score = max(0, min(100, score))

    # ── Level assignment
    if score < 20:      level = "Very Weak"
    elif score < 40:    level = "Weak"
    elif score < 60:    level = "Medium"
    elif score < 80:    level = "Strong"
    else:               level = "Excellent"

    if not feedback:
        feedback.append("Great password! No immediate improvements detected.")

    # ── Hint generation
    hint = _generate_hint(has_upper, has_lower, has_digit, has_special, length)

    checks = {
        "length_8":      length >= 8,
        "length_12":     length >= 12,
        "length_16":     length >= 16,
        "has_upper":     has_upper,
        "has_lower":     has_lower,
        "has_digit":     has_digit,
        "has_special":   has_special,
        "no_sequence":   not has_sequence,
        "no_repeat":     not has_repeat,
        "no_keyboard":   not has_keyboard,
        "no_common":     not has_common,
        "char_count":    length,
        "entropy_bits":  entropy,
    }

    return {
        "score":        score,
        "level":        level,
        "entropy_bits": entropy,
        "checks":       checks,
        "feedback":     feedback,
        "hint":         hint,
    }


def _generate_hint(upper, lower, digit, special, length) -> str:
    missing = []
    if not upper:   missing.append("uppercase letter")
    if not lower:   missing.append("lowercase letter")
    if not digit:   missing.append("number")
    if not special: missing.append("symbol like !@#$")
    if length < 12: missing.append("more characters (aim for 12+)")

    if not missing:
        return "Consider using a passphrase: 4 random words joined with symbols."
    return f"To improve: add a {', '.join(missing[:2])}."
