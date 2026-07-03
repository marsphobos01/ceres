# Search Database Implementation Schema

Documents the actual `search/models.py` implementation, as built against Epic #152 ([Epic] search DB Schema). This reflects real field definitions and constraints, not the illustrative examples in `Search Database plan.md`.

## SearchIndexEntry

A searchable summary of an object owned by another app. Never the source of truth — the owning app's data always takes precedence.

| Field | Type | Notes |
| --- | --- | --- |
| `source_app_label` | `CharField(max_length=100)` | The app that owns the source object |
| `source_object_type` | `CharField(max_length=100)` | The model name of the source object |
| `source_object_id` | `PositiveIntegerField` | The PK of the source object |
| `title` | `TextField` | Searchable title |
| `summary` | `TextField` | Searchable summary/excerpt |
| `keywords` | `TextField` | Searchable keywords |
| `owner` | `ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, null=True)` | The user who owns the source object |
| `visibility` | `CharField(choices=VisibilityChoices)` | `PUBLIC`, `SHARED`, `GROUP` — no default; must be set explicitly |
| `last_indexed` | `DateTimeField(auto_now=True)` | Updates on every save; used to detect stale entries |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

**Constraints**
- Unique on (`source_app_label`, `source_object_type`, `source_object_id`) — one index entry per source object.

## SearchAccessHint

Optional cached access information for faster permission filtering. Explicitly out of scope until search is in active use and performance requires it.

**Status:** Not implemented — left as a stub per issue notes. No fields, no migration impact.

## SearchHistoryItem

A record of a user's previous search. Immutable once created.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)` | Who performed the search |
| `query` | `TextField` | Required |
| `filters` | `JSONField(blank=True, null=True)` | Applied filters at time of search |
| `result_count` | `PositiveIntegerField` | Number of results returned |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

**Constraints**
- None beyond field-level requiredness. Records are independently deletable.

## SavedSearch

A user-saved search shortcut.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)` | Owner of the saved search |
| `name` | `CharField(max_length=100)` | Required; unique per user |
| `query` | `TextField` | Required |
| `filters` | `JSONField(blank=True, null=True)` | Saved filter configuration |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

**Constraints**
- Unique on (`user`, `name`).

## SearchSynonym

Admin-managed, product-wide synonym/alias lookup table. No user FK.

| Field | Type | Notes |
| --- | --- | --- |
| `term` | `CharField(max_length=100)` | Required |
| `synonym` | `CharField(max_length=100)` | Required |
| `scope` | `CharField(choices=ScopeChoices)` | `global`, `academics`, `content`, `files`, `planning`, `accounts`, `collaboration` — mirrors `SearchIndexEntry.source_app_label` values |
| `active` | `BooleanField(default=True)` | |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

**Constraints**
- Conditional unique constraint on (`term`, `synonym`) where `active=True` — deactivated pairs don't block re-adding the same term/synonym.

## Open items (non-blocking)

- `SearchAccessHint` is currently commented out rather than a live empty model class.
- `last_indexed` and `updated_at` both use `auto_now=True`, so they'll always match until index-population logic (#25) sets `last_indexed` explicitly.
