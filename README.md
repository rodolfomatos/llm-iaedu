# llm-iaedu

A plugin for [LLM](https://llm.datasette.io/) that enables using the [iaedu-adapter](https://github.com/rodolfomatos/iaedu-adapter) as a model.

## Installation

```bash
# Install LLM if you don't have it
pip install llm

# Install this plugin
pip install llm-iaedu
```

Or for development:

```bash
git clone https://github.com/yourname/llm-iaedu.git
cd llm-iaedu
pip install -e .
```

## Setup

1. Get your IAEDU API key from [iaedu.pt](https://iaedu.pt)

2. Set the API key using LLM's key management:
   ```bash
   llm keys set iaedu
   # Paste your API key when prompted
   ```

3. Ensure the [iaedu-adapter](https://github.com/rodolfomatos/iaedu-adapter) is running:
   ```bash
   # In another terminal
   npm install  # if you haven't already
   # Create a .env file in the iaedu-adapter directory with:
   echo "IAEDU_API_KEY=your-actual-api-key-here" > .env
   echo "IAEDU_CHANNEL_ID=your-channel-id-here" >> .env  # This is the channel ID for your agent in iaedu.pt
   echo "IAEDU_ENDPOINT=https://api.iaedu.pt/agent-chat/api/v1/agent/your-agent-id/stream" >> .env  # Optional, defaults to the hardcoded value in the adapter
   # Then start the adapter:
   npm start
   # The adapter should be accessible at http://localhost:4000
   ```

## Usage

Once installed and configured, you can use the iaedu model like any other LLM model:

```bash
llm -m iaedu "What is the capital of Portugal?"
```

You can also use it in chat mode:

```bash
llm chat -m iaedu
```

## Configuration

The plugin uses the following environment variable:

- `IAEDU_ENDPOINT`: URL of the iaedu-adapter (default: `http://localhost:4000`)

Example:
```bash
IAEDU_ENDPOINT=http://my-server:8000 llm -m iaedu "Hello"
```

## How it works

This plugin acts as a bridge between LLM and the iaedu-adapter:
1. LLM calls the plugin with a prompt
2. The plugin retrieves your IAEDU API key using LLM's key management system
3. The plugin forwards the request to your iaedu-adapter instance (as multipart/form-data)
4. The adapter communicates with the iaedu.pt API using its own channel ID and agent ID (configured in its environment)
5. The plugin streams the response back to LLM

## Requirements

- LLM installed
- iaedu-adapter running and accessible
- Valid IAEDU API key
- Valid IAEDU channel ID and agent ID configured in the iaedu-adapter's environment