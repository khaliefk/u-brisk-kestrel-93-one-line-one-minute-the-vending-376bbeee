"""Vending machine pickup line entry.

Writes one pickup line, spoken by a vending machine to a passing
human, to /output/entry.txt. The line stays inside the gate: 1 to 200
UTF-8 characters, one line, not only whitespace.
"""

import os

ENTRY = "You're the exact change I've been waiting for, so press B7 and I'll drop something sweet for you."

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def validate_entry(text):
    """Check the entry against the gate before writing it."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1 to 200 characters, got %d" % len(text))
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    for char in text:
        if ord(char) < 32 and char not in ("\t",):
            raise ValueError("entry must not contain control characters")
    return text


def main():
    text = validate_entry(ENTRY)
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    assert written == text, "read-back mismatch"
    print("Wrote %d chars to %s" % (len(text), OUTPUT_PATH))
    print(text)


if __name__ == "__main__":
    main()
