from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Optional

CODE_EXTS_DEFAULT = {".ts", ".tsx", ".js", ".jsx", ".json", ".yml", ".yaml", ".md", ".tsc", ".mjs", ".cjs"}

@dataclass
class FileScore:
    path: str
    score: float
    reasons: List[str]

def tokenize(s: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_\-/]+", s.lower())

def score_file(path: str, content: Optional[bytes], keywords: List[str], primary_modules: List[str]) -> FileScore:
    score = 0.0
    reasons: List[str] = []
    p_lower = path.lower()
    toks = tokenize(p_lower)
    kw = [k.lower() for k in keywords]
    pm = [m.lower() for m in primary_modules]

    # 1) Path matches primary modules
    for m in pm:
        m_clean = m.replace("`", "").lower()
        if m_clean and m_clean in p_lower:
            score += 5.0
            reasons.append(f"path matches primary module '{m_clean}' (+5)")

    # 2) Filename contains keyword(s)
    for k in kw:
        if k and k in p_lower:
            score += 2.0
            reasons.append(f"filename contains keyword '{k}' (+2)")

    # 3) Content keyword frequency
    if content:
        try:
            text = content.decode("utf-8", errors="ignore").lower()
        except Exception:
            text = ""
        hits = 0
        for k in kw:
            if not k:
                continue
            n = text.count(k)
            if n:
                plus = min(4.0, 0.5 * n)
                score += plus
                hits += n
        if hits:
            reasons.append(f"content contains {hits} keyword hits (+{min(4.0, 0.5*hits):.1f})")

        # 4) Bonus if appears to be API route or model
        if re.search(r"get\s*pet|petid|favorite|isfavorite|endpoint|route|api", text):
            score += 1.5
            reasons.append("content indicates API/model terms (+1.5)")

    return FileScore(path=path, score=score, reasons=reasons)

def is_candidate(path: str, include_exts: Optional[Iterable[str]] = None, exclude_dirs: Optional[Iterable[str]] = None) -> bool:
    include_exts = set(include_exts) if include_exts else CODE_EXTS_DEFAULT
    exclude_dirs = set(exclude_dirs) if exclude_dirs else {".git", "node_modules", "dist", "build", ".next"}
    _, ext = os.path.splitext(path.lower())
    if ext and ext not in include_exts:
        return False
    parts = path.split("/")
    if any(part in exclude_dirs for part in parts):
        return False
    return True
