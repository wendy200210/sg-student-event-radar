#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, text=True).strip())
PREFIX = ROOT.relative_to(REPO).as_posix() + "/"
errors = []
uuid = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
notion_url = re.compile(r"https?://(?:www\.)?(?:app\.)?notion\.(?:so|com)/(?:p/)?[0-9a-f]{32}\b", re.I)
secret = re.compile(r"(?:secret_[A-Za-z0-9_-]{20,}|ntn_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,})")

required = ["SKILL.md", "routine-prompt.md", "config.example.json", "ledger.example.json", "LICENSE"]
for name in required:
    if not (ROOT / name).exists():
        errors.append(f"Missing {name}")

tracked_output = subprocess.check_output(["git", "ls-files", "-z", "--", PREFIX], cwd=REPO)
tracked = [item.decode() for item in tracked_output.split(b"\0") if item]
for repo_path in tracked:
    relative = repo_path[len(PREFIX):]
    if relative == "local" or relative.startswith("local/"):
        errors.append(f"Tracked private state: {relative}")
    if relative.startswith("reports/") and relative != "reports/.gitkeep":
        errors.append(f"Tracked report: {relative}")
    path = REPO / repo_path
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    if uuid.search(content) or notion_url.search(content) or secret.search(content):
        errors.append(f"Identifier or secret-like value: {relative}")

for private_path in ["local/config.json", "local/ledger.json", "local/notion-state.json"]:
    result = subprocess.run(["git", "check-ignore", "-q", private_path], cwd=ROOT)
    if result.returncode != 0:
        errors.append(f"Not ignored: {private_path}")

if errors:
    raise SystemExit("PUBLIC_RELEASE_BLOCKED\n" + "\n".join(f"- {error}" for error in errors))

print(f"PUBLIC_RELEASE_OK tracked={len(tracked)}")
