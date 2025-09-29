# todo_logic.py
from collections import Counter

def add_task(tasks: list[str], title: str) -> list[str]:
    # Optimized: More efficient deduplication while preserving order
    # Create a new list with the title added, then remove duplicates
    temp_list = tasks + [title]
    # Use dict.fromkeys() to remove duplicates while preserving order (Python 3.7+)
    return list(dict.fromkeys(temp_list))

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
    # Optimized: Use built-in max() function with len as key function
    # This is more efficient and readable than manual loop
    return max(len(title) for title in titles)

def top_k_words(titles: list[str], k: int = 3) -> list[tuple[str, int]]:
    # Optimized: Use Counter for efficient counting and handle case normalization
    words = []
    for t in titles:
        # Normalize to lowercase for case-insensitive counting
        words.extend(word.lower() for word in t.split(" ") if word.strip())
    
    # Use Counter for efficient O(n) counting instead of O(n²) with list.count()
    word_counts = Counter(words)
    
    # Get the most common k words
    return word_counts.most_common(k)
