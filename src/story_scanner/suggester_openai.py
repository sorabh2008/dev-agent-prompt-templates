from __future__ import annotations
import os, math, json
from typing import List, Dict, Tuple
from openai import OpenAI
import tiktoken

SYSTEM_PROMPT = "You are a senior software engineer. Given a user story and related code files, propose surgical code changes with reasons. When helpful, suggest diff-like patches."

def _load_context(context_dir: str, max_files: int = 15, max_bytes_per_file: int = 50_000) -> List[Tuple[str, str]]:
    files = []
    for name in sorted(os.listdir(context_dir)):
        if name == "manifest.json":
            continue
        p = os.path.join(context_dir, name)
        if not os.path.isfile(p):
            continue
        with open(p, "rb") as f:
            data = f.read(max_bytes_per_file)
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            text = ""
        files.append((name, text))
    return files[:max_files]

def _count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def suggest_changes(story_path: str, context_dir: str, model: str = "gpt-4o-mini", max_tokens: int = 1500) -> str:
    with open(story_path, "r", encoding="utf-8") as f:
        story = f.read()

    files = _load_context(context_dir)
    # Construct a bounded prompt
    chunks = []
    budget = 10_000  # rough prompt token budget
    used = _count_tokens(story, model=model) + 500  # headroom
    for name, text in files:
        cost = _count_tokens(text, model=model) + 50
        if used + cost > budget:
            continue
        chunks.append(f"FILE: {name}\n````\n{text}\n````")
        used += cost

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""USER STORY:
```
{story}
```

CONTEXT FILES (subset):
{os.linesep.join(chunks)}

Please identify the minimal set of changes required across the files. If a new file is needed, propose it. Output diffs or code blocks with filenames, and list any risks or test updates needed.
"""}
    ]

    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=messages,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", required=True)
    ap.add_argument("--context", required=True)
    ap.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    ap.add_argument("--out", default="suggestions.md")
    args = ap.parse_args()

    out = suggest_changes(args.story, args.context, model=args.model)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote suggestions to {args.out}")

if __name__ == "__main__":
    main()
