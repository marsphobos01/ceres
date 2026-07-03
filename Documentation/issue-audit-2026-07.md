# Ceres Repository Issue Audit — July 2026

## Purpose

This audit reviews the Ceres issue system against:

- the canonical Ceres Vision;
- Django app ownership rules;
- the implemented database schema;
- the issue-management approach;
- the contributor and feature-development workflows.

It covers epic scope, child issues, labels, description quality, dependencies, stale decisions, and whether issues are actionable.

## Important limitation

The GitHub connector used for this audit could read issue bodies, labels, states, code, documentation, and pull requests, but did not reliably expose GitHub's native blocked/blocked-by graph. Native relationships must therefore be spot-checked in the GitHub UI. This audit treats native relationships as the execution source of truth and does not replace them with prose dependency lists.

## Overall assessment

The repository has a strong structural base:

- feature work is grouped under epics;
- database work is separated into DB epics and schema issues;
- app ownership is generally well defined;
- completed schema work has migrations and implementation documentation;
- the Ready to Start workflow is based on native dependency relationships.

The main weakness is the transition from schema planning to feature delivery. Most original feature children were generated from feature-list headings and use boilerplate descriptions. They identify a capability but do not yet define observable behaviour, exact prerequisites, implementation responsibilities, permissions, tests, or manual verification.

Those issues are valid backlog placeholders, but they must be refined using `Documentation/feature-workflow.md` before a branch is started.

## Corrections applied during the audit

### Legacy schema issues

- #3 was closed as not planned. `UserContentPermission` remains an account-level default sharing rule; per-object access belongs to source apps.
- #5 was updated to reflect the current notification category implementation and its remaining TextChoices/scope work.
- #6 was updated to acknowledge that source-reference fields and constraints exist; remaining work is naming consistency, tests, and documentation.
- #7 received standard type, priority, and app labels and remains a duplicate.

### Invalid backlog items

- #139–#142 were closed as not planned. They incorrectly treated `[Epic] Potential Modules` as a university-module marketplace. Epic #23 is a holding area for future Ceres product areas.
- #49 Groups for Generalised Search was closed as not planned for the current build because Groups are not in the canonical Search feature list.

### Application Foundation

- #235 was rewritten using the standard epic structure.
- #236 now uses the real project package (`config`) and real Django apps rather than treating Calendar, Tasks, Modules, and other product areas as separate app packages.
- #236, #238, #239, #241, and #242 are technical tasks rather than user-facing features.
- #237 and #240 remain user-facing features.
- Foundation child issues now carry relevant app ownership labels.
- #242 now describes a dependency rule and integration gate rather than maintaining a stale exhaustive downstream checklist.

### Timetable import

- #219 now reflects its merged ownership in `academics` and its relationship to `TimetableEntry`.
- #220 was moved conceptually from Calendar to Timetable and now imports `TimetableEntry` records rather than creating duplicate `CalendarEvent` records.
- #244 was created to resolve CSV mapping, Module matching, recurrence, and idempotency before implementation.

### Missing feature foundations

- #245 was created to resolve Assignment status/progress ownership between `Assignment` and linked Tasks.
- #246 was created for the unified search query service and results interface required before source-specific search integrations are independently useful.

## High-priority findings still requiring follow-up

### 1. Generic feature descriptions need refinement

Most feature children in the original #26–#142 block use a template similar to:

```text
Deliver <capability> as part of <epic>.
Confirm the required DB schema exists.
Respect app ownership.
```

That is consistent but not actionable. Before implementation, each selected issue must gain:

- a user journey;
- explicit in/out scope;
- exact blockers;
- likely URL/view/service/model/permission/UI responsibilities;
- automated test expectations;
- manual verification steps.

Do not attempt to mass-invent detailed implementation for every feature now. Refine an issue when it enters the current milestone or is about to be selected.

### 2. Native dependency graph requires UI verification

Spot-check the native graph for:

- every page-based feature being blocked by #242 until Foundation integration completes;
- source-specific search features being blocked by #246 and their source feature;
- #220 being blocked by #244 and the basic Timetable UI;
- dashboard widgets being blocked by the source features they aggregate;
- notifications being blocked by both notification infrastructure and the source event feature;
- cross-app integrations being blocked by working source features, not only completed schemas.

Avoid maintaining duplicate dependency lists in issue bodies. Bodies should explain why; native relationships should control readiness.

### 3. Modules epic is stale against the implemented schema

#11 currently mentions credit weighting, lecturer fields, explicit next/previous Lecture model references, and no sharing. The implemented schema instead has:

- Module title, code, description, colour, academic year, and semester;
- ModuleMembership for owner/member/viewer access;
- Lecture records without next/previous foreign keys.

Update #11 and #70–#73 during refinement. Ordered lecture navigation may be implemented by date/order queries without claiming a linked-list schema that does not exist.

### 4. Assignment and Task state needs one source of truth

#13 and #21 still describe composition versus inheritance as undecided, but `TaskLink` already establishes composition. #245 now tracks the remaining real question: whether `Assignment.status` represents a distinct academic submission lifecycle or duplicates Task state.

Assignment feature issues should remain blocked until #245 defines status, priority, progress, and initial TaskLink behaviour.

### 5. Friends and Study Groups ownership needs wording updates

#18 still describes profile and group ownership as undecided. Current architecture is:

- profiles and direct friendships: `accounts`;
- StudyGroup and group membership: `collaboration`;
- shared Modules: queried from `academics`;
- shared Study Sessions: queried from `planning`.

#117 should be refined as a cross-app collaboration feature rather than implying that StudyGroup is owned by `accounts`.

### 6. Group Projects contains resolved or optional dependencies

#20 should be updated so:

- tasks are linked through the shared planning Task/TaskLink system;
- linked group conversation is optional, because Messaging is not part of the canonical Group Projects feature list;
- Messaging does not block the core Group Projects workspace;
- notes and files remain source-app-owned links.

### 7. Notification epic scope exceeds the canonical feature list

#24 currently includes message notifications, study-session invitations, a notification centre, source muting, delivery tracking, and text/Discord channels. The canonical Vision explicitly lists assignment, lecture, calendar, group, friend-request notifications, and configurable preferences.

Infrastructure may support later categories, but #24 should distinguish:

- committed user-facing notification features;
- required shared notification infrastructure;
- future integrations and delivery channels.

#5 now tracks the immediate category-scope decision.

### 8. Files epic and schema differ

#22 says version history is out of scope, but `FileVersion` exists. It also promises individual, group, and link sharing, while the current `FileShare` schema only grants access to a user.

Refine #35–#41 so the first implementation matches current schema. Create separate schema/feature issues before promising group or public-link sharing.

### 9. Closed DB epics contain historical wording drift

Several completed DB epic bodies reference the retired `ceres-git-flow.md`, outdated names, or decisions that changed during implementation. Examples include:

- #148 incorrectly referring to `#18 Flashcards` even though #18 is Friends;
- #151 using `DashboardWidgetSetting` while the implemented model is `DashboardWidget`;
- DB epic titles using inconsistent app capitalisation;
- old source-reference terminology.

Closed issue history does not need a full rewrite to run the project. The implementation documents and database overview should remain the current source of truth. Correct closed bodies only where the stale text is likely to mislead future work.

### 10. Canonical Vision contains a Goals contradiction

Goals appear in the Dashboard feature list but are also listed as a Potential Future Module. Until this is resolved:

- Dashboard Goals should remain low priority;
- it must not create an accidental Goal schema inside `core`;
- a full Goals module must be promoted through #23 before implementation.

## Label standardisation

Every active implementation issue should have:

1. exactly one `type:*` label;
2. exactly one `priority:p0`–`priority:p3` label;
3. one `area:*` product-area label;
4. one `app:*` code-ownership label when a clear owning Django app exists.

`area:*` and `app:*` are different:

- `area:assignments` describes the product capability;
- `app:academics` describes where the primary code belongs.

Cross-cutting issues may have one primary owning app plus dependency notes. Holding-area epics may omit an app label.

Do not create alternative priority labels such as `priority:optional`; use `priority:p3` and explain the reason in the issue.

## Priority review

The following categories should generally be P3 until explicitly promoted:

- Potential Modules candidates;
- Messaging;
- Revision;
- mathematical notation;
- whiteboard exporting;
- calendar colour categories and academic-event distinctions;
- lecture discussions;
- Dashboard Goals, assignment progress, and study reminders where classified as COULD.

Priority does not replace dependencies. A P1 issue can still be blocked, and a P3 issue can still be technically ready.

## Standard description policy

### Epics

Use the standard sections:

- Epic goal
- Scope
- Success criteria
- Dependencies
- Notes
- native Sub-issues statement

### Features

Before implementation, use:

- Parent epic
- User behaviour
- Scope
- Out of scope
- Dependencies
- Implementation checklist
- Done when
- Manual verification

### Tasks

Use:

- Context/Purpose
- Scope
- Out of scope
- Dependencies
- Done when

### DB schema

Use:

- Model/App/Parent epic
- Purpose
- Fields
- Constraints and boundaries
- Dependencies
- Done when

## Ongoing audit workflow

Before each milestone:

1. Select candidate issues from `-is:blocked`.
2. Remove epics and out-of-scope/P3 work unless intentionally promoted.
3. Refine selected features using `feature-workflow.md`.
4. Verify native blockers in the GitHub UI.
5. Confirm labels and app ownership.
6. Compare scope with the canonical Vision.
7. Add the issue to the milestone only after it is understandable and implementable.

After every architecture or schema decision:

1. update affected open epics/features;
2. update implementation documentation;
3. add or remove native blockers;
4. avoid leaving “decide later” language after the decision has been made.

## Audit status

This audit corrected unambiguous defects and created follow-up issues for unresolved design decisions. It deliberately did not fabricate detailed implementations for the entire long-term backlog. The remaining generic feature issues are accepted as placeholders but are not implementation-ready until refined.