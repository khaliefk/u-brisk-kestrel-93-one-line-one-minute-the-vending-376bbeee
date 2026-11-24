# One line from a vending machine to someone walking past.
# The machine keeps it short: a single line, 1-200 characters,
# no blank padding, no hidden line breaks. That is the whole job.

from os import environ
from pathlib import Path

LINE = "You're the exact change I've been waiting for, so press B7 and I'll drop something sweet for you."
DEFAULT_FOLDER = "/output"
FILENAME = "entry.txt"


def target_file():
    folder = environ.get("OUTPUT_DIR")
    if folder:
        return Path(folder) / FILENAME
    explicit = environ.get("OUTPUT_PATH")
    if explicit:
        return Path(explicit)
    return Path(DEFAULT_FOLDER) / FILENAME


def passes_gate(candidate):
    if type(candidate) is not str:
        raise TypeError("pickup line has to be text")
    size = len(candidate)
    if size < 1 or size > 200:
        raise ValueError("pickup line has to be 1-200 characters long, found " + str(size))
    if not candidate.strip():
        raise ValueError("pickup line cannot be blank")
    if candidate.strip() != candidate:
        raise ValueError("pickup line cannot start or end with a space")
    if len(candidate.splitlines()) != 1:
        raise ValueError("pickup line has to fit on one line")
    bad = [ch for ch in candidate if ord(ch) < 32 or ord(ch) == 127]
    if bad:
        raise ValueError("pickup line cannot hold control or delete characters")
    return candidate


def save(candidate, where):
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(candidate, encoding="utf-8")
    back = where.read_text(encoding="utf-8")
    if back != candidate:
        raise RuntimeError("what came back from disk does not match the line")
    return where


def run():
    checked = passes_gate(LINE)
    dest = target_file()
    saved = save(checked, dest)
    print("saved " + str(len(checked)) + " characters to " + str(saved))
    print(checked)


if __name__ == "__main__":
    run()
