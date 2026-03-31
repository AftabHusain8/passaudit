"""
╔══════════════════════════════════════════════════════════════╗
║     PassAudit — Password Strength Auditor & Attack Tool     ║
║     Backend : FastAPI  |  Author : Aftab Husain             ║
║     Academic Project   |  CDAC                              ║
╚══════════════════════════════════════════════════════════════╝

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from modules.strength import analyze_strength
from modules.hasher   import hash_password
from modules.attacker import dictionary_attack
from typing import Optional
import time

# ── App Bootstrap ────────────────────────────────────────────────────────────

app = FastAPI(
    title="PassAudit API",
    description=(
        "Password Strength Auditor & Dictionary Attack Simulation\n\n"
        "**Author:** Aftab Husain | **Project:** CDAC v2.0"
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict to your domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response Models ─────────────────────────────────────────────────

class PasswordRequest(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Password must not be empty.")
        if len(v) > 256:
            raise ValueError("Password exceeds maximum length of 256 characters.")
        return v


class AnalysisResponse(BaseModel):
    # Project metadata
    author: str
    project: str

    # Stage 1 — Strength
    score: int
    level: str
    entropy_bits: float
    checks: dict
    feedback: list[str]
    hint: str

    # Stage 2 — Hashing
    hash_sha256: str
    hash_sha512: str
    hash_bcrypt: str

    # Stage 3 — Dictionary Attack
    cracked: bool
    cracked_word: Optional[str]
    wordlist_size: int
    attack_duration_ms: float


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "service": "PassAudit API",
        "version": "2.0.0",
        "author": "Aftab Husain",
        "project": "CDAC Password Security Initiative",
        "status": "online",
    }


@app.post("/analyze", response_model=AnalysisResponse, tags=["Audit"])
def analyze(req: PasswordRequest):
    password = req.password

    # ── Stage 1: Strength Analysis
    strength = analyze_strength(password)

    # ── Stage 2: Cryptographic Hashing
    hashes = hash_password(password)

    # ── Stage 3: Dictionary Attack Simulation
    t0 = time.perf_counter()
    attack = dictionary_attack(password, hashes["sha256"])
    attack_ms = round((time.perf_counter() - t0) * 1000, 3)

    # If cracked by dictionary, downgrade to Very Weak
    if attack["cracked"]:
        strength["score"] = min(strength["score"], 12)
        strength["level"] = "Very Weak"
        strength["feedback"].insert(
            0,
            "⛔ CRITICAL: Password found in the attack dictionary — change it immediately!"
        )

    return AnalysisResponse(
        author             = "Aftab Husain",
        project            = "PassAudit v2.0 — CDAC",
        score              = strength["score"],
        level              = strength["level"],
        entropy_bits       = strength["entropy_bits"],
        checks             = strength["checks"],
        feedback           = strength["feedback"],
        hint               = strength["hint"],
        hash_sha256        = hashes["sha256"],
        hash_sha512        = hashes["sha512"],
        hash_bcrypt        = hashes["bcrypt"],
        cracked            = attack["cracked"],
        cracked_word       = attack["word"],
        wordlist_size      = attack["wordlist_size"],
        attack_duration_ms = attack_ms,
    )


@app.get("/wordlist/count", tags=["Info"])
def wordlist_count():
    from modules.attacker import WORDLIST
    return {"total_words": len(WORDLIST), "author": "Aftab Husain"}
