# accounts — Implemented Database Schema

This document describes the models as actually implemented in `accounts/models.py`, and how to use them. Unlike `Accounts Database plan.md`, which describes the intended design, this reflects the current code. Update this file (not the plan) whenever the models change.

No migrations have been created yet as of writing — this describes the model definitions only.

## UserProfile

One profile per user, holding public/private display details.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='profile'` — access via `user.profile` |
| `display_name` | `CharField(255)` | Required |
| `profile_picture` | `ImageField` | Optional; requires Pillow installed |
| `university` | `CharField(255)` | Optional |
| `course` | `CharField(255)` | Optional |
| `bio` | `TextField` | Optional |
| `visibility` | `CharField(255)`, choices `public` / `friends` / `private` | Default `private` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** every `User` should have exactly one `UserProfile` (enforced by the one-to-one relationship). Access it with `user.profile`. The `visibility` field only stores the user's preference — nothing in this model enforces who can actually see the profile; that access control needs to be applied wherever profile data gets displayed.

## AccountPreference

One row per user for account-level and privacy settings.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='preference'` — access via `user.preference` |
| `timezone` | `TimeZoneField` | Default `UTC`; requires `django-timezone-field` installed |
| `email_notifications` | `BooleanField` | Default `True` |
| `searchable` | `BooleanField` | Default `True` |

**Usage:** access with `user.preference`. There is deliberately no `visibility`/profile-visibility field here — that lives solely on `UserProfile` to avoid storing the same state twice.

## Friendship

A friend request or accepted friendship between two users.

| Field | Type | Notes |
| --- | --- | --- |
| `user_one` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendships_as_user_one'` |
| `user_two` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendships_as_user_two'` |
| `requested_by` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendship_requests_sent'` — records who actually sent the request |
| `status` | `CharField(255)`, choices `requested` / `accepted` / `blocked` / `removed` / `rejected` | Default `requested` |
| `requested_at` | `DateTimeField` | Auto-set on create |
| `accepted_at`, `rejected_at`, `removed_at`, `blocked_at` | `DateTimeField`, nullable | Set manually by application code when `status` changes |

**Constraints:**
- `unique_friendship` — unique together on `(user_one, user_two)`.
- `user_one_before_user_two` — `user_one_id < user_two_id`. This also rules out self-friendship as a side effect (a strict less-than can never hold if the two IDs are equal).
- `requested_by_either_user` — `requested_by` must equal `user_one` or `user_two`.

**Usage — important:** `user_one`/`user_two` are always stored in a fixed order (lower ID first); this is what lets the database enforce "only one relationship per pair of people." This is *not* the same as who requested the friendship — that's what `requested_by` is for. Whatever code creates a `Friendship` must sort the two users itself before assigning `user_one`/`user_two`; the constraint only rejects the wrong order, it doesn't sort for you. To check whether two users have any relationship (pending, accepted, etc.), query for the sorted pair and read `status`. The `*_at` timestamp fields are not set automatically when `status` changes — application code updating the status needs to set the matching timestamp too.

## FriendRequestEvent

Optional history log of actions taken on a `Friendship`.

| Field | Type | Notes |
| --- | --- | --- |
| `friendship` | `ForeignKey(Friendship)` | `related_name='events'` — access via `friendship.events.all()` |
| `actor_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friend_request_events'` |
| `action` | `CharField(255)`, choices `requested` / `accepted` / `rejected` / `removed` / `blocked` | Required |
| `note` | `CharField(255)` | Optional |
| `created_at` | `DateTimeField` | Auto-set on create |

**Validation:** `clean()` checks that `actor_user` is one of `friendship.user_one` / `friendship.user_two`, since a `CheckConstraint` can't reach across tables to enforce this at the database level. `save()` is overridden to call `self.full_clean()` before saving, so this check runs on every save — including direct `.save()`/`.create()` calls that don't go through a form or serializer.

**Usage:** this table is optional history — nothing else depends on it existing. Useful for an activity feed or audit trail of what happened to a friendship over time.

## UserContentPermission

A default sharing-permission rule one user sets for another, to be used later by the `content`/`files` apps.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='content_permissions'` |
| `target_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='targeted_permissions'` |
| `permission_level` | `CharField(255)`, choices `view` / `comment` / `edit` | Required |
| `applies_to` | `CharField(255)`, choices `all_content` only for now | `specific_content` is commented out — see TODO in the model |

**Constraints:**
- `unique_permission` — unique together on `(owner, target_user, applies_to)`.
- `owner_not_target_user` — `owner` cannot equal `target_user`.

**Usage:** represents "by default, `target_user` gets `permission_level` access to everything `owner` shares." Since `applies_to` currently only supports `all_content`, this model can't yet express per-item permissions. When the `content`/`files` apps are built, `specific_content` scope will need a foreign key added here pointing at the actual content/file item — see the TODO comment in the model.

## How the models relate

```
User (Django auth)
 ├─ profile              → UserProfile (1:1)
 ├─ preference           → AccountPreference (1:1)
 ├─ friendships_as_user_one / friendships_as_user_two / friendship_requests_sent → Friendship (M:N via user_one/user_two, tracked direction via requested_by)
 ├─ friend_request_events → FriendRequestEvent (M:1, via actor_user)
 └─ content_permissions / targeted_permissions → UserContentPermission (M:N via owner/target_user)

Friendship
 └─ events → FriendRequestEvent (1:M)
```
