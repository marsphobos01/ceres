# files

Owns uploaded files and reusable file-management behaviour.

This app is the home for file storage, file metadata, organisation, tags, file search, previews, sharing, recent files, and attachment relationships.

## Does not own

Separate upload systems for lectures, assignments, notes, study sessions, group projects, or messages should not be created. Attachments should be relationships to file records here rather than independent upload tables in each feature app. In-module file filtering and sorting queries `StoredFile`, `FileTag`, and `FileShare` directly and does not depend on the `search` app or `SearchIndexEntry`.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Stored file | A single uploaded file record | Owner user reference; original filename as short text; storage path as text; MIME type as short text; file size as positive integer; checksum as short text; visibility as choice text; created timestamp | Storage path required; file size must be zero or greater; checksum can be used to detect duplicates |
| File version | A previous or replacement version of a file | Stored file reference; version number as positive integer; storage path as text; file size as positive integer; uploaded by user reference; created timestamp | Version number unique per stored file; storage path required |
| File link | A relationship between a file and another app's object | Stored file reference; linked app label as short text; linked object type as short text; linked object identifier as positive integer; relationship type as choice text | One link per file, target object, and relationship type; target access must be checked before display |
| File share | Direct sharing permission for a file | Stored file reference; shared with user reference; permission level as choice text; shared by user reference; expires timestamp | One share per file and user; permission limited to view, comment, or edit |
| File tag | A reusable tag for files | Owner user reference; name as short text; colour as short text | Tag name unique per owner |
| File preview | Generated preview metadata for a file | Stored file reference; preview type as choice text; preview path as text; status as choice text; generated timestamp | One active preview per file and preview type; status limited to pending, ready, failed, or expired |

## Cross-app linking

Lecture attachments, assignment attachments, note attachments, study-session resources, project files, and message files should all point back to stored file records here. Files appearing in global Ceres search are handled separately — a `files` indexer writes `StoredFile` summaries into `SearchIndexEntry` in the `search` app.
