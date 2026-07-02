# accounts

Owns user identity, account settings, personal preferences, profiles, and user-to-user relationships.

This app is the home for registration, authentication, account management, profile details, privacy preferences, friend profiles, friend requests, accepted friendships, blocked or removed users, and shared-content permissions tied to user relationships.

It should not own study groups, group projects, messaging, or shared project content. Those responsibilities belong to `collaboration`.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| User profile | Public and private profile details for a user | User reference; display name as short text; profile image file reference; university as short text; course as short text; bio as long text; visibility as choice text; created and updated timestamps | One profile per user; display name required; visibility limited to private, friends, or public |
| Account preference | User-level account and privacy settings | User reference; timezone as short text; email notifications flag as boolean; searchable profile flag as boolean | One preference record per user; timezone required |
| Friendship | Direct relationship or pending friend request between two users | First user reference; second user reference; requested-by user reference; status as choice text; requested timestamp; accepted timestamp; rejected timestamp; removed timestamp; blocked timestamp | Users must be stored in a consistent order; only one relationship should exist for the same pair of users; requested-by must be one of the two users; status limited to requested, accepted, rejected, blocked, or removed |
| Friend request event | Optional history of friendship actions | Friendship reference; actor user reference; action as choice text; note as short text; created timestamp | Action required; actor must be one of the users involved in the friendship |
| User content permission | User-to-user sharing permission defaults | Owner user reference; target user reference; permission level as choice text; applies-to scope as choice text | Owner and target must be different users; one permission per owner, target, and scope |

This app should describe who users are and how they relate to one another. Study groups, project membership, messages, shared notes, and shared files should be represented in their owning apps and reference these user records.
