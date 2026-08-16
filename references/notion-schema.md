# Optional Notion schema

Read this file only when the user chooses Notion or an existing connection is recorded. Notion is optional; local Markdown and JSON must remain usable without it.

Create or reuse one database named `SG Student Event Radar`. Read it back before writing and save IDs only in `local/notion-state.json`.

## Properties

| Property | Type | Owner |
|---|---|---|
| Event | title | agent |
| Date and time | date | agent |
| Location | rich text | agent |
| Organiser | rich text | agent |
| Industry / field | multi-select | agent |
| Event type | select | agent |
| Price SGD | number | agent |
| Score | number | agent |
| Why it fits me | rich text | agent |
| People access | rich text | agent |
| Suggested preparation | rich text | agent |
| Schedule conflict | rich text | agent |
| Registration deadline | date | agent |
| Registration URL | URL | agent |
| My choice | select | user |
| Status | select | shared by rule |
| Last verified | date | agent |
| Verification status | select | agent |
| Batch date | date | agent |
| Sources | rich text | agent |

Use `Interested`, `Considering`, and `Not interested` for `My choice`. Never overwrite a non-empty choice. New rows use `To review`. Only user evidence can justify `Registered` or `Attended`.

## Views

- `Today's 5-minute review`: latest batch, empty choice, `To review`, score descending, deadline then date ascending.
- `Interested and prepare`.
- `Considering`.
- `All upcoming`.

Upsert by normalized Registration URL. If a compatible task database exists, relate one concrete preparation action for newly interested events. Otherwise keep preparation as text; do not create a second task system.

If Notion read fails, continue locally and label the run partial. If a write fails, retain `sync_status: pending` in the ledger for a later retry.
