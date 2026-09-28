#!/usr/bin/env python3
"""Improve the impeccable-harness SKILL.md based on eval results.

Takes eval results (from run_eval.py) and generates an improved SKILL.md
body by calling `opencode run` as a subprocess, feeding it the current
SKILL.md plus failure observations. Writes a candidate file for review
(it never overwrites the original without the user's confirmation).

Context-flow guarantees:
- No blind truncation: extracts a relevant excerpt (last half + error
  lines) with a larger budget and logs how many chars were dropped.
- Saves evals/results-before.json (snapshot) so the improvement can be
  validated against the previous version (closed cycle).
- Multi-turn: continues the same opencode session when a session id is
  present in the results.
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import parse_skill_md, load_results, save_json, find_opencode

OPENCODE = find_opencode()

BUDGET_PER_FAILURE = 8000
ERROR_MARKERS = ("error", "fail", "timeout", "traceback", "exception", "denied", "invalid")


def extract_excerpt(output: str, budget: int = BUDGET_PER_FAILURE) -> tuple[str, int]:
    """Return (relevant_excerpt, dropped_chars). Prioritizes the tail
    (where final errors usually live) plus lines containing error markers."""
    if len(output) <= budget:
        return output, 0
    lines = output.splitlines()
    error_lines = [
        ln for ln in lines
        if any(m in ln.lower() for m in ERROR_MARKERS)
    ]
    tail = "\n".join(lines[len(lines) // 2:])
    parts = []
    used = 0
    if error_lines:
        block = "\n".join(error_lines)[: budget // 2]
        parts.append(f"[ERROR LINES]\n{block}")
        used += len(block)
    remaining = budget - used
    block_tail = tail[-remaining:] if remaining > 0 else ""
    parts.append(f"[OUTPUT TAIL]\n{block_tail}")
    dropped = len(output) - sum(len(p) for p in parts)
    return "\n".join(parts), max(dropped, 0)


def call_opencode(prompt: str, model: str | None, timeout: int = 600, session_id: str | None = None) -> str:
    cmd = [OPENCODE, "run", prompt]
    if model:
        cmd.extend(["--model", model])
    if session_id:
        cmd.extend(["-s", session_id])
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(f"opencode failed ({result.returncode}): {result.stderr[-1000:]}")
    return result.stdout


def main():
    ap = argparse.ArgumentParser(description="Improve SKILL.md from eval results")
    ap.add_argument("--results", default=None, help="Results JSON (default: evals/results.json)")
    ap.add_argument("--skill", default=None, help="SKILL.md to improve (default: this skill)")
    ap.add_argument("--model", default=None, help="provider/model for opencode")
    ap.add_argument("--out", default=None, help="Output candidate path")
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent
    skill_path = Path(args.skill) if args.skill else skill_dir / "SKILL.md"
    results_path = Path(args.results) if args.results else skill_dir / "evals" / "results.json"
    out_path = Path(args.out) if args.out else skill_dir / "evals" / "SKILL.candidate.md"
    before_path = results_path.parent / "results-before.json"

    parsed = parse_skill_md(skill_path)
    results = load_results(results_path)
    failures = [r for r in results if not r["passed"]]
    if not failures:
        print("All evals passed. Nothing to improve.")
        return

    # Snapshot the previous results for closed-cycle validation.
    if results_path != before_path:
        save_json(results, before_path)

    session_id = next((r.get("session_id") for r in results if r.get("session_id")), None)
    failure_summary_parts = []
    total_dropped = 0
    for r in failures:
        excerpt, dropped = extract_excerpt(r["output"] or r.get("error") or "")
        total_dropped += dropped
        note = f" (+{dropped} chars dropped from output)" if dropped else ""
        failure_summary_parts.append(
            f"Eval {r['id']}: {r['prompt']}\nExpected: {r['expected_output']}\n"
            f"Got (relevant excerpt{note}):\n{excerpt}"
        )
    if total_dropped:
        print(f"Context note: {total_dropped} chars dropped across failures (prioritized error lines + tail).")
    else:
        print("Context note: full failure outputs included (no truncation).")
    failure_summary = "\n\n".join(failure_summary_parts)

    prompt = (
        "You are a prompt engineer improving an AI harness skill (SKILL.md).\n"
        "Below are the current SKILL.md and the eval failures observed.\n"
        "Rewrite the SKILL.md body to fix the failures while keeping all existing\n"
        "gates, rules and structure intact. Do not simplify or remove governance.\n"
        "Output ONLY the full improved SKILL.md file content (with frontmatter).\n\n"
        f"=== CURRENT SKILL.MD ===\n{parsed['body']}\n\n"
        f"=== EVAL FAILURES ===\n{failure_summary}\n"
    )

    print("Asking opencode to rewrite the SKILL.md...")
    improved = call_opencode(prompt, args.model, session_id=session_id)
    out_path.write_text(improved, encoding="utf-8")
    print(f"Candidate written: {out_path}")
    print("Next: validate it with validate_improvements.py (closed cycle) before replacing SKILL.md.")


if __name__ == "__main__":
    main()
