#!/usr/bin/env python3
"""verify_hmac_v1.py  –  Provably-fair commitment verification (HMAC-SHA256).

Usage example:
    python scripts/verify_hmac_v1.py --seed e3c0... --hash f12a... --json game.json

The script validates that:
1. The JSON file contains a pre-serialized payload string (exactly as used by the server).
2. HMAC-SHA256(serverSeed, payload) equals the commitment hash shown at game start.

Important:
- This tool does NOT attempt to re-simulate game outcomes.
- It only verifies the published commitment (hash) against the revealed serverSeed.

Exit codes:
    0 – commitment is valid
    1 – commitment is invalid (mismatch)
"""

from __future__ import annotations

import argparse
import json
import hmac
import hashlib
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Crypto
# ---------------------------------------------------------------------------

def compute_hmac_sha256_hex(seed: str, msg: str) -> str:
    """Compute commitment as lowercase hex HMAC-SHA256.

    Args:
        seed: serverSeed (revealed after the game ends)
        msg : pre-serialized payload string (must match server input byte-for-byte)

    Returns:
        64-char hex digest (lowercase).
    """
    return hmac.new(seed.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).hexdigest()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_payload(path: Path) -> str:
    """Load game JSON and extract 'payload' field.

    Expected format:
        {
          "payload": "mines|[0,0,...,-1]|...",
          ...
        }

    Notes:
    - The payload is assumed to be already serialized by the exporter.
    - Any whitespace / casing / separators inside the payload MUST be preserved.
    """
    try:
        game = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        sys.exit(f"Failed to read JSON file '{path}': {exc}")

    payload = game.get("payload")
    if payload is None:
        sys.exit('JSON file must contain "payload" field (string)')
    if not isinstance(payload, str):
        sys.exit('JSON "payload" field must be a string')

    return payload


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify provably-fair commitment (payload is pre-serialized)"
    )
    parser.add_argument("--seed", required=True, help="serverSeed revealed after game ends")
    parser.add_argument("--hash", required=True, help="hash/commitment shown at game start")
    parser.add_argument("--json", required=True, type=Path, help="path to game JSON file")
    args = parser.parse_args()

    # 1. Read payload from JSON
    payload = load_payload(args.json)

    # 2. Compute expected commitment
    expected = compute_hmac_sha256_hex(args.seed, payload)

    # 3. Compare with provided commitment (case-insensitive)
    ok = expected.lower() == args.hash.lower()

    # 4. Output verification details
    print("=== Provably Fair Verification ===")
    print("Message :", payload)
    print("Computed:", expected)
    print("Provided:", args.hash)
    print("Result  :", "VALID ✅" if ok else "INVALID ❌")

    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()