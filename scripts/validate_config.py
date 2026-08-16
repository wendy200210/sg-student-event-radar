#!/usr/bin/env python3
import argparse
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description="Validate an SG Student Event Radar configuration.")
parser.add_argument("--config", help="Configuration path; defaults to private local config")
args = parser.parse_args()
if args.config:
    CONFIG_PATH = Path(args.config).expanduser().resolve()
else:
    CONFIG_PATH = ROOT / "local/config.json"
    if not CONFIG_PATH.exists():
        CONFIG_PATH = ROOT / "config.example.json"

try:
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        config = json.load(handle)
except Exception as exc:
    raise SystemExit(f"CONFIG_INVALID\n- Invalid JSON: {exc}")

errors = []
profile = config.get("student_profile", {})
focus = config.get("focus", {})
constraints = config.get("constraints", {})
output = config.get("output", {})

if not config.get("onboarding_complete"):
    errors.append("onboarding_complete must be true; run scripts/configure_profile.py")
if config.get("timezone") != "Asia/Singapore":
    errors.append("timezone must be Asia/Singapore")
if profile.get("education_stage") not in {"polytechnic", "undergraduate", "master", "PhD", "graduate transition"}:
    errors.append("education_stage must be polytechnic, undergraduate, master, PhD, or graduate transition")
try:
    dt.datetime.strptime(profile.get("graduation_date", ""), "%Y-%m")
except ValueError:
    errors.append("graduation_date must use YYYY-MM")
if not isinstance(profile.get("career_stage"), list) or not profile.get("career_stage"):
    errors.append("career_stage must contain at least one value")
if not isinstance(focus.get("industries"), list) or not 1 <= len(focus.get("industries", [])) <= 5:
    errors.append("industries must contain 1 to 5 values")
if not isinstance(focus.get("goals"), list) or not focus.get("goals"):
    errors.append("goals must contain at least one value")

integer_ranges = {
    "lookahead_days": (1, 180),
    "daily_review_limit": (1, 8),
    "minimum_score": (0, 10)
}
for key, (lower, upper) in integer_ranges.items():
    value = constraints.get(key)
    if not isinstance(value, int) or not lower <= value <= upper:
        errors.append(f"{key} must be an integer from {lower} to {upper}")
if not isinstance(constraints.get("max_price_sgd"), (int, float)) or constraints.get("max_price_sgd", -1) < 0:
    errors.append("max_price_sgd must be non-negative")
if constraints.get("online_policy") not in {"reject", "allow", "allow_if_high_value"}:
    errors.append("online_policy must be reject, allow, or allow_if_high_value")
if output.get("mode") not in {"local", "notion", "both"}:
    errors.append("output.mode must be local, notion, or both")
if output.get("mode") in {"notion", "both"} and not output.get("notion_enabled"):
    errors.append("notion_enabled must be true when output.mode uses Notion")

sources = config.get("sources")
if not isinstance(sources, list) or not sources:
    errors.append("sources must be a non-empty array")
    sources = []
seen = set()
for index, source in enumerate(sources):
    source_id = source.get("id")
    if not source_id or not source.get("name"):
        errors.append(f"sources[{index}] needs id and name")
    if source_id in seen:
        errors.append(f"duplicate source id: {source_id}")
    seen.add(source_id)
    if source.get("cadence") not in {"daily", "weekly"}:
        errors.append(f"{source_id}: cadence must be daily or weekly")
    if source.get("cadence") == "weekly" and not source.get("weekday"):
        errors.append(f"{source_id}: weekly source needs weekday")
    if not (source.get("url") or (source.get("type") == "websearch" and isinstance(source.get("queries"), list))):
        errors.append(f"{source_id}: source needs url or websearch queries")

if errors:
    raise SystemExit("CONFIG_INVALID\n" + "\n".join(f"- {error}" for error in errors))

try:
    display_path = CONFIG_PATH.relative_to(ROOT)
except ValueError:
    display_path = CONFIG_PATH
print(f"CONFIG_OK industries={len(focus['industries'])} sources={len(sources)} file={display_path}")
