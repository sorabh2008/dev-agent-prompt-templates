# Dev Agent MVP: Design Summary and Plan of Action

## 🌟 Objective

Build a Python-based Dev Agent that:

* Accepts a prompt: *"Read the User Story <JIRA Link>. Analyse the Acceptance Criteria. Using <Git Repo Link> as reference, suggest code changes including dev changes and unit test additions."*
* Clones the given GitHub repo.
* Extracts and analyzes the acceptance criteria from the JIRA link.
* Selects relevant files from the repo based on those criteria.
* Passes those files and the story context to OpenAI (GPT-4) to generate suggestions for:

  * Development changes
  * Unit test changes

## ✅ Decision Summary

### 1. GitHub Repo Integration

* Use `GitPython` to clone and inspect the repo.
* Avoid passing the entire repo due to token limits.

### 2. JIRA Story Analysis

* Initial approach: fetch the JIRA page and parse it with `BeautifulSoup`.
* Fallback: manually pass acceptance criteria text for MVP.

### 3. Code File Selection

**Key decision:** Avoid embeddings for MVP due to complexity.

* Use keyword matching from acceptance criteria.
* Restrict to supported file types (`.py`, `.js`, `.ts`, `.java`).
* Filter out binary/large files and known excluded folders.

### 4. Prompting Strategy for OpenAI

* Combine story title + acceptance criteria + code file content.
* Keep system prompt focused: *"You are a senior software engineer..."*

### 5. Output Format

* Clearly separated sections for each file:

  ```
  # File: user_service.py
  + def login_with_otp(...):
  ...
  ```

## 🔧 Detailed Plan of Action

### Step 1: Setup and Dependencies

Install required packages:

```bash
pip install openai gitpython beautifulsoup4 requests python-dotenv
```

### Step 2: Fetch GitHub Repo

```python
from git import Repo
import tempfile

def clone_repo(github_url):
    temp_dir = tempfile.mkdtemp()
    Repo.clone_from(github_url, temp_dir)
    return temp_dir
```

### Step 3: Extract Acceptance Criteria (Manual for MVP)

For MVP, acceptance criteria can be pasted as text input. Later we can enhance this using requests + BeautifulSoup if JIRA allows scraping.

### Step 4: Extract Keywords

```python
import re

def extract_keywords(text):
    return {kw.lower() for kw in re.findall(r'\b\w{4,}\b', text)}
```

### Step 5: File Filtering by Keyword

```python
import os

EXCLUDED_DIRS = {'.git', 'node_modules', '__pycache__'}
SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java'}
MAX_FILE_SIZE = 50 * 1024

def is_supported_file(file_path):
    return (
        os.path.splitext(file_path)[1] in SUPPORTED_EXTENSIONS
        and os.path.getsize(file_path) <= MAX_FILE_SIZE
    )

def get_relevant_files(repo_path, acceptance_criteria):
    keywords = extract_keywords(acceptance_criteria)
    matching_files = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            full_path = os.path.join(root, file)
            if is_supported_file(full_path):
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    if any(kw in content for kw in keywords):
                        matching_files.append(full_path)
    return matching_files
```

### Step 6: Feed Context to GPT

```python
import openai

def suggest_code_changes(user_story, criteria, code_reference, model="gpt-4"):
    messages = [
        {"role": "system", "content": "You're a senior software developer. Suggest dev and unit test changes based on the user story and code context. Output only code blocks and filenames."},
        {"role": "user", "content": f"User Story: {user_story}\n\nAcceptance Criteria:\n{criteria}\n\nCode Context:\n{code_reference}"}
    ]
    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0.2)
    return response.choices[0].message['content']
```

### Step 7: Main Agent Workflow

```python
def dev_agent(prompt, jira_url, github_url):
    # Step 1: Input acceptance criteria manually (for MVP)
    user_story = "Sample JIRA Story Title"
    acceptance_criteria = input("Paste acceptance criteria:\n")

    # Step 2: Clone repo
    repo_path = clone_repo(github_url)

    # Step 3: Get relevant files
    files = get_relevant_files(repo_path, acceptance_criteria)
    code_context = ""
    for file in files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            code_context += f"\n\n# File: {file}\n" + f.read()

    # Step 4: Get suggestions
    suggestions = suggest_code_changes(user_story, acceptance_criteria, code_context)
    print("\n\ud83c\udf1f Suggested Code Changes:\n")
    print(suggestions)
```

---

## 🚀 Next Steps Post-MVP

* ✨ Add semantic search with embeddings
* 📅 JIRA API integration for structured story fetch
* 🌐 GitHub API integration for commit diffs, PR automation
* 🎓 Fine-tuned prompt strategy with memory for multi-step reasoning
* 🚀 Run linters/tests on generated changes

---

This plan provides a lean but effective MVP setup that can be extended into a fully-featured Dev Agent after initial testing and validation.
