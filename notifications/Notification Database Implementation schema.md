# notifications — Implemented Database Schema

This document describes the models as actually implemented in `notifications/models.py`, and how to use them. Unlike `Notifications Database plan.md`, which describes the intended design, this reflects the current code. Update this file (not the plan) whenever the models change.

`notifications/migrations/0001_initial.py` has been generated and applied. Note: on the shared dev database, a stale `django_migrations` record from an earlier version of this app has been known to mask schema mismatches — if `python manage.py showmigrations notifications` shows `0001_initial` as applied but the admin errors on a missing column, the applied migration record and the actual table are out of sync and need to be reconciled before trusting this document against a live database.

## Notification

A feed item sent from one user (the actor) to another (the recipient).

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key (no explicit override) |
| `recipient` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='recipient_fk'` — access via `user.recipient_fk`. Name reads like a field, not a reverse manager; consider renaming to something like `received_notifications` |
| `actor` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='actor_fk'` — access via `user.actor_fk`. Same naming note as `recipient` |
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

**Usage:** unlike the earlier version of this model, `Notification` now carries a source reference (`source_app` / `source_object_type` / `source_object_id`) so a row can be traced back to the assignment, lecture, group, etc. that triggered it — this was previously a TODO. It's a manually-tracked reference rather than Django's built-in `contenttypes.GenericForeignKey`; worth evaluating whether to migrate to that framework before much logic is built on top of these three fields. There is currently no dedicated `notification_name`/short-label field — `title` serves that purpose.

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

**Constraints:** none implemented yet. `Meta.constraints` is present but empty, with a TODO — still needs source-reference fields before a rule like "one active reminder per recipient/source/time" can be written.

**Usage — important:**
- No field yet links a reminder back to what it's reminding about (a commented-out `object_id` line is left as a TODO) — this is the same gap flagged on `Notification` before the source-reference fields were added there; `Reminder` hasn't received the same treatment yet.
- `frequency` beyond `O` (Once) is defined but not functional — no process exists yet to act on `next_fire_at` or reschedule recurring reminders. Treat any reminder with `frequency != "O"` as unimplemented.

## NotificationPreferences

A user's notification settings per category and channel.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notification_preferences'` — access via `user.notification_preferences` |
| `category` | `CharField(100)`, choices from `CATEGORY_CHOICES` | Same category set as `Notification.category`. Now a `CharField`, consistent with `category` elsewhere — this was previously a `TextField`, an inconsistency that's now resolved |
| `channel` | `CharField(100)`, choices `A` (All) / `T` (Text) / `E` (Email) / `D` (Discord) / `I` (In App) | Choices defined in module-level `CHANNEL_CHOICES`, shared with `NotificationDelivery` |
| `enabled_flag` | `BooleanField` | Default `True` |
| `quiet_hours_start` | `TimeField` | Required |
| `quiet_hours_end` | `TimeField` | Required |

**Constraints:** none implemented yet. "One preference per user, category, and channel" is not yet enforced at the database level.

**Usage:** a user's full preference set is `user.notification_preferences.all()` — one row per category/channel combination they've configured, rather than a single row with multiple channels selected. A user wanting Assignment Reminders by both email and Discord has two rows: `(category="AR", channel="E")` and `(category="AR", channel="D")`. `quiet_hours_start`/`quiet_hours_end` apply per row as currently modeled, so they're duplicated across a user's rows rather than set once globally. The `read_at` field present in an earlier version of this model (which didn't conceptually belong on a preference row) has been removed.

## NotificationDelivery

A delivery attempt for a notification, on a specific channel.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `notification` | `ForeignKey(Notification)` | `related_name='delivery'` — access via `notification.delivery.all()` |
| `channel` | `CharField(100)`, choices from `CHANNEL_CHOICES` | Shared with `NotificationPreferences.channel` |
| `delivery_status` | `CharField(100)`, choices `P` (Pending) / `S` (Sent) / `F` (Failed) / `SK` (Skipped) | Required |
| `attempted_at` | `DateTimeField` | Auto-set on create |
| `provider_response` | `TextField` | Required, no default — every delivery attempt must supply a response value even if there isn't one yet |

**Constraints:** none implemented yet. Intended to be a `UniqueConstraint` on `(notification, channel)` so the same notification can't get duplicate delivery rows on the same channel, while still allowing separate rows per channel.

**Usage:** one `Notification` can have multiple `NotificationDelivery` rows — one per channel it was sent on. `related_name='delivery'` reads as singular but returns a manager for potentially many rows (`notification.delivery.all()`); `deliveries` would read more naturally.

## MutedContent

A source a user has muted.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='muted_content'` — access via `user.muted_content` |
| `muted_until` | `DateTimeField` | Required |

**Constraints:** none active. A `UniqueConstraint` named `unique_mute_per_user_and_source` referencing a `source` field is written out but commented out (inside the class body, along with the missing `source` field itself) rather than live — this was previously an *active* constraint referencing a nonexistent field, which would have failed Django's system checks and blocked `makemigrations`/`migrate`/`check`. Commenting it out unblocked migrations; it still needs the source-reference field(s) added before the constraint can be restored.

**Usage:** not usable yet — without a source-reference field, a `MutedContent` row can record *who* muted something but not *what* they muted.

## Known open items across this app

These affect more than one model and are worth resolving together rather than per-model:

- **Source references.** Only `Notification` has the *source app label / source object type / source object identifier* pattern so far. `Reminder` and `MutedContent` still need it before they can point at "the thing this is about" (an assignment, lecture, group, etc.).
- **Generic references are hand-rolled.** `Notification`'s source fields are three loosely-connected columns rather than Django's `contenttypes` framework (`ContentType` + `GenericForeignKey`), which exists for exactly this pattern. Worth evaluating before more logic depends on the current approach.
- **Uniqueness constraints.** `Reminder`, `NotificationPreferences`, `NotificationDelivery`, and `MutedContent` all need database-level uniqueness rules that aren't implemented yet, mostly because they depend on the source-reference fields above.
- **Recurrence on `Reminder` is unimplemented** beyond the field definitions — no scheduler exists yet.
- **Related names on `Notification` (`recipient_fk`, `actor_fk`) read like field names, not reverse accessors** — worth revisiting for clarity (e.g. `received_notifications` / `sent_notifications`).

## How the models relate

```
User (Django auth)
 ├─ recipient_fk               → Notification (1:M, as recipient)
 ├─ actor_fk                   → Notification (1:M, as actor)
 ├─ reminders                  → Reminder (1:M, via recipient)
 ├─ notification_preferences   → NotificationPreferences (1:M, one row per category+channel)
 └─ muted_content               → MutedContent (1:M) — non-functional until `source` exists

Notification
 └─ delivery → NotificationDelivery (1:M, one row per channel attempted)
```
