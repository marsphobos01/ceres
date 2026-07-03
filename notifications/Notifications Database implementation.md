# notifications — Implemented Database Schema

This document describes the models currently present in `notifications/models.py`.

It records the code as it exists, including known inconsistencies. It must not be read as confirmation that every model currently passes Django system checks. Issues #5 and #6 track the remaining remediation.

## Current migration state

The app currently includes migrations through `0004_alter_notificationdelivery_status.py`.

The model code contains a partial source-reference rename on `Reminder` that is not represented by a migration. Do not generate feature work against this inconsistency; complete #6 first.

## Shared choices

### `CategoryChoices`

`CategoryChoices(models.TextChoices)` is shared by `Notification.category` and `NotificationPreferences.category`.

| Stored value | Label | Product scope |
| --- | --- | --- |
| `AR` | Assignment Reminder | Current Vision |
| `LR` | Lecture Reminder | Current Vision |
| `CR` | Calendar Reminder | Current Vision |
| `GU` | Group Update | Current Vision |
| `FR` | Friend Request | Current Vision |
| `NM` | New Message | Future/optional integration |
| `SSI` | Study Session Invite | Future/optional integration |

Known issue #5:

- enum member names currently contain spelling mistakes;
- current versus optional scope must remain explicit;
- tests have not yet been added.

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
| `category` | `CharField(3)` | Uses `CategoryChoices.choices` |
| `title` | `CharField(120)` | Required |
| `body` | `TextField` | Required |
| `source_app` | `CharField(120)` | Generic source app reference; naming is under #6 |
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
| `source_app_label` | `CharField(120)` | Partially renamed in model code; no matching migration currently exists |
| `source_object_type` | `CharField(120)` | Generic source model name |
| `source_object_id` | `PositiveIntegerField` | Generic source primary key |
| `remind_at` | `DateTimeField` | Required |
| `status` | `CharField` | `P`, `S`, or `C` through nested `StatusChoices` |
| `created_at` | `DateTimeField` | Set on create |
| `updated_at` | `DateTimeField` | Set on save |

### Known invalid constraint

The model currently declares `unique_reminder` using:

```text
recipient, source_app, source_object_type, source_object_id, remind_at
```

However, the model field is named `source_app_label`, not `source_app`.

This is an unresolved defect tracked by #6. The constraint, model field, migration state, and documentation must be made consistent before Reminder-dependent feature work starts.

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
| `source_app` | `CharField(120)` | Naming is under #6 |
| `source_object_type` | `CharField(120)` | Generic source model name |
| `source_object_id` | `PositiveIntegerField` | Generic source primary key |
| `muted_until` | `DateTimeField` | Required |
| `created_at` | `DateTimeField` | Set on create |

Constraint:

```text
unique_mute_per_user_and_source(
    user,
    source_app,
    source_object_type,
    source_object_id,
)
```

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

### #5 — notification categories

- Correct enum member spelling.
- Keep current versus optional category scope explicit.
- Add category tests.

### #6 — source-reference consistency

- Choose one field vocabulary across Notification, Reminder, and MutedContent.
- Repair `unique_reminder` so it references a real field.
- Add the required migration.
- Add duplicate and valid-distinct-record tests.
- Confirm `python manage.py check` and `python manage.py test notifications` pass.

Until #5 and #6 close again, notification feature issues should treat this implementation document as an accurate record of current state, not as a declaration that the schema is ready.