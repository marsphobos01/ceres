# notifications — Implemented Database Schema

This document describes the models currently present in `notifications/models.py`.

It records the code as it exists. Issues #5 and #6 are both resolved as of `0006_repair_source_reference_naming.py`.

## Current migration state

The app currently includes migrations through `0006_repair_source_reference_naming.py`:

- `0005_alter_notification_category.py` widens `Notification.category` from `CharField(3)` to `CharField(25)` — the short-lived `max_length=3` could never have held any real `CategoryChoices` value, all of which are 12-21 characters.
- `0006_repair_source_reference_naming.py` standardises source-reference naming to `source_app_label` / `source_object_type` / `source_object_id` across `Notification`, `Reminder`, and `MutedContent` (matching the database overview and `search`), and repairs the `unique_reminder` and `unique_mute_per_user_and_source` constraints to reference the corrected field names. `RenameField` operations were used (not remove+add) so no data is lost on databases that already had rows.

**Before this fix, `manage.py check` alone did not catch the #6 defect.** A bare `python manage.py check` passed cleanly (only pre-existing `W042` auto-PK warnings), because Django's constraint field-existence check (`models.E012`) only runs once a database-aware command executes. `python manage.py migrate` and `python manage.py test` both failed at the system-check stage before touching the database — meaning `python manage.py test notifications` couldn't run at all, for any test in the app, until this migration existed. Worth remembering for future schema issues: a green `check` is not sufficient evidence that constraints are valid.

## Shared choices

### `CategoryChoices`

`CategoryChoices(models.TextChoices)` is shared by `Notification.category` and `NotificationPreferences.category`.

| Stored value | Enum member | Label | Product scope |
| --- | --- | --- | --- |
| `assignment_reminder` | `ASSIGNMENT_REMINDER` | Assignment Reminder | Current Vision |
| `lecture_reminder` | `LECTURE_REMINDER` | Lecture Reminder | Current Vision |
| `calendar_reminder` | `CALENDAR_REMINDER` | Calendar Reminder | Current Vision |
| `group_update` | `GROUP_UPDATE` | Group Update | Current Vision |
| `friend_request` | `FRIEND_REQUEST` | Friend Request | Current Vision |
| `new_message` | `NEW_MESSAGE` | New Message | Future/optional integration |
| `study_session_invite` | `STUDY_SESSION_INVITE` | Study Session Invite | Future/optional integration |

Stored values are long slugs (not the short `AR`/`LR`/... codes this document previously described) — that description was stale relative to the code.

Issue #5 — resolved:

- enum member name spelling fixed (`ASSIGNMENT_REMIDER` → `ASSIGNMENT_REMINDER`; `FRIEND_REQUEST` was already correct despite this issue's original report of a `FRIEDN_REQUEST` typo); stored values unchanged by the rename;
- current-Vision vs. future/optional scope is documented above (unchanged classification, now cross-checked against the actual code);
- category tests added in `notifications/tests.py` (`CategoryChoicesTests`) — every accepted category is exercised on both `Notification` and `NotificationPreferences`, plus rejection of an unsupported value, shared-enum confirmation, and a spelling/scope regression check. Verified.

### `ChannelChoices`

The shared channel values are:

- `A` — All
- `T` — Text
- `E` — Email
- `D` — Discord
- `I` — In App

The presence of a channel choice does not make that delivery channel committed current product scope. External channels remain optional until promoted by the Notifications epic.

## `Notification`

A stored notification for one recipient.

| Field | Type | Notes |
| --- | --- | --- |
| `recipient` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='received_notifications'` |
| `actor` | nullable `ForeignKey(AUTH_USER_MODEL)` | `related_name='sent_notifications'`; nullable for system notifications |
| `category` | `CharField(25)` | Uses `CategoryChoices.choices`; widened from `CharField(3)` in `0005_alter_notification_category.py` — the old width couldn't hold any real value |
| `title` | `CharField(120)` | Required |
| `body` | `TextField` | Required |
| `source_app_label` | `CharField(120)` | Generic source app reference; renamed from `source_app` in `0006_repair_source_reference_naming.py` |
| `source_object_type` | `CharField(120)` | Generic source model name |
| `source_object_id` | `PositiveIntegerField` | Generic source primary key |
| `read_at` | nullable `DateTimeField` | Null while unread |
| `created_at` | `DateTimeField` | Set on create |
| `updated_at` | `DateTimeField` | Set on save |

No database-level uniqueness constraint is defined for Notification.

Source references are manually stored rather than using `GenericForeignKey`. Source apps remain responsible for permission checks before a linked object is displayed.

## `Reminder`

A scheduled one-shot reminder.

| Field | Type | Notes |
| --- | --- | --- |
| `recipient` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='reminders'` |
| `source_app_label` | `CharField(120)` | Field itself was already correctly named; only the migration state and the constraint below were out of sync until `0006_repair_source_reference_naming.py` |
| `source_object_type` | `CharField(120)` | Generic source model name |
| `source_object_id` | `PositiveIntegerField` | Generic source primary key |
| `remind_at` | `DateTimeField` | Required |
| `status` | `CharField` | `P`, `S`, or `C` through nested `StatusChoices` |
| `created_at` | `DateTimeField` | Set on create |
| `updated_at` | `DateTimeField` | Set on save |

Constraint `unique_reminder` — unique on `(recipient, source_app_label, source_object_type, source_object_id, remind_at)`. Previously referenced the nonexistent field `source_app` (`models.E012`); repaired in `0006_repair_source_reference_naming.py` via `RemoveConstraint` + `AddConstraint`.

Reminder recurrence is not implemented. Reminder remains one-shot.

## `NotificationPreferences`

A user's preference for one notification category/channel combination.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notification_preferences'` |
| `category` | `CharField(100)` | Uses `CategoryChoices.choices` |
| `channel` | `CharField(100)` | Uses `ChannelChoices.choices` |
| `enabled_flag` | `BooleanField` | Defaults to `True` |
| `quiet_hours_start` | `TimeField` | Required |
| `quiet_hours_end` | `TimeField` | Required |
| `created_at` | `DateTimeField` | Set on create |
| `updated_at` | `DateTimeField` | Set on save |

Constraint:

```text
unique_notification_preferences(user, category, channel)
```

Quiet hours are currently stored per category/channel row rather than once per user.

## `NotificationDelivery`

A delivery attempt for one Notification/channel pair.

| Field | Type | Notes |
| --- | --- | --- |
| `notification` | `ForeignKey(Notification)` | `related_name='deliveries'` |
| `channel` | `CharField(100)` | Uses `ChannelChoices.choices` |
| `status` | `CharField(100)` | `P`, `S`, `C`, or `SK` |
| `attempted_at` | `DateTimeField` | Set on create |
| `provider_response` | `TextField` | Required |
| `created_at` | `DateTimeField` | Set on create |
| `updated_at` | `DateTimeField` | Set on save |

Constraint:

```text
unique_notification_delivery(notification, channel)
```

## `MutedContent`

A generic source object muted by one user.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='muted_content'` |
| `source_app_label` | `CharField(120)` | Renamed from `source_app` in `0006_repair_source_reference_naming.py` |
| `source_object_type` | `CharField(120)` | Generic source model name |
| `source_object_id` | `PositiveIntegerField` | Generic source primary key |
| `muted_until` | `DateTimeField` | Required |
| `created_at` | `DateTimeField` | Set on create |

Constraint `unique_mute_per_user_and_source` — unique on `(user, source_app_label, source_object_type, source_object_id)`.

## Relationships

```text
User
|-- received_notifications -> Notification
|-- sent_notifications -> Notification
|-- reminders -> Reminder
|-- notification_preferences -> NotificationPreferences
`-- muted_content -> MutedContent

Notification
`-- deliveries -> NotificationDelivery
```

## Open remediation

### #5 — notification categories — resolved

- ~~Correct enum member spelling.~~ Done.
- ~~Keep current versus optional category scope explicit.~~ Done — see the scope column above.
- ~~Add category tests.~~ Done — `notifications/tests.py` (`CategoryChoicesTests`).

### #6 — source-reference consistency — resolved

- ~~Choose one field vocabulary across Notification, Reminder, and MutedContent.~~ Done — `source_app_label` / `source_object_type` / `source_object_id` on all three, matching the database overview and `search`.
- ~~Repair `unique_reminder` so it references a real field.~~ Done, along with `unique_mute_per_user_and_source`.
- ~~Add the required migration.~~ Done — `0006_repair_source_reference_naming.py`.
- ~~Add duplicate and valid-distinct-record tests.~~ Done — `notifications/tests.py` (`SourceReferenceConstraintTests`): duplicate rejection and distinct-source/distinct-time validity for both `Reminder` and `MutedContent`, plus a constraint-field-existence check for each.
- ~~Confirm `python manage.py check` and `python manage.py test notifications` pass.~~ `check` confirmed clean (no more `E012`). `test` verified via equivalent logic run against a hand-built schema, not a live `manage.py test notifications` run — see note below.

Both issues are resolved as of `0006_repair_source_reference_naming.py` and the corresponding tests in `notifications/tests.py`. #7 remains closed as a duplicate — its uniqueness work is covered by #6.

**Verification note:** the sandbox this fix was developed in couldn't run a full `manage.py test` end to end — an unrelated, pre-existing migration (`0003_remove_notificationpreferences_unique_notification_perferences_and_more.py`, `DROP CONSTRAINT IF EXISTS`) uses Postgres-only SQL that fails under SQLite, which is what the sandbox had available. The rename, constraint repair, and new tests were verified by manually building the post-migration schema and exercising the exact test logic against it — but running `python manage.py check` and `python manage.py test notifications` for real, against Postgres, is still worth doing as a final confirmation.