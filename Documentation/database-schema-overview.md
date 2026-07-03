# Database Schema Overview

This is a high-level planning reference for the Ceres database. It describes app ownership, cross-app rules, example flows, and constraint themes without defining Django model code.

The most important boundary rule is that each app owns its own records. Other apps should link to those records rather than duplicating them. For detailed per-table field definitions, see the plan doc inside each app directory.

## App-owned table groups

| App | Main tables | What they own |
| --- | --- | --- |
| `accounts` | User profile, account preference, privacy preference, friendship, friend request, blocked user, friend request event, user content permission | Identity, profile details, privacy settings, direct user relationships, and friend request audit events |
| `academics` | Module, module membership, lecture, timetable entry, assignment, revision topic | University structure, teaching sessions, assignments, and revision topics |
| `planning` | Calendar event, task, task assignment, task link, study session, study session participant, deadline, timetable import | Time, tasks, deadlines, study sessions, timetable import jobs, and planning behaviour. A `Goal` table has been discussed but has no schema issue yet — not a scoped table |
| `content` | Note, note link, content collection, tag, tagged content, whiteboard, note version | Reusable academic content, notes, whiteboards, tags, and content organisation |
| `collaboration` | Study group, group membership, group invitation, group project, project membership, discussion thread, discussion message, conversation, conversation participant, chat message | Shared workspaces, projects, discussions, and messaging |
| `files` | Stored file, file version, file link, file share, file tag, file preview | Uploaded files, metadata, previews, versions, sharing, and attachments |
| `notifications` | Notification, reminder, notification preference, notification delivery, muted content | Alerts, reminders, delivery attempts, read state, and notification preferences |
| `search` | Search index entry, search history item, saved search, search synonym (search access hint is deferred and not yet implemented) | Search summaries, history, saved searches, suggestions, and optional access hints |
| `core` | Dashboard layout, dashboard widget setting, quick action preference, user interface preference | Presentation preferences for the overall Ceres experience |
| `config` | No product tables | Project configuration only |

## Cross-app ownership rules

| Data concept | Owning app | Other apps should do this |
| --- | --- | --- |
| User identity and direct friendships | `accounts` | Reference users and friendships rather than duplicating profile data |
| Modules, lectures, assignments, and timetable entries | `academics` | Link to academic records when displaying notes, tasks, files, discussions, or reminders |
| Tasks, planning progress, deadlines, calendar events, and study sessions | `planning` | Use task links and deadline links instead of adding separate task systems |
| Notes and whiteboards | `content` | Create note links instead of separate lecture, assignment, project, or meeting note tables |
| Study groups, group projects, discussions, and messages | `collaboration` | Reference notes, files, tasks, and users from their owning apps |
| Uploaded files and attachments | `files` | Create file links instead of separate upload records |
| In-module file filtering and sorting | `files` | Query `StoredFile`, `FileTag`, and `FileShare` directly; no dependency on `search` app or `SearchIndexEntry` |
| Files appearing in global Ceres search | `search` | A `files` indexer writes `StoredFile` summaries into `SearchIndexEntry`; this is separate from in-module filtering |
| Alerts and reminders | `notifications` | Send source context and let notifications decide storage and delivery |
| Global search | `search` | Index summaries and always respect source app permissions |
| Dashboard and shared interface preferences | `core` | Store presentation choices only |

## Example high-level flow

| User action | Tables likely involved |
| --- | --- |
| A student creates a module | User, module, module membership |
| A student adds a lecture note | User, module, lecture, note, note link |
| A student uploads a lecture attachment | User, stored file, file link, lecture |
| A student creates an assignment plan | Assignment, task, task link, deadline, reminder |
| A group project is created | User, study group, group project, project membership |
| A group project uses shared work | Group project, task link, note link, file link, discussion thread |
| A notification is created for a deadline | Deadline, reminder, notification, notification delivery |
| A search result is shown | Search index entry plus permission checks against the source app |

## Constraint themes

| Theme | Suggested rule |
| --- | --- |
| Ownership | Most tables should include an owner, creator, or recipient user where appropriate |
| Uniqueness | Use uniqueness rules for one-to-one settings, membership records, links, shares, and duplicate relationship prevention. Key notification constraints: `NotificationPreferences (user, category, channel)`, `NotificationDelivery (notification, channel)`, `Reminder (recipient, source_app, source_object_type, source_object_id, remind_at)`, `MutedContent (user, source_app, source_object_type, source_object_id)` |
| Choices | Use controlled choices for statuses, roles, permissions, visibility, notification categories, and content formats |
| Time | Store created and updated timestamps on records that users edit or review |
| Access | Any cross-app link must be permission checked through the source app before display |
| Reuse | Notes, files, tasks, notifications, and search should be shared systems, not reimplemented per feature |
