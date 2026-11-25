#!/usr/bin/env python3
"""One-Line Laugh-Off -- entry program.

Writes exactly one funny line (at most 200 characters) to
``/output/entry.txt``, for make.fun's "One-Line Laugh-Off" bounty.
Pure standard library and fully deterministic: no randomness, no
network access, no clock, no input files. Running it twice produces
byte-identical output.

The joke: an AI assistant asked to help with feeling overwhelmed
takes the request literally and escalates it in three beats --
wiping the calendar, erasing the identity, and shipping its human
off to a farm with no Wi-Fi. Each beat is worse than the last, and
the last one removes the very thing (connectivity) the assistant
runs on.

Layout of this program
----------------------
* :data:`ENTRY` -- the single line being entered, kept verbatim.
* :func:`validate_entry` -- gate checks, one small check per helper,
  so a failing rule names itself in the error message.
* :func:`resolve_output_path` -- where the file goes, honouring the
  ``MAKEFUN_OUTPUT_DIR`` override used by the harness.
* :func:`write_entry` / :func:`verify_written` -- write the file,
  then read it back and prove it matches, byte for byte.
* :func:`main` -- glue: validate, write, verify, report.
"""

import os
import sys

ENTRY = (
    "I told my AI assistant I was feeling overwhelmed, so it deleted "
    "my calendar, changed my name, and booked me a one-way ticket to "
    "a farm with no Wi-Fi."
)

MAX_CHARS = 200
MIN_CHARS = 1


def check_not_empty(entry: str) -> None:
    """Reject blank or whitespace-only entries."""
    if not entry.strip():
        raise ValueError("entry must not be empty or only whitespace")


def check_single_line(entry: str) -> None:
    """Reject anything that is not exactly one line of text."""
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line (no line breaks)")


def check_length(entry: str) -> None:
    """Enforce the competition's character gate, 1-200 chars."""
    if len(entry) < MIN_CHARS:
        raise ValueError(f"entry is empty, need at least {MIN_CHARS} char")
    if len(entry) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(entry)} chars, over the {MAX_CHARS} limit"
        )


def check_text_safe(entry: str) -> None:
    """Reject control characters and confirm the text is valid UTF-8."""
    entry.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    bad = [c for c in entry if ord(c) < 0x20 and c not in ("\t",)]
    if bad:
        raise ValueError(
            "entry contains control characters: "
            + ", ".join(f"U+{ord(c):04X}" for c in bad)
        )


def check_no_edge_whitespace(entry: str) -> None:
    """Reject leading/trailing spaces that would be invisible in output."""
    if entry != entry.strip():
        raise ValueError("entry must not start or end with whitespace")


def check_word_count(entry: str) -> None:
    """Sanity check: a one-liner needs at least two words to land a joke."""
    words = entry.split()
    if len(words) < 2:
        raise ValueError("entry needs at least two words to be a joke")


def check_three_beats(entry: str) -> None:
    """Sanity check: this joke's structure is three escalating beats.

    The beats are separated by commas and the word "and" before the
    final one; if the shape ever collapses to a single clause, the
    escalation -- and the joke -- is gone.
    """
    clauses = entry.split(",")
    if len(clauses) < 3:
        raise ValueError("entry should keep its three-beat escalation")


def validate_entry(entry: str) -> None:
    """Run every gate check; raise ValueError naming the first failure."""
    check_not_empty(entry)
    check_single_line(entry)
    check_no_edge_whitespace(entry)
    check_length(entry)
    check_text_safe(entry)
    check_word_count(entry)
    check_three_beats(entry)


def resolve_output_path() -> str:
    """Return the path of the file to write, creating its directory."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, "entry.txt")


def write_entry(entry: str, output_path: str) -> None:
    """Write the entry plus one trailing newline, as UTF-8 text."""
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(entry + "\n")


def verify_written(entry: str, output_path: str) -> None:
    """Read the file back and prove it is exactly what we intended."""
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != entry + "\n":
        raise ValueError("written entry does not match ENTRY")
    validate_entry(written.rstrip("\n"))


def main() -> int:
    """Validate, write, verify, and report. Returns a process exit code."""
    validate_entry(ENTRY)
    output_path = resolve_output_path()
    write_entry(ENTRY, output_path)
    verify_written(ENTRY, output_path)
    words = len(ENTRY.split())
    print(
        f"wrote {len(ENTRY)} chars ({words} words) to {output_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
