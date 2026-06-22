# llm-iaedu

Plugin for [LLM](https://llm.datasette.io/) that enables using the
[iaedu.pt](https://iaedu.pt) API as a model — no adapter, no Docker.

## Quick Start

### Linux / macOS
```bash
# Install
pip install llm-iaedu

# Set API key
llm keys set iaedu

# Ask anything
llm -m iaedu "What is the capital of Portugal?"
```

### Ubuntu / Debian (PEP 668)
Ubuntu 23.04+ blocks system-wide `pip install`. Use one of:

**Option A — pip install --user** (simpler):
```bash
pip install --user llm-iaedu
llm keys set iaedu
llm -m iaedu "What is the capital of Portugal?"
```

**Option B — pipx** (if you already `pipx install llm`):
```bash
pipx inject llm llm-iaedu
llm keys set iaedu
llm -m iaedu "What is the capital of Portugal?"
```

## Setup

### Quick (interactive)

```bash
make configure
```

Paste the three values from iaedu.pt (Endpoint URL, API Key, Channel ID)
when prompted. The script creates `~/.config/iaedu/env` with everything
needed — works from any directory.

### Manual

Create `~/.config/iaedu/env`:

```
IAEDU_ENDPOINT=https://api.iaedu.pt/agent-chat/api/v1/agent/your-agent-id/stream
IAEDU_CHANNEL_ID=your-channel-id
IAEDU_API_KEY=your-api-key
```

Or place a `.env` in any project directory for local config.

### Config Precedence

1. Current shell (`export IAEDU_*`)
2. `./.env` (local)
3. `~/.config/iaedu/env` (global)
4. `~/.iaedu.env` (legacy)

## Usage

```bash
# One-off
llm -m iaedu "What is the capital of Portugal?"

# Default model (just skip -m)
llm models default iaedu
llm "What is the capital of Portugal?"

# Interactive chat
llm chat -m iaedu

# Pipe input
cat file.txt | llm -m iaedu
```

## Development

```bash
git clone https://github.com/rodolfomatos/llm-iaedu.git
cd llm-iaedu

# Standard
make setup
# ... or Ubuntu/Debian:
make ubuntu-setup
# ... or pipx:
make pipx-setup

make check
```

## How it works

The plugin calls the iaedu.pt API directly — no adapter server required.
It loads config from environment variables or `.env` files,
sends prompts as multipart form data, and streams token responses.

## Requirements

- Python 3.8+
- `llm` CLI
- iaedu.pt account with API key, channel ID, and agent ID

## Project

- [VISION](docs/VISION.md) — problem, solution, value proposition
- [REQUIREMENTS](docs/REQUIREMENTS.md) — functional and non-functional
- [ROADMAP](docs/ROADMAP.md) — backlog and progress
- [CHANGELOG](CHANGELOG.md) — version history
- [CLAUDE.md](CLAUDE.md) — operational contract for AI agents
