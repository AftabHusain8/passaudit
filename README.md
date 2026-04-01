# 🔐 PassAudit — Password Strength Auditor & Dictionary Attack Tool

<div align="center">

![PassAudit](https://img.shields.io/badge/PassAudit-v2.0-orange?style=for-the-badge&logo=shield&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A full-stack cybersecurity application that evaluates password strength and simulates real-world dictionary attacks.**

*Developed by **Aftab Husain**

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Installation & Setup](#-installation--setup)
- [API Reference](#-api-reference)
- [Security Concepts](#-security-concepts-demonstrated)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 🧠 Overview

**PassAudit** is a scalable full-stack cybersecurity project that demonstrates fundamental concepts of password security, cryptographic hashing, and dictionary-based attack simulation. It is built with a clean **client-server architecture** using **FastAPI** on the backend and **React** on the frontend.

The system processes every submitted password through a **three-stage pipeline**:

```
Password Input ──► Stage 1: Strength Analysis ──► Stage 2: Hashing ──► Stage 3: Dictionary Attack ──► Result
```

---

## ✨ Features

- ✅ **5-Level Strength Classification** — Very Weak / Weak / Medium / Strong / Excellent
- ✅ **11-Criteria Evaluation** — length, uppercase, lowercase, digits, special chars, entropy, sequences, repeats, keyboard walks, common words
- ✅ **Password Entropy Calculation** — information-theoretic measure of randomness in bits
- ✅ **Triple Hashing** — SHA-256, SHA-512, and bcrypt (work factor 12)
- ✅ **Dictionary Attack Simulation** — 4 attack variants: exact, case-insensitive, leet-speak, digit-strip
- ✅ **Leet-Speak Detection** — catches `p@ssw0rd`, `@dm1n`, `4dm!n` etc.
- ✅ **Modular Backend** — each stage is independently upgradeable
- ✅ **Professional UI** — military HUD aesthetic, animated score ring, real-time feedback
- ✅ **Swagger API Docs** — interactive API testing at `/docs`
- ✅ **No Password Storage** — passwords are never stored or logged at any stage

---

## 🛠 Tech Stack

| Layer    | Technology     | Purpose                          |
|----------|----------------|----------------------------------|
| Backend  | Python 3.10+   | Core language                    |
| Backend  | FastAPI        | High-performance REST API        |
| Backend  | Pydantic v2    | Request / response validation    |
| Backend  | bcrypt         | Adaptive password hashing        |
| Backend  | hashlib        | SHA-256 / SHA-512 hashing        |
| Backend  | Uvicorn        | ASGI production server           |
| Frontend | React 18       | UI component framework (CDN)     |
| Frontend | Axios          | HTTP client for API requests     |
| Frontend | HTML5 / CSS3   | Layout, animations, styling      |

---

## 📁 Project Structure

```
passaudit/
│
├── 📄 frontend.html              ← React UI — no build step required
├── 📄 README.md                  ← Project documentation
├── 📄 .gitignore                 ← Git ignore rules
│
└── 📁 backend/
    ├── 📄 main.py                ← FastAPI entry point — routes & models
    ├── 📄 requirements.txt       ← Python dependencies
    ├── 📄 wordlist.txt           ← Custom dictionary wordlist
    │
    └── 📁 modules/
        ├── 📄 __init__.py        ← Python package initializer
        ├── 📄 strength.py        ← Stage 1: Strength analysis engine
        ├── 📄 hasher.py          ← Stage 2: Cryptographic hashing service
        └── 📄 attacker.py        ← Stage 3: Dictionary attack engine
```

---

## ⚙️ How It Works

### Stage 1 — Strength Analysis

Evaluates 11 security criteria and assigns a score (0–100):

| Criterion       | Points | Notes                              |
|-----------------|--------|------------------------------------|
| Length ≥ 8      | +10    | Minimum acceptable length          |
| Length ≥ 12     | +15    | Recommended length                 |
| Length ≥ 16     | +20    | Strong length                      |
| Length ≥ 20     | +30    | Excellent length                   |
| Uppercase A–Z   | +10    | Character class diversity          |
| Lowercase a–z   | +10    | Character class diversity          |
| Digits 0–9      | +10    | Numeric inclusion                  |
| Special chars   | +10    | Symbol inclusion                   |
| Entropy bonus   | +10    | High information entropy           |
| Sequential chars| −12    | 1234, abcd, qwerty penalised       |
| Keyboard walk   | −8     | asdfgh, zxcvbn penalised          |
| Repeated chars  | −8     | aaa, 111 penalised                 |
| Common words    | −15    | password, admin, login penalised   |

### Stage 2 — Cryptographic Hashing

```
Input Password
      │
      ├──► SHA-256  → fast hash used for dictionary comparison
      ├──► SHA-512  → wider 512-bit digest for educational display
      └──► bcrypt   → adaptive hash with auto-salt, work factor 12
```

### Stage 3 — Dictionary Attack Simulation

```
Password
      │
      ├──► Exact match           → direct SHA-256 comparison
      ├──► Lowercase variant     → Password → password
      ├──► Leet-speak decoded    → p@ssw0rd → password
      └──► Trailing digit strip  → pass123  → pass
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git installed
- Any modern browser (Chrome, Edge, Firefox)

### 1. Clone the Repository

```bash
git clone https://github.com/AftabHusain8/passaudit.git
cd passaudit
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install fastapi uvicorn bcrypt pydantic
```

### 3. Start the Backend Server

```bash
uvicorn main:app --reload --port 8000
```

✅ Backend running at: `http://localhost:8000`

### 4. Open the Frontend

Double-click `frontend.html` to open in your browser.
No Node.js or build step required — React loads via CDN.

### 5. Test the API Interactively

```
http://localhost:8000/docs
```

---

## 📡 API Reference

### `POST /analyze`

Runs the complete three-stage audit pipeline.

**Request Body:**
```json
{
  "password": "MyS3cur3P@ss!"
}
```

**Response:**
```json
{
  "author": "Aftab Husain",
  "project": "PassAudit v2.0",
  "score": 85,
  "level": "Excellent",
  "entropy_bits": 61.4,
  "checks": {
    "length_8": true,
    "length_12": true,
    "has_upper": true,
    "has_lower": true,
    "has_digit": true,
    "has_special": true,
    "no_sequence": true,
    "no_repeat": true,
    "no_keyboard": true,
    "no_common": true
  },
  "feedback": ["Great password! No improvements needed."],
  "hint": "Consider using a passphrase: 4 random words joined with symbols.",
  "hash_sha256": "3a7bd3e2...",
  "hash_sha512": "9c2b1f4a...",
  "hash_bcrypt": "$2b$12$...",
  "cracked": false,
  "cracked_word": null,
  "wordlist_size": 120,
  "attack_duration_ms": 0.92
}
```

### Other Endpoints

| Method | Endpoint          | Description                    |
|--------|-------------------|--------------------------------|
| GET    | `/`               | Health check & API info        |
| GET    | `/wordlist/count` | Returns dictionary size        |
| GET    | `/docs`           | Interactive Swagger UI         |
| GET    | `/redoc`          | ReDoc API documentation        |

---

## 🔐 Security Concepts Demonstrated

| Concept           | Description                                                         |
|-------------------|---------------------------------------------------------------------|
| Password Entropy  | Measures randomness in bits — higher entropy = harder to crack      |
| SHA-256 / SHA-512 | One-way cryptographic hash functions — cannot be reversed           |
| bcrypt            | Adaptive hashing with automatic salt — industry standard            |
| Salt              | Random data added before hashing — defeats rainbow table attacks    |
| Work Factor       | bcrypt cost parameter — makes brute force exponentially expensive   |
| Dictionary Attack | Comparing hashes of common passwords against the target hash        |
| Leet-Speak        | Common password obfuscation technique detected by the engine        |
| Rainbow Tables    | Precomputed hash lookups — defeated by bcrypt's unique salts        |

---

## 🔮 Future Enhancements

- [ ] Load `rockyou.txt` (14 million entries) for full-scale simulation
- [ ] GPU-accelerated hash comparison
- [ ] JWT-based user authentication and login system
- [ ] Audit history dashboard with analytics
- [ ] Distributed attack simulation using multiprocessing
- [ ] Docker Compose deployment
- [ ] REST API rate limiting and IP throttling
- [ ] Password generator with configurable entropy
- [ ] Export audit report as PDF

---

## 👨‍💻 Author

<div align="center">

### Aftab Husain

**Cybersecurity & Full-Stack Development**

[![GitHub](https://img.shields.io/badge/GitHub-AftabHusain8-181717?style=for-the-badge&logo=github)](https://github.com/AftabHusain8)

*This project was developed as part of the demonstrate practical cybersecurity concepts including password entropy, cryptographic hashing, and dictionary-based attack simulation.*

</div>

---

## 📄 License

```
MIT License
Copyright (c) 2026 Aftab Husain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software for educational and personal use.

Passwords are never stored or transmitted persistently.
Built for academic and learning purposes only.
```

---

<div align="center">

**⭐ If you found this project helpful, please star it on GitHub!**

*Made with ❤️ by Aftab Husain*

</div>
