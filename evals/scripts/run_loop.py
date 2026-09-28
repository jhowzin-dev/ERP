#!/usr/bin/env python3
"""Run the impeccable-harness Golden Loop in a single command.

Orchestrates the CLOSED cycle:
  run_eval.py -> generate_review.py -> [improve_description.py if --improve
  and failures] -> validate_improvements.py -> aggregate_benchmark.py

Safety Rails: max 5 iterations, per-eval timeout, exit-code checking at
every step. Never replaces SKILL.md automatically — the candidate is only
adopted by the user (or by --adopt when validation shows improvement).

Usage:
  python run_loop.py --dir <project>
  python run_loop.py --dir <project> --improve --iterations 3
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent
SKILL_DIR = SCRIPTS.parent
MAX_ITERATIONS = 5

sys.path.insert(0, str(SCRIPTS))
from utils import safe_console

safe_console()


def run(script, *args, check=True):
    cmd = [sys.executable, str(SCRIPTS / script), *map(str, args)]
    result = subprocess.run(cmd, cwd=str(SKILL_DIR))
    if check and result.returncode != 0:
        print(f"[GATE-FAIL] {script} exited with {result.returncode}")
        sys.exit(result.returncode)
    return result.returncode


def results_stats(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    import json
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data = [r for r in data if isinstance(r, dict)]
    except Exception:
        return 0, 0
    return sum(1 for r in data if r.get("passed")), len(data)


def main():
    ap = argparse.ArgumentParser(description="Golden Loop of the impeccable-harness")
    ap.add_argument("--dir", default=None, help="Project directory to run evals in")
    ap.add_argument("--evals", default=None, help="Evals file (default: skill evals)")
    ap.add_argument("--out", default=None, help="Results output path")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--improve", action="store_true", help="Improve SKILL.md when evals fail (closed cycle)")
    ap.add_argument("--iterations", type=int, default=1, help="Max refine+retest iterations (max 5, Safety Rail)")
    ap.add_argument("--adopt", action="store_true", help="Adopt candidate SKILL.md if validation shows improvement")
    args = ap.parse_args()

    iterations = max(1, min(args.iterations, MAX_ITERATIONS))
    if args.iterations > MAX_ITERATIONS:
        print(f"Safety Rail: iterations clamped to {MAX_ITERATIONS}.")

    out_path = Path(args.out) if args.out else SKILL_DIR / "evals" / "results.json"
    candidate_path = SKILL_DIR / "evals" / "SKILL.candidate.md"

    common = ["--dir", args.dir or ".", "--timeout", args.timeout, "--parallel", args.parallel]
    eval_args = (["--evals", args.evals] if args.evals else [])

    print("=== GOLDEN LOOP: Test -> Review -> Refine -> Test ===\n")
    run("run_eval.py", "--out", out_path, *common, *eval_args)
    run("eval-viewer/generate_review.py", out_path, check=False)

    passed, total = results_stats(out_path)
    print(f"\nLoop result: {passed}/{total}")

    for it in range(1, iterations + 1):
        if passed == total:
            print("\nGoal Gate: OBJETIVO ALCANÇADO (todos os evals passam).")
            break
        if not args.improve:
            print(f"\n{total - passed} falha(s). Rode com --improve para entrar no ciclo fechado.")
            break

        print(f"\n=== ITERAÇÃO {it}/{iterations}: Refine -> Test ===")
        run("improve_description.py", "--results", out_path)
        if not candidate_path.exists():
            print("Nenhum candidate gerado; encerrando o loop.")
            break
        run("validate_improvements.py", "--evals", args.evals or "", "--timeout", args.timeout, "--parallel", args.parallel)

        new_passed, new_total = results_stats(SKILL_DIR / "evals" / "results-candidate.json")
        if new_total and new_passed > passed:
            print(f"Validação: {passed}/{total} → {new_passed}/{new_total} ✓")
            if args.adopt:
                import shutil
                candidate_path.replace(SKILL_DIR / "SKILL.md")
                print("Candidate adotado como novo SKILL.md (--adopt).")
                passed, total = new_passed, new_total
            else:
                print("Candidate NÃO adotado automaticamente. Revise e adote com:")
                print(f'  cp "{candidate_path}" "{SKILL_DIR / "SKILL.md"}"')
                passed, total = new_passed, new_total
        else:
            print("⚠️ Candidate não melhorou; iterar mais pode não valer a pena.")

    if passed == total:
        run("aggregate_benchmark.py", "--compare",
            SKILL_DIR / "evals" / "results-before.json" if (SKILL_DIR / "evals" / "results-before.json").exists() else out_path,
            out_path, check=False)
        print("\n=== LOOP CONCLUÍDO: OBJETIVO ALCANÇADO ===")
    else:
        print(f"\n=== LOOP CONCLUÍDO PARCIAL: {passed}/{total} (revisione review.html) ===")


if __name__ == "__main__":
    main()
