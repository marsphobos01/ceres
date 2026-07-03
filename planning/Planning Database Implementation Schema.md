# planning — Implemented Database Schema

This document describes the models as actually implemented in `planning/models.py`, and how to use them. There is no separate plan document for this app yet (unlike `accounts`, which has `Accounts Database plan.md`) — this file is the only record of the design for now, so keep it updated whenever the models change.

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
| `recurrence_type` | `CharField(11)`, choices, nullable | Choices from nested `RecurrenceTypeChoices`: None, Daily (label is currently misspelled `"Dayly"`), Weekly, Biweekly, Monthly |
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
| `priority` | `CharField(100)`, choices | Nested `PriorityChoices`: High/Medium/Low/Urgent. `max_length=100` is oversized for single-character codes |
| `status` | `CharField(100)`, choices | Nested `StatusChoices`: Not Started/In Progress/Completed/Canceled. Same oversized `max_length` note |
| `due_date` | `DateTimeField` | Required |
| `parent_task` | `ForeignKey("self")`, nullable | `on_delete=CASCADE`, `related_name='children'` — deleting a parent task cascades to delete all its children recursively |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField`, nullable | Not `auto_now` — unlike every other model in this file, this field will not update itself on save; it must be set manually if it's meant to be used |

**Constraints:** none implemented.

**Usage:** `parent_task` uses `null=True` (so top-level tasks with no parent are valid) but not `blank=True`, so forms/admin will still treat it as a required field unless that's added. A task's subtasks are `task.children.all()`.

## TaskAssignment

Links a `Task` to the user(s) assigned to work on it.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `task` | `ForeignKey(Task)` | `related_name='task_assignment'` — reads as singular though a task can have several assignments; `task_assignments` would read more naturally |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='task_assigned_to_user'` |
| `assigned_by` | `ForeignKey(AUTH_USER_MODEL)`, nullable | `related_name='task_assigned_by_user'` |
| `assigned_date` | `DateTimeField`, nullable | |

No `created_at`/`updated_at` on this model, unlike the others in this file.

**Constraints:**
- `task_assignment_unique` — unique on `(task, user)`; a user can only be assigned to a given task once.

**Usage:** a task's assignees are `task.task_assignment.all()`.

## TaskLink

Generic link from a `Task` to any other object in the project (Assignment, Lecture, RevisionTopic, etc.), via Django's `contenttypes` framework.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `task` | `ForeignKey(Task)` | `related_name='task_link'` — same singular-name note as `TaskAssignment` |
| `content_type` | `ForeignKey(ContentType)` | Required |
| `object_id` | `PositiveIntegerField` | Required |
| `linked_object` | `GenericForeignKey('content_type', 'object_id')` | Convenience accessor; not a real column |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `task_link_unique` — unique on `(task, content_type, object_id)`; a task can't be linked to the same object twice.

**Usage:** registered in `planning/admin.py`; included in `planning/migrations/0001_initial.py`. `content_type`/`object_id` are required here — unlike the same generic-reference pattern on `Deadline` below, where both are nullable. Requiring them on `TaskLink` seems correct (a link without a target doesn't mean anything); worth double-checking whether `Deadline`'s optionality is intentional.

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

**Usage:** `module` is optional (`null=True`), so ad hoc study sessions not tied to a specific module are valid. Now that `academics.Module` exists, this FK is live rather than deferred.

## StudySessionsParticipant

A user's invitation/response status for a `StudySession`.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `session` | `ForeignKey(StudySession)` | `related_name='session_key'` — an unusual name for a reverse accessor; reads like a field rather than a related-object manager (`participants` would be more conventional) |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='participant_user_key'` — same naming note |
| `response` | `CharField(100)`, choices | Nested `ResponceChoices` (class name is misspelled — "Responce"): Invited/Accepted/Declined. Same oversized `max_length` note as `Task.priority`/`Task.status` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:** none implemented. Nothing currently prevents the same user having multiple participant rows for the same session — compare to `TaskAssignment`'s unique `(task, user)` constraint above.

**Usage:** a session's participants are `session.session_key.all()` (see naming note).

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
| `created_at` | `DateTimeField` | Auto-set on create. Currently declared twice in the model body — the second definition silently overwrites the first since both are identical, so there's no functional bug, but the duplicate line should be removed |
| `updated_at` | `DateTimeField` | Auto-set on every save |

**Constraints:** none implemented.

**Usage:** `content_type`/`object_id` are both optional, so a `Deadline` can exist without pointing at anything. Confirm that's intentional — a deadline that isn't a deadline *for* anything is a bit ambiguous — before building logic on top of it.

## Known open items across this app

- `updated_at` is inconsistent: `auto_now` on `CalendarEvent`, `StudySession`, and `Deadline`, but a plain nullable field on `Task` (won't self-update), and absent entirely on `TaskAssignment` and `StudySessionsParticipant`.
- Several `choices` fields (`Task.priority`, `Task.status`, `StudySessionsParticipant.response`) use `max_length=100` for one-to-two-character codes.
- Two label/name typos: `RecurrenceTypeChoices.DAILY` displays as `"Dayly"`; `StudySessionsParticipant`'s choices class is named `ResponceChoices`.
- Two generic-relation patterns (`TaskLink.linked_object`, `Deadline.links_to`) use different accessor names for the same `contenttypes` pattern.
- `Deadline` has a duplicated `created_at` field definition (harmless but should be cleaned up).
- Several `related_name`s read like field names rather than reverse managers (`TaskAssignment.task` → `task_assignment`, `TaskLink.task` → `task_link`, `StudySessionsParticipant.session` → `session_key`, `StudySessionsParticipant.user` → `participant_user_key`).
- No uniqueness constraint on `StudySessionsParticipant` — a user can be added to the same session more than once.

## How the models relate

```
User (Django auth)
  - events -> CalendarEvent (1:M)
  - tasks -> Task (1:M)
  - task_assigned_to_user / task_assigned_by_user -> TaskAssignment
  - sessions -> StudySession (1:M)
  - participant_user_key -> StudySessionsParticipant
  - deadlines -> Deadline (1:M)

Task
  - children -> Task (1:M, self-referencing via parent_task)
  - task_assignment -> TaskAssignment (1:M)
  - task_link -> TaskLink (1:M)

StudySession
  - session_key -> StudySessionsParticipant (1:M)

TaskLink / Deadline
  - linked_object / links_to -> any model, via contenttypes (ContentType + object_id)
```
