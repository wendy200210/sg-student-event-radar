# Onboarding

Use a short interview or `python3 scripts/configure_profile.py`. Do not start discovery until `python3 scripts/validate_config.py` passes.

## Required decisions

Ask one concise question at a time when interviewing:

1. Education stage and expected graduation month.
2. Current career stage: exploration, internship, full-time search, project building, startup, or academic development.
3. One to five industries or sectors.
4. Specific fields, roles, organisations, or skills when known.
5. What attendance should achieve: insight, job access, relationships, portfolio output, startup progress, or academic progress.
6. Look-ahead window, ticket budget, availability, exam periods, preferred areas, language, and online-event policy.
7. Daily recommendation limit from one to eight.
8. Local output, Notion, or both.

The agent may translate natural-language answers into the JSON schema, then show a compact summary before saving. Store all answers only in `local/config.json`.

## Keyword generation

For each chosen industry, generate:

- direct industry terms;
- two to six field or function terms;
- professional bodies, regulators, accelerators, credible communities, and target organisations in Singapore;
- opportunity terms tied to the configured goals;
- exclusions for irrelevant admissions, sales funnels, or generic motivation content.

Do not add a field merely because it is popular. Technology, AI, finance, consulting, healthcare, consumer, sustainability, arts, public policy, and research must use the same neutral pipeline.

## Example profiles

- Finance undergraduate: asset management and risk; internship search; CFA Society and bank practitioner access; exams block two weeks.
- Healthcare master's student: health services and medtech; industry understanding plus project partners; hospital and regulator events; patient data sales pitches excluded.
- Consumer postgraduate: brand management and retail operations; graduate search; case competitions and practitioner workshops; generic influencer events excluded.
