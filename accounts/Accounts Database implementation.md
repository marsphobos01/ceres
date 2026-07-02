# accounts - Implemented Database Schema

This document describes the models as actually implemented in `accounts/models.py`, and how to use them. Unlike `Accounts Database plan.md`, which describes the intended design, this reflects the current code. Update this file whenever the models change.

The accounts schema is partially aligned with the decomposed plan. `FriendRequest` is the dedicated model for pending and resolved friend requests, so request-specific state no longer lives on `Friendship`. `BlockedUser` is the dedicated model for user blocks, so block-specific state no longer lives on `Friendship`.

## UserProfile

One profile per user, holding public/private display details.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='profile'`; access via `user.profile` |
| `display_name` | `CharField(255)` | Required |
| `profile_image` | `ImageField`, nullable | Optional; requires Pillow installed |
| `university` | `CharField(255)`, nullable | Optional |
| `course` | `CharField(255)`, nullable | Optional |
| `bio` | `TextField`, nullable | Optional |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

`#153` is resolved: the image field is named `profile_image`, matching the plan.

## AccountPreference

One row per user for account-level settings.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='preference'`; access via `user.preference` |
| `timezone` | `TimeZoneField` | Default `UTC`; requires `django-timezone-field` |
| `email_notifications` | `BooleanField` | Default `True` |
| `searchable` | `BooleanField` | Default `True` |
| `language` | `CharField(max_length=10)` | Default `'en'`; ISO language code |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

`searchable` remains here rather than in `PrivacyPreference` because discoverability is separate from profile visibility.

## PrivacyPreference

One row per user for privacy-related settings.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='privacy'`; access via `user.privacy` |
| `profile_visibility` | `CharField(255)` | Choices: `public`, `friends_only`, `private`; default `private` |
| `show_online_status` | `BooleanField` | Default `True` |
| `allow_friend_requests` | `BooleanField` | Default `True` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

This is the single source of truth for profile visibility; `UserProfile` no longer has a visibility field.

## FriendRequest

Dedicated lifecycle record for a friend request between two users. This resolves the `#157` decision in favor of a separate `FriendRequest` model instead of keeping pending/rejected request state on `Friendship`.

| Field | Type | Notes |
| --- | --- | --- |
| `from_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='sent_friend_requests'`; the sender |
| `to_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='received_friend_requests'`; the recipient |
| `status` | `CharField(255)` | Choices: `pending`, `accepted`, `rejected`; default `pending` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- `unique_pending_friend_request` prevents duplicate pending requests for the same `(from_user, to_user)` pair.
- `from_user_not_to_user` prevents a user from sending a request to themselves.

**Usage:** create a `FriendRequest` when one user asks to connect with another. Accepting the request should update the request status to `accepted` and create or update a corresponding accepted `Friendship`. Rejecting the request should update the request status to `rejected`. Pending and rejected request state should not be written to `Friendship`.

## Friendship

Confirmed friendship between two users. Requests are tracked separately in `FriendRequest`; blocking is tracked separately in `BlockedUser`.

| Field | Type | Notes |
| --- | --- | --- |
| `user_one` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendships_as_user_one'` |
| `user_two` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendships_as_user_two'` |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_friendship` is unique on `(user_one, user_two)`.
- `user_one_before_user_two` requires `user_one_id < user_two_id`. Code creating a `Friendship` must sort the two users before saving.

**Usage:** query for the sorted pair to determine whether two users are friends. Pending and rejected requests live in `FriendRequest`, not here. Blocks live in `BlockedUser`, not here.

## BlockedUser

Dedicated block record between two users. This resolves the `#158` decision in favor of a separate `BlockedUser` model because blocking can exist without a prior friendship.

| Field | Type | Notes |
| --- | --- | --- |
| `blocker` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='blocked_users'`; the user who initiated the block |
| `blocked` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='blocked_by'`; the user being blocked |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_blocked_user` prevents duplicate blocks for the same `(blocker, blocked)` pair.
- `no_self_blocking` prevents a user from blocking themselves.

**Usage:** create a `BlockedUser` row when one user blocks another. A block does not require an existing `Friendship`, and block state should not be written to `Friendship`.

## FriendRequestEvent

Optional note/audit record attached to a `Friendship`.

| Field | Type | Notes |
| --- | --- | --- |
| `friendship` | `ForeignKey(Friendship)` | `related_name='events'`; access via `friendship.events.all()` |
| `actor_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friend_request_events'` |
| `note` | `CharField(255)`, nullable | Optional |
| `created_at` | `DateTimeField` | Auto-set on create |

**Validation:** `clean()` requires `actor_user` to be one of `friendship.user_one` or `friendship.user_two`; `save()` calls `full_clean()` so this is enforced on every save.

## UserContentPermission

A default sharing-permission rule one user sets for another.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='content_permissions'` |
| `target_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='targeted_permissions'` |
| `permission_level` | `CharField(255)` | Choices: `view`, `comment`, `edit` |
| `applies_to` | `CharField(255)` | Currently only `all_content` |

**Constraints:**
- `unique_permission` is unique on `(owner, target_user, applies_to)`.
- `owner_not_target_user` prevents a user from granting permissions to themselves.

**Usage:** represents the default access `target_user` has to everything `owner` shares. Per-item overrides are intended to live in the owning app once `applies_to='specific_content'` exists.

## How the models relate

```
User (Django auth)
  - profile -> UserProfile (1:1)
  - preference -> AccountPreference (1:1)
  - privacy -> PrivacyPreference (1:1)
  - sent_friend_requests / received_friend_requests -> FriendRequest
  - blocked_users / blocked_by -> BlockedUser
  - friendships_as_user_one / friendships_as_user_two -> Friendship
  - friend_request_events -> FriendRequestEvent
  - content_permissions / targeted_permissions -> UserContentPermission

Friendship
  - events -> FriendRequestEvent
```
