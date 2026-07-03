# Ceres Issue Management Approach

## Purpose

This document defines how Ceres structures Epics, Features, DB schema work, Tasks, Bugs, dependencies, and GitHub Project tracking.

## Label taxonomy

Every active implementation issue should have:

1. **Exactly one type label**
   - `type:epic`
   - `type:db-epic`
   - `type:feature`
   - `type:bug`
   - `type:db-schema`
   - `type:task`

2. **Exactly one priority label**
   - `priority:p0` — critical or release-blocking
   - `priority:p1` — high
   - `priority:p2` — normal/default
   - `priority:p3` — low, optional, COULD, or future

3. **One product-area label**
   - Examples: `area:calendar`, `area:assignments`, `area:generalised-search`, `area:foundation`

4. **One code-ownership label where a clear owning Django app exists**
   - Examples: `app:planning`, `app:academics`, `app:search`, `app:core`

`area:*` and `app:*` are different. An Assignment feature uses `area:assignments` but is primarily owned by `app:academics`. A cross-app feature should still identify its primary owner and list other app dependencies in its body.

Holding-area epics may omit an app label. Supporting labels such as `documentation`, `duplicate`, or `wontfix` are optional.

Do not invent alternative priority labels such as `priority:optional`; use `priority:p3` and explain why.

## Core structure

### Epics are outcome containers

Use an epic for a large product or engineering outcome spanning several executable issues.

Examples:

- `[Epic] Calendar`
- `[Epic] Generalised Search`
- `[Epic] Application Foundation`
- `[Epic] Notifications DB Schema`

Epics normally have:

- `type:epic` or `type:db-epic`;
- one priority;
- one area or app ownership label;
- native Sub-issues for execution work.

### Sub-issues hold execution work

- User-facing capability: `type:feature`
- Model/migration/constraint change: `type:db-schema`
- Broken behaviour: `type:bug`
- Engineering, documentation, integration, or architecture chore: `type:task`

Use native **Sub-issues** for progress. Markdown checklists may describe acceptance criteria but must not duplicate the child issue list as the execution source of truth.

### Feature and schema planning are separate

When schema work is significant, create a DB epic and concrete schema children. Feature issues should be blocked by the exact schema issues they require, not merely by a vague app-level statement.

Schema completion only means a feature can safely build against the data shape. It does not guarantee that shared application foundations or source features exist.

## Description standards

### Epic template

```markdown
## Epic goal
One-paragraph outcome.

## Scope
- In scope: ...
- Out of scope: ...

## Success criteria
- [ ] ...

## Dependencies
- Depends on #...
- External: ...

## Notes
Important ownership and architecture decisions.

---
Tracking is managed via native **Sub-issues** below.
```

### Feature template

A feature may begin as a short backlog placeholder, but **must be refined before implementation** using `Documentation/feature-workflow.md`.

```markdown
## Parent epic
#...

## User behaviour
Given ...
When ...
Then ...

## Scope
- ...

## Out of scope
- ...

## Dependencies
- Blocked by #... because ...

## Implementation checklist
- [ ] URL/view or entry point
- [ ] Validation
- [ ] Service/business logic
- [ ] Model queries/changes
- [ ] Permission checks
- [ ] UI and feedback states
- [ ] Automated tests
- [ ] Documentation

## Done when
- [ ] Observable behaviour works
- [ ] Permission and failure cases pass

## Manual verification
1. ...
```

### Task template

```markdown
## Context or purpose
...

## Scope
- ...

## Out of scope
- ...

## Dependencies
- ...

## Done when
- [ ] ...
```

### DB schema template

```markdown
## Model / App / Parent epic
...

## Purpose
...

## Fields
...

## Constraints and boundaries
...

## Dependencies
...

## Done when
- [ ] Model and migration
- [ ] Admin registration
- [ ] Tests/checks
- [ ] Implementation documentation
```

## Dependency rules

Native GitHub blocked/blocked-by relationships control readiness.

- Block a feature on exact schema issues it requires.
- Block page-based work on the Application Foundation integration gate (#242) until it closes.
- Block cross-app integrations on working source features, not only source schemas.
- A search indexer should wait for both the shared search foundation and the source feature/data contract.
- Dashboard widgets should wait for the source capability they aggregate.
- Notifications should wait for both notification infrastructure and the source event behaviour.
- Avoid using blockers to express preference only; a blocker means the later issue cannot be completed coherently yet.
- Avoid exhaustive dependency lists duplicated in bodies. Explain important reasoning in prose and maintain the actual graph natively.
- Split backend-only work from UI delivery where the backend can be independently implemented and tested.

## Ready to Start workflow

Use:

```text
-is:blocked
```

Then narrow by milestone, priority, and area. Exclude epics when selecting implementation work.

An issue is truly ready to start only when:

- native blockers are closed;
- it is in the current product slice/milestone;
- its description is refined and actionable;
- app ownership and permissions are understood.

## Priority and product scope

The canonical Ceres Vision defines committed scope. Anything not listed there requires explicit promotion before implementation.

Use P3 for COULD/future work unless deliberately promoted. Priority does not replace blockers: a P1 issue may be blocked, while a P3 issue may be technically ready.

## Project workflow

Project fields may mirror labels:

- Work Type: Epic / DB Epic / Feature / Bug / DB Schema / Task
- Module: product area
- Priority: P0–P3
- Status: Backlog / Ready / In Progress / Review / Done

Recommended automation:

- new item → Backlog;
- issue closed → Done;
- Done → close issue;
- label-to-field mapping for type and priority.

Do not create a manually maintained Readiness field. GitHub's native blocker graph is the readiness source of truth.

## PR closing convention

Use:

```text
Closes #123
```

This closes the issue and updates project progress after merge.

## Practical rules

- If it spans weeks and many issues → Epic.
- If it delivers observable user behaviour → Feature.
- If it changes models/migrations/constraints → DB Schema.
- If it fixes broken behaviour → Bug.
- If it is an engineering, architecture, integration, or documentation step → Task.
- Prefer small coherent issues over mega-issues.
- Update open epic/feature wording after architecture decisions; do not leave resolved decisions described as undecided.
- Use `Documentation/issue-audit-2026-07.md` as the current backlog audit reference.