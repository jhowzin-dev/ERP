#!/usr/bin/env python3
"""Run eval prompts for the impeccable-harness through `opencode run`.

Runs each eval case (optionally inside a target project via --dir),
captures the output, applies the Goal Gate (exit code 0) + heuristic
success check and saves results as JSON for the eval-viewer.

Modes:
- Default: each eval runs in an isolated fresh session (correct for
  measuring the skill in isolation).
- --shared-session: reuses one opencode session across evals so
  earlier evals inform later ones (accumulated context within a run).
- --skip-passed: cache — skips evals that passed in the last results.
"""

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import load_evals, save_json, heuristic_check, find_opencode

OPENCODE = find_opencode()


def parse_session_id(json_events: str) -> str | None:
    """Extract the sessionID from `opencode run --format json` output."""
    import json as _json
    for line in json_events.splitlines():
        try:
            obj = _json.loads(line)
        except _json.JSONDecodeError:
            continue
        sid = obj.get("sessionID")
        if sid:
            return sid
    return None


def run_single(eval_case, skill_dir, project_dir, timeout, session_id=None):
    prompt = eval_case.get("prompt") or eval_case.get("task") or ""
    cmd = [OPENCODE, "run", prompt]
    if project_dir:
        cmd.extend(["--dir", project_dir])
    if session_id:
        cmd.extend(["-s", session_id])
    started = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, cwd=project_dir or Path.cwd()
        )
        output = (result.stdout or "") + "\n" + (result.stderr or "")
        exit_code = result.returncode
        error = result.stderr[-2000:] if result.returncode != 0 else ""
    except subprocess.TimeoutExpired:
        output, exit_code, error = "", 124, f"timeout after {timeout}s"
    duration = round(time.time() - started, 1)

    # Goal Gate: exit code 0 is a hard requirement.
    gate_ok = exit_code == 0
    passed = gate_ok and heuristic_check(eval_case.get("expected_output", ""), output)
    return {
        "id": eval_case.get("id"),
        "prompt": prompt,
        "expected_output": eval_case.get("expected_output", ""),
        "output": output[:20000],
        "error": error,
        "exit_code": exit_code,
        "goal_gate_passed": gate_ok,
        "passed": passed,
        "duration_s": duration,
        "session_id": session_id,
    }


def main():
    ap = argparse.ArgumentParser(description="Run harness evals via opencode")
    ap.add_argument("--evals", default=None, help="Path to evals.json (default: skill evals)")
    ap.add_argument("--dir", default=None, help="Project directory to run opencode in")
    ap.add_argument("--out", default=None, help="Output results JSON path")
    ap.add_argument("--timeout", type=int, default=600, help="Per-eval timeout in seconds")
    ap.add_argument("--parallel", type=int, default=2, help="Number of parallel runs (ignored with --shared-session)")
    ap.add_argument("--shared-session", action="store_true", help="Reuse one opencode session across evals (accumulated context)")
    ap.add_argument("--skip-passed", action="store_true", help="Skip evals that passed in the last results (cache)")
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent  # repo-root evals/
    evals_path = Path(args.evals) if args.evals else skill_dir / "evals.json"
    eval_cases = load_evals(evals_path)
    out_path = Path(args.out) if args.out else skill_dir / "evals" / "results.json"

    # Cache: skip evals that already passed.
    if args.skip_passed and out_path.exists():
        try:
            prev = [r for r in load_results_safe(out_path) if isinstance(r, dict)]
            passed_ids = {r.get("id") for r in prev if r.get("passed")}
            skipped = [ec for ec in eval_cases if ec.get("id") in passed_ids]
            eval_cases = [ec for ec in eval_cases if ec.get("id") not in passed_ids]
            if skipped:
                print(f"Cache: skipping {len(skipped)} eval(s) already passed: {[e.get('id') for e in skipped]}")
        except Exception as e:
            print(f"Cache ignored ({e})")

    if not eval_cases:
        print("Nothing to run (all cached).")
        return

    print(f"Running {len(eval_cases)} evals (timeout {args.timeout}s each)...")

    results = []
    if args.shared_session:
        session_id = None
        for ec in eval_cases:
            r = run_single(ec, skill_dir, args.dir, args.timeout, session_id=session_id)
            if not session_id and r["exit_code"] == 0 and r["output"]:
                session_id = parse_session_id(r["output"]) or None
            status = "PASS" if r["passed"] else ("GATE-FAIL" if not r["goal_gate_passed"] else "FAIL")
            print(f"  [{status}] eval {r['id']} ({r['duration_s']}s)")
            results.append(r)
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            futures = {
                ex.submit(run_single, ec, skill_dir, args.dir, args.timeout): ec
                for ec in eval_cases
            }
            for fut in as_completed(futures):
                r = fut.result()
                status = "PASS" if r["passed"] else ("GATE-FAIL" if not r["goal_gate_passed"] else "FAIL")
                print(f"  [{status}] eval {r['id']} ({r['duration_s']}s)")
                results.append(r)

    results.sort(key=lambda r: r.get("id") or 0)

    # Merge with cached results when skipping passed evals.
    if args.skip_passed and out_path.exists():
        try:
            prev = [r for r in load_results_safe(out_path) if isinstance(r, dict)]
            prev_ids = {r.get("id") for r in results}
            cached = [r for r in prev if r.get("id") not in prev_ids]
            results = sorted(results + cached, key=lambda r: r.get("id") or 0)
        except Exception:
            pass

    save_json(results, out_path)
    passed = sum(1 for r in results if r["passed"])
    print(f"\nSuccess rate: {passed}/{len(results)} ({100 * passed // max(len(results), 1)}%)")


def load_results_safe(path: Path) -> list:
    import json
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


if __name__ == "__main__":
    main()
