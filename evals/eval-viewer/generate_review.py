#!/usr/bin/env python3
"""Generate a review HTML from eval results for visual inspection.

Usage: python generate_review.py [results.json]
Output: evals/review.html (self-contained, open in a browser).
"""

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from utils import load_results

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Impeccable Harness — Eval Review</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;background:#0f1117;color:#e6e6e6}
 .card{background:#171a23;border:1px solid #2a2f3d;border-radius:10px;padding:1rem 1.25rem;margin:1rem 0}
 .pass{border-left:4px solid #3fb96f}.fail{border-left:4px solid #e05252}.gate{border-left:4px solid #e0a52e}
 h1{font-size:1.4rem}h2{font-size:1.05rem;margin:.2rem 0}
 .meta{color:#8b93a7;font-size:.85rem}
 pre{background:#0b0d12;padding:.75rem;border-radius:6px;overflow:auto;font-size:.8rem;white-space:pre-wrap}
 .pill{display:inline-block;padding:.1rem .5rem;border-radius:999px;font-size:.75rem;background:#2a2f3d}
</style></head><body>
<h1>Impeccable Harness — Eval Review</h1>
<p class="meta">{summary}</p>
{cards}
</body></html>"""


def load_delta(results_path: Path) -> str:
    """Show the last validation delta from results-before.json, if any."""
    before_path = results_path.parent / "results-before.json"
    if not before_path.exists():
        return ""
    try:
        before = [r for r in load_results(before_path) if isinstance(r, dict)]
        old = sum(1 for r in before if r.get("passed"))
        new = sum(1 for r in load_results(results_path) if isinstance(r, dict) and r.get("passed"))
        total = max(len(before), 1)
        old_pct = 100 * old // total
        new_pct = 100 * new // total
        delta = new_pct - old_pct
        symbol = "✓" if delta > 0 else ("=" if delta == 0 else "⚠️")
        return f" &nbsp;|&nbsp; Validação: {old_pct}% → {new_pct}% {symbol}"
    except Exception:
        return ""


def main():
    results_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "evals" / "results.json"
    results = load_results(results_path)
    total = len(results)
    passed = sum(1 for r in results if isinstance(r, dict) and r.get("passed"))

    cards = []
    for r in results:
        cls = "pass" if r.get("passed") else ("gate" if not r.get("goal_gate_passed") else "fail")
        status = "PASS" if r.get("passed") else ("GATE-FAIL" if not r.get("goal_gate_passed") else "FAIL")
        cards.append(
            f'<div class="card {cls}"><h2>Eval {html.escape(str(r.get("id")))} '
            f'<span class="pill">{status}</span></h2>'
            f'<p>{html.escape(r.get("prompt", ""))}</p>'
            f'<p class="meta">Esperado: {html.escape(r.get("expected_output", ""))} · '
            f'exit={r.get("exit_code")} · {r.get("duration_s")}s</p>'
            f'<pre>{html.escape((r.get("output") or r.get("error") or "")[:4000])}</pre></div>'
        )

    html_out = TEMPLATE.replace(
        "{summary}",
        f"{passed}/{total} passed ({100 * passed // max(total, 1)}%) — {results_path}{load_delta(results_path)}",
    ).replace("{cards}", "\n".join(cards))
    out = results_path.parent / "review.html"
    out.write_text(html_out, encoding="utf-8")
    print(f"Review generated: {out}")


if __name__ == "__main__":
    main()
