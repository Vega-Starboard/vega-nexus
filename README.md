# Vega Nexus

[![Release](https://img.shields.io/github/v/release/Vega-Starboard/vega-nexus?label=release)](https://github.com/Vega-Starboard/vega-nexus/releases/tag/v0.1.0)
[![CI](https://github.com/Vega-Starboard/vega-nexus/actions/workflows/ci.yml/badge.svg)](https://github.com/Vega-Starboard/vega-nexus/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Local-first AI orchestration router for multi-model workflows.**

Vega Nexus decides which AI provider should handle a given task based on cost, risk, complexity, and latency signals. It is not a model provider itself and does not require API keys for dry-run routing.

## Why Vega Nexus?

Modern development workflows increasingly span multiple AI providers - each with different strengths, costs, and risk profiles. Vega Nexus provides a local, auditable routing layer that:

- Classifies tasks by type (bulk, reasoning, security, implementation)
- Scores complexity and risk before selecting a provider
- Records every routing decision for inspection
- Works entirely offline with no external API calls during routing

## Features

- **Task classification** - analyzes task text for security, implementation, bulk, and reasoning signals
- **Provider routing** - selects from configured providers (DeepSeek, Codex/GPT, Claude, Ollama) based on scored criteria
- **Cost-aware decisions** - factors provider cost tiers into routing choices
- **Risk escalation** - automatically escalates high-risk or security-sensitive tasks to strongest review tier
- **Dry-run mode** - preview routing decisions without executing any provider call
- **JSONL run history** - local, inspectable audit trail of every classification and route
- **Dual config formats** - JSON and YAML provider profiles with documented examples
- **Explain command** - review the reasoning behind the last routing decision

## Install

```bash
git clone https://github.com/Vega-Starboard/vega-nexus.git
cd vega-nexus
python3 -m pip install --user -e .
```

Requires Python 3.10+. No external dependencies beyond the standard library.

## Quickstart

```bash
# Classify a task without routing
PYTHONPATH=src python3 -m vega_nexus classify --task "Refactor this repo and write tests"

# Route a task from a file (dry-run, no provider call)
PYTHONPATH=src python3 -m vega_nexus route --task-file examples/tasks/refactor.md --dry-run

# Explain the last routing decision
PYTHONPATH=src python3 -m vega_nexus explain --last-run
```

## Commands

### `classify`

Analyze task text and output classification scores.

```bash
vega-nexus classify --task "Add authentication middleware"
vega-nexus classify --task-file path/to/task.md
```

Output: JSON with `kind`, `scores`, `complexity`, `risk`, and `latency` fields.

### `route`

Classify a task and select the appropriate provider.

```bash
vega-nexus route --task "Generate README boilerplate" --dry-run
vega-nexus route --task-file path/to/task.md
```

Output: JSON record with `selected_provider`, `classification`, and `reasons`. Appended to local run history.

### `explain`

Display the reasoning from the most recent routing decision.

```bash
vega-nexus explain --last-run
```

Output: Human-readable summary of provider choice, task kind, risk/complexity scores, and decision reasons.

## Configuration

Provider profiles are defined in `examples/routing-config.json` (JSON) or `examples/routing-config.yaml` (YAML). Each provider entry specifies:

| Field | Description |
|-------|-------------|
| `cost` | Relative cost tier (1-5, lower is cheaper) |
| `latency` | Expected latency tier (1-5) |
| `risk_ceiling` | Maximum risk level this provider can handle (1-5) |
| `strength` | Task categories where this provider excels |

### Default Provider Profiles

| Provider | Cost | Best For |
|----------|------|----------|
| DeepSeek Flash | 1 | Bulk, formatting, metadata, boilerplate |
| DeepSeek V4 Pro | 2 | Implementation, research, substantial drafts |
| Codex/GPT | 5 | Architecture, security, integration review |
| Claude | 4 | Critique, long-context analysis |
| Ollama | 0 | Local, privacy-sensitive, offline work |

## Routing Policy

The router evaluates tasks across four signal categories:

- **Bulk** - repetitive, formatting, metadata, boilerplate, summarization
- **Reasoning** - architecture, planning, design, risk analysis, review
- **Security** - auth, secrets, tokens, exploit-adjacent terminology
- **Implementation** - code generation, tests, refactors, CLI/API work

**Escalation rule:** Tasks scoring risk >= 4 are automatically routed to Codex/GPT regardless of other signals.

See [`docs/routing-policy.md`](docs/routing-policy.md) for the full policy specification.

## Outputs & Artifacts

- **Classification JSON** - structured task analysis (stdout from `classify`)
- **Route record JSON** - provider selection with reasoning (stdout from `route`)
- **Run history** - JSONL file at `.vega-nexus/runs.jsonl` (configurable via `--history`)

## Privacy & Safety

- **Local-only** - all processing happens on your machine
- **No API keys required** - dry-run routing never contacts external providers
- **No telemetry** - zero network calls during classification or routing
- **Auditable** - every decision is recorded in local JSONL history

## Project Status

**MVP - v0.1.0 released.** Dry-run routing works locally with inspectable decision records. Provider execution adapters are not yet implemented; this release handles the classification and selection layer only.

### Known Limitations

- No live provider execution (routing decisions only)
- Provider cost tables are static, not pulled from live metadata
- Config validation is minimal - malformed configs may produce unclear errors

## Roadmap

- [ ] Provider execution adapters (optional, opt-in API calls)
- [ ] Richer config validation with schema checking
- [ ] Live cost tables from provider metadata endpoints
- [ ] Batch routing for multiple tasks
- [ ] Plugin system for custom provider profiles

## Development

```bash
git clone https://github.com/Vega-Starboard/vega-nexus.git
cd vega-nexus
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Running Tests

```bash
python3 scripts/verify.py
```

### Project Structure

```
vega-nexus/
+-- src/vega_nexus/
|   +-- __init__.py
|   +-- __main__.py
|   `-- cli.py
+-- examples/
|   +-- routing-config.json
|   +-- routing-config.yaml
|   `-- tasks/
|       `-- refactor.md
+-- docs/
|   `-- routing-policy.md
+-- pyproject.toml
`-- README.md
```

## Repository Topics

`ai-orchestration` `multi-model` `routing` `local-first` `cli-tool` `deepseek` `llm-router` `task-classification` `cost-optimization` `python`

## Support & Security

- **Issues:** [GitHub Issues](https://github.com/Vega-Starboard/vega-nexus/issues)
- **License:** MIT - see [LICENSE](LICENSE)
- **Security:** This tool performs no network calls during routing. If you discover a vulnerability in the classification logic, please open an issue rather than attempting to demonstrate it against production systems.

---
