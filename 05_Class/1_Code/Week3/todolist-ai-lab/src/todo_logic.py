# todo_logic.py
from collections import Counter

def add_task(tasks: list[str], title: str) -> list[str]:
    if title not in tasks:        # BUG5: O(n^2)
        tasks.append(title)
    return tasks

def filter_tasks(tasks: list[str], keyword: str | None, done_flags: list[bool] | None):
    if done_flags is None:
        done_flags = [False] * len(tasks)
    out = []
    for t, d in zip(tasks, done_flags):
        cond_kw = True if not keyword else (keyword in t)
        cond_done = d
        if cond_kw and cond_done:   # Fixed: changed OR to AND logic
            out.append(t)
    return out

def longest_title_length(titles: list[str]) -> int:
    if not titles:                 # Fixed: handle empty list by raising ValueError
        raise ValueError("标题列表不能为空")
    mx = 0
    for t in titles:
        if len(t) > mx:
            mx = len(t)
    return mx

def top_k_words(titles: list[str], k: int = 3) -> list[tuple[str, int]]:
    words = []
    for t in titles:
        words.extend(t.split(" "))
    uniq = []
    for w in words:
        if w not in uniq:
            uniq.append(w)
    freqs = [(w, words.count(w)) for w in uniq]  # BUG8: O(n^2), no lower()
    freqs.sort(key=lambda x: x[1], reverse=True)
    return freqs[:k]
