# academics

Owns the university-specific academic structure of Ceres.

This app is the home for modules, lectures, timetable entries, assignments, assignment participants, and future revision features. It contains module details and membership, lecture metadata, basic room and lecturer information, Lecture Hub views, assignment details, assignment deadlines, group-assignment membership, and assignment filtering such as upcoming or completed.

## Does not own

General notes, file storage, generic tasks, personal calendar events, and group discussions belong to `content`, `files`, `planning`, and `collaboration`. Assignments belong here, but their generic planning behaviour should come from `planning` — priority, work state, progress, reusable tasks, and shared deadline behaviour should not be recreated independently inside this app.

Academic Assignment membership is also distinct from collaboration membership. `AssignmentParticipant` records who is involved in a specific academic group Assignment; it does not create or reuse a `StudyGroup`, `GroupMembership`, `GroupProject`, or `ProjectMembership`.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Module | A university module or class | Owner user reference; module code as short text; title as short text; description as long text; academic year as short text; term as choice text; colour as short text; archived flag as boolean | Module code and title required; module code should be unique per owner and academic year |
| Module membership | A user's relationship to a module | Module reference; user reference; role as choice text; joined timestamp | One membership per module and user; role limited to owner, member, or viewer |
| Lecture | A lecture or teaching session attached to a module | Module reference; title as short text; starts at datetime; ends at datetime; room as short text; lecturer as short text; description as long text | Title and start time required; end time must be after start time when provided |
| Timetable entry | Recurring or scheduled academic timetable item | Module reference; lecture reference if applicable; weekday as choice text; start time; end time; room as short text; recurrence start and end dates | End time must be after start time; timetable entries should belong to a module |
| Assignment | An academic assignment, coursework item, or assessment | Module reference; title as short text; brief as long text; due datetime; weighting as decimal number; type as choice text; group assignment flag as boolean; submission status; created and updated timestamps | Title required; planning state and task progress come from `planning`; populated group Assignments cannot be changed to individual until participants are removed |
| Assignment participant | A user's participation in one academic group Assignment | Assignment reference; user reference; created timestamp | Unique on assignment and user; only valid for group Assignments; the user must own or belong to the Assignment's Module |
| Revision topic | A revisable topic within a module | Module reference; title as short text; confidence score as small integer; priority as choice text; last reviewed date | Confidence score should stay within the chosen scale, such as 1 to 5 |

## Assignment participant permissions

- `AssignmentParticipant` is the single source of truth for who is involved in an academic group Assignment.
- `Assignment.is_group` describes the assessment type and is not inferred from participant count.
- Module owners and users with `ModuleMembership.Role.OWNER` may manage participants.
- Being a participant does not grant permission to edit Assignment details or membership.
- Module members and viewers may be eligible participants, but cannot manage participants unless they also hold the owner role.

## Cross-app linking

Academic records may link to notes in `content`, files in `files`, tasks and deadlines in `planning`, and discussions or group work in `collaboration`. Those links should not cause this app to duplicate the external data.
