# notifications — Implemented Database Schema

This document describes the models as actually implemented in `notifications/models.py`, and how to use them. Unlike `Notifications Database plan.md`, which describes the intended design, this reflects the current code. Update this file (not the plan) whenever the models change.

No migrations have been created yet as of writing — this describes the model definitions only.

## Notification

An item in a user's notification feed.

| Field | Type | Notes |
| --- | --- | --- |
| `notification_id` | `BigAutoField` | Explicit primary key |
| `notification_name` | `CharField(100)` | Required |
| `notification_content` | `TextField` | Required |
| `category` | `CharField(100)`, choices `A` (Academic) / `C` (Colaboration) | Choices defined in module-level `CATEGORY_CHOICES`; marked TODO to refine |
| `created_at` | `DateTimeField` | Auto-set on create |
| `read_at` | `DateTimeField`, nullable | Unset while unread |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notifications'` — access via `user.notifications` |

**Constraints:**
- `notification_category_valid` — `CheckConstraint` requiring `category` to be one of `A` / `C`. Enforces the choices at the database level, not just in forms/admin.

**Usage:** access a user's feed with `user.notifications.all()`. There is no field yet identifying *what* a notification is about (e.g. which assignment or lecture triggered it) — a commented-out `object_id` field is left as a TODO. Until that's added, a `Notification` row only carries a name/content/category and can't be traced back to its source.

## Reminder

A scheduled reminder for a deadline, lecture, event, or task.

| Field | Type | Notes |
| --- | --- | --- |
| `reminder_id` | `BigAutoField` | Explicit primary key |
| `reminder_content` | `TextField` | Required |
| `recipient` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='reminders'` — access via `user.reminders` |
| `created_at` | `DateTimeField` | Auto-set on create |
| `remind_at` | `DateTimeField` | Required |
| `next_fire_at` | `DateTimeField`, nullable | Reserved for recurrence; unused while `frequency` is `O` |
| `frequency` | `CharField(10)`, choices `O` (Once) / `RD` / `RW` / `RB` / `RM` (Repeat Daily/Weekly/Biweekly/Monthly) | Default `O` |
| `status` | `CharField(100)`, choices `S` (Scheduled) / `ST` (Sent) / `C` (Canceled) | Default `S` |

**Constraints:** none implemented yet. `Meta.constraints` is present but empty, with a TODO — the plan's "one active reminder per recipient, source object, and remind-at time" rule needs the source-reference fields (see below) before it can be written.

**Usage — important:**
- Like `Notification`, there is no field yet linking a reminder back to what it's reminding about — the same commented-out `object_id` TODO applies here.
- `frequency` beyond `O` (Once) is defined but not yet functional. Recurrence would require distinguishing a fixed anchor time from a mutable "next time this fires" value, and a background process to actually reschedule and dispatch reminders — neither exists yet. Treat any reminder with `frequency != "O"` as unimplemented for now.

## NotificationPreferences

A user's notification settings per category and channel.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notification_preferences'` — access via `user.notification_preferences` |
| `category` | `TextField`, choices `A` / `C` | Uses module-level `CATEGORY_CHOICES`, same values as `Notification.category`. Implemented as `TextField` rather than `CharField`, inconsistent with `category`/`channel` elsewhere in this app |
| `channel` | `CharField(100)`, choices `A` (All) / `T` (Text) / `E` (Email) / `D` (Discord) / `I` (In App) | Choices defined in module-level `CHANNEL_CHOICES`, shared with `NotificationDelivery` |
| `read_at` | `DateTimeField`, nullable | Present on the model but not conceptually part of a preference row — read state belongs to `Notification` |
| `enabled_flag` | `BooleanField` | Default `True` |
| `quiet_hours_start` | `TimeField` | Required |
| `quiet_hours_end` | `TimeField` | Required |

**Constraints:** none implemented yet. The plan's "one preference per user, category, and channel" rule is not yet enforced at the database level.

**Usage:** a user's full preference set is `user.notification_preferences.all()` — one row per category/channel combination they've configured, rather than a single row with multiple channels selected. A user wanting Academic notifications by both email and Discord has two rows: `(category="A", channel="E")` and `(category="A", channel="D")`. `quiet_hours_start`/`quiet_hours_end` apply per row as currently modelled, so they're duplicated across a user's rows rather than set once globally.

## NotificationDelivery

A delivery attempt for a notification, on a specific channel.

| Field | Type | Notes |
| --- | --- | --- |
| `notification` | `ForeignKey(Notification)` | `related_name='delivery'` — access via `notification.delivery.all()` |
| `channel` | `CharField(100)`, choices from module-level `CHANNEL_CHOICES` | Shared with `NotificationPreferences.channel` |
| `delivery_status` | `CharField(100)`, choices `P` (Pending) / `S` (Sent) / `F` (Failed) / `SK` (Skipped) | Required |
| `attempted_at` | `DateTimeField` | Auto-set on create |
| `provider_response` | `TextField` | Required |

**Constraints:** none implemented yet. Intended to be a `UniqueConstraint` on `(notification, channel)` so the same notification can't get duplicate delivery rows on the same channel, while still allowing separate rows per channel (e.g. one email row and one Discord row for the same notification).

**Usage:** one `Notification` can have multiple `NotificationDelivery` rows — one per channel it was sent on. `related_name='delivery'` reads as singular but actually returns a manager (`notification.delivery.all()`), since the relationship is one-to-many; a plural name like `deliveries` would read more naturally here.

## MutedContent

A source a user has muted.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='muted_content'` — access via `user.muted_content` |
| `muted_until` | `DateTimeField` | Required |

**Constraints — currently broken:** `Meta.constraints` includes a `UniqueConstraint` named `unique_mute_per_user_and_source` referencing a `source` field, but no such field exists on the model yet (a commented-out line is left as a TODO). As written, this will fail Django's system checks and block `makemigrations`/`migrate`/`check`. This needs either the source-reference fields added, or the constraint removed/commented out until they are.

**Usage:** not usable yet — without a source-reference field, a `MutedContent` row can record *who* muted something but not *what* they muted.

## Known open items across this app

These affect more than one model and are worth resolving together rather than per-model:

- **Source references.** `Notification`, `Reminder`, and `MutedContent` all need a way to point at "the thing this is about" (an assignment, lecture, group, etc.), via the plan's *source app label / source object type / source object identifier* fields rather than a single generic FK. None of the three have this yet.
- **Uniqueness constraints.** `Reminder`, `NotificationPreferences`, `NotificationDelivery`, and `MutedContent` all have plan-specified uniqueness rules that aren't implemented yet, mostly because they depend on the source-reference fields above.
- **`MutedContent`'s constraint is actively broken**, not just incomplete — see above.

## How the models relate

```
User (Django auth)
 ├─ notifications              → Notification (1:M)
 ├─ reminders                  → Reminder (1:M, via recipient)
 ├─ notification_preferences   → NotificationPreferences (1:M, one row per category+channel)
 └─ muted_content              → MutedContent (1:M) — non-functional until `source` exists

Notification
 └─ delivery → NotificationDelivery (1:M, one row per channel attempted)
```
