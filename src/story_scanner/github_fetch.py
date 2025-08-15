from __future__ import annotations
import os
import base64
import requests
from typing import Dict, List, Optional, Tuple

GITHUB_API = "https://api.github.com"

def _headers():
    token = os.getenv("GITHUB_TOKEN")
    hdrs = {"Accept": "application/vnd.github+json", "User-Agent": "repo-scanner"}
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    return hdrs

def parse_repo_url(repo_url: str) -> Tuple[str, str]:
    # Accept forms like https://github.com/owner/repo(.git)?
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid repo URL")
    owner = parts[-2]
    repo = parts[-1].removesuffix(".git")
    return owner, repo

def get_default_branch(owner: str, repo: str) -> str:
    r = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}", headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json().get("default_branch", "main")

def get_tree(owner: str, repo: str, branch: str, recursive: bool = True) -> List[Dict]:
    params = {"recursive": "1"} if recursive else {}
    r = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}", headers=_headers(), params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "tree" not in data:
        raise RuntimeError(f"Unexpected tree response: {data}")
    return data["tree"]

def get_file(owner: str, repo: str, path: str, ref: Optional[str] = None) -> bytes:
    # Use the contents API for raw content
    params = {"ref": ref} if ref else {}
    r = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}", headers=_headers(), params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list):
        raise IsADirectoryError(path)
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"])
    # Fallback: fetch download_url
    dl = data.get("download_url")
    if not dl:
        raise RuntimeError(f"No download_url for {path}")
    raw = requests.get(dl, headers=_headers(), timeout=60)
    raw.raise_for_status()
    return raw.content
