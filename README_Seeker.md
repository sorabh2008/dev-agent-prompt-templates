# repo-scanner

A Python CLI that scans a GitHub repository using a given user story, fetches the most relevant files,
and builds a **context bundle** for an LLM. Optionally, it can call OpenAI to suggest code changes.

## Features
- Parse structured hints from a story (keywords, primary modules, acceptance criteria).
- Crawl a GitHub repo (without `git`) using the GitHub REST API (works with public repos; supports token for private / higher rate limits).
- Score & rank files using multiple signals (path matches, keyword hits in filename/content, filetype).
- Export a `context/` folder with selected files and a `manifest.json` explaining *why* each file was chosen.
- Optional: call OpenAI to generate suggested changes given the story + context files.

## Quickstart

```bash
# 1) Create and activate a venv (recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run a full scan and build a context bundle
python -m story_scanner.cli scan   --repo https://github.com/ln-nicolas/petstore-client-ts   --branch main   --story stories/NEW_FEATURE.md   --out context

# 4) (Optional) Ask OpenAI for suggested changes based on the context
export OPENAI_API_KEY=YOUR_KEY
python -m story_scanner.cli suggest   --story stories/NEW_FEATURE.md   --context context   --model gpt-4o-mini   --out suggestions.md
```

> Tip: Set `GITHUB_TOKEN` for higher GitHub API rate limits: `export GITHUB_TOKEN=ghp_...`

## How it works

1. **Parse Story** → Extract keywords, primary modules, acceptance criteria.
2. **Crawl Repo** → List files via GitHub API; pull candidate files by extension.
3. **Score & Rank** → Use heuristics:
   - Filename/path contains story keywords
   - File content keyword frequency
   - File matches "Primary Modules" glob patterns
   - File type is likely to be relevant (e.g., `.ts`, `.tsx`, `.js`, `.md`, `.yaml`, `.yml`, `.json`)
4. **Bundle Context** → Copy top-N files to `/context` and write `manifest.json` with scores and rationales.
5. **(Optional) Suggest** → Calls OpenAI with the story + context snippets to propose diffs or change plans.

## Configuration

- **Branch** defaults to `main` if not specified.
- **File Types**: Defaults focus on app and API client stacks; override with `--include-ext` / `--exclude-ext`.
- **OpenAI**: Provide `OPENAI_API_KEY`. Select model via `--model` or `OPENAI_MODEL`. Chunking handles long contexts.

## Notes
- This tool reads repos via HTTP; it does **not** modify your repo.
- For private repos, you must provide a `GITHUB_TOKEN` with read access.

## License
MIT
