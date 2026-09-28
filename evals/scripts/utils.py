#!/usr/bin/env python3
"""Shared utilities for impeccable-harness scripts."""

import json
import re
import shutil
import sys
from pathlib import Path

OPENCODE_EXE_CANDIDATES = (
    r"C:\Users\jhona\AppData\Roaming\npm\node_modules\opencode-ai\bin\opencode.exe",
)


def find_opencode() -> str:
    """Resolve the opencode CLI executable. On Windows the npm `opencode`
    shim is a .ps1/.cmd that subprocess cannot spawn directly, so locate
    the real exe."""
    for candidate in OPENCODE_EXE_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    exe = shutil.which("opencode")
    if exe and exe.lower().endswith(".exe"):
        return exe
    # Fall back to shim resolution via cmd.exe wrapper.
    return "opencode.cmd" if sys.platform == "win32" else "opencode"


def safe_console() -> None:
    """Make stdout/stderr tolerant to non-cp1252 symbols (Windows consoles)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def parse_skill_md(path: Path) -> dict:
    """Parse a SKILL.md file, returning its frontmatter and body."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {"frontmatter": {}, "body": text}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return {"frontmatter": fm, "body": m.group(2)}


def load_evals(path: Path) -> list:
    """Load eval cases from an evals.json file.

    Supports both the harness project format
    ({\"project_harness_evals\": [...]}) and the skill format
    ({\"evals\": [...]}) and a bare list.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    for key in ("project_harness_evals", "evals", "skill_harness_evals"):
        if key in data:
            return data[key]
    raise ValueError(f"No eval cases found in {path}")


def save_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {path}")


def load_results(path: Path) -> list:
    return json.loads(path.read_text(encoding="utf-8"))


def heuristic_check(expected: str, output: str) -> bool:
    """Cheap success check: fraction of meaningful keywords in the
    expected result that appear in the agent output (threshold 60%)."""
    if not output:
        return False
    words = [w.lower() for w in re.findall(r"[a-zA-Z0-9_.\-/]{4,}", expected or "")]
    if not words:
        return bool(output.strip())
    out = output.lower()
    hits = sum(1 for w in set(words) if w in out)
    return hits / len(set(words)) >= 0.6
