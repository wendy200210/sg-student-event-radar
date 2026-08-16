#!/usr/bin/env python3
import argparse
import json
import os
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "local" / "config.json"
TEMPLATE = ROOT / "config.example.json"


def split_values(value):
    return [item.strip() for item in value.replace("，", ",").split(",") if item.strip()]


def ask(label, default=""):
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def atomic_write(path, value):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.chmod(temporary, 0o600)
    temporary.replace(path)


def merge_profile(config, profile):
    result = deepcopy(config)
    for section in ("student_profile", "focus", "constraints", "output"):
        incoming = profile.get(section, {})
        if incoming:
            result[section].update(incoming)
    result["onboarding_complete"] = True
    return result


def interactive_profile():
    print("SG Student Event Radar setup. Separate multiple values with commas.")
    return {
        "student_profile": {
            "education_stage": ask("Education stage (polytechnic/undergraduate/master/PhD/graduate transition)"),
            "graduation_date": ask("Expected graduation date (YYYY-MM)"),
            "career_stage": split_values(ask("Current stages (industry exploration/internship/full-time/project/academic)")),
            "institutions": split_values(ask("Institutions (optional)"))
        },
        "focus": {
            "industries": split_values(ask("Industries or sectors (1-5)")),
            "fields": split_values(ask("Specific fields or topics")),
            "target_roles": split_values(ask("Target roles (optional)")),
            "target_companies": split_values(ask("Target companies or organisations (optional)")),
            "skills": split_values(ask("Skills to build (optional)")),
            "goals": split_values(ask("Goals (industry understanding/job access/network/project/startup/academic)")),
            "exclude_topics": split_values(ask("Topics to exclude (optional)"))
        },
        "constraints": {
            "lookahead_days": int(ask("Look-ahead days", "45")),
            "max_price_sgd": float(ask("Maximum ticket price in SGD", "50")),
            "daily_review_limit": int(ask("Maximum daily recommendations", "5")),
            "minimum_score": int(ask("Minimum score from 0 to 10", "6")),
            "languages": split_values(ask("Languages", "English")),
            "online_policy": ask("Online policy (reject/allow/allow_if_high_value)", "allow_if_high_value"),
            "preferred_areas": split_values(ask("Preferred Singapore areas (optional)")),
            "schedule_constraints": split_values(ask("Recurring unavailable times (optional)")),
            "exam_periods": split_values(ask("Exam periods YYYY-MM-DD..YYYY-MM-DD (optional)"))
        },
        "output": {
            "mode": ask("Output mode (local/notion/both)", "local"),
            "notion_enabled": False
        }
    }


parser = argparse.ArgumentParser(description="Configure a private SG Student Event Radar profile.")
parser.add_argument("--profile", help="JSON file containing student_profile, focus, constraints, and output")
parser.add_argument("--output", help="Override output path; intended for testing and portable setup")
args = parser.parse_args()

with TEMPLATE.open(encoding="utf-8") as handle:
    base = json.load(handle)
if TARGET.exists():
    with TARGET.open(encoding="utf-8") as handle:
        base = json.load(handle)

if args.profile:
    with Path(args.profile).open(encoding="utf-8") as handle:
        supplied = json.load(handle)
else:
    supplied = interactive_profile()

configured = merge_profile(base, supplied)
output_path = Path(args.output).expanduser().resolve() if args.output else TARGET
atomic_write(output_path, configured)
print(f"PROFILE_SAVED {output_path}")
