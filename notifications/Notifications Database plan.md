# notifications

Owns alerts, reminders, notification preferences, and notification state.

This app is the home for assignment reminders, lecture reminders, calendar reminders, group updates, friend requests, message notifications, study-session invitations, channels, categories, reminder timing, muted groups, read state, unread state, and configurable preferences.

Other apps should generate events that may need notifications, but this app controls how those alerts are stored, presented, read, and configured.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Notification | An item in a user's notification feed | Recipient user reference; actor user reference if applicable; category as choice text; title as short text; body as long text; source app label as short text; source object type as short text; source object identifier as positive integer; read timestamp; created timestamp | Recipient and title required; category limited to supported notification categories |
| Reminder | A scheduled reminder for a deadline, lecture, event, or task | Recipient user reference; source app label as short text; source object type as short text; source object identifier as positive integer; remind at datetime; status as choice text | Remind-at timestamp required; one active reminder per recipient, source object, and remind-at time |
| Notification preference | A user's notification settings | User reference; category as choice text; channel as choice text; enabled flag as boolean; quiet hours start and end times | One preference per user, category, and channel; category and channel must use supported choices |
| Notification delivery | A delivery attempt for a notification | Notification reference; channel as choice text; delivery status as choice text; attempted timestamp; provider response as long text | Delivery status limited to pending, sent, failed, or skipped |
| Muted context | A group, project, conversation, or other context a user muted | User reference; source app label as short text; source object type as short text; source object identifier as positive integer; muted until datetime | One mute per user and source object |

Other apps should supply the event context. This app decides whether to create a notification, when to remind the user, how to deliver it, and whether it is read or muted.
