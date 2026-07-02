# accounts

Owns user identity, account settings, personal preferences, profiles, and user-to-user relationships.

This app is the home for registration, authentication, account management, profile details, privacy preferences, friend profiles, friend requests, accepted friendships, blocked or removed users, and shared-content permissions tied to user relationships.

## Does not own

Study groups, group projects, messaging, and shared project content belong to `collaboration`.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| User profile | Public and private profile details for a user | User reference; display name as short text; profile image file reference; university as short text; course as short text; bio as long text; visibility as choice text; created and updated timestamps | One profile per user; display name required; visibility limited to private, friends, or public |
| Account preference | User-level account settings | User reference; timezone as short text; email notifications flag as boolean; searchable profile flag as boolean | One preference record per user; timezone required |
| Privacy preference | User-level privacy settings, kept separate from account preferences to avoid mixing concerns | User reference; profile visibility as choice text; show online status flag as boolean; allow friend requests flag as boolean; created and updated timestamps | One preference record per user; visibility limited to public, friends_only, or private |
| Friendship | A confirmed friendship between two users | First user reference; second user reference; created timestamp | Users must be stored in a consistent order (lower ID first); only one record per pair; does not track requests or blocks |
| Friend request | A pending or resolved friend request between two users | Sender user reference; recipient user reference; status as choice text; created and updated timestamps | Unique constraint on (from_user, to_user); status limited to pending, accepted, declined, or cancelled |
| Blocked user | A block relationship from one user to another | Blocker user reference; blocked user reference; created timestamp | Unique constraint on (blocker, blocked); separate from friendship to keep query logic clean |
| Friend request event | Optional history of friend request actions | Friend request reference; actor user reference; action as choice text; note as short text; created timestamp | Action required; actor must be one of the two users involved in the request |
| User content permission | User-to-user sharing permission defaults | Owner user reference; target user reference; permission level as choice text; applies-to scope as choice text | Owner and target must be different users; one permission per owner, target, and scope |

## Cross-app linking

This app describes who users are and how they relate to one another. Study groups, project membership, messages, shared notes, and shared files should be represented in their owning apps and reference these user records.
