#!/usr/bin/env python3
"""The Best Advice I Ever Got — make.fun entry (program/v1).

Writes exactly one sentence (at most 200 characters) about the best advice
the writer ever received to /output/entry.txt, with no trailing newline.
A 600-byte UTF-8 ceiling guards the entry, and the write is verified by
reading the file back and comparing it to the validated text.

The sentence: one concrete scene (twelve years old, crying over a lost race),
one reversal (losing does not matter — finishing does), one landing line
(still hearing it every time I want to quit).

Standard library only. Test hook: setting ENTRY_OVERRIDE runs validation on
that text instead of ENTRY (used by the negative tests; the grader never
sets it). ENTRY_OUT overrides the output path (default /output/entry.txt).
"""
import os
import sys

ENTRY = (
    "At twelve, crying over a lost race, my father said, "
    "'You don't have to win \u2014 you have to finish,' "
    "and I still hear him every time I want to quit."
)

MAX_CHARS = 200
MAX_BYTES = 600


def validate(text):
    """Raise ValueError unless text is a valid single-sentence entry."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError("entry exceeds 200 characters")
    if len(text.encode("utf-8", "surrogatepass")) > MAX_BYTES:
        raise ValueError("entry exceeds 600 bytes when UTF-8 encoded")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    for ch in text:
        code = ord(ch)
        if code < 0x20 and ch != "\t":
            raise ValueError("entry contains a control character")
        if 0xD800 <= code <= 0xDFFF:
            raise ValueError("entry contains a lone surrogate")
    body = text[:-1] if text.endswith(".") else text
    if any(c in body for c in ".!?"):
        raise ValueError("entry must be a single sentence")
    if not text.endswith("."):
        raise ValueError("entry must end with a full stop")
    return True


def main():
    text = os.environ.get("ENTRY_OVERRIDE", ENTRY)
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    out = os.environ.get("ENTRY_OUT", "/output/entry.txt")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(out, "r", encoding="utf-8", newline="") as f:
        if f.read() != text:
            print("write round-trip mismatch", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
