#!/usr/bin/env python3
"""Aggregate multiple eval result files into a benchmark summary.

Usage: python aggregate_benchmark.py results1.json results2.json ...
       python aggregate_benchmark.py --compare results-before.json results-candidate.json
Output: evals/benchmark.json with per-file success rates and variance.
"""

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import load_results, save_json, safe_console

safe_console()


def rate(results):
    results = [r for r in results if isinstance(r, dict)]
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    return passed, total


def compare(file_a: Path, file_b: Path) -> dict:
    a_passed, a_total = rate(load_results(file_a))
    b_passed, b_total = rate(load_results(file_b))
    a_pct = 100 * a_passed // max(a_total, 1)
    b_pct = 100 * b_passed // max(b_total, 1)
    delta = b_pct - a_pct
    verdict = "IMPROVED" if delta > 0 else ("EQUAL" if delta == 0 else "WORSE")
    result = {
        "before": str(file_a),
        "after": str(file_b),
        "before_passed": a_passed,
        "after_passed": b_passed,
        "before_rate": a_pct / 100,
        "after_rate": b_pct / 100,
        "delta_pct": delta,
        "verdict": verdict,
    }
    symbol = "✓" if delta > 0 else ("=" if delta == 0 else "⚠️")
    print(f"Compare: {a_pct}% → {b_pct}% {symbol} {verdict}")
    print(f"         ({a_passed}/{a_total} → {b_passed}/{b_total})")
    return result


def main():
    args = sys.argv[1:]
    if args and args[0] == "--compare":
        if len(args) < 3:
            print("Usage: python aggregate_benchmark.py --compare before.json after.json")
            sys.exit(1)
        result = compare(Path(args[1]), Path(args[2]))
        out = Path("evals") / "benchmark.json"
        save_json(result, out)
        return

    if len(args) < 1:
        print("Usage: python aggregate_benchmark.py results1.json [results2.json ...]")
        sys.exit(1)

    benchmark = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        try:
            results = load_results(path)
        except Exception as e:
            print(f"Skipping {path}: {e}")
            continue
        if not isinstance(results, list):
            raise ValueError("expected a list of result objects")
        results = [r for r in results if isinstance(r, dict)]
        total = len(results)
        passed = sum(1 for r in results if r.get("passed"))
        gates = sum(1 for r in results if r.get("goal_gate_passed"))
        durations = [r["duration_s"] for r in results if isinstance(r.get("duration_s"), (int, float))]
        benchmark.append({
            "file": str(path),
            "total": total,
            "passed": passed,
            "success_rate": round(passed / total, 3) if total else 0.0,
            "goal_gate_rate": round(gates / total, 3) if total else 0.0,
            "avg_duration_s": round(statistics.mean(durations), 1) if durations else None,
        })

    rates = [b["success_rate"] for b in benchmark if b["total"]]
    summary = {
        "runs": benchmark,
        "mean_success_rate": round(statistics.mean(rates), 3) if rates else None,
        "success_rate_stddev": round(statistics.stdev(rates), 3) if len(rates) > 1 else None,
    }
    out = Path("evals") / "benchmark.json"
    save_json(summary, out)
    for b in benchmark:
        print(f"  {b['file']}: {b['passed']}/{b['total']} ({b['success_rate']:.0%})")
    if summary["mean_success_rate"] is not None:
        print(f"Mean: {summary['mean_success_rate']:.0%}  StdDev: {summary['success_rate_stddev']}")


if __name__ == "__main__":
    main()
