# Quality Gates

## Gate 1 — Lint
`ruff check llm_iaedu.py` must exit 0.

## Gate 2 — Format
`ruff format --check llm_iaedu.py` must produce no diff.

## Gate 3 — Build
`python3 -m build` must succeed without warnings.

## Gate 4 — Functional
`llm -m iaedu` must connect to the API and return a response (requires valid config).

## Domain-Specific

### Plugin Integration
- Plugin must appear in `llm plugins` output
- Model must appear in `llm models list` output
- `llm keys set iaedu` must be a valid key storage mechanism

### Configuration
- `.env` files with any subset of `IAEDU_*` vars must not crash
- Missing required vars must produce a clear error message
- Config precedence (shell > ./.env > ~/.config/iaedu/env > ~/.iaedu.env) must be respected
