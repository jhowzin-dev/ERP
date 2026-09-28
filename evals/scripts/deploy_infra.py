#!/usr/bin/env python3
"""Deploy the impeccable-harness validation infra into a target project.

Called by the skill at Step 5 (Framework de Validação) when building the
orchestration, so the project gets the executable validation system:

  <project>/evals/
    scripts/          (run_eval, improve_description, validate_improvements,
                       aggregate_benchmark, run_trigger_eval, package_skill, utils)
    eval-viewer/      (generate_review.py)
    evals.json        (project-specific eval cases template)

Never overwrites existing project files without --force.

Usage:
  python deploy_infra.py --dir <project>
  python deploy_infra.py --dir <project> --force
"""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import safe_console

safe_console()

SKILL_DIR = Path(__file__).parent.parent

EVALS_TEMPLATE = """{
  "project_harness_evals": [
    {
      "id": 1,
      "task": "Descrição da tarefa complexa que o agente deve resolver",
      "expected_result": "O que define o sucesso desta tarefa",
      "critical_gate": "Qual Gate do OminiCore é crucial aqui?"
    }
  ]
}
"""

COPY_DIRS = ("scripts", "eval-viewer")


def main():
    ap = argparse.ArgumentParser(description="Deploy validation infra into a project")
    ap.add_argument("--dir", required=True, help="Target project directory")
    ap.add_argument("--force", action="store_true", help="Overwrite existing deployed scripts")
    args = ap.parse_args()

    project = Path(args.dir).resolve()
    if not project.exists():
        print(f"Target project does not exist: {project}")
        sys.exit(1)

    evals_dir = project / "evals"
    evals_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy executable infra (scripts + eval-viewer).
    for dirname in COPY_DIRS:
        src = SKILL_DIR / dirname
        dst = evals_dir / dirname
        if dst.exists():
            if not args.force:
                print(f"Skip (exists, use --force to overwrite): {dst}")
                continue
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"Deployed: {dst}")

    # 2. Create project evals.json template (never overwrite without --force).
    evals_file = evals_dir / "evals.json"
    if evals_file.exists() and not args.force:
        print(f"Skip (exists): {evals_file}")
    else:
        evals_file.write_text(EVALS_TEMPLATE, encoding="utf-8")
        print(f"Deployed: {evals_file}")

    # 3. Deploy-time check: all deployed scripts import cleanly here.
    import subprocess
    import_names = ", ".join(p.stem for p in sorted((evals_dir / "scripts").glob("*.py")))
    check = subprocess.run(
        [sys.executable, "-c", f"import sys; sys.path.insert(0, r'{evals_dir / 'scripts'}'); import {import_names}"],
        capture_output=True, text=True, cwd=str(project),
    )
    gate_ok = check.returncode == 0
    print(f"\nDeploy-time check: {'PASS (Goal Gate: exit 0)' if gate_ok else 'FAIL'}")
    if not gate_ok:
        print(check.stderr[-1000:])

    print("\nPróximos passos (o orquestrador deve executar):")
    print("1. Preencher evals/evals.json com prompts realistas da stack do projeto.")
    print(f"2. Rodar o baseline: python evals/scripts/run_eval.py --dir \"{project}\" --evals \"{evals_file}\"")
    print("3. Entrar no Loop de Ouro: python evals/scripts/run_loop.py --dir <projeto> --improve")

    sys.exit(0 if gate_ok else 1)


if __name__ == "__main__":
    main()
