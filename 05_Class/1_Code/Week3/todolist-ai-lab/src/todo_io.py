# todo_io.py
from pathlib import Path

def write_tasks(path, lines, encoding="utf-8"):
    with open(path, "w", encoding=encoding) as f:    # Fixed: added with statement and encoding
        for line in lines:
            f.write(str(line) + "\n")

def read_tasks(path, encoding="utf-8"):
    p = Path(path)
    if not p.exists():           # Fixed: raise FileNotFoundError instead of returning []
        raise FileNotFoundError(f"文件 {path} 不存在")
    with open(path, "r", encoding=encoding) as f:   # Fixed: added encoding parameter
        return [line.rstrip("\n") for line in f.readlines()]
