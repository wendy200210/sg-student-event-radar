#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / "local"


def read_json(path):
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        raise SystemExit(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")


def write_atomic(path, value):
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.chmod(temporary, 0o600)
    read_json(temporary)
    temporary.replace(path)


def create_from_template(target, template):
    if target.exists():
        read_json(target)
        return "reused"
    write_atomic(target, read_json(template))
    return "created"


LOCAL.mkdir(mode=0o700, parents=True, exist_ok=True)
(ROOT / "reports").mkdir(parents=True, exist_ok=True)

config = create_from_template(LOCAL / "config.json", ROOT / "config.example.json")
ledger = create_from_template(LOCAL / "ledger.json", ROOT / "ledger.example.json")
notion_path = LOCAL / "notion-state.json"
if notion_path.exists():
    read_json(notion_path)
    notion = "reused"
else:
    write_atomic(notion_path, {
        "version": 1,
        "database_id": None,
        "data_source_id": None,
        "actions_data_source_id": None
    })
    notion = "created"

print(json.dumps({"ok": True, "config": config, "ledger": ledger, "notion": notion}))
