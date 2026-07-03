# Timetable CSV Import — Decisions

**Parent epic:** #10 — [Epic] Timetable
**Resolves:** the data-mapping decisions blocking #220
**Source data:** `academics/CSV-TEST-DOC/timetable_2026-07-03.csv` (a real MyTimetable export, used to ground every decision below in actual data rather than assumption)

## Key finding that shapes everything below

The export is **per-occurrence, not per-pattern**: every row already carries its own concrete date (`Start date`). There is no single weekly/fortnightly rule to extract — the same nominal session (e.g. KV4008's Tuesday lecture) can change room mid-term, and enrichment/induction weeks appear as their own dated rows rather than gaps in a pattern. Treating this as a recurrence-detection problem would require re-inventing exception-tracking the schema doesn't have. Treating it as what it actually is — a list of one-off sessions — fits `TimetableEntry.recurrence_type = one_off` directly, using the existing `date` field. This decision is the foundation for the ones that follow.

## Column mapping

| CSV column | Destination | Notes |
| --- | --- | --- |
| `Description` | `Lecture.title` | Creates one `Lecture` per row (see "Module and Lecture matching" below). |
| `Module code` | `TimetableEntry.module` (via `Lecture.module`) | Matched against accessible `Module.code`. See "Module matching." |
| `Start day` | `TimetableEntry.day_of_week` | `Mon`/`Tue`/`Wed`/`Thu`/`Fri`/`Sat`/`Sun` lowercased to match `DayOfWeek` choices (`mon`, `tue`, ...) directly. |
| `Start date` | `TimetableEntry.date` and `Lecture.date` | Every row sets this — see row-strategy decision above. |
| `Start time` | `TimetableEntry.start_time` | Direct. |
| `End day` | *(ignored)* | Not stored — the schema has no separate end-day field. In this export `End day` always equals `Start day`; if a future export ever has an overnight session, the importer should reject that row rather than silently drop the day boundary (there's nowhere to put it). |
| `End date` | *(ignored)* | Same reasoning as `End day`. |
| `End time` | `TimetableEntry.end_time` | Direct. |
| `Duration` | *(ignored)* | Redundant with start/end time; can be used as an optional cross-check assertion in the importer, not stored. |
| `Type` | *(ignored — not stored)* | No destination field on `TimetableEntry` or `Lecture`. `Description` already conveys session type in most rows (e.g. "Workshop 1/01"). Not filtered on except for the Draft-row rule below — see "Row filtering." |
| `Staff member(s)` | `Lecture.lecturer_name` | Multiple names (comma-separated in the source) are joined with `; ` into the single `CharField`. `Lecture.lecturer_email` stays blank — the export has no email column. |
| `Room(s)` | `TimetableEntry.room` and `Lecture.room` | Stored as the raw string, including multi-room values (e.g. `"SPF 001 (Sport Central Main Hall), Students Union (Domain)"`). Blank for online sessions — left blank, not defaulted to a sentinel like `"Online"`. |
| `Student set(s)` | *(ignored)* | Blank in every sample row; no destination field. |
| `Department` | *(ignored)* | No destination field on `Module` today. Not needed for matching since matching is by `code`, not department. |
| `Size` | *(ignored)* | Informational only. |
| `Draft` | *(filter, not stored)* | `Yes` rows are skipped entirely — see "Row filtering." |
| `This activity takes place on location` | *(ignored)* | Redundant with whether `Room(s)` is populated. |
| `This activity takes place online` | *(ignored)* | Same as above. |

Every column now has an explicit destination or an explicit ignore rule.

## Module and Lecture matching

- **Module matching:** case-insensitive exact match against `Module.code`, scoped to Modules the importing user can access (`Module.owner == user` or an existing `ModuleMembership`). This directly satisfies the epic's requirement that rows only ever create/update data the user is allowed to touch.
- **Missing module (your decision):** if a row's code doesn't match any accessible Module, the importer offers to create a new Module from the row (using `Module code` as `code` and `Description`'s module-level context, not the per-session title, as a starting `title` — needs a human-readable module title source; the CSV doesn't have one, so the user must supply/confirm the title when creating). If the user declines, the row is skipped (counted in `skipped_rows`, not `error_rows` — this was a deliberate choice, not a failure).
- **Lecture matching:** one `Lecture` is created per imported row rather than matched/reused. The `Lecture` model already represents a single dated session (it has its own `date` field), which is exactly what each CSV row is — there's no separate "lecture template" to match against. A `Lecture` is only skipped (not created) when its corresponding `TimetableEntry` is skipped for any reason (unmatched module, Draft row, or protected manual edit).

## Idempotency — duplicate/update identity

Two entries are "the same session" if they share `(module, date, start_time, end_time)`. This is enough to uniquely identify a session in the sample data — a Module can't have two sessions starting at the same time on the same day.

Re-running an import:
- **No existing match:** create a new `TimetableEntry` (and its `Lecture`). Counts toward `imported_rows`.
- **Existing match, not manually edited:** update the existing `TimetableEntry`'s `room` and the linked `Lecture`'s `title`/`lecturer_name`/`room` from the new row. Counts toward `imported_rows` (see the row-count note below — this conflates "created" and "updated," a known limitation, not a schema requirement of this decision).
- **Existing match, manually edited (your decision, see below):** skip. Counts toward `skipped_rows`.

## Manually-edited entries (your decision — requires schema work)

Re-imports must never silently overwrite a `TimetableEntry` a user has hand-edited (e.g. corrected a room). The current schema has no way to represent "this row was edited outside the importer," so this decision **requires a new field**:

- Add `TimetableEntry.is_manually_edited` (`BooleanField`, default `False`).
- Set it to `True` whenever a user edits a `TimetableEntry` directly (not via import).
- The importer checks this flag before updating an existing match; if `True`, skip and log rather than overwrite.

**This is schema/migration work for #220, not for this decision issue** — flagging it here so #220 is scoped correctly, per this issue's own rule that migrations are only created if a decision changes the schema. No migration has been created as part of this document.

## Date ranges / teaching weeks

No new representation is needed. Because every row imports as `recurrence_type = one_off` with its own `date`, the existing schema already represents date ranges and teaching-week variation (including enrichment weeks, which appear as their own dated rows in the source data) without any change. `TimetableEntry.recurrence_type`'s `weekly`/`fortnightly` values remain unused by the importer — they stay available for manually-created entries, which is a separate, already-supported path.

## Row filtering (your decision)

Only one filter is applied: rows where `Draft = Yes` are skipped entirely (counted in `skipped_rows`). `Type = "Induction (New)"` and `Type = "Enrichment Week"` rows are imported normally, like any other session — no special-casing.

## Import log row-count meanings

For `TimetableImport`:

- `total_rows`: every data row read from the CSV, after the metadata header block (the file's first several lines — timetable name, period, subscription list — are not data rows and are not counted).
- `imported_rows`: rows that resulted in a `TimetableEntry` being created **or** updated. (Known limitation: this doesn't distinguish "new" from "updated" — `TimetableImport` has no `updated_rows` field. Not adding one here since it's not required for #220 to be implementable; worth a follow-up if the UI needs to show that distinction later.)
- `skipped_rows`: rows deliberately not imported for an expected reason — `Draft = Yes`, an unmatched module the user chose to ignore, or a match against a manually-edited entry.
- `error_rows`: rows that couldn't be processed due to a real problem — malformed date/time values, missing required fields, or similar parsing failures. Module-matching outcomes are never errors; they're always either imports or deliberate skips.

## Permission behaviour

- A user can only import timetable entries into Modules they own or are a member of (`ModuleMembership`), same access rule as everywhere else `Module`-scoped data is touched in `academics`.
- Creating a new Module from an unmatched row (per the missing-module decision) makes the importing user its `owner`, same as any other Module creation.
- `TimetableImport.owner` records who ran the import, for audit/history — matches the existing field.

## Manual verification examples

Using real rows from `academics/CSV-TEST-DOC/timetable_2026-07-03.csv`:

1. **Straightforward one-off import.** Row: `"Lecture ","KV4011","Mon","2025-09-29","11:00","Mon","2025-09-29","13:00","2:00","Lecture","Aslam, Nauman, Issac, Biju","CCE1-003 (TLT)",...`. Expect: one `Lecture` titled `"Lecture "` (module KV4011), one `TimetableEntry` with `day_of_week=mon`, `date=2025-09-29`, `start_time=11:00`, `end_time=13:00`, `room="CCE1-003 (TLT)"`, `recurrence_type=one_off`. `imported_rows` increments by 1.
2. **Room change across two imports of the "same" session.** KV4008's Tuesday lecture is at `"CCE1-001 (TLT)"` on `2025-10-01` but at `"SQX 020 (TLT)"` by `2025-11-25` — these are two *different* `TimetableEntry` rows (different dates), not a conflict, since identity is per-`(module, date, start_time, end_time)`. Re-importing the same file twice should not create duplicates or errors for either.
3. **Manually-edited protection.** After import, a user edits the `2025-10-01` KV4008 entry's room by hand (`is_manually_edited` becomes `True`). Re-running the same import: that row is skipped (`skipped_rows` increments), and the user's room correction survives.
4. **Missing module.** A row with module code `KV9999` (not present in any accessible Module) triggers the create-or-ignore prompt. If the user declines, that row is skipped, not errored.
5. **Draft row.** Any row with `Draft = Yes` (none in the current sample, but should be tested with a synthetic row) is skipped and never reaches module-matching at all.

## Update text for #220

Paste into #220 to replace its current scope/description:

---

**Parent epic:** #10 — [Epic] Timetable

**Blocked by:** this decision (now resolved — see `academics/CSV-TEST-DOC/Timetable-CSV-Import-Decisions.md`)

**Goal:** import a MyTimetable CSV export into `academics.TimetableEntry` (never `planning.CalendarEvent`), following the mapping and rules in the linked decision doc.

**Scope:**
- Parse the CSV per the column mapping table (see decision doc) — every column has an explicit destination or ignore rule.
- Match `Module code` to an accessible `Module` (owned or member); on no match, offer to create a new Module or skip the row.
- Create one `Lecture` and one `TimetableEntry` per row, `recurrence_type=one_off`, using `(module, date, start_time, end_time)` as the idempotency key.
- **Schema prerequisite:** add `TimetableEntry.is_manually_edited` (`BooleanField`, default `False`), set on direct user edits, checked by the importer before overwriting an existing match.
- Skip `Draft = Yes` rows.
- Populate `TimetableImport.total_rows` / `imported_rows` / `skipped_rows` / `error_rows` per the definitions in the decision doc.

**Out of scope:** folder/collection-style organisation of imports, weekly/fortnightly pattern detection, distinguishing created-vs-updated row counts.

**Manual verification:** see the five examples in the decision doc's "Manual verification examples" section — cover them as test cases.

---

## What changed as part of this decision

- `academics/CSV-TEST-DOC/Timetable-CSV-Import-Decisions.md` (this file) — the single source of truth for the import decisions.
- `academics/Academics Database implementation.md` — added pointers from `TimetableEntry` and `TimetableImport` to this document.
- No model, migration, or test changes — the `is_manually_edited` field is scoped to #220, not created here.
