# academics - Implemented Database Schema

This document describes the models as actually implemented in `academics/models.py`, and how to use them. Unlike `Academics Database plan.md`, which describes the intended design, this reflects the current code. Update this file whenever the models change.

The academics schema covers modules, module membership, lectures, timetable entries, assignments, and revision topics.

## Differences from the earlier design plan

The implemented schema follows epic #146 and its child schema issues (`Module` #160, `ModuleMembership` #161, `Lecture` #162, `TimetableEntry` #163, `Assignment` #164, `RevisionTopic` #165). Some concepts from the earlier design plan were not included in the current models, and a couple of fields were implemented differently than described:

- `Module` has no `archived` flag, and there is no uniqueness constraint on module code per owner and academic year.
- `Module`'s `semester` field is the plan's `term` concept under a different name.
- `ModuleMembership`'s `role` choices are `owner`, `member`, `viewer`, not the plan's `owner`, `student`, `tutor`, `collaborator`.
- `Lecture` has a single `date` field rather than separate start and end times, so there is no constraint that an end time falls after a start time. `lecturer` is split into `lecturer_name` and `lecturer_email` rather than one field.
- `TimetableEntry` has a single `date` field for one-off events rather than separate recurrence start and end dates, and there is no constraint that `end_time` falls after `start_time`.
- `Assignment.weighting` has no constraint requiring it to be zero or greater.
- `RevisionTopic.confidence` is a `red`/`amber`/`green` choice field, not the plan's numeric confidence score, and there is no `priority` or `last_reviewed` field.

These may be considered as future schema enhancements if required by feature implementation.

`Assignment.status` is addressed separately below — it is a deliberate divergence from the plan, not an unimplemented item or an accidental overlap.

## Module

A university module or class.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='owned_modules'` |
| `title` | `CharField(255)` | Required |
| `code` | `CharField(20)`, nullable | Optional |
| `description` | `TextField`, nullable | Optional |
| `colour` | `CharField(6)`, nullable | Optional hex colour code |
| `academic_year` | `CharField(9)`, nullable | e.g. `"2023/2024"` |
| `semester` | `CharField(10)`, nullable | Choices: `autumn`, `spring`, `summer`, `full_year` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## ModuleMembership

A user's relationship to a module.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='module_memberships'` |
| `module` | `ForeignKey(Module)` | `related_name='memberships'` |
| `role` | `CharField(10)` | Choices: `owner`, `member`, `viewer`; default `member` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_user_module` is unique on `(user, module)`.

## Lecture

A lecture or teaching session attached to a module.

| Field | Type | Notes |
| --- | --- | --- |
| `module` | `ForeignKey(Module)` | `related_name='lectures'` |
| `title` | `CharField(255)` | Required |
| `date` | `DateTimeField`, nullable | Single date/time field; no separate end time |
| `room` | `CharField(100)`, nullable | Optional |
| `lecturer_name` | `CharField(255)`, nullable | Optional |
| `lecturer_email` | `EmailField`, nullable | Optional |
| `description` | `TextField`, nullable | Optional free-text details about the lecture (renamed from `notes` in migration `0007` — real lecture notes belong to the `content` app's Note system, so the old name invited confusion with the "one notes system" rule) |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## TimetableEntry

A recurring or scheduled academic timetable item.

| Field | Type | Notes |
| --- | --- | --- |
| `module` | `ForeignKey(Module)` | `related_name='timetable_entries'` |
| `lecture` | `ForeignKey(Lecture)`, nullable | `related_name='timetable_entries'`; optional link to a specific lecture |
| `day_of_week` | `CharField(10)` | Choices: `mon` through `sun` |
| `start_time` | `TimeField` | Required |
| `end_time` | `TimeField` | Required; no database constraint enforcing it falls after `start_time` |
| `room` | `CharField(100)`, nullable | Optional |
| `recurrence_type` | `CharField(20)` | Choices: `weekly`, `fortnightly`, `one_off`; default `weekly` |
| `date` | `DateField`, nullable | Used for one-off events |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## Assignment

An academic assignment, coursework item, or assessment.

| Field | Type | Notes |
| --- | --- | --- |
| `module` | `ForeignKey(Module)` | `related_name='assignments'` |
| `title` | `CharField(255)` | Required |
| `description` | `TextField`, nullable | Optional |
| `deadline` | `DateTimeField`, nullable | Optional |
| `weighting` | `DecimalField(5,2)`, nullable | Percentage; no constraint requiring zero or greater |
| `submission_type` | `CharField(20)`, nullable | Choices: `essay`, `report`, `presentation`, `exam`, `practical`, `other` |
| `is_group` | `BooleanField` | Default `False` |
| `status` | `CharField(20)` | Choices: `not_started`, `in_progress`, `submitted`, `completed`; default `not_started` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** the earlier academics plan proposed that generic status and progress behaviour should live in `planning`. The implemented schema deliberately retains an academic lifecycle `status` on `Assignment`, as explicitly required by academics epic #146 and Assignment issue #164. This status records assignment-level states such as `submitted`, while planning tasks retain their own execution status, priority, breakdown, and reminders — issue #164 only prohibits those from being duplicated here. The similarly named statuses should be treated as separate concepts (assessment lifecycle vs. linked task execution state), although clearer naming such as `submission_status` could be considered in a future schema change. No model change is needed based on this alone.

## RevisionTopic

A revisable topic within a module.

| Field | Type | Notes |
| --- | --- | --- |
| `module` | `ForeignKey(Module)` | `related_name='revision_topics'` |
| `title` | `CharField(255)` | Required |
| `confidence` | `CharField(10)`, nullable | Choices: `red`, `amber`, `green` |
| `notes` | `TextField`, nullable | Optional |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## How the models relate

```
User (Django auth)
  - owned_modules -> Module
  - module_memberships -> ModuleMembership

Module
  - memberships -> ModuleMembership
  - lectures -> Lecture
  - timetable_entries -> TimetableEntry
  - assignments -> Assignment
  - revision_topics -> RevisionTopic

Lecture
  - timetable_entries -> TimetableEntry (optional link)
```
