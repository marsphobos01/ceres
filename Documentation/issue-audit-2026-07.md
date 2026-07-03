# Ceres Repository Issue Audit — July 2026

## Scope

This audit checked every Ceres issue and epic against the canonical Vision, Django app ownership, implemented models and migrations, issue-management rules, and the live native GitHub relationship graph.

The native graph was exported with `gh api` using GitHub's blocked-by, blocking, parent, and sub-issue endpoints. Temporary GitHub Actions workflows were used only to provide an authenticated `gh` environment and were removed from the final review branch after verification.

## Verified result

After correction, the native dependency graph contains:

- **339 unique blocked-by relationships**;
- **201 participating issues**;
- **no duplicate relationships**;
- **no dependency cycles**.

The audit added **119 missing dependencies** and removed **7 incorrect or obsolete dependencies**.

Native parent relationships were explicitly verified for:

- #219 under Academics DB Schema #146;
- #220 and #244 under Timetable #10;
- #236–#242 under Application Foundation #235;
- #245 and #254 under Assignments #13;
- #246 under Generalised Search #25;
- #249 under Dashboard #8;
- #250 under Lecture Hub #12;
- #251 under Notes #14;
- #252 under Notifications #24;
- #253 under Tasks #21;
- #255 under Files #22;
- #256 under Potential Modules #23.

Closed invalid issues #49 and #139–#142 have no native parent.

## Alignment statement

The issue system now aligns with the documentation at the **architecture, ownership, scope, priority, parent, and dependency** levels.

Not every long-term feature issue is already implementation-ready. The issue-management documentation deliberately allows broad backlog placeholders, provided they are refined using `Documentation/feature-workflow.md` before work begins. A placeholder may therefore align with the process without yet containing a complete URL/view/service/test design.

The final verification also found one current code/documentation exception in Notifications. Issues #5 and #6 were reopened to track that remediation, so the inconsistency is represented honestly in the graph rather than being hidden behind completed issues.

## Corrections applied

### Issue quality and scope

- Closed #3 as not planned because per-object access belongs to source apps.
- Reopened #5 and #6 after verifying that the merged implementation did not yet satisfy their acceptance criteria.
- Standardised #7 as a duplicate.
- Closed invalid Potential Modules issues #139–#142.
- Closed out-of-scope Groups search #49.
- Deferred optional `SearchAccessHint` work #210 and #228 as not planned for the current build.

### Notification alignment discovered during final verification

#5 and #6 were automatically closed by a merged PR, but final code/documentation verification found unresolved work:

- `CategoryChoices` exists, but enum member names contain spelling errors and the implementation documentation still describes old module-level dictionaries.
- Notification category current-build versus future scope is not fully documented.
- No notification model tests were added.
- `Reminder` now defines `source_app_label`, but its uniqueness constraint still references `source_app`.
- `Notification` and `MutedContent` still use `source_app`, so the generic reference vocabulary is inconsistent.
- No migration was added for the `Reminder.source_app` to `source_app_label` rename.
- `notifications/Notifications Database implementation.md` still documents the old field and choice definitions.

Those issues remain genuine blockers for notification feature work and must pass `python manage.py check`, migrations, tests, and documentation review before closing again.

### Application Foundation

- Standardised epic #235 and children #236–#242.
- Corrected #236 to use the real `config` package and existing Django apps.
- Added app/type labels and native parent relationships.
- Added missing Foundation ordering: #238 blocks #239 and #240.
- Kept #242 as the final page-level integration gate.

### Timetable import

- Moved #219 to Academics DB Schema #146.
- Moved #220 from Calendar to Timetable #10.
- Corrected #220 to create/update `TimetableEntry`, not duplicate `CalendarEvent` rows.
- Created #244 for CSV mapping, Module matching, recurrence, and idempotency.
- Made #220 depend on #244 and basic Timetable issue #66.

### Missing foundations and decisions

Created:

- #249 — core Dashboard page and widget layout;
- #250 — core Lecture Hub detail page;
- #251 — core Notes pages;
- #252 — Notification Centre;
- #253 — recurring Task schema;
- #254 — Assignment participant schema;
- #255 — Files organisation decision;
- #256 — Goals scope decision.

These are native children of their owning epics and block only the work that genuinely requires them.

### Cross-feature dependencies

- #26–#34 now depend on shared Search foundation #246 and their source feature.
- #50–#58 now depend on Dashboard foundation #249 and their source capability.
- Files features #36–#41 depend on basic Files issue #35.
- Lecture Hub children depend on #250.
- Notes children depend on #251.
- Notification features depend on notification infrastructure plus the source behaviour.
- Assignment planner/progress work depends on #245 and the relevant Task features.
- #80 depends on Assignment participant schema #254.
- #138 depends on recurring Task schema #253.

Incorrect dependencies on `SearchIndexEntry` were removed from internal Files, Notes, and Group Projects search features.

### Epic architecture

Open Modules, Assignments, Friends, Group Projects, Tasks, Notifications, and Search epics were updated where their descriptions contradicted implemented architecture.

The corrected rules include:

- Module sharing uses `ModuleMembership`;
- Lecture navigation does not invent next/previous foreign keys;
- Assignments compose with Tasks through `TaskLink`;
- Study Groups belong to `collaboration`;
- Messaging is optional for core Group Projects;
- source apps retain ownership of Notes, Files, Tasks, and permissions.

## Remaining explicit decisions and remediation

The audit is complete, but these issues intentionally remain open:

- **#5:** finish notification category naming, scope documentation, migrations where needed, and tests;
- **#6:** make notification source-reference names consistent, repair the invalid Reminder constraint, add the required migration, tests, and documentation updates;
- **#244:** exact timetable CSV mapping and duplicate rules;
- **#245:** Assignment lifecycle versus Task status/progress;
- **#253:** recurring Task persistence and history;
- **#254:** group Assignment participant relationship;
- **#255:** tag-only versus folder/collection Files organisation;
- **#256:** Goals as Dashboard capability, promoted module, or deferred work.

These are not audit omissions. They are real product, schema, or remediation tasks represented as blockers.

## Description policy

Issue descriptions are governed by `Documentation/issue-management-approach.md` and `Documentation/feature-workflow.md`.

Before implementation, a feature must define:

- observable user behaviour;
- scope and exclusions;
- exact blockers;
- primary app ownership;
- likely URL/view/service/model/permission/UI responsibilities;
- automated tests;
- manual verification.

The original generic feature descriptions may remain as backlog placeholders, but they are not implementation-ready until refined for a milestone.

## Label policy

Every active implementation issue should have:

1. one `type:*` label;
2. one `priority:p0`–`priority:p3` label;
3. one `area:*` label;
4. one `app:*` label where a primary Django app exists.

`area:*` describes the product capability. `app:*` describes code ownership. P3 is used for optional, COULD, deferred, or future work.

## Dependency policy

Native blocked/blocked-by relationships are the readiness source of truth.

- Page features wait for #242.
- Cross-app integrations wait for working source features, not only schemas.
- Search integrations wait for #246 and their source feature.
- Dashboard widgets wait for #249 and their source capability.
- Notification integrations wait for infrastructure and source behaviour.
- Decision issues block only the features governed by that decision.

Issue bodies explain why a relationship exists; they should not manually duplicate the complete graph.

## Ongoing workflow

Before each milestone:

1. Start from `-is:blocked`.
2. Exclude epics and intentionally deferred work.
3. Narrow by milestone, priority, and area.
4. Refine candidate issues using `feature-workflow.md`.
5. Confirm native parent/blocker relationships and app ownership.
6. Begin work only when the issue is understandable and implementable.

## Status

**Complete.**

The issue inventory, epic structure, labels, native dependency graph, native parent graph, and major architecture consistency have been audited. Unambiguous defects were corrected; genuine unresolved decisions and detected remediation work are represented by explicit blocking issues.