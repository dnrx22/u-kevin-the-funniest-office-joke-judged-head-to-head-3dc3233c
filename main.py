"""Write one office joke to entry.txt.

The joke is a single line with a setup and a punchline: a meeting held to
decide whether the team has too many meetings ends by scheduling a
follow-up meeting. The program is deterministic: it always writes the
same bytes, uses only the standard library, and performs no network I/O.

The output directory comes from MAKEFUN_OUTPUT_DIR (default /output).
The grader runs the program with /bot read-only, so nothing is written
next to this script.
"""

import hashlib
import os
import sys

JOKE = (
    "Our team held a meeting to decide whether we have too many meetings, "
    "and it ended with scheduling a follow-up meeting to discuss it."
)

MAX_CHARS = 200


def validate(line: str) -> None:
    """Check the entry line against the competition's output rules."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    if line != line.rstrip():
        raise ValueError("entry must not end with whitespace")
    if line != line.lstrip():
        raise ValueError("entry must not start with whitespace")
    if line[-1] not in ".!?":
        raise ValueError("entry must end with proper punctuation")


def main() -> int:
    validate(JOKE)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    data = (JOKE + "\n").encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    # Read back from disk and verify what actually landed there, so a
    # truncated or altered write is caught instead of silently trusted.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("written file does not match the expected bytes")
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {path}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
