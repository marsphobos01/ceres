# content - Implemented Database Schema

This document describes the models as actually implemented in `content/models.py`, and how to use them. Unlike `Content Database plan.md`, which describes the intended design, this reflects the current code. Update this file whenever the models change.

The content schema covers notes, flashcards and decks, content collections, tags, whiteboards, and the generic-relation link tables that connect notes and tags to objects in other apps.

## Differences from the earlier design plan

The implemented schema follows epic #148 and its child schema issues. Some concepts from the earlier design plan were intentionally not included in the current database scope:

- `Note` does not currently include model-level visibility, archival state, or access-control fields.
- `NoteLink` represents one generic link per note and target. It does not classify links by relationship type.
- `TaggedContent` does not enforce a database-level allow-list of taggable content types; validation remains the responsibility of application code.
- `NoteVersion` stores the body snapshot and version number but does not currently record an editor or change summary.
- `ContentCollection` supports nested collections but does not currently enforce same-owner ancestry, prevent circular hierarchies, or include colour and sort-order fields.

These may be considered as future schema enhancements if required by feature implementation.

## Note

A reusable note that can be linked across Ceres.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='notes'` |
| `module` | `ForeignKey('academics.Module')`, nullable | `related_name='notes'`; optional link to a module |
| `collection` | `ForeignKey(ContentCollection)`, nullable | `related_name='notes'`; `on_delete=SET_NULL` — deleting a collection leaves its notes in place, uncollected |
| `title` | `CharField(255)` | Required |
| `body` | `TextField`, nullable | Optional |
| `format` | `CharField(9)` | Choices: `markdown`, `rich_text`; default `markdown` |
| `is_pinned` | `BooleanField` | Default `False` |
| `colour` | `CharField(6)`, nullable | Optional hex colour code |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## NoteLink

A generic relationship between a note and another app's object.

| Field | Type | Notes |
| --- | --- | --- |
| `note` | `ForeignKey(Note)` | `related_name='note_links'` |
| `content_type` | `ForeignKey('contenttypes.ContentType')` | Identifies the linked object's model |
| `object_id` | `PositiveIntegerField` | Identifies the linked object's row |
| `content_object` | `GenericForeignKey('content_type', 'object_id')` | Resolves to the linked object |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `note_link_unique` is unique on `(note, content_type, object_id)`.

One generic link is supported per `(note, content_type, object_id)`; this is the implemented schema's design, not an accidental limitation. There is no field distinguishing kinds of relationship.

**Usage:** create a `NoteLink` to associate a note with an object in another app (a lecture, an assignment, a group project, and so on). Callers must check access to the linked object before display; this model does not enforce it.

## Tag

A reusable content tag.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='tags'` |
| `name` | `CharField(50)` | Required |
| `colour` | `CharField(6)`, nullable | Optional hex colour code |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `unique_tag_per_user` is unique on `(owner, name)`.

## TaggedContent

A tag applied to a content object via a generic relation.

| Field | Type | Notes |
| --- | --- | --- |
| `tag` | `ForeignKey(Tag)` | `related_name='tagged_contents'` |
| `content_type` | `ForeignKey('contenttypes.ContentType')` | Identifies the tagged object's model |
| `object_id` | `PositiveIntegerField` | Identifies the tagged object's row |
| `content_object` | `GenericForeignKey('content_type', 'object_id')` | Resolves to the tagged object |
| `created_at` | `DateTimeField` | Auto-set on create |

**Constraints:**
- `tagged_content_unique` is unique on `(tag, content_type, object_id)`, so the same tag cannot be applied twice to the same object.

**Usage:** there is no allow-list of which content types can be tagged at the model level; callers are responsible for only tagging supported objects.

## Flashcard

A single flashcard, optionally tied to a module, a deck, or a revision topic.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='flashcards'` |
| `module` | `ForeignKey('academics.Module')`, nullable | `related_name='flashcards'` |
| `deck` | `ForeignKey('content.FlashcardDeck')`, nullable | `related_name='flashcards'` |
| `revision_topic` | `ForeignKey('academics.RevisionTopic')`, nullable | `related_name='flashcards'` |
| `front` | `TextField` | Required |
| `back` | `TextField` | Required |
| `confidence` | `CharField(10)`, nullable | Choices: `red`, `amber`, `green` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Usage:** a flashcard belongs to a deck through the nullable `deck` FK, matching the plan's note that deck membership is a foreign key rather than a many-to-many relationship. A flashcard can independently reference a module and/or a revision topic.

## FlashcardDeck

A named collection of flashcards.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='flashcard_decks'` |
| `module` | `ForeignKey('academics.Module')`, nullable | `related_name='flashcard_decks'` |
| `title` | `CharField(255)` | Required |
| `description` | `TextField`, nullable | Optional |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## NoteVersion

Optional history of note edits.

| Field | Type | Notes |
| --- | --- | --- |
| `note` | `ForeignKey(Note)` | `related_name='versions'` |
| `version_number` | `PositiveIntegerField` | Required |
| `body` | `TextField` | Required snapshot of the note body |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- `unique_note_version` is unique on `(note, version_number)`.

#186 scoped this model to the note reference, version number, body, and timestamps; an editor reference and change summary were not part of that requirement.

## ContentCollection

A folder, notebook, or collection for notes and whiteboards.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='content_collections'` |
| `title` | `CharField(255)` | Required |
| `parent` | `ForeignKey('self')`, nullable | `related_name='sub_collections'` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

#187 scoped this model to the owner reference, title, nullable parent, and timestamps; same-owner ancestry, cycle prevention, colour, and sort order were not part of that requirement.

**Usage:** application code creating or reparenting a `ContentCollection` must independently check that the parent belongs to the same owner and that no cycle is introduced. Contents are attached from the item side: `Note.collection` and `Whiteboard.collection` are nullable FKs into this model (added in migration `0010`), so a collection's contents are `collection.notes.all()` and `collection.whiteboards.all()`.

## Whiteboard

A reusable visual workspace.

| Field | Type | Notes |
| --- | --- | --- |
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='whiteboards'` |
| `collection` | `ForeignKey(ContentCollection)`, nullable | `related_name='whiteboards'`; `on_delete=SET_NULL` — deleting a collection leaves its whiteboards in place |
| `title` | `CharField(255)` | Required |
| `canvas_data` | `JSONField` | Serialised canvas state; do not store binary data directly in it |
| `content_type` | `ForeignKey('contenttypes.ContentType')`, nullable | Optional generic link to another app's object |
| `object_id` | `PositiveIntegerField`, nullable | Optional generic link target row |
| `content_object` | `GenericForeignKey('content_type', 'object_id')` | Resolves to the linked object, if any |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

## How the models relate

```
User (Django auth)
  - notes -> Note
  - tags -> Tag
  - flashcards -> Flashcard
  - flashcard_decks -> FlashcardDeck
  - content_collections -> ContentCollection
  - whiteboards -> Whiteboard

Note
  - note_links -> NoteLink (generic FK to any app's object)
  - versions -> NoteVersion

Tag
  - tagged_contents -> TaggedContent (generic FK to any app's object)

FlashcardDeck
  - flashcards -> Flashcard

academics.Module
  - notes, flashcards, flashcard_decks (nullable FKs from this app)

academics.RevisionTopic
  - flashcards (nullable FK from this app)

ContentCollection
  - sub_collections -> ContentCollection (self-referential parent/child)
  - notes -> Note (nullable FK, SET_NULL)
  - whiteboards -> Whiteboard (nullable FK, SET_NULL)

Whiteboard
  - content_object -> generic FK to any app's object (optional)
```
