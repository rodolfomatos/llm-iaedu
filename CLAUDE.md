# llm-iaedu — Operational Contract

## Intent
Single-file Python plugin for `llm` CLI that calls iaedu.pt API.
Users do `llm -m iaedu "question"` from any directory.

## Non-Goals
- No multi-file architecture (single plugin file)
- No adapter server, no Docker, no Node.js
- No local model inference

## Critical Files
- `llm_iaedu.py` — only source file; plugin entry point
- `pyproject.toml` — package metadata
- `~/.config/iaedu/env` — global user config

## Never-Do
- Do NOT add Node.js/Go/Rust dependencies
- Do NOT require a running server/daemon
- Do NOT add `python-dotenv` — keep it zero-dependency beyond llm+httpx
- Do NOT refactor into multiple files without explicit request
- Do NOT add emojis to source code

## Testing
```bash
# Manual test
llm -m iaedu "question"

# Lint
ruff check llm_iaedu.py

# Build check
python3 -m build
```

## Config Precedence
1. `os.environ` (explicit export or `source .env`)
2. `./.env` (local)
3. `~/.config/iaedu/env` (global)
4. `~/.iaedu.env` (legacy)
