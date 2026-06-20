# Roadmap

## Backlog

| Item | Impact | Effort | Priority | Status |
|------|--------|--------|----------|--------|
| Unit tests with mocked API responses | Medium | Medium | P1 | Pending |
| CI via GitHub Actions (lint + test on push) | Medium | Small | P1 | Pending |
| PyPI release automation | Medium | Small | P2 | Pending |
| `llm chat` conversation history via thread_id persistence | Low | Small | P2 | Done |

## Done

- [x] Initial plugin with adapter-based architecture (v0.1)
- [x] Direct API integration — removed adapter dependency (v0.2)
- [x] Native iaedu SSE parser (type: token / type: message)
- [x] Global config at `~/.config/iaedu/env`
- [x] `.env` auto-load from current directory
- [x] `IAEDU_API_KEY` env var fallback
- [x] `IAEDU_AGENT_ID` support (cleaner than full endpoint URL)
- [x] `make start` and `make check` targets
- [x] AES project doc structure (VISION, REQUIREMENTS, ROADMAP, CLAUDE.md)
- [x] Network error handling (timeout, connect, auth, not-found, stream)
- [x] Stable thread_id per conversation for chat history
- [x] PEP8 import ordering
- [x] LICENCE, CHANGELOG, CHECKLIST, QUALITY_GATES
