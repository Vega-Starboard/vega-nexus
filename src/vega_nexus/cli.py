from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_CONFIG = Path("examples/routing-config.json")
DEFAULT_HISTORY = Path(".vega-nexus/runs.jsonl")

SIGNALS = {
    "security": ["security", "auth", "secret", "token", "exploit", "vulnerability", "xss", "csrf"],
    "implementation": ["implement", "refactor", "tests", "code", "module", "cli", "api"],
    "bulk": ["format", "metadata", "readme", "boilerplate", "summarize", "cleanup"],
    "reasoning": ["architecture", "design", "plan", "risk", "strategy", "review"],
}

def load_task(args: argparse.Namespace) -> str:
    if getattr(args, "task", None):
        return args.task
    if getattr(args, "task_file", None):
        return Path(args.task_file).read_text(encoding="utf-8")
    raise SystemExit("provide --task or --task-file")

def classify_task(task: str) -> dict:
    text = task.lower()
    scores = {name: sum(1 for word in words if word in text) for name, words in SIGNALS.items()}
    complexity = min(5, 1 + len(task.split()) // 18 + scores["implementation"] + scores["reasoning"])
    risk = min(5, scores["security"] * 2 + (1 if "production" in text else 0))
    latency = 2 if len(task) < 240 else 3
    kind = max(scores, key=scores.get) if any(scores.values()) else "bulk"
    return {"kind": kind, "scores": scores, "complexity": complexity, "risk": risk, "latency": latency}

def choose_provider(classification: dict) -> tuple[str, list[str]]:
    reasons = []
    kind = classification["kind"]
    risk = classification["risk"]
    complexity = classification["complexity"]
    if risk >= 4:
        reasons.append("high-risk or security-sensitive task requires strongest review")
        return "codex-gpt", reasons
    if kind == "bulk" and complexity <= 3:
        reasons.append("low-risk repetitive work favors economical bulk routing")
        return "deepseek-flash", reasons
    if kind in {"implementation", "reasoning"}:
        reasons.append("substantial draft or analysis favors DeepSeek V4 Pro")
        return "deepseek-v4-pro", reasons
    reasons.append("defaulting to economical provider for bounded work")
    return "deepseek-flash", reasons

def write_history(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")

def last_history(path: Path) -> dict:
    if not path.exists():
        raise SystemExit("no run history found")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise SystemExit("run history is empty")
    return json.loads(lines[-1])

def command_classify(args: argparse.Namespace) -> int:
    task = load_task(args)
    print(json.dumps(classify_task(task), indent=2))
    return 0

def command_route(args: argparse.Namespace) -> int:
    task = load_task(args)
    classification = classify_task(task)
    provider, reasons = choose_provider(classification)
    record = {
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "task": task.strip(),
        "dry_run": args.dry_run,
        "classification": classification,
        "selected_provider": provider,
        "reasons": reasons,
    }
    write_history(args.history, record)
    print(json.dumps(record, indent=2))
    return 0

def command_explain(args: argparse.Namespace) -> int:
    record = last_history(args.history)
    print(f"Selected provider: {record['selected_provider']}")
    print(f"Task kind: {record['classification']['kind']}")
    print(f"Risk: {record['classification']['risk']} Complexity: {record['classification']['complexity']}")
    for reason in record["reasons"]:
        print(f"- {reason}")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Route AI work by cost, risk, complexity, and task type.")
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("classify", "route"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--task")
        cmd.add_argument("--task-file", type=Path)
        if name == "route":
            cmd.add_argument("--dry-run", action="store_true")
            cmd.set_defaults(func=command_route)
        else:
            cmd.set_defaults(func=command_classify)
    explain = sub.add_parser("explain")
    explain.add_argument("--last-run", action="store_true")
    explain.set_defaults(func=command_explain)
    return parser

def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)
