#!/usr/bin/env python3
"""Package a skill into a distributable zip.

Usage:
  python package_skill.py                       # packages this skill
  python package_skill.py --skill <path/to/skill> --out <dir>
Excludes __pycache__, eval results, candidates, backups and review HTML.
"""

import argparse
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules"}
EXCLUDE_SUFFIXES = (".pyc",)
EXCLUDE_NAMES = {
    "results.json", "results-candidate.json", "results-before.json",
    "trigger_results.json", "review.html", "trigger_review.html",
    "SKILL.candidate.md", "SKILL.original.bak.md", "benchmark.json",
}


def main():
    ap = argparse.ArgumentParser(description="Package a skill into a zip")
    ap.add_argument("--skill", default=None, help="Skill directory (default: this skill)")
    ap.add_argument("--out", default=None, help="Output directory for the zip (default: skill parent)")
    args = ap.parse_args()

    skill_dir = Path(args.skill).resolve() if args.skill else Path(__file__).parent.parent
    if not (skill_dir / "SKILL.md").exists():
        print(f"Not a skill directory (no SKILL.md): {skill_dir}")
        sys_exit(1)

    out_dir = Path(args.out).resolve() if args.out else skill_dir.parent
    zip_path = out_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_dir():
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            if path.suffix in EXCLUDE_SUFFIXES or path.name in EXCLUDE_NAMES:
                continue
            zf.write(path, path.relative_to(skill_dir))
    print(f"Packaged: {zip_path}")


def sys_exit(code):
    import sys
    sys.exit(code)


if __name__ == "__main__":
    main()
