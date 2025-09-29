# todo_io.py
from pathlib import Path

def write_tasks(path, lines, encoding="utf-8"):
    f = open(path, "w")          # BUG1&2: no with, no encoding
    for line in lines:
        f.write(str(line) + "\n")
    f.close()

def read_tasks(path, encoding="utf-8"):
    p = Path(path)
    if not p.exists():           # BUG3: should raise FileNotFoundError
        return []
    with open(path, "r") as f:   # BUG4: no encoding
        return [line.rstrip("\n") for line in f.readlines()]
