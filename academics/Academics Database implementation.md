# academics - Implemented Database Schema

This document describes the models implemented in `academics/models.py`. Update it whenever the schema changes.

The academics schema covers modules, module memberships, lectures, timetable entries, timetable imports, assignments, assignment participants, and revision topics.

## Module

A university module owned by a user.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='owned_modules'` |
| `title` | `CharField(255)` | Required |
| `code` | `CharField(20)`, nullable | Optional |
| `description` | `TextField`, nullable | Optional |
| `colour` | `CharField(6)`, nullable | Optional hex colour |
| `academic_year` | `CharField(9)`, nullable | Example: `2025/2026` |
| `semester` | `CharField(10)`, nullable | `autumn`, `spring`, `summer`, `full_year` |
| `created_at`, `updated_at` | `DateTimeField` | Automatic timestamps |

## ModuleMembership

Connects a user to a Module.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='module_memberships'` |
| `module` | `ForeignKey(Module)` | `related_name='memberships'` |
| `role` | `CharField(10)` | `owner`, `member`, `viewer`; default `member` |
| `created_at` | `DateTimeField` | Automatic timestamp |

`unique_user_module` prevents duplicate membership rows for the same user and Module.

## Lecture

A teaching session attached to a Module. It stores a title, optional date, room, lecturer details, description, and timestamps.

## TimetableEntry

A recurring or one-off timetable item. It belongs to a Module and may optionally link to a Lecture. It stores weekday, start and end times, room, recurrence type, optional one-off date, and timestamps.

## TimetableImport

Tracks a timetable import job, including its owner, filename, processing status, row totals, error details, and timestamps.

## Assignment

An academic assessment belonging to a Module.

| Field | Type | Notes |
| --- | --- | --- |
| `module` | `ForeignKey(Module)` | `related_name='assignments'` |
| `title` | `CharField(255)` | Required |
| `description` | `TextField`, nullable | Optional |
| `deadline` | `DateTimeField`, nullable | Optional |
| `weighting` | `DecimalField(5,2)`, nullable | Optional percentage |
| `submission_type` | `CharField(20)`, nullable | Essay, report, presentation, exam, practical, or other |
| `is_group` | `BooleanField` | Describes whether the assessment is group work |
| `submission_status` | `CharField(20)` | `not_submitted` or `submitted` |
| `participants` | `ManyToManyField(AUTH_USER_MODEL)` | Uses `AssignmentParticipant` as its through model |
| `created_at`, `updated_at` | `DateTimeField` | Automatic timestamps |

`submission_status` records only the academic submission lifecycle. Task priority, work state, progress, and breakdown remain in `planning` through linked Tasks.

A populated group Assignment cannot be changed to individual work. Participant rows must be removed first.

Permission helpers:

- `can_manage_participants(user)` is true for the Module owner or a Module member with the `owner` role.
- `add_participant(actor=..., user=...)` checks permission and creates a validated participant row.
- `remove_participant(actor=..., user=...)` checks permission and removes the participant row.
- Being a participant does not itself grant permission to edit the Assignment or manage its participants.

## AssignmentParticipant

The single source of truth for who is involved in an academic group Assignment.

| Field | Type | Notes |
| --- | --- | --- |
| `assignment` | `ForeignKey(Assignment)` | `related_name='participant_memberships'`; cascades on deletion |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='assignment_participations'`; cascades on deletion |
| `created_at` | `DateTimeField` | Automatic timestamp |

Rules:

- `unique_assignment_participant` prevents duplicate `(assignment, user)` rows.
- Participants may only be added to Assignments where `is_group=True`.
- A participant must own or have membership of the Assignment's Module.
- Normal saves and Many-to-Many bulk additions run model validation.
- The model has no participant role. Task allocation belongs to `planning`.
- This relationship is separate from Study Group and Group Project membership in `collaboration`.

Useful accessors:

- `assignment.participants.all()` returns participant users.
- `assignment.participant_memberships.all()` returns join records.
- `user.participating_assignments.all()` returns the user's Assignments.
- `user.assignment_participations.all()` returns the user's join records.

## RevisionTopic

A revisable topic attached to a Module. Confidence uses the controlled values `red`, `amber`, and `green`.

## Relationship summary

```text
Module -> ModuleMembership -> User
Module -> Lecture -> TimetableEntry
Module -> Assignment -> AssignmentParticipant -> User
Module -> RevisionTopic
User -> TimetableImport
```
