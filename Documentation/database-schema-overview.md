# Database Schema Overview

This is a loose planning chart for the Ceres database. It describes likely tables, fields, data types, and relationships without defining Django model code.

The most important boundary rule is that each app owns its own records. Other apps should link to those records rather than duplicating them.

## App-owned table groups

| App | Main tables | What they own |
| --- | --- | --- |
| `accounts` | User profile, account preference, privacy preference, friendship, friend request, blocked user, friend request event, user content permission | Identity, profile details, privacy settings, and direct user relationships |
| `academics` | Module, module membership, lecture, timetable entry, assignment, revision topic | University structure, teaching sessions, assignments, and revision topics |
| `planning` | Calendar event, task, task assignment, task link, study session, study session participant, deadline, goal | Time, tasks, deadlines, study sessions, and planning behaviour |
| `content` | Note, note link, content collection, tag, tagged content, whiteboard, note version | Reusable academic content, notes, whiteboards, tags, and content organisation |
| `collaboration` | Study group, group membership, group invitation, group project, project membership, discussion thread, discussion message, conversation, conversation participant, chat message | Shared workspaces, projects, discussions, and messaging |
| `files` | Stored file, file version, file link, file share, file tag, file preview | Uploaded files, metadata, previews, versions, sharing, and attachments |
| `notifications` | Notification, reminder, notification preference, notification delivery, muted context | Alerts, reminders, delivery attempts, read state, and notification preferences |
| `search` | Search index entry, search access hint, search history item, saved search, search synonym | Search summaries, history, saved searches, suggestions, and optional access hints |
| `core` | Dashboard layout, dashboard widget setting, quick action preference, user interface preference | Presentation preferences for the overall Ceres experience |
| `config` | No product tables | Project configuration only |

## Loose relationship chart

| Source table | Relationship | Target table | Notes |
| --- | --- | --- | --- |
| User profile | belongs to | User | One profile per user |
| Account preference | belongs to | User | One preference record per user |
| Privacy preference | belongs to | User | One preference record per user; separated from account preference to keep concerns distinct |
| Friendship | connects | User to User | Confirmed friendships only; lower user ID always stored first to prevent duplicate pairs |
| Friend request | sent from | User to User | Tracks pending and resolved requests separately from confirmed friendships |
| Blocked user | issued by | User against User | Kept separate from friendship so block checks never touch friendship records |
| Friend request event | records action on | Friend request | Optional audit trail; actor must be one of the two users on the request |
| User content permission | grants access from | User to User | Used as a default sharing rule, not a replacement for app-specific permissions |
| Module | owned by | User | The user owns or manages the module record |
| Module membership | connects | Module to User | Supports shared modules or future tutor/collaborator access |
| Lecture | belongs to | Module | Lectures should not own notes or files directly |
| Timetable entry | belongs to | Module or Lecture | Academic timetable stays in `academics` |
| Assignment | belongs to | Module | Assignment planning details link into `planning` |
| Revision topic | belongs to | Module | May link to study sessions, notes, and tasks |
| Calendar event | owned by | User | May display academic records without owning them |
| Task assignment | connects | Task to User | Allows responsibility and allocation |
| Task link | connects | Task to any supported source object | Used for assignments, group projects, study sessions, notes, modules, and lectures |
| Study session participant | connects | Study session to User | Tracks invitations and attendance |
| Deadline | points to | Assignment, task, event, project, or revision plan | Central deadline behaviour lives in `planning` |
| Goal | owned by | User | May be linked to tasks or revision later |
| Note | owned by | User | Notes are reusable and should not be recreated in other apps |
| Note link | connects | Note to module, lecture, assignment, study session, group project, or revision topic | Lets one note appear in several academic contexts |
| Content collection | belongs to | User | Can nest inside another collection |
| Tagged content | connects | Tag to note or whiteboard | Tag ownership stays with `content` |
| Whiteboard | owned by | User | Can be linked from collaboration or academic contexts |
| Note version | belongs to | Note | Optional edit history |
| Study group | created by | User | Group identity lives in `collaboration` |
| Group membership | connects | Study group to User | Roles and membership status live here |
| Group invitation | connects | User to study group or group project | Recipient accepts or declines |
| Group project | owned by | User or study group | Uses external tasks, notes, and files |
| Project membership | connects | Group project to User | Project roles live here |
| Discussion thread | points to | Module, lecture, assignment, group project, or study group | One discussion system for multiple contexts |
| Discussion message | belongs to | Discussion thread | Replies use a parent message reference |
| Conversation participant | connects | Conversation to User | Messaging membership lives here |
| Chat message | belongs to | Conversation | File attachments should link to `files` |
| Stored file | owned by | User | One reusable file record |
| File version | belongs to | Stored file | Version number unique per file |
| File link | connects | Stored file to module, lecture, assignment, note, study session, group project, or message | Attachments are links to reusable files |
| File share | connects | Stored file to User | Direct file sharing permission |
| File preview | belongs to | Stored file | Generated preview metadata |
| Notification | sent to | User | May point back to any source app object |
| Reminder | scheduled for | User and source object | Can remind about assignments, lectures, events, tasks, or projects |
| Notification preference | belongs to | User | One preference per category and channel |
| Notification delivery | belongs to | Notification | Tracks channel delivery attempts |
| Muted context | connects | User to source object | Used to suppress noisy groups, projects, or conversations |
| Search index entry | summarizes | Any supported source object | Search is not the source of truth |
| Search access hint | connects | Search index entry to User or group | Optional cache that must respect source permissions |
| Search history item | belongs to | User | Can be deleted independently |
| Saved search | belongs to | User | Reusable search shortcut |
| Dashboard layout | belongs to | User | Presentation only |
| Dashboard widget setting | belongs to | User | References widget keys, not source records |
| Quick action preference | belongs to | User | Presentation only |

## Cross-app ownership rules

| Data concept | Owning app | Other apps should do this |
| --- | --- | --- |
| User identity and direct friendships | `accounts` | Reference users and friendships rather than duplicating profile data |
| Modules, lectures, assignments, and timetable entries | `academics` | Link to academic records when displaying notes, tasks, files, discussions, or reminders |
| Tasks, planning progress, deadlines, calendar events, and study sessions | `planning` | Use task links and deadline links instead of adding separate task systems |
| Notes and whiteboards | `content` | Create note links instead of separate lecture, assignment, project, or meeting note tables |
| Study groups, group projects, discussions, and messages | `collaboration` | Reference notes, files, tasks, and users from their owning apps |
| Uploaded files and attachments | `files` | Create file links instead of separate upload records |
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
| Uniqueness | Use uniqueness rules for one-to-one settings, membership records, links, shares, and duplicate relationship prevention |
| Choices | Use controlled choices for statuses, roles, permissions, visibility, notification categories, and content formats |
| Time | Store created and updated timestamps on records that users edit or review |
| Access | Any cross-app link must be permission checked through the source app before display |
| Reuse | Notes, files, tasks, notifications, and search should be shared systems, not reimplemented per feature |
