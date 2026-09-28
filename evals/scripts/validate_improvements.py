#!/usr/bin/env python3
"""Validate the improved SKILL.md candidate (closed cycle).

Temporarily swaps SKILL.md with the candidate, re-runs the evals,
restores the original, and compares with results-before.json showing
the delta. If the candidate is worse, recommends discarding it.

Flow: Test -> Review -> Refine -> Test (closed).
"""

import argparse
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import load_results, save_json, safe_console

safe_console()


def rate(results) -> tuple[int, int]:
    total = len(results)
    passed = sum(1 for r in results if isinstance(r, dict) and r.get("passed"))
    return passed, total


def main():
    ap = argparse.ArgumentParser(description="Validate improved SKILL.md candidate")
    ap.add_argument("--skill", default=None, help="SKILL.md (default: this skill)")
    ap.add_argument("--candidate", default=None, help="Candidate file (default: evals/SKILL.candidate.md)")
    ap.add_argument("--before", default=None, help="Baseline results (default: evals/results-before.json)")
    ap.add_argument("--evals", default=None, help="Evals file to run against the candidate")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--parallel", type=int, default=2)
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent
    skill_path = Path(args.skill) if args.skill else skill_dir / "SKILL.md"
    candidate_path = Path(args.candidate) if args.candidate else skill_dir / "evals" / "SKILL.candidate.md"
    before_path = Path(args.before) if args.before else skill_dir / "evals" / "results-before.json"
    evals_arg = ["--evals", args.evals] if args.evals else []

    if not candidate_path.exists():
        print(f"No candidate found: {candidate_path}\nRun improve_description.py first.")
        sys.exit(1)

    backup_path = skill_dir / "evals" / "SKILL.original.bak.md"
    shutil.copy2(skill_path, backup_path)

    results_candidate_path = skill_dir / "evals" / "results-candidate.json"
    try:
        shutil.copy2(candidate_path, skill_path)
        print("Candidate swapped in. Re-running evals against the improved skill...")
        import subprocess
        cmd = [sys.executable, str(Path(__file__).parent / "run_eval.py"),
               "--out", str(results_candidate_path), "--timeout", str(args.timeout),
               "--parallel", str(args.parallel), *evals_arg]
        result = subprocess.run(cmd, cwd=str(skill_dir))
        if result.returncode != 0:
            print("Eval run against candidate failed.")
    finally:
        shutil.copy2(backup_path, skill_path)
        backup_path.unlink(missing_ok=True)
        print(f"Original SKILL.md restored: {skill_path}")

    if not results_candidate_path.exists():
        sys.exit(1)

    new_results = load_results(results_candidate_path)
    new_passed, total = rate(new_results)

    before = load_results(before_path) if before_path.exists() else None
    if before:
        old_passed, _ = rate(before)
        delta = new_passed - old_passed
        old_pct = 100 * old_passed // max(total, 1)
        new_pct = 100 * new_passed // max(total, 1)
        verdict = "✓ MELHOROU" if delta > 0 else ("= IGUAL" if delta == 0 else "⚠️ PIOROU — descarte o candidate")
        print(f"\nDelta: {old_pct}% → {new_pct}% {verdict}")
        print(f"       ({old_passed}/{total} → {new_passed}/{total})")

        per_eval = []
        old_by_id = {r.get("id"): r for r in before if isinstance(r, dict)}
        for r in new_results:
            if not isinstance(r, dict):
                continue
            eid = r.get("id")
            was = old_by_id.get(eid, {}).get("passed")
            now = r.get("passed")
            if was != now:
                per_eval.append(f"  eval {eid}: {'PASS' if was else 'FAIL'} → {'PASS' if now else 'FAIL'}")
        if per_eval:
            print("Mudanças por eval:")
            print("\n".join(per_eval))
    else:
        print(f"\nNo baseline found ({before_path}). New rate: {new_passed}/{total}")

    print("\nIf approved, replace SKILL.md with:")
    print(f"  cp \"{candidate_path}\" \"{skill_path}\"")


if __name__ == "__main__":
    main()
