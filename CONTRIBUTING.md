# Contributing

## Development Setup

```bash
python3 -m pip install --user -e .
python3 scripts/verify.py
```

## Pull Requests

- Keep changes focused.
- Update docs when behavior changes.
- Add or update examples when a command shape changes.
- Run `python3 scripts/verify.py` before opening a pull request.

## Boundaries

Do not add secrets, telemetry, or hidden remote calls. Vega Nexus is a routing and explanation tool; live provider execution should remain explicit and optional.
