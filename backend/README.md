# PassAudit v2.0
## Password Strength Auditor & Dictionary Attack Tool
### Developed by **Aftab Husain** | CDAC Academic Initiative

---

## Project Overview

PassAudit is a full-stack cybersecurity application that evaluates password security and
demonstrates real-world attack simulations. It is built with a clean client-server
architecture that separates concerns and allows independent scaling of each component.

---

## Project Structure

```
passaudit/
├── backend/
│   ├── main.py               ← FastAPI entry point — API routing & response models
│   ├── requirements.txt      ← Python dependencies
│   ├── wordlist.txt          ← Custom dictionary entries (add your own)
│   └── modules/
│       ├── __init__.py
│       ├── strength.py       ← Stage 1: Password strength + entropy analysis
│       ├── hasher.py         ← Stage 2: SHA-256, SHA-512, bcrypt hashing
│       └── attacker.py       ← Stage 3: Dictionary attack engine
└── frontend.html             ← Self-contained React UI (no build step)
```

---

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Frontend

Open `frontend.html` directly in any browser.
No Node.js, no build step — React loads via CDN.

---

## The Three-Stage Pipeline

### Stage 1 — Strength Analysis (`modules/strength.py`)

Evaluates 11 criteria:

| Criterion        | Max Points | Penalty |
|------------------|------------|---------|
| Length (8–20+)   | 30 pts     | —       |
| Uppercase A–Z    | 10 pts     | —       |
| Lowercase a–z    | 10 pts     | —       |
| Digits 0–9       | 10 pts     | —       |
| Special chars    | 10 pts     | —       |
| Entropy bonus    | 10 pts     | —       |
| Sequential chars | —          | −12     |
| Repeating chars  | —          | −8      |
| Keyboard walk    | —          | −8      |
| Common words     | —          | −15     |
| All-digit/case   | —          | −10     |

**Levels:** Very Weak / Weak / Medium / Strong / Excellent

### Stage 2 — Cryptographic Hashing (`modules/hasher.py`)

| Algorithm | Use Case                         |
|-----------|----------------------------------|
| SHA-256   | Fast comparison in attack engine |
| SHA-512   | Educational — wider digest       |
| bcrypt    | Production-grade, work factor 12 |

Passwords are **never stored in plaintext** at any stage.

### Stage 3 — Dictionary Attack (`modules/attacker.py`)

Four attack variants checked per submission:
1. **Exact match** — direct SHA-256 comparison
2. **Case-insensitive** — lowercase variant
3. **Leet-speak decode** — `@→a`, `0→o`, `1→i`, `3→e`, `$→s`
4. **Trailing-digit strip** — `pass123 → pass`

Add custom entries to `wordlist.txt` (one per line).
For production simulation, replace with `rockyou.txt`.

---

## API Reference

### `POST /analyze`

```json
Request:  { "password": "MyS3cur3!" }

Response:
{
  "author": "Aftab Husain",
  "project": "PassAudit v2.0 — CDAC",
  "score": 72,
  "level": "Strong",
  "entropy_bits": 47.6,
  "checks": { "length_8": true, "has_upper": true, ... },
  "feedback": ["Add more special characters.", ...],
  "hint": "Consider using a passphrase.",
  "hash_sha256": "a3f5...",
  "hash_sha512": "9c2b...",
  "hash_bcrypt": "$2b$12$...",
  "cracked": false,
  "cracked_word": null,
  "wordlist_size": 120,
  "attack_duration_ms": 0.87
}
```

### `GET /wordlist/count`
Returns the current number of dictionary entries.

---

## Security Concepts Demonstrated

- **Password Entropy** — information-theoretic measure of randomness
- **Cryptographic Hashing** — one-way transformation; SHA-256, SHA-512, bcrypt
- **Salt** — bcrypt auto-generates unique salts to prevent rainbow table attacks
- **Dictionary Attack** — comparing hashes of known passwords against a target hash
- **Leet-Speak** — common evasion technique; the engine accounts for it
- **Work Factor** — bcrypt's adaptive cost makes brute-force computationally expensive

---

## Future Enhancements

- Load full `rockyou.txt` (14M entries) for realistic attack simulation
- Add JWT authentication and user dashboards
- Distributed attack simulation with multiprocessing
- Database logging of audit results (PostgreSQL)
- Docker Compose deployment (backend + nginx + frontend)
- REST API rate limiting and IP throttling

---

*Developed by **Aftab Husain** as part of the CDAC academic initiative.*
*For educational purposes only. No passwords are stored or transmitted persistently.*
