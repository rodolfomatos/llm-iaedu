# Requirements

## Functional

| ID | Description | Priority |
|----|-------------|----------|
| F1 | Plugin registers an `iaedu` model with the `llm` CLI | Must |
| F2 | Plugin sends prompts to the iaedu.pt API and returns responses | Must |
| F3 | Plugin streams tokens as they arrive from the API | Must |
| F4 | Plugin supports `llm chat -m iaedu` interactive mode | Must |
| F5 | API key can be set via `llm keys set iaedu` or `IAEDU_API_KEY` env var | Must |
| F6 | Channel ID can be set via `IAEDU_CHANNEL_ID` env var | Must |
| F7 | Agent endpoint can be set via `IAEDU_ENDPOINT` or `IAEDU_AGENT_ID` | Must |
| F8 | Plugin auto-loads config from `./.env` and `~/.config/iaedu/env` | Must |
| F9 | Clear error messages when required config is missing | Must |

## Non-Functional

| ID | Description | Priority |
|----|-------------|----------|
| NF1 | No external dependencies beyond `llm` and `httpx` | Must |
| NF2 | No separate server process required — single-process architecture | Must |
| NF3 | Timeout of 120s for API requests | Must |
| NF4 | Plugin must work on Linux, macOS, Windows (via WSL) | Should |
| NF5 | Installation via `pip install llm-iaedu` | Must |

## Out of Scope

- Multi-agent orchestration (different from multiple models)
- Local model inference
- Authentication UI beyond `llm keys`
