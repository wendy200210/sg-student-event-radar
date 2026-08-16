#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

PROFILES = {
    "finance": {
        "student_profile": {"education_stage": "undergraduate", "graduation_date": "2027-06", "career_stage": ["internship"]},
        "focus": {"industries": ["financial services"], "fields": ["asset management", "risk"], "target_roles": ["risk analyst"], "goals": ["job access", "industry understanding"]},
        "constraints": {"max_price_sgd": 30, "exam_periods": ["2026-11-10..2026-11-30"]}
    },
    "healthcare": {
        "student_profile": {"education_stage": "master", "graduation_date": "2027-01", "career_stage": ["industry exploration", "project"]},
        "focus": {"industries": ["healthcare"], "fields": ["health services", "medtech"], "target_roles": ["operations"], "goals": ["industry understanding", "project"]},
        "constraints": {"max_price_sgd": 50, "online_policy": "allow_if_high_value"}
    },
    "consumer": {
        "student_profile": {"education_stage": "graduate transition", "graduation_date": "2026-12", "career_stage": ["full-time search"]},
        "focus": {"industries": ["consumer goods", "retail"], "fields": ["brand management", "retail operations"], "target_roles": ["management trainee"], "goals": ["job access", "relationships"]},
        "constraints": {"daily_review_limit": 4, "max_price_sgd": 20}
    }
}


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)


with tempfile.TemporaryDirectory(prefix="sg-student-radar-") as temporary:
    temp = Path(temporary)
    for name, profile in PROFILES.items():
        profile_path = temp / f"{name}-profile.json"
        config_path = temp / f"{name}-config.json"
        profile_path.write_text(json.dumps(profile), encoding="utf-8")
        configured = run(PYTHON, "scripts/configure_profile.py", "--profile", str(profile_path), "--output", str(config_path))
        if configured.returncode != 0:
            raise SystemExit(f"{name} configure failed:\n{configured.stderr}")
        validated = run(PYTHON, "scripts/validate_config.py", "--config", str(config_path))
        if validated.returncode != 0:
            raise SystemExit(f"{name} validation failed:\n{validated.stderr}")
        print(f"PROFILE_OK {name}")

    invalid_profile = dict(PROFILES["finance"])
    invalid_profile["focus"] = dict(invalid_profile["focus"], industries=[])
    invalid_input = temp / "invalid-profile.json"
    invalid_config = temp / "invalid-config.json"
    invalid_input.write_text(json.dumps(invalid_profile), encoding="utf-8")
    run(PYTHON, "scripts/configure_profile.py", "--profile", str(invalid_input), "--output", str(invalid_config))
    rejected = run(PYTHON, "scripts/validate_config.py", "--config", str(invalid_config))
    if rejected.returncode == 0 or "industries must contain 1 to 5 values" not in rejected.stderr:
        raise SystemExit("invalid profile was not rejected correctly")
    print("INVALID_PROFILE_REJECTED")

cases = {
    "https://Example.com/e/1/?utm_source=x&b=2&a=1#top": "https://example.com/e/1?a=1&b=2",
    "https://example.com/e/1?ref=feed": "https://example.com/e/1",
    "http://example.com:80/": "http://example.com/",
    "https://example.com:444/path/": "https://example.com:444/path"
}
for raw, expected in cases.items():
    result = run(PYTHON, "scripts/normalize_url.py", raw)
    if result.returncode != 0 or result.stdout.strip() != expected:
        raise SystemExit(f"normalization failed for {raw}: {result.stdout}{result.stderr}")
print(f"URL_NORMALIZATION_OK cases={len(cases)}")
