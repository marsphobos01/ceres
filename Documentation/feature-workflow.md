# Ceres Feature Development Workflow

This guide explains how Morgan and Tom should take a Ceres feature from **Ready to Start** through planning, implementation, testing, review, and merge.

It complements [Contributor Workflow](contributor-workflow.md), which covers branches, pull requests, and repository rules.

## Why feature work is different

A database issue normally says exactly what to construct:

```text
Create model -> add fields -> add constraints -> migrate -> verify
```

A feature issue describes an outcome:

```text
A student can search for a module.
```

That outcome may need URLs, views, forms, helper functions, queries, permissions, templates, tests, and documentation. The first part of feature work is therefore **refinement**, not coding.

## Workflow overview

```text
Select a ready feature
-> define the user behaviour
-> check prerequisites
-> create an implementation checklist
-> create a branch
-> implement in small stages
-> test permissions and failures
-> manually verify the journey
-> update documentation
-> open and merge a PR
```

## 1. Select a feature

Open the project's **Ready to Start** view using:

```text
-is:blocked
```

Then narrow it using priority, area, or the current milestone. Exclude epics when selecting implementation work:

```text
-label:"type:epic"
priority:p1
area:modules
milestone:"MVP 0.1"
```

Before assigning the issue, read:

1. The feature issue.
2. Its parent epic.
3. Its completed database-schema blocker.
4. The owning app's implementation documentation.
5. [Django App Structure](Django%20App%20Structure.md).

Assign yourself and move the issue to **In Progress** before beginning work.

## 2. Define the observable behaviour

Rewrite the issue as a user journey:

```text
Given <starting situation>,
when <user action>,
then <observable result>.
```

Also define an important failure or permission case.

Example:

```text
Given a logged-in student who owns a module,
when they search using its title or code,
then the module appears in Academic search results.

Given a student with no access to that module,
when they perform the same search,
then the module does not appear.
```

If you cannot describe the behaviour clearly, refine the issue before coding.

## 3. Check the real prerequisites

A feature can have its schema blocker closed while still depending on missing user-facing foundations.

Ask:

- Does the page or shared interface exist?
- Does the source feature work independently?
- Is there a working destination for links?
- Are shared services and result formats established?
- Are permission rules defined?
- Are the required models stable?
- Would this issue accidentally require building a sibling feature?

If a prerequisite is missing:

1. Find or create its issue.
2. Add a native **Blocked by** relationship.
3. Move the selected feature out of active work.
4. Implement the prerequisite first.

Do not silently turn one feature into an untracked mega-issue.

## 4. Map the implementation

Use this path to discover what the feature needs:

```text
User action
-> URL
-> view or endpoint
-> input validation
-> service or helper logic
-> model queries or changes
-> permission checks
-> response or template
-> tests
```

Not every feature needs every layer.

### URLs and views

Decide which app owns the route, what the view receives, what it fetches or changes, and whether authentication is required. Views should coordinate requests rather than contain all business logic.

### Validation

Identify required fields, invalid states, and user-facing errors. Use Django forms where they fit. Use focused validation functions for imported data such as CSV rows.

### Helpers and services

Create a helper when the logic has one meaningful responsibility, deserves focused tests, or should not live in a view or signal.

Examples:

```text
index_module(module)
parse_timetable_row(row)
calculate_assignment_progress(assignment)
user_can_view_note(user, note)
```

Start simply with `services.py`. Split into a `services/` package only when the app genuinely has several separate responsibilities.

### Models and permissions

Identify which app owns the data and whether the feature creates, reads, updates, or deletes it. Do not duplicate data owned by another app.

For every object, decide who can view or edit it. Backend permission checks are required; hiding a button is not sufficient.

### Templates and feedback

Define success, empty, validation-error, and failure states. Decide where the user goes next and ensure the page uses the shared Ceres layout.

### Tests

Plan tests for:

- successful behaviour;
- invalid input;
- ownership and permission isolation;
- empty or missing records;
- repeated execution when duplicates are possible.

Tests are the feature equivalent of a successful migration: they prove that the promised behaviour exists.

## 5. Refine the GitHub issue

Add a feature-specific checklist to the issue body or a planning comment:

```markdown
## User behaviour
Given ...
When ...
Then ...

## Implementation checklist
- [ ] Add or update the required URL
- [ ] Implement the view or endpoint
- [ ] Add validation or form handling
- [ ] Add focused service logic
- [ ] Add model queries or updates
- [ ] Enforce permissions
- [ ] Add the UI and feedback states
- [ ] Add automated tests
- [ ] Manually verify the full journey
- [ ] Update affected documentation

## Out of scope
- ...

## Manual verification
1. ...
2. ...
3. ...
```

Replace generic entries with the actual tasks for that feature.

Split the issue into sub-issues when parts can be reviewed independently, two people can safely work separately, one part blocks multiple features, or the branch would otherwise change unrelated systems.

## 6. Create the branch

```bash
git checkout main
git pull origin main
git checkout -b feature/short-description
```

Examples:

```text
feature/search-modules
feature/calendar-month-view
feature/create-personal-event
```

One branch should normally implement one issue.

## 7. Implement in small stages

A useful order is:

1. Write or outline the expected tests.
2. Implement the smallest business-logic unit.
3. Add queries and permission checks.
4. Connect the logic to the view or endpoint.
5. Add templates and user feedback.
6. Run focused tests.
7. Run the wider test suite.
8. Manually test the full journey.

Use meaningful commits, for example:

```text
test: define module search permissions
feat: add module search indexer
feat: include modules in search results
feat: render module result links
```

## 8. Test and verify

Use the narrowest suitable tests:

- Unit tests for focused services.
- Model tests for model behaviour.
- View tests for authentication, responses, redirects, and permissions.
- Integration tests for complete flows.

Where permissions matter, manually test with an owner or permitted account and a separate account with no access.

Before opening the PR, run:

```bash
python manage.py check
python manage.py test
```

If models changed, also follow the database checklist in [Contributor Workflow](contributor-workflow.md).

## 9. Review against the issue

Reread the feature and confirm:

- The user can complete the promised action.
- Invalid and empty states are handled.
- Permissions are enforced by the backend.
- App ownership boundaries are respected.
- The branch contains no unrelated work.
- Tests prove the behaviour.
- Affected documentation is accurate.

Do not complete a checkbox merely because a file exists. Complete it because the observable behaviour works.

## 10. Open the pull request

```bash
git push -u origin feature/short-description
```

Use a PR description like:

```markdown
## Summary
What user-facing capability was added.

## Implementation
The main components and decisions.

## Testing
- Automated tests run
- Manual verification steps

## Screenshots
Include for interface changes.

Closes #<issue-number>
```

The other contributor should review behaviour, permissions, architecture boundaries, tests, maintainability, and the manual verification path.

## 11. After merge

1. Confirm the issue closed.
2. Confirm the Project item moved to Done.
3. Check which dependent issues became ready.
4. Delete the merged branch.
5. Return to the Ready to Start view.

Create explicit follow-up issues for unfinished work rather than leaving hidden TODOs.

## Definition of done

A feature is done when:

- [ ] The observable user behaviour works.
- [ ] The implementation matches the issue scope.
- [ ] Permissions are enforced.
- [ ] Invalid and empty states are handled.
- [ ] Automated tests pass.
- [ ] The full journey is manually verified.
- [ ] Relevant documentation is updated.
- [ ] The app starts without errors.
- [ ] The PR is reviewed and merged.
- [ ] The issue closes through `Closes #...`.

## Worked example: #26 Modules for Generalised Search

### Intended behaviour

```text
A student searches using a module title or code.
Modules they own or belong to appear under Academic results.
Modules they cannot access do not appear.
Selecting a result opens the module detail page.
```

### Prerequisites

Confirm that:

- the shared global-search service and result format exist;
- the global-search page exists;
- module detail pages and named URLs exist;
- module access rules are agreed;
- `Module`, `ModuleMembership`, and `SearchIndexEntry` are stable.

If these do not exist, #26 should be blocked by their issues rather than implementing them all itself.

### Implementation checklist

```markdown
- [ ] Define how Module fields map into SearchIndexEntry
- [ ] Add a focused Module indexer
- [ ] Create or update an entry when a Module is saved
- [ ] Remove the entry when a Module is deleted
- [ ] Provide a way to index existing Modules
- [ ] Include Modules in the shared search query
- [ ] Check access against Module and ModuleMembership
- [ ] Return the standard Academic result format
- [ ] Link results to the Module detail route
- [ ] Test title, code, synchronisation, and permissions
- [ ] Update search implementation documentation
```

### Possible responsibilities

```text
search/services/module_indexing.py
    build_module_index_data(module)
    index_module(module)
    remove_module_from_index(module)

search/signals.py
    trigger indexing when a Module is saved or deleted

search/services/query.py
    include module entries and permission-check source Modules

search/management/commands/rebuild_search_index.py
    index existing records

search/tests/
    indexing, query, and permission tests
```

These file names are examples, not mandatory architecture. Use the smallest structure that clearly separates responsibilities.

### Tests proving completion

```text
Creating a Module creates an index entry
Updating it updates the entry
Deleting it removes the entry
Existing Modules can be backfilled
Searching by title or code finds it
The owner and members can see it
An unrelated user cannot see it
The result links to the correct Module page
```

## Quick start checklist

Before writing feature code:

- [ ] I read the issue, epic, schema blocker, and owning-app docs.
- [ ] I can describe the user journey clearly.
- [ ] I know what is out of scope.
- [ ] All real prerequisites exist.
- [ ] Missing prerequisites are represented by native blockers.
- [ ] I mapped the URL, view, logic, permissions, UI, and tests.
- [ ] The issue has a concrete implementation checklist.
- [ ] I assigned myself and moved it to In Progress.
- [ ] I created a focused branch from the latest `main`.

When these are true, the feature is ready to implement.