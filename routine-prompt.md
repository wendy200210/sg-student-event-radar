# SG Student Event Radar — authoritative run protocol

Run in `Asia/Singapore`. Produce a small personalized review queue, preserve decisions, and report evidence gaps honestly.

## 0. Initialize and validate

Run `python3 scripts/init_local_state.py` and `python3 scripts/validate_config.py`. Read `local/config.json`, `local/ledger.json`, and `local/notion-state.json`. If onboarding is incomplete, stop and guide configuration. Never scan with the public example profile.

## 1. Read choices first

When Notion is enabled and connected, query existing non-archived records before browsing. Otherwise read local preference signals. Map `Not interested` to a reversible long-term dismissal, `Considering` to deferred review, and `Interested` to preparation. Never overwrite a user's choice.

If Notion read fails, continue using the local ledger, label the run partial, and warn that recent choices may be missing.

## 2. Build the search plan

Read [references/source-strategy.md](references/source-strategy.md). Combine due general sources with profile-derived official sources and goal-specific search queries. Expand placeholders only from private configuration. Attempt at least three independent sources unless fewer are currently reachable; explain any shortfall.

Run daily sources every scan and weekly sources only on their configured Singapore weekday. Record source state. Retry a failure once at most.

## 3. Collect light candidates

From listing pages collect only title, stable event URL, displayed date, organiser, price marker, registration marker, and the profile term that caused the match. Reject obvious past or irrelevant listings cheaply.

## 4. Deduplicate before details

Normalize each URL with `python3 scripts/normalize_url.py "URL"`. Check ledger keys, canonical URLs, and alternate URLs before fetching details:

- dismissed: skip until the user reverses it;
- factual hard rejection: skip;
- current scoring-version quality rejection: skip until recheck;
- future kept item: skip unless verification is due;
- deferred: fetch only when due;
- pending, interested with missing facts, or unseen: fetch.

Track avoided detail fetches.

## 5. Verify survivors

Obtain direct evidence for date and time, Singapore venue or online format, price, registration status, organiser, student eligibility, agenda, speakers and roles, interaction format, likely people access, concrete output, and canonical registration URL. Keep factual evidence separate from inference. Missing essentials yield `needs_verification`.

## 6. Gate, score, and check schedule

Read [references/scoring-rubric.md](references/scoring-rubric.md). Apply hard gates, then score 0–10 using the user's current education stage, career stage, goals, and constraints. Check recurring commitments and exam periods. Do not lower the configured threshold.

## 7. Persist atomically

Write every fetched candidate, including rejections, to the private ledger with verdict, reason, evidence, score breakdown, scoring version, timestamps, source, event date, recheck date, user action, and sync status. Write a temporary file, validate JSON, then rename. Stop before external writes if persistence fails.

## 8. Select the five-minute queue

Choose only newly qualified, undecided events. Sort by score descending, registration urgency, then event date. Limit to `daily_review_limit`; do not pad the queue.

## 9. Deliver locally and optionally to Notion

Always write `reports/YYYY-MM-DD.md` and a machine-readable queue in private state. If Notion is enabled, follow [references/notion-schema.md](references/notion-schema.md), upsert by normalized URL, preserve `My choice`, and read back representative writes.

For each newly interested event, create or propose one smallest concrete preparation action. Never register, pay, message, invite, submit, or add a calendar event without action-time confirmation.

## 10. Report run quality

Report `complete`, `partial`, or `failed`; per-source statuses; counts for discovered, deduplicated, fetched, rejected, deferred, kept, and synced; selected events; verification gaps; and required user actions.

A valid run requires at least one successful due source. A successful source with zero qualified events is `success_zero`, not failure. A timestamp or empty report is never proof of a successful scan.
