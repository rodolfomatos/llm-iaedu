# VISION

## Problem
Using LLM models hosted on iaedu.pt requires custom integration — there is no
off-the-shelf plugin for the `llm` CLI tool.

## Solution
`llm-iaedu` is a plugin for [LLM](https://llm.datasette.io/) that registers the
`iaedu` model, allowing users to call iaedu.pt-hosted models directly from the
command line with the same interface as any other LLM model.

## Value Proposition
- Zero-friction: one `pip install` and one `llm keys set iaedu` away from using
  iaedu.pt models from the terminal
- Works from any directory — no adapter servers, no Docker containers
- Supports streaming, chat mode, and piped input like any LLM model

## Target Audience
- Developers and power users who interact with LLMs via the terminal
- Users of iaedu.pt who want a CLI interface to their hosted models
