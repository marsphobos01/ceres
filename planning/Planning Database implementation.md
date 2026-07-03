# planning — Implemented Database Schema

This document describes the models as actually implemented in `planning/models.py`, and how to use them. Unlike `Planning Database plan.md`, which describes the intended design, this reflects the current code. Update this file whenever the models change.

## Differences from the earlier design plan

Issue references for this app haven't been supplied yet, so the notes below describe each gap against `Planning Database plan.md` only, without attributing it to a specific epic or issue decision. (See `content`, `academics`, and `collaboration`'s implementation docs for the pattern once references are available — those cite the epic and per-model schema issue that scoped each divergence.)

- `TaskLink` and `Deadline` both implement their generic links with a real `content_type`/`object_id` `GenericForeignKey`, rather than the plan's separate app-label/object-type text fields — a closer match to normal Django practice than the plan described.
- `Deadline` has no uniqueness constraint ensuring the source object is unique when the deadline mirrors another app's object, and has no `reminder enabled` boolean flag, both of which the plan calls for.
- `StudySessionsParticipant.response` choices are `Invited`, `Accepted`, `Declined` — the plan's `attended` status is not present. The plan also describes separate `invited` and `responded` timestamps; the implementation only has a single `created_at`. (The plan's "one participant per session and user" rule is now enforced by the `unique_study_session_participant` constraint.)
- `Goal` is intentionally absent, matching the plan's explicit note that it isn't a scoped table yet — this isn't a gap, just confirmation that the models correctly haven't gotten ahead of an unwritten schema issue.

These may be considered as future schema enhancements if required by feature implementation. The "Known open items" section further down covers implementation-quality issues (naming, inconsistent `max_length`) that are separate from plan divergence.

## CalendarEvent

A single calendar entry owned by a user.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='events'` — access via `user.events` |
| `title` | `CharField(100)` | Required |
| `description` | `TextField` | Required |
| `start` | `DateTimeField` | Required |
| `end` | `DateTimeField` | Required |
| `allday` | `BooleanField` | No default — must be supplied explicitly on every create |
| `colour` | `CharField(6)`, nullable | Optional; expected to hold a hex colour code |
| `location` | `CharField(100)` | Required |
| `recurrence_type` | `CharField(11)`, choices, nullable | Choices from nested `RecurrenceTypeChoices`: None, Daily, Weekly, Biweekly, Monthly |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- `calendarevent_end_gt_start` — `CheckConstraint` requiring `end` to be strictly after `start`.

**Usage:** `start`/`end` must be supplied in the correct order — the constraint will reject a save otherwise. `recurrence_type` is stored but nothing currently reads it; there's no recurrence-expansion logic yet.

## Task

A user's task, optionally nested under a parent task.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='tasks'` — access via `user.tasks` |
| `title` | `CharField(100)` | Required |
| `description` | `TextField` | Required |
| `priority` | `CharField(100)`, choices | Nested `PriorityChoices`: High (`H`) / Medium (`M`) / Low (`L`) / Urgent (`U`). `max_length=100` is oversized for single-character codes |
| `status` | `CharField(100)`, choices | Nested `StatusChoices`: Not Started (`NS`) / In Progress (`IP`) / Completed (`CP`) / Canceled (`CN`). Same oversized `max_length` note |
| `due_date` | `DateTimeField` | Required |
| `parent_task` | `ForeignKey("self")`, nullable | `on_delete=CASCADE`, `related_name='children'` — deleting a parent task cascades to delete all its children recursively |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField(auto_now=True)`, nullable | Auto-set on every save (column remains nullable for pre-existing rows) |

**Constraints:** none implemented.

**Usage:** a task's subtasks are `task.children.all()`. Note the status codes: `CP` = Completed, `CN` = Canceled (earlier drafts used `CA`/`CD`, which read backwards — any dev data saved with those codes should be recreated or updated).

## TaskAssignment

Links a `Task` to the user(s) assigned to work on it.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `task` | `ForeignKey(Task)` | `related_name='assignments'` — access via `task.assignments` |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='task_assignments'` |
| `assigned_by` | `ForeignKey(AUTH_USER_MODEL)`, nullable | `related_name='given_task_assignments'` |
| `assigned_date` | `DateTimeField`, nullable | |

No `created_at`/`updated_at` on this model, unlike the others in this file.

**Constraints:**
- `task_assignment_unique` — unique on `(task, user)`; a user can only be assigned to a given task once.

**Usage:** a task's assignees are `task.assignments.all()`; a user's assignments are `user.task_assignments.all()`.

## TaskLink

Generic link from a `Task` to any other object in the project (Assignment, Lecture, RevisionTopic, etc.), via Django's `contenttypes` framework.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `task` | `ForeignKey(Task)` | `related_name='links'` — access via `task.links` |
| `content_type` | `ForeignKey(ContentType)` | Required |
| `object_id` | `PositiveIntegerField` | Required |
| `linked_object` | `GenericForeignKey('content_type', 'object_id')` | Convenience accessor; not a real column |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `task_link_unique` — unique on `(task, content_type, object_id)`; a task can't be linked to the same object twice.

**Usage:** `content_type`/`object_id` are required here — unlike the same generic-reference pattern on `Deadline` below, where both are nullable. Requiring them on `TaskLink` seems correct (a link without a target doesn't mean anything); worth double-checking whether `Deadline`'s optionality is intentional.

## StudySession

A scheduled or informal study session, optionally tied to a module.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='sessions'` |
| `module` | `ForeignKey(academics.Module, on_delete=CASCADE)`, nullable | `related_name='sessions'` (added in `0003_studysession_module.py`) — shares the name `owner` also uses for its `related_name`, but since they target different models (`User` vs `Module`) there's no clash: `user.sessions` and `module.sessions` are distinct reverse managers |
| `title` | `CharField(100)`, nullable | Optional |
| `start` | `DateTimeField` | Required |
| `end` | `DateTimeField`, nullable | Optional |
| `location` | `CharField(100)`, nullable | Optional |
| `notes` | `TextField` | Required |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- `studysession_end_gt_start` — `CheckConstraint` requiring `end` to be after `start`. Since `end` is nullable, a session saved with no `end` automatically satisfies the constraint (a `NULL` comparison doesn't fail a Postgres `CHECK`) — sessions with no end time bypass this rule. Worth confirming that's the intended behavior rather than an oversight.

**Usage:** `module` is optional, so ad hoc study sessions not tied to a specific module are valid.

## StudySessionsParticipant

A user's invitation/response status for a `StudySession`.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `session` | `ForeignKey(StudySession)` | `related_name='participants'` — access via `session.participants` |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='study_session_participations'` |
| `response` | `CharField(100)`, choices | Nested `ResponseChoices`: Invited/Accepted/Declined. Same oversized `max_length` note as `Task.priority`/`Task.status` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_study_session_participant` — unique on `(session, user)`; the same user can't be added to a session twice.

**Usage:** a session's participants are `session.participants.all()`.

## Deadline

A due date, optionally linked to any object via `contenttypes`.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='deadlines'` |
| `title` | `CharField(100)` | Required |
| `due` | `DateTimeField` | Required |
| `content_type` | `ForeignKey(ContentType)`, nullable | Optional — unlike `TaskLink.content_type`, which is required |
| `object_id` | `PositiveIntegerField`, nullable | Optional |
| `links_to` | `GenericForeignKey('content_type', 'object_id')` | Same generic-reference pattern as `TaskLink`, but named differently (`linked_object` there vs. `links_to` here) — worth standardizing on one name across the app |
| `is_dismissed` | `BooleanField` | Default `False` |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField` | Auto-set on every save |

**Constraints:** none implemented.

**Usage:** `content_type`/`object_id` are both optional, so a `Deadline` can exist without pointing at anything. Confirm that's intentional — a deadline that isn't a deadline *for* anything is a bit ambiguous — before building logic on top of it.

## TimetableImport

A record of a bulk timetable import job (e.g. an uploaded timetable file), tracking its processing status and row-level outcomes. This model isn't mentioned in `Planning Database plan.md` at all — it doesn't correspond to any of the plan's example tables.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='timetable_imports'` |
| `filename` | `CharField(100)` | Required |
| `status` | `CharField(21)`, choices | Nested `Status`: `pending`, `processing`, `completed`, `completed_with_errors`, `failed`; default `pending` |
| `total_rows` | `PositiveIntegerField` | Default `0` |
| `imported_rows` | `PositiveIntegerField` | Default `0` |
| `skipped_rows` | `PositiveIntegerField` | Default `0` |
| `error_rows` | `PositiveIntegerField` | Default `0` |
| `error_detail` | `JSONField` | Blank allowed; default `list` — expected to hold structured per-row error info |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:** none implemented — nothing enforces `imported_rows + skipped_rows + error_rows` against `total_rows`.

**Usage:** created when a user uploads a timetable file for bulk import (presumably feeding `academics.TimetableEntry`/`Lecture` rows, though nothing in this app's code links the two directly). `status` tracks the job's lifecycle; `error_detail` should hold enough structure to show the user what went wrong per row. Since this model doesn't appear in the plan, treat its scope and any related schema issue as unconfirmed rather than assuming this documents an agreed design.

## Known open items across this app

- `updated_at` is absent on `TaskAssignment` and `StudySessionsParticipant`, unlike the other models in this file.
- Several `choices` fields (`Task.priority`, `Task.status`, `StudySessionsParticipant.response`) use `max_length=100` for one-to-two-character codes.
- Two generic-relation patterns (`TaskLink.linked_object`, `Deadline.links_to`) use different accessor names for the same `contenttypes` pattern.
- Required `description` (on `Task` and `CalendarEvent`) and required `notes` (on `StudySession`) force text on every row; other apps make long-text fields optional.
- `TimetableImport` has no constraint tying `imported_rows`/`skipped_rows`/`error_rows` to `total_rows`, and nothing in `planning` links an import job to the `academics` rows it presumably creates.

Resolved in the 0005 migration pass: the `"Dayly"` label typo, the `ResponceChoices` class-name typo, the backwards `CA`/`CD` status codes, the duplicated `created_at` on `Deadline`, the missing `blank=True` on nullable fields (including `parent_task`, so admin forms no longer demand a parent for every task), the field-like `related_name`s, the non-updating `Task.updated_at`, and the missing uniqueness constraint on `StudySessionsParticipant`.

## How the models relate

```
User (Django auth)
  - events -> CalendarEvent (1:M)
  - tasks -> Task (1:M)
  - task_assignments / given_task_assignments -> TaskAssignment
  - sessions -> StudySession (1:M)
  - study_session_participations -> StudySessionsParticipant
  - deadlines -> Deadline (1:M)

Task
  - children -> Task (1:M, self-referencing via parent_task)
  - assignments -> TaskAssignment (1:M)
  - links -> TaskLink (1:M)

StudySession
  - participants -> StudySessionsParticipant (1:M)

TaskLink / Deadline
  - linked_object / links_to -> any model, via contenttypes (ContentType + object_id)

TimetableImport
  - owner -> User (M:1); not otherwise linked to any other model in this app
```
