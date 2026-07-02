# planning

Owns time, scheduling, tasks, deadlines, and study activity.

This app is the home for calendar views, personal and recurring events, shared calendars, the central task engine, priorities, categories, deadlines, progress, assignees, task allocation, study sessions, and potential goals or habits features.

## Does not own

The university timetable remains part of `academics`, even when timetable items are displayed in calendar-style views. Assignments remain academic objects in `academics`, but assignment planning data should use this app's task and deadline behaviour.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Calendar event | A personal or shared calendar item | Owner user reference; title as short text; description as long text; starts at datetime; ends at datetime; all-day flag as boolean; location as short text; recurrence type as choice text | Title and start time required; end time must be after start time unless all-day rules allow otherwise |
| Task | The shared planning engine used across Ceres | Owner user reference; title as short text; description as long text; status as choice text; priority as choice text; due datetime; parent task reference (self, nullable — for sub-tasks); created and updated timestamps | Title required; status limited to not_started, in_progress, completed, or cancelled; no direct FK to academics models — links to academic objects go through Task link instead |
| Task assignment | Who is responsible for a task | Task reference; assigned user reference; assigned by user reference; assigned timestamp | One assignment per task and user |
| Task link | A generic link between a task and another app's object | Task reference; linked app label as short text; linked object type as short text; linked object identifier as positive integer | One link per task and target object; target must be checked before display |
| Study session | A planned or completed study session | Owner user reference; module reference (nullable); title as short text (nullable); starts at datetime; ends at datetime; location as short text; notes as long text | Title and start time required; end time must be after start time when provided |
| Study session participant | A participant invited to a study session | Study session reference; user reference; response status as choice text; invited timestamp; responded timestamp | One participant per session and user; status limited to invited, accepted, declined, or attended |
| Deadline | A central deadline record that can point to another object | Owner user reference; title as short text; due datetime; source app label as short text; source object type as short text; source object identifier as positive integer; reminder enabled flag as boolean | Due date required; source object should be unique when the deadline mirrors another app's object |

**Goal is not yet a scoped or tracked table.** It's mentioned above as a possible future feature ("potential goals or habits features") but there is no corresponding DB schema issue for it on GitHub, and no field design has been agreed. Treat "Goal" as an idea, not a planned table, until it has an actual schema issue — do not build against a `Goal` model assuming this table exists.

## Cross-app linking

Tasks should be reusable across assignments, modules, lectures, study sessions, group projects, and notes. Deadlines may point to assignment, task, calendar event, group project, or revision plan objects in their respective apps.
