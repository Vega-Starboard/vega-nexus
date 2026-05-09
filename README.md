# Vega Nexus

[![Release](https://img.shields.io/github/v/release/Vega-Starboard/vega-nexus?label=release)](https://github.com/Vega-Starboard/vega-nexus/releases/tag/v0.1.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Vega Nexus is a local orchestration router for deciding which AI provider should handle a task. It is not a model provider and does not require API keys for dry-run routing.

## Features

- Python CLI with `classify`, `route`, and `explain`
- JSON routing config plus documented YAML example
- Provider profiles for Codex/GPT, DeepSeek V4 Pro, DeepSeek V4 Flash, Claude, Ollama, and future providers
- Cost, risk, complexity, and latency scoring
- Escalation policy for high-risk or security-sensitive tasks
- Local JSONL run history

## Install

```bash
python3 -m pip install --user -e .
```

## Usage

```bash
PYTHONPATH=src python3 -m vega_nexus classify --task "Refactor this repo and write tests"
PYTHONPATH=src python3 -m vega_nexus route --task-file examples/tasks/refactor.md --dry-run
PYTHONPATH=src python3 -m vega_nexus explain --last-run
```

## Status

MVP. `v0.1.0` is released. Dry-run routing works locally and records inspectable route decisions.

## Roadmap

- Add optional provider execution adapters
- Add richer config validation
- Add cost tables from live provider metadata
