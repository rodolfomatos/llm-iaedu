# llm-iaedu

Plugin for [LLM](https://llm.datasette.io/) that enables using the
[iaedu.pt](https://iaedu.pt) API as a model — no adapter, no Docker.

## Quick Start

```bash
# Install
pip install llm-iaedu

# Set API key
llm keys set iaedu

# Set as default model (optional)
llm models default iaedu

# Ask anything
llm "What is the capital of Portugal?"
```

## Setup

### 1. API Key

```bash
llm keys set iaedu
# Paste your API key when prompted
```

Alternatively, set `IAEDU_API_KEY` in your config file.

### 2. Channel + Agent

Create `~/.config/iaedu/env`:

```
IAEDU_CHANNEL_ID=your-channel-id
IAEDU_AGENT_ID=your-agent-id
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
make setup
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
