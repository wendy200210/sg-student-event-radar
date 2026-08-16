# Source strategy

## Three source layers

1. **General discovery**: Singapore pages on Luma, Eventbrite, Meetup, university ecosystems, public calendars, and credible event aggregators.
2. **Profile-derived sources**: industry associations, regulators, government bodies, professional societies, accelerators, research institutes, target organisations, and relevant school centres generated from private configuration.
3. **Opportunity queries**: searches combining Singapore, configured industries or fields, goals, event formats, student eligibility, target roles, and the current year.

Attempt at least three independent sources in a normal scan. A source can be discovered dynamically, but record why it matches the profile and its last successful check in the private ledger.

## Evidence order

Use aggregators for discovery, then verify material facts in this order:

1. official registration page;
2. organiser's event page;
3. official host, venue, institution, or partner page;
4. event platform detail page;
5. search snippet only as an unverified lead.

Do not award points from organiser prestige or a title keyword alone. Verify date and time, Singapore venue or online format, price, eligibility, registration status, agenda, speakers and roles, interaction format, and registration URL.

## Query templates

Expand placeholders only from private configuration. Useful combinations include:

- `Singapore {{industry}} {{field}} workshop networking register {{year}}`
- `Singapore {{target_role}} student industry event {{year}}`
- `site:official-domain Singapore event students {{year}}`
- `{{target_company}} Singapore open house challenge workshop careers {{year}}`
- `Singapore university students {{industry}} competition case challenge {{year}}`

If a required placeholder is empty, skip that query and record `skipped_missing_configuration`.

## Source health and access

Record each due source as `success`, `success_zero`, or `failed`, and each non-due source as `skipped_not_due`. Retry once at most. Never bypass access controls. A signed-in browser is allowed only when the user already controls the session and the task permits reading it.

## URL identity

Normalize before detail fetch. Strip ordinary tracking parameters but retain event identity and access tokens needed to reopen the page. Merge cross-posts only when title, organiser, date, and event identity agree; otherwise preserve both and flag possible duplication.
