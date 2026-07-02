# collaboration

Owns shared spaces and communication between users.

This app is the home for study groups, group projects, group membership, invitations, project workspaces, project roles, shared academic activity, discussions, messaging, collaboration permissions, and group-project coordination.

## Does not own

User identity, general files, general notes, and generic tasks belong to `accounts`, `files`, `content`, and `planning`. This app coordinates those shared systems rather than recreating them.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Study group | A shared study space | Created by user reference; name as short text; description as long text; visibility as choice text; created and updated timestamps | Name required; visibility limited to private, invite-only, or discoverable |
| Group membership | A user's membership in a study group | Study group reference; user reference; role as choice text; status as choice text; joined timestamp | One membership per group and user; role limited to owner, admin, member, or viewer |
| Group invitation | An invitation to join a study group or project | Sender user reference; recipient user reference; target type as choice text; target identifier as positive integer; status as choice text; expires timestamp | Recipient required; status limited to pending, accepted, declined, expired, or cancelled |
| Group project | A collaborative project workspace | Study group reference if applicable; owner user reference; title as short text; description as long text; status as choice text; due datetime; created and updated timestamps | Title required; status limited to active, paused, completed, or archived |
| Project membership | A user's role in a group project | Project reference; user reference; role as choice text; allocation label as short text; joined timestamp | One membership per project and user; user should have permission to access the project |
| Discussion thread | A discussion attached to an academic or collaborative context | Created by user reference; title as short text; linked app label as short text; linked object type as short text; linked object identifier as positive integer; locked flag as boolean | Title required; linked target must be permission checked |
| Discussion message | A message inside a discussion thread | Thread reference; author user reference; body as long text; parent message reference for replies; edited timestamp; created timestamp | Body required unless an attachment-only message is allowed; author must have thread access |
| Conversation | A direct or group messaging container | Conversation type as choice text; created timestamp | Type limited to direct or group; has no direct participant fields — participants are managed entirely via Conversation participant |
| Conversation participant | A user's membership in a conversation | Conversation reference; user reference; muted flag as boolean; joined timestamp | One participant per conversation and user |
| Chat message | A message in a conversation | Conversation reference; author user reference; body as long text; reply-to message reference (self, nullable — threaded replies); direct file attachment reference (nullable, `files.StoredFile`); created and updated timestamps | Author must be a participant; message belongs to exactly one conversation; attachment is a simple nullable FK rather than a File share record, since a message either has one file or it doesn't |

## Cross-app linking

Shared files, shared notes, and task boards should reference `files`, `content`, and `planning` rather than duplicating those systems inside this app.
