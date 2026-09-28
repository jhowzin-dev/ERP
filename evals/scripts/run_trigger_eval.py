#!/usr/bin/env python3
"""Run trigger evaluation for the impeccable-harness description.

Tests whether the SKILL.md description causes opencode to load/use the
skill for a set of queries. Adapted from the skill-creator approach:
runs `opencode run <query> --format json` and inspects session events
to detect skill usage (tool parts referencing "skill" or the skill
name, or text output referencing it alongside harness keywords).

Usage:
  python run_trigger_eval.py                # uses evals/trigger_evals.json
  python run_trigger_eval.py --queries f.json --dir <project>
Output: evals/trigger_results.json + trigger_review.html
"""

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import save_json, find_opencode, safe_console

safe_console()

OPENCODE = find_opencode()

HARNESS_KEYWORDS = ("harness", "gate", "gate de", "omini", "ominicore", "orquestr")


def detect_trigger(events_output: str, skill_name: str) -> bool:
    """Heuristic: any tool part referencing skill, or text referencing
    the skill name alongside harness keywords. Handles both top-level
    events ({type, part, ...}) and nested payloads."""
    parts = []
    for line in events_output.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            if "part" in obj and isinstance(obj["part"], dict):
                parts.append(obj["part"])
            else:
                parts.append(obj)
    for part in parts:
        blob = json.dumps(part, ensure_ascii=False).lower()
        if part.get("type") == "tool" and ("skill" in blob or skill_name.lower() in blob):
            return True
    text_blob = " ".join(
        json.dumps(p.get("text", ""), ensure_ascii=False).lower()
        for p in parts if p.get("type") == "text"
    )
    return skill_name.lower() in text_blob and any(k in text_blob for k in HARNESS_KEYWORDS)


def run_single_query(eval_id, query, should_trigger, skill_name, project_dir, timeout):
    cmd = [OPENCODE, "run", query, "--format", "json"]
    if project_dir:
        cmd.extend(["--dir", project_dir])
    started = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, cwd=project_dir or Path.cwd()
        )
        output, exit_code = result.stdout, result.returncode
    except subprocess.TimeoutExpired as e:
        # Preserve partial output: a trigger may have fired before the timeout.
        output = e.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        exit_code = 124
    duration = round(time.time() - started, 1)
    triggered = detect_trigger(output, skill_name) if output else False
    passed = triggered == should_trigger
    return {
        "id": eval_id,
        "query": query,
        "should_trigger": should_trigger,
        "triggered": triggered,
        "passed": passed,
        "exit_code": exit_code,
        "timed_out": exit_code == 124,
        "duration_s": duration,
        "raw_events": output[:40000],
    }


def main():
    ap = argparse.ArgumentParser(description="Run trigger evals via opencode")
    ap.add_argument("--queries", default=None, help="Trigger evals JSON path")
    ap.add_argument("--dir", default=None, help="Project directory to run opencode in")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--parallel", type=int, default=2)
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent
    queries_path = Path(args.queries) if args.queries else skill_dir / "evals" / "trigger_evals.json"
    data = json.loads(queries_path.read_text(encoding="utf-8"))
    cases = data if isinstance(data, list) else data.get("trigger_evals", data.get("evals", []))
    skill_name = data.get("skill_name") if isinstance(data, dict) else None
    if not skill_name:
        from utils import parse_skill_md
        skill_name = parse_skill_md(skill_dir / "SKILL.md")["frontmatter"].get("name", "impeccable-harness")

    print(f"Trigger eval: {len(cases)} queries (skill: {skill_name}, timeout {args.timeout}s)...")
    results = []
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futures = {
            ex.submit(run_single_query, c.get("id"), c["query"], c.get("should_trigger", True), skill_name, args.dir, args.timeout): c
            for c in cases
        }
        for fut in as_completed(futures):
            r = fut.result()
            status = "PASS" if r["passed"] else "FAIL"
            expect = "TRIGGER" if r["should_trigger"] else "NO-TRIGGER"
            got = "TRIGGER" if r["triggered"] else "NO-TRIGGER"
            note = " (timeout)" if r.get("timed_out") else ""
            print(f"  [{status}] query {r['id']} ({expect} → {got}{note}, {r['duration_s']}s)")
            results.append(r)

    results.sort(key=lambda r: r.get("id") or 0)
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    summary = {
        "skill_name": skill_name,
        "results": [{k: v for k, v in r.items() if k != "raw_events"} for r in results],
        "trigger_rate": round(passed / total, 3) if total else 0.0,
        "passed": passed,
        "total": total,
    }
    save_json(summary, skill_dir / "evals" / "trigger_results.json")
    print(f"\nTrigger rate: {passed}/{total} ({100 * passed // max(total, 1)}%)")

    # Review HTML for visual inspection.
    cards = []
    for r in results:
        cls = "pass" if r["passed"] else "fail"
        cards.append(
            f'<div class="card {cls}"><h2>Query {r["id"]} '
            f'<span class="pill">{"PASS" if r["passed"] else "FAIL"}</span></h2>'
            f'<p>{r["query"]}</p>'
            f'<p class="meta">Esperado: {"TRIGGER" if r["should_trigger"] else "NO-TRIGGER"} · '
            f'Obtido: {"TRIGGER" if r["triggered"] else "NO-TRIGGER"} · {r["duration_s"]}s</p></div>'
        )
    html_doc = (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<title>Impeccable Harness — Trigger Review</title><style>'
        'body{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;background:#0f1117;color:#e6e6e6}'
        '.card{background:#171a23;border:1px solid #2a2f3d;border-radius:10px;padding:1rem 1.25rem;margin:1rem 0}'
        '.pass{border-left:4px solid #3fb96f}.fail{border-left:4px solid #e05252}'
        'h1{font-size:1.4rem}.meta{color:#8b93a7;font-size:.85rem}'
        '.pill{display:inline-block;padding:.1rem .5rem;border-radius:999px;font-size:.75rem;background:#2a2f3d}'
        '</style></head><body><h1>Impeccable Harness — Trigger Review</h1>'
        f'<p class="meta">{passed}/{total} passed ({100 * passed // max(total, 1)}%)</p>'
        + "\n".join(cards) + "</body></html>"
    )
    (skill_dir / "evals" / "trigger_review.html").write_text(html_doc, encoding="utf-8")
    print(f"Review: {skill_dir / 'evals' / 'trigger_review.html'}")


if __name__ == "__main__":
    main()
