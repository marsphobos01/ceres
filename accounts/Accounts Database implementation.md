# accounts — Implemented Database Schema

This document describes the models as actually implemented in `accounts/models.py`, and how to use them. Unlike `Accounts Database plan.md`, which describes the intended (decomposed) design, this reflects the current code. Update this file (not the plan) whenever the models change.

**The decomposition described in the plan is partially complete.** `Friendship` still combines relationship state, request state, and block state into one model with a `status` field, rather than being split into separate `Friendship`/`FriendRequest`/`BlockedUser` models. This matches the "current drift to resolve" described in the GitHub schema-alignment issues (`#153`–`#159`) — those issues are the tracked work to bring the code in line with the plan. `#153` (naming) and `#155` (`PrivacyPreference`) are now implemented.

## UserProfile

One profile per user, holding public/private display details.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='profile'` — access via `user.profile` |
| `display_name` | `CharField(255)` | Required |
| `profile_image` | `ImageField`, nullable | Optional; requires Pillow installed |
| `university` | `CharField(255)`, nullable | Optional |
| `course` | `CharField(255)`, nullable | Optional |
| `bio` | `TextField`, nullable | Optional |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** every `User` should have exactly one `UserProfile` (enforced by the one-to-one relationship). Access it with `user.profile`. Profile visibility no longer lives here — see `PrivacyPreference` below.

**`#153` resolved:** field renamed from `profile_picture` to `profile_image`, matching the plan.

## AccountPreference

One row per user for account-level settings.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='preference'` — access via `user.preference` |
| `timezone` | `TimeZoneField` | Default `UTC`; requires `django-timezone-field` installed |
| `email_notifications` | `BooleanField` | Default `True` |
| `searchable` | `BooleanField` | Default `True` |
| `language` | `CharField(max_length=10)` | Default `'en'`; ISO language code |
| `created_at` | `DateTimeField` | `auto_now_add=True` — set on creation |
| `updated_at` | `DateTimeField` | `auto_now=True` — updated on every save |

**Usage:** access with `user.preference`.

**Intentionally not merged into `PrivacyPreference` (`#155`):** `searchable` controls discoverability in search/friend-lookup, which is a distinct concern from profile visibility level. It stays here rather than moving to the new model.

## PrivacyPreference

One row per user for privacy-related settings, kept separate from `AccountPreference` to avoid mixing concerns, per the plan.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='privacy'` — access via `user.privacy` |
| `profile_visibility` | `CharField(255)`, choices `public` / `friends_only` / `private` | Default `private` |
| `show_online_status` | `BooleanField` | Default `True` |
| `allow_friend_requests` | `BooleanField` | Default `True` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** access with `user.privacy`. This is the single source of truth for profile visibility — `UserProfile` no longer has a visibility field of its own.

## Friendship

The single model currently handling relationship state, request state, *and* block state together — not yet decomposed into separate models.

| Field | Type | Notes |
| --- | --- | --- |
| `user_one` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendships_as_user_one'` |
| `user_two` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendships_as_user_two'` |
| `requested_by` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friendship_requests_sent'` — whichever of the two users initiated |
| `status` | `CharField(255)`, choices `requested` / `accepted` / `blocked` / `removed` / `rejected` | Default `requested` |
| `requested_at` | `DateTimeField` | Auto-set on create |
| `accepted_at`, `rejected_at`, `removed_at`, `blocked_at` | `DateTimeField`, nullable | Set when the corresponding transition happens; application code's responsibility, not automatic |

**Constraints:**
- `unique_friendship` — unique on `(user_one, user_two)`.
- `requested_by_either_user` — `requested_by` must equal `user_one` or `user_two`.
- `user_one_before_user_two` — `user_one_id < user_two_id`, enforced at the database level. Whatever code creates a `Friendship` must sort the two users before assigning `user_one`/`user_two`.

**Usage:** this one row represents the entire lifecycle of a relationship between two users — request, acceptance, rejection, removal, or block — tracked via `status` rather than separate tables. To check whether two users are friends, query for the sorted pair with `status='accepted'`. To check for a block, query with `status='blocked'`. There is no dedicated "pending requests" or "blocked users" table; both are just `Friendship` rows in a particular `status`.

**Known drift from the plan (`#156`, `#157`, `#158`):** the plan describes this decomposed into separate `Friendship` (confirmed only), `FriendRequest`, and `BlockedUser` models. That decomposition is tracked but not done — do not write code assuming those separate models exist.

## FriendRequestEvent

Optional history log of status transitions on a `Friendship`.

| Field | Type | Notes |
| --- | --- | --- |
| `friendship` | `ForeignKey(Friendship)` | `related_name='events'` — access via `friendship.events.all()`. **Not** a FK to a separate `FriendRequest` model — no such model exists. |
| `actor_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='friend_request_events'` |
| `action` | `CharField(255)`, choices `requested` / `accepted` / `rejected` / `removed` / `blocked` | Required — mirrors `Friendship.status`'s choices, not the plan's `sent`/`accepted`/`declined`/`cancelled` |
| `note` | `CharField(255)`, nullable | Optional |
| `created_at` | `DateTimeField` | Auto-set on create |

**Validation:** `clean()` requires `actor_user` to be one of `friendship.user_one` or `friendship.user_two`; `save()` calls `full_clean()` so this is enforced on every save, not just in forms.

**Usage:** optional history — nothing else depends on it existing. Useful for an activity feed or audit trail of a `Friendship`'s lifecycle.

## UserContentPermission

A default sharing-permission rule one user sets for another.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='content_permissions'` |
| `target_user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='targeted_permissions'` |
| `permission_level` | `CharField(255)`, choices `view` / `comment` / `edit` | Required |
| `applies_to` | `CharField(255)`, choices `all_content` only | `specific_content` is commented out in the model with a TODO, pending `content`/`files` apps being built — see `#159` and `#3` |

**Constraints:**
- `unique_permission` — unique on `(owner, target_user, applies_to)`.
- `owner_not_target_user` — `owner` cannot equal `target_user`.

**Usage:** represents "by default, `target_user` gets `permission_level` access to everything `owner` shares." Per-item overrides are intended to live in the owning app once `applies_to='specific_content'` exists, which it doesn't yet.

## How the models relate

```
User (Django auth)
 ├─ profile                                    → UserProfile (1:1)
 ├─ preference                                  → AccountPreference (1:1)
 ├─ privacy                                     → PrivacyPreference (1:1)
 ├─ friendships_as_user_one / friendships_as_user_two → Friendship (M:N, sorted pair)
 ├─ friendship_requests_sent                    → Friendship (1:M, via requested_by)
 ├─ friend_request_events                       → FriendRequestEvent (1:M, via actor_user)
 └─ content_permissions / targeted_permissions  → UserContentPermission (M:N)

Friendship
 └─ events → FriendRequestEvent (1:M)
```

No `FriendRequest` or `BlockedUser` models exist — do not reference them in code until the `#156`–`#158` alignment issues are resolved.
