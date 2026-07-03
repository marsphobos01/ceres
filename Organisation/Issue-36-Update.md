Paste this into #36 to replace its current scope/description. See `Organisation/Organisation-Decision.md` for the full reasoning.

---

## Parent epic

#22 — [Epic] Files

## Labels

`type:feature`, `area:files`, `priority:p2` (adjust priority to match the rest of the Files epic's sequencing)

## Goal

Let a user organise their files using tags and contextual links — no folders. This replaces any earlier scope in this issue that described folder or collection behaviour; that's explicitly deferred (see the decision doc).

## User journey

1. A user uploads a file (`StoredFile`).
2. From the file's detail view, the user can:
   - Apply one or more existing tags, or create a new tag, via `FileTag` (reusing `content.Tag` — the same tags used elsewhere in the product).
   - See which contexts the file is linked to (module, lecture, assignment, study session, group project, message) via `FileLink`, and add/remove links from that view.
3. From a tag or a context (e.g. a module page), the user can see every file associated with it — tags and links both support lookup in either direction.
4. There is no folder browsing view, no "move file" action, and no nested containers. A file can carry any number of tags and links at once; removing one doesn't affect the others.

## Scope

- In scope: tag assignment/removal UI, link assignment/removal UI, filtering/browsing files by tag or by linked context.
- Out of scope: folders, collections, nested containers, moving a file between containers. Not promised anywhere in this issue.

## Schema

No schema change. `FileTag` and `FileLink` already exist in `files/models.py` and are documented in `files/Files Database implementation.md`.

## Notes

If folder-style browsing turns out to be needed later, that's new, separate scope with its own ownership/nesting/movement/deletion decisions — see "What's deferred, not decided" in `Organisation/Organisation-Decision.md`. Don't reopen that discussion inside this issue; file a new one against epic #22 if/when it's needed.
