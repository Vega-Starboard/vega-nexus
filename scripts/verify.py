#!/usr/bin/env python3
from __future__ import annotations

import os
import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "vega_nexus"
COMMANDS = [['classify', '--task', 'Refactor this repo and write tests'], ['route', '--task-file', 'examples/tasks/refactor.md', '--dry-run'], ['explain', '--last-run']]
REQUIRED_FILES = ['README.md', 'LICENSE', 'SECURITY.md', 'PRIVACY.md', 'docs/routing-policy.md', 'examples/routing-config.yaml', 'src/vega_nexus/cli.py']


def fail(message: str) -> None:
    print(f"verify: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")
    for path in (ROOT / "src" / PACKAGE).glob("*.py"):
        py_compile.compile(str(path), doraise=True)
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    for args in COMMANDS:
        result = subprocess.run(
            [sys.executable, "-m", PACKAGE, *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail("command failed: " + " ".join(args) + "\n" + result.stderr)
    print("verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
