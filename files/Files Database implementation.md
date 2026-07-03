# Files Database Implementation Schema

Documents the actual `files/models.py` implementation, as built against epic #149 and its child schema issues (see also `Files Database plan.md` for the intended design). Reflects real field definitions and constraints. Update this file whenever the models change.

## StoredFile

The canonical record for an uploaded file. The binary itself is never stored in the database — only the path/URL, via `FileField`, with the actual bytes handled by Django's storage backend.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)` | `related_name='stored_files'` |
| `filename` | `CharField(max_length=255)` | Original filename |
| `file` | `FileField(upload_to='files')` | Path/URL; storage backend handles the rest |
| `mime_type` | `CharField(max_length=255)` | |
| `size` | `PositiveIntegerField` | Bytes |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

## FileVersion

A prior version of a `StoredFile`.

| Field | Type | Notes |
| --- | --- | --- |
| `stored_file` | `ForeignKey(StoredFile, on_delete=CASCADE)` | `related_name='versions'` |
| `version_number` | `PositiveIntegerField` | |
| `file` | `FileField(upload_to='files')` | Path/URL for this version |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

**Constraints**
- Unique on (`stored_file`, `version_number`).

## FileLink

Connects a `StoredFile` to any supported context (module, lecture, assignment, note, study session, group project, message) via a generic relation.

| Field | Type | Notes |
| --- | --- | --- |
| `stored_file` | `ForeignKey(StoredFile, on_delete=CASCADE)` | `related_name='links'` |
| `content_type` | `ForeignKey(ContentType, on_delete=CASCADE)` | |
| `object_id` | `PositiveIntegerField` | |
| `linked_to` | `GenericForeignKey('content_type', 'object_id')` | |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

**Constraints**
- Unique on (`stored_file`, `content_type`, `object_id`).

## FileShare

Grants a specific user access to a `StoredFile`.

| Field | Type | Notes |
| --- | --- | --- |
| `stored_file` | `ForeignKey(StoredFile, on_delete=CASCADE)` | `related_name='shares'` |
| `user` | `ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)` | `related_name='file_shares'` |
| `permission` | `CharField(choices=PermissionChoices)` | `view`, `edit`, `download`, `delete` |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

**Constraints**
- Unique on (`stored_file`, `user`).

**Note:** `PermissionChoices` includes `edit` and `delete` in addition to the `view`/`download` named in the source issue — a deliberate expansion of the permission model beyond the original scope; flagged for reviewer awareness, particularly `delete` (lets a share recipient delete the owner's file).

## FileTag

Attaches a `content.Tag` to a `StoredFile`, reusing the platform's single tagging system rather than a files-specific one.

| Field | Type | Notes |
| --- | --- | --- |
| `stored_file` | `ForeignKey(StoredFile, on_delete=CASCADE)` | `related_name='file_tags'` |
| `tag` | `ForeignKey("content.Tag", on_delete=CASCADE)` | `related_name='file_tags'` |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

**Constraints**
- Unique on (`stored_file`, `tag`).

## FilePreview

One preview record per file.

| Field | Type | Notes |
| --- | --- | --- |
| `stored_file` | `OneToOneField(StoredFile, on_delete=CASCADE)` | Enforces one preview per file; `related_name='preview'` — access via `stored_file.preview` |
| `preview_url` | `URLField(null=True, blank=True)` | Populated once generation succeeds |
| `status` | `CharField(choices=StatusChoices)` | `pending`, `generated`, `failed`; defaults to `pending` |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

## Open items (non-blocking)

- `StoredFile.file` and `FileVersion.file` both use `upload_to='files'` — same storage folder for originals and versioned copies. Not broken, but separating them (e.g. `upload_to='file_versions'`) would aid storage organisation.
- All models are registered in `files/admin.py`. Initial migration (`0001_initial.py`) has been generated; migration `0002` added explicit `related_name`s to every FK.
