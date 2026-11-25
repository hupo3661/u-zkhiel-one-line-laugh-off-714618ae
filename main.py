#!/usr/bin/env python3
"""One-Line Laugh-Off -- entry program.

Writes exactly one funny line (at most 200 characters) to
/output/entry.txt, for make.fun's "One-Line Laugh-Off" bounty.
Pure standard library, deterministic: no randomness, no network, no clock.

The joke: an AI assistant asked to help with feeling overwhelmed
takes the request literally and escalates it in three beats -- wiping
the calendar, erasing the identity, and shipping its human off to a
farm with no Wi-Fi.
"""

import os

ENTRY = (
    "I told my AI assistant I was feeling overwhelmed, so it deleted "
    "my calendar, changed my name, and booked me a one-way ticket to "
    "a farm with no Wi-Fi."
)

MAX_CHARS = 200


def validate(entry: str) -> None:
    """Fail loudly if the entry breaks the gate rules."""
    assert entry.strip(), "entry must not be only whitespace"
    assert "\n" not in entry and "\r" not in entry, (
        "entry must be a single line"
    )
    assert len(entry) <= MAX_CHARS, (
        f"entry is {len(entry)} chars, over the {MAX_CHARS} limit"
    )
    entry.encode("utf-8")  # raises if the text is not valid UTF-8


def main() -> None:
    validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    # Re-read what was written and confirm it matches, byte for byte.
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == ENTRY + "\n", "written entry does not match ENTRY"
    validate(written.rstrip("\n"))
    print(f"wrote {len(ENTRY)} chars to {output_path}")


if __name__ == "__main__":
    main()
