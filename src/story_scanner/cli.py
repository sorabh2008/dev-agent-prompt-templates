from __future__ import annotations
import os, sys, json
import argparse
from typing import Dict, List
from .story_parser import parse_story
from .github_fetch import parse_repo_url, get_default_branch, get_tree, get_file
from .ranker import is_candidate, score_file, CODE_EXTS_DEFAULT
from .context_builder import write_context

def scan_repo(repo_url: str, branch: str | None, story_path: str, out_dir: str, top_n: int = 15,
              include_ext: List[str] | None = None) -> str:
    with open(story_path, "r", encoding="utf-8") as f:
        story_md = f.read()
    story = parse_story(story_md)
    owner, repo = parse_repo_url(repo_url)
    if not branch:
        branch = get_default_branch(owner, repo)

    # Fetch file list
    tree = get_tree(owner, repo, branch=branch, recursive=True)

    # Filter candidates & fetch content to score
    include_exts = set(include_ext) if include_ext else CODE_EXTS_DEFAULT
    scores = []
    files: Dict[str, bytes] = {}
    for node in tree:
        if node.get("type") != "blob":
            continue
        path = node.get("path")
        if not is_candidate(path, include_exts):
            continue
        try:
            content = get_file(owner, repo, path, ref=branch)
        except Exception:
            continue
        files[path] = content
        fs = score_file(path, content, story.keywords, story.primary_modules)
        scores.append(fs)

    return write_context(out_dir, files, scores, top_n=top_n)

def main():
    ap = argparse.ArgumentParser(prog="repo-scanner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_scan = sub.add_parser("scan", help="Scan a repo and build a context bundle")
    ap_scan.add_argument("--repo", required=True, help="GitHub repository URL")
    ap_scan.add_argument("--branch", default=None, help="Branch (default: repo default)")
    ap_scan.add_argument("--story", required=True, help="Path to the user story markdown")
    ap_scan.add_argument("--out", default="context", help="Output context directory")
    ap_scan.add_argument("--top", type=int, default=15, help="Top-N files to include")
    ap_scan.add_argument("--include-ext", nargs="*", default=None, help="Extensions to include (e.g., .ts .tsx .js .json .md .yml .yaml)")

    ap_suggest = sub.add_parser("suggest", help="Call OpenAI to suggest changes from story + context")
    ap_suggest.add_argument("--story", required=True)
    ap_suggest.add_argument("--context", required=True)
    ap_suggest.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    ap_suggest.add_argument("--out", default="suggestions.md")

    args = ap.parse_args()

    if args.cmd == "scan":
        out_dir = scan_repo(args.repo, args.branch, args.story, args.out, top_n=args.top, include_ext=args.include_ext)
        print(f"Context written to: {out_dir}")
        print(f"Manifest: {os.path.join(out_dir, 'manifest.json')}")
    elif args.cmd == "suggest":
        from .suggester_openai import suggest_changes
        out = suggest_changes(args.story, args.context, model=args.model)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote suggestions to {args.out}")
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
