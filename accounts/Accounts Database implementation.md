# accounts — Implemented Database Schema

This document describes the models as actually implemented in `accounts/models.py`, and how to use them. Unlike `Accounts Database plan.md`, which describes the intended design, this reflects the current code. Update this file (not the plan) whenever the models change.

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

One row per user for account-level settings.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='preference'` — access via `user.preference` |
| `timezone` | `TimeZoneField` | Default `UTC`; requires `django-timezone-field` installed |
| `email_notifications` | `BooleanField` | Default `True` |
| `searchable` | `BooleanField` | Default `True` |

**Usage:** access with `user.preference`. Account settings only — privacy settings live in `PrivacyPreference`.

## PrivacyPreference

One row per user for privacy-specific settings, kept separate from account preferences to avoid mixing concerns.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | One record per user |
| `profile_visibility` | `CharField`, choices `public` / `friends_only` / `private` | Default `private` |
| `show_online_status` | `BooleanField` | Default `True` |
| `allow_friend_requests` | `BooleanField` | Default `True` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** access with `user.privacy_preference`. Controls visibility and discoverability independently of account-level settings.

## Friendship

A confirmed friendship between two users. Requests, blocks, and history are handled by separate models.

| Field | Type | Notes |
| --- | --- | --- |
| `user_a` | `ForeignKey(AUTH_USER_MODEL)` | Lower user ID of the pair |
| `user_b` | `ForeignKey(AUTH_USER_MODEL)` | Higher user ID of the pair |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- Unique constraint on `(user_a, user_b)`.
- `user_a_id < user_b_id` — lower ID always stored as `user_a` to prevent duplicate pairs regardless of direction.

**Usage:** represents a confirmed, active friendship only. Whatever code creates a `Friendship` must sort the two users before assigning `user_a`/`user_b`. To check whether two users are friends, query for the sorted pair.

## FriendRequest

A pending or resolved request from one user to another.

| Field | Type | Notes |
| --- | --- | --- |
| `from_user` | `ForeignKey(AUTH_USER_MODEL)` | The user who sent the request |
| `to_user` | `ForeignKey(AUTH_USER_MODEL)` | The user who received the request |
| `status` | `CharField`, choices `pending` / `accepted` / `declined` / `cancelled` | Default `pending` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- Unique constraint on `(from_user, to_user)`.

**Usage:** when a request is accepted, application code should create a `Friendship` record and update this record's status to `accepted`. History of request actions is recorded in `FriendRequestEvent`.

## BlockedUser

A block from one user directed at another.

| Field | Type | Notes |
| --- | --- | --- |
| `blocker` | `ForeignKey(AUTH_USER_MODEL)` | The user who issued the block |
| `blocked` | `ForeignKey(AUTH_USER_MODEL)` | The user who was blocked |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- Unique constraint on `(blocker, blocked)`.

**Usage:** kept separate from `Friendship` so that block checks never accidentally touch friendship records. Before displaying any user-to-user content or interaction, check whether a `BlockedUser` record exists in either direction.

## FriendRequestEvent

Optional history log of actions taken on a `FriendRequest`.

| Field | Type | Notes |
| --- | --- | --- |
| `friend_request` | `ForeignKey(FriendRequest)` | `related_name='events'` — access via `friend_request.events.all()` |
| `actor_user` | `ForeignKey(AUTH_USER_MODEL)` | The user who performed the action |
| `action` | `CharField`, choices `sent` / `accepted` / `declined` / `cancelled` | Required |
| `note` | `CharField(255)` | Optional |
| `created_at` | `DateTimeField` | Auto-set on create |

**Validation:** `actor_user` must be one of `friend_request.from_user` or `friend_request.to_user`.

**Usage:** this table is optional history — nothing else depends on it existing. Useful for an activity feed or audit trail.

## UserContentPermission

A default sharing-permission rule one user sets for another.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='content_permissions'` |
| `target_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='targeted_permissions'` |
| `permission_level` | `CharField`, choices `view` / `comment` / `edit` | Required |
| `applies_to` | `CharField`, choices `all_content` only for now | `specific_content` scope to be added when `content`/`files` apps are built |

**Constraints:**
- Unique constraint on `(owner, target_user, applies_to)`.
- `owner` cannot equal `target_user`.

**Usage:** represents "by default, `target_user` gets `permission_level` access to everything `owner` shares." Per-item overrides live in the owning app.

## How the models relate

```
User (Django auth)
 ├─ profile                  → UserProfile (1:1)
 ├─ preference               → AccountPreference (1:1)
 ├─ privacy_preference       → PrivacyPreference (1:1)
 ├─ friendships_as_a / friendships_as_b → Friendship (M:N via user_a/user_b)
 ├─ sent_requests / received_requests   → FriendRequest (1:M)
 ├─ blocks_issued / blocks_received     → BlockedUser (1:M)
 └─ content_permissions / targeted_permissions → UserContentPermission (M:N)

FriendRequest
 └─ events → FriendRequestEvent (1:M)
```
