# Files Organisation — Decision

**Parent epic:** #22 — [Epic] Files
**Related issue:** #36
**Status:** Decided

## Decision

The first release of Files organisation is **tag-based, using the existing schema** — `FileTag` (via the shared `content.Tag` system) plus `FileLink` (generic link to whatever context a file belongs to: module, lecture, assignment, study session, group project, message). No folder or collection model is introduced.

No schema change is required. `FileTag` and `FileLink` are already implemented in `files/models.py` — see `files/Files Database implementation.md` for the full field-level reference, and its new "Organisation" section for how tags and links specifically answer the ownership/nesting/movement/deletion questions below.

## Why

- A file is already organised in practice by two independent, flat mechanisms: what it's tagged with, and what it's linked to. Neither requires hierarchy to be useful.
- `files` already avoids duplicate systems by design — one tagging system (shared with `content`), one generic-link pattern (`contenttypes`). A folder model would be a third organisational axis layered on top of two that already work; that's added complexity without a demonstrated need yet.
- Nesting, movement, and deletion-cascade rules for folders are genuine design questions (see below) that don't have obvious answers yet. Deciding them now, before any user-facing folder UI is scoped, risks designing against the wrong requirements.
- This keeps the first vertical slice through Files narrow, consistent with the project's general preference for a smallest-complete-path first pass over premature abstraction.

## What this decision answers (for the chosen model)

- **Ownership:** unchanged from today — a file's tags and links carry no independent ownership; access continues to follow `StoredFile.owner` and `FileShare`.
- **Nesting:** none. Tags are flat; a file can carry any number of them. Links are flat; a file can link to multiple contexts simultaneously, and contexts don't nest at the file layer.
- **Movement:** not applicable. There's no container for a file to be "in," so there's nothing to move it out of — retagging or relinking isn't a move.
- **Deletion:** `FileTag` and `FileLink` rows cascade-delete when their `StoredFile` is deleted. Deleting a `content.Tag` cascades to `FileTag` rows only; the file itself is unaffected.

## What's deferred, not decided

A folder/collection model may be worth revisiting once real usage shows tags and links aren't enough (for example, if users want to browse files the way they browse a filesystem, rather than by search/filter). If that happens, these questions need real answers before implementation, not defaults inherited from this decision:

- **Ownership:** are folders personal (one owner) or shared (e.g. scoped to a group project or module)? Can a file's tags/links stay independent of which folder(s) it's in, or would a folder imply exclusive containment?
- **Nesting:** how deep can folders nest, if at all? `content.ContentCollection` already implements a self-referential `parent` FK for organising notes — reusing that pattern (rather than inventing a second one) is the natural default, but the depth/cycle-prevention rules still need deciding.
- **Movement:** can a file belong to more than one folder at once, or is containment exclusive? What happens to sharing/permissions when a file moves into a folder owned or shared differently than the file itself?
- **Deletion:** does deleting a folder cascade-delete its contents, or re-parent them (to root, or to the folder's parent)? This is exactly the kind of deletion behaviour the project's modelling guidance says to decide deliberately rather than default into.

None of this is being designed now. It's recorded here so a future folder proposal starts from these open questions instead of from zero.

## What changed as a result

- No migration, no new model, no test changes — the decision doesn't touch the schema.
- `files/Files Database implementation.md` — added an "Organisation" section documenting this decision and its answers to ownership/nesting/movement/deletion for the current (tag + link) model.
- `Organisation/Issue-36-Update.md` — rewritten user journey for #36, scoped to tags and links, with folder language removed.
