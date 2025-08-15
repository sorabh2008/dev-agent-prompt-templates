from __future__ import annotations
import os, json
from typing import List, Dict
from dataclasses import asdict
from .ranker import FileScore

def write_context(out_dir: str, files: Dict[str, bytes], scores: List[FileScore], top_n: int = 15) -> str:
    os.makedirs(out_dir, exist_ok=True)
    picked = sorted(scores, key=lambda s: s.score, reverse=True)[:top_n]

    manifest = {
        "selected": [
            {"path": s.path, "score": s.score, "reasons": s.reasons}
            for s in picked
        ],
        "discarded": [
            {"path": s.path, "score": s.score}
            for s in sorted(scores, key=lambda s: s.score, reverse=True)[top_n:]
        ]
    }

    for s in picked:
        path = s.path
        data = files.get(path, b"")
        out_path = os.path.join(out_dir, path.replace("/", "__"))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return os.path.abspath(out_dir)
