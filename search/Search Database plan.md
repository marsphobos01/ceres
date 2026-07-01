# search

Owns product-wide search behaviour.

This app is the home for global search, search suggestions, grouped results, filtering, recent searches, search history, and permission-aware result handling across Ceres.

Search may query modules, lectures, notes, assignments, files, friends, messages, tasks, and events, but it should not own the underlying content. Results must respect the same access rules as the original app that owns each item.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Search index entry | A searchable summary of an object owned by another app | Source app label as short text; source object type as short text; source object identifier as positive integer; title text; summary text; keywords text; owner user reference; visibility as choice text; updated timestamp | One index entry per source object; never treat this as the source of truth |
| Search access hint | Optional cached access information for faster filtering | Search index entry reference; user reference or group reference; access level as choice text; expires timestamp | Must be refreshed when source permissions change; access level limited to view or none |
| Search history item | A user's previous search | User reference; query text; filters as structured JSON; result count as positive integer; created timestamp | Query required; can be deleted without affecting source content |
| Saved search | A user-saved search shortcut | User reference; name as short text; query text; filters as structured JSON; created and updated timestamps | Name and query required; name unique per user |
| Search synonym | Optional product-wide synonym or alias | Term as short text; synonym as short text; scope as choice text; active flag as boolean | Term and synonym required; avoid duplicate active pairs |

The search index can make querying faster, but the owning app remains authoritative. Permission checks should still be enforced using the source app's access rules before results are shown.
