# Ceres Issue Management Approach

## Purpose
This document defines how we structure Epics, Features, DB schema work, and tracking in GitHub Issues + Projects for Ceres.

---

## Label Taxonomy

Each issue should have:

1. **One type label**
   - `type:epic`
   - `type:db-epic` (the DB-schema counterpart to a feature epic, e.g. `[Epic] notifications DB Schema`)
   - `type:feature`
   - `type:bug`
   - `type:db-schema`
   - `type:task`

2. **One area label**
   - `area:notifications`
   - `area:files`
   - `area:generalised-search`
   - etc.

3. **One priority label**
   - `priority:p0` = critical / urgent (highest)
   - `priority:p1` = high
   - `priority:p2` = normal (default)
   - `priority:p3` = low (lowest)

Other labels (e.g. `wontfix`) are optional/supporting labels.

---

## Core Structure

## 1) Epics are containers
Use epics for large outcomes spanning multiple issues.

Examples:
- `[Epic] Notifications`
- `[Epic] Files`
- `[Epic] Generalised Search`
- `[Epic] Notifications DB Schema` (when schema work is substantial)

Epic labels:
- `type:epic`
- one `area:*`
- one `priority:*` (usually `p1` or `p2`)

---

## 2) Sub-issues hold execution work
All implementation work should be created as native **Sub-issues** under an epic.

Feature sub-issues:
- `type:feature`

Schema sub-issues:
- `type:db-schema`

Bug sub-issues:
- `type:bug`

Small engineering chores:
- `type:task`

---

## 3) Track progress with native Sub-issues (not markdown checklists)
We use GitHub's native Sub-issues for progress tracking.

- Closing a child issue updates epic progress automatically (e.g. `0/7 -> 1/7`).
- Manual markdown checkboxes in the epic body are optional for acceptance criteria, but not used for execution tracking.

---

## 4) Keep feature and schema planning separate when needed
When schema work is significant, create a dedicated DB epic for that area.

Example:
- `[Epic] Notifications` (product behavior/features)
- `[Epic] Notifications DB Schema` (models/migrations/constraints)

Then link dependencies:
- Feature issues that require schema should be marked as blocked by relevant DB schema issues.

---

## Epic Body Template

Use this template for epic descriptions:

```markdown
## Epic goal
One-paragraph outcome this epic delivers.

## Scope
- In scope: ...
- Out of scope: ...

## Success criteria
- [ ] ...
- [ ] ...

## Dependencies
- Depends on #<issue-number> ...
- External: ...

## Notes
Design decisions, constraints, links.

---
Tracking is managed via native **Sub-issues** below.
```

---

## Dependency Rules

Use issue relationships to reflect sequencing:

- If a feature cannot proceed until schema exists, mark feature issue as **blocked by** schema issue.
- Keep broad umbrella issues (e.g. "Implement main schema"), but add concrete blocker/fix issues as separate children when needed.
- Avoid hiding multiple real blockers inside one mega-issue.

---

## Project Workflow

Project fields should mirror labels where useful:

- **Work Type**: Epic / Feature / Bug / DB Schema / Task
- **Module**: maps to `area:*`
- **Priority**: P0–P3

Recommended automations:

- Item added -> `Status = Backlog`
- Issue closed -> `Status = Done`
- `Status = Done` -> Close issue
- Label-to-field mapping:
  - `type:epic` -> Work Type = Epic
  - `type:feature` -> Work Type = Feature
  - `type:bug` -> Work Type = Bug
  - `type:db-schema` -> Work Type = DB Schema
  - `type:task` -> Work Type = Task

---

## PR Closing Convention

Use in PR descriptions:

- `Closes #<issue-number>`

This auto-closes issues and keeps project state in sync.

---

## Practical Rules of Thumb

- If it spans weeks and many issues -> **Epic**
- If it delivers a user-facing capability -> **Feature**
- If it changes models/migrations/constraints -> **DB Schema**
- If it fixes broken behavior -> **Bug**
- If it's small implementation/admin work -> **Task**

When in doubt:
- Prefer smaller concrete sub-issues over oversized umbrella issues.
- Keep one source of truth for execution: native Sub-issues.
