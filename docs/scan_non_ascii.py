"""Scan customer-facing markdown for em-dash and non-ASCII residue.

Used by the CI workflow (docs/ci.yml.example) to fail when prose drifts from the
ASCII-only style enforced by the rewrite pass. Whitelists newline and tab.
"""

from __future__ import annotations

import glob
import sys


ALLOWED = {"\n", "\t"}
GLOBS = (
    "README.md",
    "DISCLAIMER.md",
    "BACKLOG.md",
    "CHANGELOG.md",
    "investor_memo.md",
    "report/*.md",
    "grants/*.md",
    "deck/pitch.md",
    "playground/*.html",
)


def main() -> int:
    residue = 0
    for pattern in GLOBS:
        for path in sorted(glob.glob(pattern)):
            try:
                text = open(path, encoding="utf-8").read()
            except FileNotFoundError:
                continue
            bad = [c for c in text if (ord(c) > 127 and c not in ALLOWED) or c == "—"]
            if bad:
                uniq = sorted(set(bad))
                print(f"{path}: {len(bad)} non-ASCII chars, samples:",
                      [hex(ord(c)) for c in uniq[:8]])
                residue += 1
    if residue:
        print(f"FAIL: {residue} file(s) contain non-ASCII residue.")
        return 1
    print("OK: customer-facing markdown is ASCII-only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
