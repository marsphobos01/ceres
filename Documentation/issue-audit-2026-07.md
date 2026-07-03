# Ceres Repository Issue Audit — July 2026

## Scope

This audit checked Ceres issues and epics against:

- the canonical Vision;
- Django app ownership;
- implemented models and migrations;
- issue-management and contributor workflows;
- GitHub's native blocked/blocked-by graph;
- GitHub's native parent/sub-issue graph.

The native graph was inspected and corrected with authenticated `gh api` calls. Temporary workflow files used for that inspection were removed or reset and were not merged into `main`.

## Verified audit baseline

The corrected dependency graph contained:

- **339 unique blocked-by relationships**;
- **201 participating issues**;
- **no duplicate relationships**;
- **no dependency cycles**.

The original audit added **119 missing dependencies** and removed **7 incorrect or obsolete dependencies**.

## Structural corrections completed

The audit corrected or standardised:

- Application Foundation #235–#242;
- Timetable import ownership and mapping;
- Dashboard, Lecture Hub, Notes, Notifications and Search foundation issues;
- Assignment/Task ownership;
- Assignment participants;
- Files organisation scope;
- recurring Task persistence planning;
- Goals scope;
- invalid Potential Modules and out-of-scope Search children;
- cross-app source-feature dependencies.

Native parent relationships were verified for the relevant feature and DB epics. Closed invalid issues #49 and #139–#142 have no active parent.

## Post-audit resolutions

### Assignment and Task state — resolved

#245 defined the ownership boundary and PR #260 implemented it:

- `Assignment.submission_status` stores only academic submission state;
- planning Tasks remain the source of work state, priority and progress;
- no duplicate Assignment priority/progress fields were added.

### Files organisation — resolved

#255 chose tag-and-context-link organisation for the first release:

- `FileTag` and `FileLink` are the organisation mechanism;
- folders, collections, nesting and move operations are deferred;
- #36 now describes the implementable tag/link user journey.

### Goals scope — resolved

#256 and PR #264 removed Goals from the current Dashboard Vision scope:

- Goals remain only under #23 Potential Modules;
- #8 no longer promises a Goals widget;
- #57 is closed as not planned for the current build;
- no Goal model belongs in `core`.

### Timetable CSV decisions — resolved, with a new schema prerequisite

#244 and PR #265 defined the import mapping and idempotency rules:

- MyTimetable rows import as one-off dated entries;
- Module matching uses accessible `Module.code` values;
- import identity is `(module, date, start_time, end_time)`;
- manually edited matches must never be overwritten.

#267 now tracks the required `TimetableEntry.is_manually_edited` field and natively blocks #220. #220 has been updated with the complete implementation contract.

### Assignment participants — implemented, pending real verification

#254 completed the design decision. #261 and PR #263 added:

- `AssignmentParticipant`;
- the `Assignment.participants` through relationship;
- validation and permission helpers;
- migration, admin integration, tests and documentation.

#261 is reopened until the real PostgreSQL migration/check/test commands pass.

### Recurring Task persistence — partially implemented

#253 and PR #266 added the recurrence models, fields, migration and constraints.

#253 is reopened because the original acceptance criteria also require:

- `TaskRecurrence` admin registration;
- recurrence model tests;
- Planning implementation documentation;
- successful PostgreSQL migration/check/test verification.

#253 natively blocks #138 until those remaining items are complete.

### Notification schema — implemented, pending real PostgreSQL verification

#5 and #6 were implemented by PR #259:

- category enum names and scope were standardised;
- source-reference names now use `source_app_label` consistently;
- uniqueness constraints were repaired;
- data-preserving migrations and tests were added;
- Notifications implementation documentation was updated.

Both issues are reopened until the real project commands pass against PostgreSQL, including the existing migration history.

## Current stabilisation issues

These are the remaining issues to finish before declaring the codebase, documentation and issue tracker fully verified:

| Issue | Remaining work |
| --- | --- |
| #5 | Run Notifications migration/check/tests against PostgreSQL and record success |
| #6 | Verify source-reference migrations and constraints on clean and existing PostgreSQL databases |
| #253 | Add recurrence admin registration, model tests and Planning documentation; run verification |
| #261 | Run Academics migration/check/tests against PostgreSQL and record success |
| #267 | Add `TimetableEntry.is_manually_edited`, migration, tests, admin and documentation |

#244, #245, #254, #255 and #256 are correctly closed because their decisions are complete and any remaining implementation or verification work has an explicit follow-up issue.

## Manual verification commands

Run from an up-to-date local checkout configured to use PostgreSQL:

```bash
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test notifications
python manage.py test academics
python manage.py test planning
```

After each successful group, paste the command output or a concise success record into the relevant issue before closing it.

A clean-database migration run is especially important for #6. Where possible, also run against an existing development database containing the earlier Notifications migrations.

## Description and readiness policy

A feature is ready to start only when:

- native blockers are closed;
- its parent and app ownership are correct;
- its user behaviour and boundaries are refined;
- required schema and verification issues are complete.

Broad long-term feature issues may remain backlog placeholders, but they must be refined with `Documentation/feature-workflow.md` before implementation.

## Status

**Audit complete; stabilisation verification in progress.**

The issue architecture and dependency graph are aligned. The remaining known code/documentation verification work is explicitly represented by #5, #6, #253, #261 and #267.