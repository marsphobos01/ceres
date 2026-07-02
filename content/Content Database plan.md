# content

Owns reusable user-created academic content.

This app is the home for notes, whiteboards, content organisation, folders or collections, tags, note search, rich text or markdown content, images, tables, checklists, code blocks, and future mathematical notation support.

## Does not own

Separate note systems for lectures, assignments, study sessions, or group projects should not be created. Notes and whiteboards may be linked to those contexts, but the content itself remains owned here. Meeting notes for group projects may be created from collaboration workflows, but the note content stays in this app.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Note | A reusable note that can be linked across Ceres | Owner user reference; title as short text; body as long text; format as choice text; visibility as choice text; archived flag as boolean; created and updated timestamps | Title required; format limited to supported formats such as rich text or markdown |
| Note link | A relationship between a note and another app's object | Note reference; linked app label as short text; linked object type as short text; linked object identifier as positive integer; relationship type as choice text | One link per note, target object, and relationship type; target access must be checked before display |
| Content collection | A folder, notebook, or collection for notes and whiteboards | Owner user reference; name as short text; parent collection reference; colour as short text; sort order as positive integer | Name required; parent collection must belong to the same owner; prevent circular parent relationships |
| Tag | A reusable content tag | Owner user reference; name as short text; colour as short text | Tag name unique per owner; name required |
| Tagged content | A tag applied to a content object | Tag reference; content type as choice text; content identifier as positive integer | One tag per content object; content identifier must point to a supported content type |
| Whiteboard | A reusable visual workspace | Owner user reference; title as short text; canvas data as structured JSON; thumbnail file reference; visibility as choice text; created and updated timestamps | Title required; canvas data should remain within accepted size limits |
| Note version | Optional history of note edits | Note reference; editor user reference; body snapshot as long text; change summary as short text; created timestamp | Version must belong to an existing note; editor must have edit access |

## Cross-app linking

Other apps should link to notes and whiteboards through relationship records instead of creating separate lecture notes, assignment notes, study-session notes, or project notes tables.
