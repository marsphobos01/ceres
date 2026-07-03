# collaboration - Implemented Database Schema

This document describes the models as actually implemented in `collaboration/models.py`, and how to use them. Unlike `Collaboration Database plan.md`, which describes the intended design, this reflects the current code. Update this file whenever the models change.

The collaboration schema covers study groups, group projects, membership and invitations, discussions, and direct/group messaging.

## Differences from the earlier design plan

The implemented schema follows epic #150 and its child schema issues (`StudyGroup` #195, `GroupMembership` #196, `GroupInvitation` #197, `GroupProject` #198, `ProjectMembership` #199, `DiscussionThread` #200, `DiscussionMessage` #201, `Conversation` #202, `ConversationParticipant` #203, `ChatMessage` #204). Some concepts from the earlier design plan were not included in the current models, and a few things were implemented differently than described:

- `StudyGroup` uses `title` rather than the plan's `name`, has no `visibility` field, and has no `updated_at` timestamp.
- `GroupMembership.role` choices are `member`, `owner`, not the plan's `owner`, `admin`, `member`, `viewer`.
- `GroupInvitation` targets a study group or project through two nullable direct foreign keys, rather than the plan's generic target-type/target-identifier pair. There is no `expires` timestamp, and `status` choices are `pending`, `accepted`, `declined`, `cancelled` — the plan's `expired` status is not present.
- `ProjectMembership` has no `allocation` label field.
- `DiscussionThread` links to its target with a real `GenericForeignKey` (`content_type`/`object_id`) rather than the plan's separate app-label/object-type text fields — a closer match to normal Django practice than the plan described. It has no `locked` flag.
- `DiscussionMessage` uses `updated_at` (auto-set) rather than the plan's `edited` timestamp, and has no attachment field, so attachment-only messages (without body text) aren't supported here the way the plan allows. `ChatMessage`, by contrast, does support a nullable attachment.

These may be considered as future schema enhancements if required by feature implementation.

`GroupProject.status` and the `GroupInvitation` target-validation approach are addressed separately below, since both are deliberate scope decisions rather than gaps.

## StudyGroup

A shared study space.

| Field | Type | Notes |
| --- | --- | --- |
| `created_by` | `ForeignKey(AUTH_USER_MODEL)` | |
| `title` | `CharField(255)` | Required |
| `description` | `TextField` | Blank allowed |
| `created_at` | `DateTimeField` | Auto-set on create |

## GroupMembership

A user's membership in a study group.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | |
| `study_group` | `ForeignKey(StudyGroup)` | |
| `role` | `CharField(10)` | Choices: `member`, `owner`; default `member` |
| `status` | `CharField(10)` | Choices: `active`, `invited`, `left`; default `active` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_membership` is unique on `(user, study_group)`.

## GroupProject

A collaborative project workspace.

| Field | Type | Notes |
| --- | --- | --- |
| `created_by` | `ForeignKey(AUTH_USER_MODEL)` | |
| `study_group` | `ForeignKey(StudyGroup)`, nullable | Optional |
| `module` | `ForeignKey('academics.Module')`, nullable | Optional |
| `title` | `CharField(255)` | Required |
| `description` | `TextField` | Blank allowed |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** the earlier plan proposed `status` (`active`/`paused`/`completed`/`archived`) and a due date. Issue #198 deliberately scoped this model to `created_by`, nullable `study_group`, nullable `module`, `title`, blank `description`, and timestamps only — it does not require a status or a deadline. This is a plan-versus-approved-scope difference, not a failed implementation; do not add the field during this epic unless #198 is formally changed.

## GroupInvitation

An invitation to join a study group or project.

| Field | Type | Notes |
| --- | --- | --- |
| `invited_by` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='sent_invitations'` |
| `invited_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='received_invitations'` |
| `study_group` | `ForeignKey(StudyGroup)`, nullable | Set for a study group invite |
| `group_project` | `ForeignKey(GroupProject)`, nullable | Set for a project invite |
| `status` | `CharField(10)` | Choices: `pending`, `accepted`, `declined`, `cancelled`; default `pending` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Validation:** `clean()` requires exactly one of `study_group` or `group_project` to be set — not both, and not neither. This is intentionally not a database-level constraint: epic #150 and issue #197 both specify that the exactly-one-target rule is enforced through `clean()` rather than the database, so the absence of a `CheckConstraint` here is correct as implemented.

## ProjectMembership

A user's role in a group project.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | |
| `group_project` | `ForeignKey(GroupProject)` | |
| `role` | `CharField(10)` | Choices: `owner`, `editor`, `viewer`; default `viewer` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_project_membership` is unique on `(user, group_project)`.

## DiscussionThread

A discussion attached to an academic or collaborative context.

| Field | Type | Notes |
| --- | --- | --- |
| `created_by` | `ForeignKey(AUTH_USER_MODEL)` | |
| `title` | `CharField(255)` | Required |
| `content_type` | `ForeignKey('contenttypes.ContentType')` | Identifies the linked object's model |
| `object_id` | `PositiveIntegerField` | Identifies the linked object's row |
| `content_object` | `GenericForeignKey('content_type', 'object_id')` | Resolves to the linked object |
| `created_at` | `DateTimeField` | Auto-set on create |

**Usage:** callers must check access to the linked object before display; this model does not enforce it.

## DiscussionMessage

A message inside a discussion thread.

| Field | Type | Notes |
| --- | --- | --- |
| `thread` | `ForeignKey(DiscussionThread)` | |
| `author` | `ForeignKey(AUTH_USER_MODEL)` | |
| `body` | `TextField` | Required |
| `parent` | `ForeignKey('self')`, nullable | Optional reply-to reference |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## Conversation

A direct or group messaging container.

| Field | Type | Notes |
| --- | --- | --- |
| `type` | `CharField(10)` | Choices: `direct`, `group` |
| `created_at` | `DateTimeField` | Auto-set on create |

Has no direct participant fields; participants are managed entirely via `ConversationParticipant`.

## ConversationParticipant

A user's membership in a conversation.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | |
| `conversation` | `ForeignKey(Conversation)` | |
| `muted` | `BooleanField` | Default `False` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_conversation_participant` is unique on `(user, conversation)`.

## ChatMessage

A message in a conversation.

| Field | Type | Notes |
| --- | --- | --- |
| `conversation` | `ForeignKey(Conversation)` | |
| `author` | `ForeignKey(AUTH_USER_MODEL)` | |
| `body` | `TextField` | Required |
| `parent` | `ForeignKey('self')`, nullable | Optional reply-to reference |
| `attachment` | `ForeignKey('files.StoredFile')`, nullable, `on_delete=SET_NULL` | A message either has one file or it doesn't |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** author must be a participant in `conversation`; this is not enforced at the model level.

## How the models relate

```
User (Django auth)
  - created study groups, projects, threads, messages (via created_by/author FKs)
  - sent_invitations / received_invitations -> GroupInvitation

StudyGroup
  - GroupMembership (via study_group)
  - GroupProject (optional, via study_group)
  - GroupInvitation (optional target, via study_group)

GroupProject
  - ProjectMembership (via group_project)
  - GroupInvitation (optional target, via group_project)

DiscussionThread
  - DiscussionMessage (via thread)
  - content_object -> generic FK to any app's object

Conversation
  - ConversationParticipant (via conversation)
  - ChatMessage (via conversation)

ChatMessage
  - attachment -> files.StoredFile (optional)
```
