# notifications — Implemented Database Schema

This document describes the models as actually implemented in `notifications/models.py`, and how to use them. Unlike `Notifications Database plan.md`, which describes the intended design, this reflects the current code. Update this file (not the plan) whenever the models change.

`notifications/migrations/0001_initial.py` has been generated and applied. A repair migration (`0002_repair_stale_notification_tables.py`) has since been added to address a known issue where a stale `django_migrations` record from an earlier version of this app masked schema mismatches. If `python manage.py showmigrations notifications` shows `0002_repair_stale_notification_tables` as applied but the admin still errors on a missing column, check that migration's contents before assuming the mismatch is resolved.

## Notification

A feed item sent from one user (the actor) to another (the recipient).

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key (no explicit override) |
| `recipient` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='noticication_recipient_fk'` — access via `user.noticication_recipient_fk`. Name has a typo (`noticication` for "notification") and reads like a field, not a reverse manager; consider renaming to something like `received_notifications` |
| `actor` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notification_actor_fk'` — access via `user.notification_actor_fk`. Same naming-convention note as `recipient` (minus the typo) |
| `category` | `CharField(3)`, choices `AR`/`LR`/`CR`/`GU`/`FR`/`NM`/`SSI` | Choices defined in module-level `CATEGORY_CHOICES` (Assignment Reminder, Lecture Reminder, Calendar Reminder, Group Update, Friend Request, New Message, Study Session Invite) |
| `title` | `CharField(120)` | Required |
| `body` | `TextField` | Required |
| `source_app` | `CharField(120)` | Which app the source object belongs to |
| `source_object_type` | `CharField(120)` | Model name of the source object |
| `source_object_id` | `PositiveIntegerField` | Primary key of the source object |
| `read_at` | `DateTimeField`, nullable | Unset while unread |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField` | Auto-set on every save |

**Constraints:** none implemented.

**Usage:** `Notification` carries a source reference (`source_app` / `source_object_type` / `source_object_id`) so a row can be traced back to the assignment, lecture, group, etc. that triggered it. It's a manually-tracked reference rather than Django's built-in `contenttypes.GenericForeignKey`. `Reminder` and `MutedContent` now use the same hand-rolled pattern (see below) — worth evaluating whether to migrate all three to `contenttypes` before more logic depends on the current approach. There is no dedicated `notification_name`/short-label field — `title` serves that purpose.

## Reminder

A scheduled, one-shot reminder for a deadline, lecture, event, or task.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `recipient` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='reminder_recipient_fk'` — access via `user.reminder_recipient_fk` |
| `source_app` | `CharField(120)` | Which app the source object belongs to |
| `source_object_type` | `CharField(120)` | Model name of the source object |
| `source_object_id` | `PositiveIntegerField` | Primary key of the source object |
| `remind_at` | `DateTimeField` | Required |
| `status` | `CharField(120)`, choices `P`/`S`/`C` | Choices from module-level `STATUS_CHOICES`: Pending, Sent, Canceled |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField` | Auto-set on every save |

**Constraints:**
- `unique_reminder` — unique on `(recipient, source_app, source_object_type, source_object_id, remind_at)`.

**Usage:** this model has been substantially rebuilt since it was first documented. It now carries the same source-reference triple as `Notification`, so it can point at the thing it's reminding about — this was previously a gap. In the process, the earlier `reminder_id`/`reminder_content` fields were dropped in favour of the standard `id`, and recurrence support (`next_fire_at`, `frequency`) has been removed entirely rather than implemented — `Reminder` is currently one-shot only, consistent with `STATUS_CHOICES` offering no repeat-related states.

## NotificationPreferences

A user's notification settings per category and channel.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notification_preferences'` — access via `user.notification_preferences` |
| `category` | `CharField(100)`, choices from `CATEGORY_CHOICES` | Same category set as `Notification.category` |
| `channel` | `CharField(100)`, choices `A` (All) / `T` (Text) / `E` (Email) / `D` (Discord) / `I` (In App) | Choices defined in module-level `CHANNEL_CHOICES`, shared with `NotificationDelivery` |
| `enabled_flag` | `BooleanField` | Default `True` |
| `quiet_hours_start` | `TimeField` | Required |
| `quiet_hours_end` | `TimeField` | Required |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField` | Auto-set on every save |

**Constraints:**
- `unique_notification_perferences` — unique on `(user, category, channel)`; one preference row per category/channel combination per user. Constraint name has a typo ("perferences" for "preferences") — cosmetic, but worth fixing before it's referenced elsewhere (e.g. in a migration dependency or error-handling code).

**Usage:** a user's full preference set is `user.notification_preferences.all()` — one row per category/channel combination they've configured, rather than a single row with multiple channels selected. A user wanting Assignment Reminders by both email and Discord has two rows: `(category="AR", channel="E")` and `(category="AR", channel="D")`. `quiet_hours_start`/`quiet_hours_end` apply per row as currently modeled, so they're duplicated across a user's rows rather than set once globally.

## NotificationDelivery

A delivery attempt for a notification, on a specific channel.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `notification` | `ForeignKey(Notification)` | `related_name='delivery'` — access via `notification.delivery.all()` |
| `channel` | `CharField(100)`, choices from `CHANNEL_CHOICES` | Shared with `NotificationPreferences.channel` |
| `status` | `CharField(100)`, choices `P` (Pending) / `S` (Sent) / `F` (Failed) / `SK` (Skipped) | Required. Field is named `status`, not `delivery_status` |
| `attempted_at` | `DateTimeField` | Auto-set on create |
| `provider_response` | `TextField` | Required, no default — every delivery attempt must supply a response value even if there isn't one yet |
| `created_at` | `DateTimeField` | Auto-set on create |
| `updated_at` | `DateTimeField` | Auto-set on every save |

**Constraints:**
- `unique_notification_delivery` — unique on `(notification, channel)`; the same notification can't get duplicate delivery rows on the same channel, while still allowing separate rows per channel.

**Usage:** one `Notification` can have multiple `NotificationDelivery` rows — one per channel it was sent on. `related_name='delivery'` reads as singular but returns a manager for potentially many rows (`notification.delivery.all()`); `deliveries` would read more naturally.

## MutedContent

A source a user has muted.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='muted_content'` — access via `user.muted_content` |
| `source_app` | `CharField(120)` | Which app the muted object belongs to |
| `source_object_type` | `CharField(120)` | Model name of the muted object |
| `source_object_id` | `PositiveIntegerField` | Primary key of the muted object |
| `muted_until` | `DateTimeField` | Required |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_mute_per_user_and_source` — unique on `(user, source_app, source_object_type, source_object_id)`. This constraint previously referenced a `source` field that didn't exist and had to be commented out to unblock migrations; the source-reference fields have since been added and the constraint is now live.

**Usage:** a `MutedContent` row can now record both who muted something and what they muted — the earlier gap (a row that recorded *who* but not *what*) is resolved.

## Known open items across this app

These affect more than one model and are worth resolving together rather than per-model:

- **Generic references are hand-rolled.** `Notification`, `Reminder`, and `MutedContent` all use three loosely-connected columns (`source_app`/`source_object_type`/`source_object_id`) rather than Django's `contenttypes` framework (`ContentType` + `GenericForeignKey`), which exists for exactly this pattern. Now that the pattern is used consistently across three models, it's worth evaluating a move to `contenttypes` before a fourth model repeats it.
- **Recurrence on `Reminder` was removed rather than implemented.** The earlier `next_fire_at`/`frequency` fields are gone; `Reminder` is one-shot only for now.
- **Related names on `Notification` (`noticication_recipient_fk`, `notification_actor_fk`) read like field names, not reverse accessors**, and `noticication_recipient_fk` has a typo — worth revisiting for clarity (e.g. `received_notifications` / `sent_notifications`).
- **`NotificationPreferences`'s constraint name (`unique_notification_perferences`) has a typo** — cosmetic, but worth a clean rename while nothing else depends on the literal string.

All four models that need database-level uniqueness (`Reminder`, `NotificationPreferences`, `NotificationDelivery`, `MutedContent`) now have their constraints implemented.

## How the models relate

```
User (Django auth)
 ├─ noticication_recipient_fk  → Notification (1:M, as recipient)
 ├─ notification_actor_fk      → Notification (1:M, as actor)
 ├─ reminder_recipient_fk      → Reminder (1:M, via recipient)
 ├─ notification_preferences   → NotificationPreferences (1:M, one row per category+channel)
 └─ muted_content               → MutedContent (1:M, carries its own source reference)

Notification
 └─ delivery → NotificationDelivery (1:M, one row per channel attempted)
```
