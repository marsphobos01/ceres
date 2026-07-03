# Goals Scope — Decision

**Status:** Decided
**Related issues:** #8, #23, #57

## Decision

Goals is **deferred**. It remains solely a Potential Future Module — not a current-build Dashboard feature, not a current-build product pillar. No `Goal` model is created anywhere, including `core`.

## Why

Goals appeared in two incompatible places in the Vision: listed (unquoted, i.e. current-build) under `## Features > ### Dashboard`, and separately under `## Potential Future Modules`, which explicitly states those modules are "not in scope for the current build." Per the project's own feature-priority rules, potential modules stay outside active scope until explicitly promoted — and nothing here promoted Goals; it just drifted into the Features section inconsistently. Promoting it now, or inventing a same-name-but-different "represented by an existing concept" version, would both be scope creep relative to what's actually been decided about the product so far.

There's also an architecture reason this couldn't have gone into `core` regardless of scope: `core` is presentation/aggregation only and doesn't own product-domain data. If Goals is ever promoted, its data model belongs to `planning` (which already lists "Potential goals" among its responsibilities) — `core` would only ever display an aggregated view, the same way it displays deadlines and tasks it doesn't own.

## What changed

- `Documentation/Ceres Vision Document.md`:
  - Removed "Goals" from `## Product Pillars > ### Organisation`.
  - Removed "Goals" from `## Features > ### Dashboard` (the canonical feature reference — this was the actual conflict).
  - Left "Goals" in `## Potential Future Modules` — now the single place Goals is mentioned as in-scope-for-anything.
  - Left the `## Information Architecture` diagram untouched — it's positioned as the full eventual app map (it lists Habits and Placement alongside Goals, both also Potential Future Modules), not a current-build claim.
- No schema, migration, or model changes — there was never a `Goal` model to remove, and none is being added.

## Issue updates

I don't have direct access to GitHub, so I can't edit #8, #23, or #57 myself. Suggested updates below — please review before pasting, since I'm inferring each issue's likely role from the parent issue's text, not from their actual current content.

### #57

This is the issue this decision was raised to unblock ("so #57 does not accidentally create an unsupported Goal model inside `core`"). Recommend: **close as deferred**, referencing this decision doc. #57 has no real source of data to build against (Goals isn't promoted), so there's nothing to implement. If/when Goals is promoted in the future, it should be a new issue against `planning`, not a reopening of this one against `core`.

### #8 and #23

I don't know what these currently contain — likely the Dashboard feature/epic and a `core`-related epic or schema issue, based on where this decision touches. Whichever they are, the relevant update is the same: remove or correct any reference to Goals as a current-build Dashboard feature or as `core`-owned scope, and link to this decision doc as the reason. If either of these is actually unrelated to Goals, they don't need touching — worth a quick check before editing.
