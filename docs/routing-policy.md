# Routing Policy

Routing is based on task signals:

- `bulk`: repetitive, formatting, metadata, boilerplate
- `reasoning`: architecture, planning, critique, design
- `security`: auth, secrets, scanning, exploit-adjacent words
- `implementation`: code generation, tests, refactors

The router escalates high-risk security or production-sensitive work to Codex/GPT-level review. DeepSeek Flash is preferred for low-risk bulk work. DeepSeek V4 Pro is preferred for substantial drafts and analysis. Ollama is treated as a local experimental provider.
