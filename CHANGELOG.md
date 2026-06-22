# Changelog

## 0.5 (2026-06-22)

### Changed
- Key precedence: env var (from `_load_dotenv`) takes priority over `llm keys` — `llm-iaedu configure` is now the single required config step
- Error messages now point to `llm iaedu-configure` instead of `llm keys set iaedu`

### Added
- `configure()` output now includes `llm models default iaedu` tip for single-command usage

## 0.4 (2026-06-22)

### Added
- `llm iaedu-configure` subcommand via `register_commands` hook — works after pipx inject (no separate pipx install needed)
- `OSError` catch in error handling for broader connection error coverage

### Changed
- `llm-iaedu start` now prints usage instead of "unknown command"

## 0.3 (2026-06-22)

### Added
- `llm-iaedu configure` CLI command — interactive setup without Makefile
- `[project.scripts]` entry point: `llm-iaedu = "llm_iaedu:main"`
- `python -m llm_iaedu configure` support for pipx-inject installs
- Ubuntu/Debian PEP 668 installation guide in README

### Fixed
- `make check` / `make doctor` variable expansion bug (PID+var instead of value)
- `make check` incorrectly referenced `IAEDU_AGENT_ID` instead of `IAEDU_ENDPOINT`
- `ubuntu-setup` Makefile target tried `--user` which doesn't bypass PEP 668

## 0.2 (2026-06-20)

### Changed
- Rewrote plugin to call iaedu.pt API directly — eliminated Node.js adapter dependency
- Rewrote SSE parser to handle native iaedu format (`type: token`, `type: message`)
- Fixed duplicated output when both token events and message event yield content
- Config auto-loads from `./.env` or `~/.config/iaedu/env` — no `python-dotenv` needed
- Added `IAEDU_AGENT_ID` env var (cleaner than full `IAEDU_ENDPOINT` URL)
- Added `IAEDU_API_KEY` env var as fallback for `llm keys set iaedu`
- Added stable thread ID per conversation for chat history support
- Added network error handling with descriptive messages
- Improved import ordering to PEP8
- Changed bare `Exception` raises to `ValueError` and `RuntimeError`

### Added
- `make start`, `make check`, `make lint`, `make doctor`, `make metrics` targets
- `docs/VISION.md`, `docs/REQUIREMENTS.md`, `docs/ROADMAP.md`
- `CLAUDE.md` operational contract
- `.env.example` template
- `.gitignore` (prevents committing secrets)
- `LICENSE` (Apache 2.0)

### Removed
- `package-lock.json` (empty, Node.js adapter no longer needed)

## 0.1 (2026-06-19)

### Added
- Initial plugin with adapter-based architecture
- `llm -m iaedu` model registration
- Multipart/form-data forwarding to local iaedu-adapter process
