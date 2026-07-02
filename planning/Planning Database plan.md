# planning

Owns time, scheduling, tasks, deadlines, and study activity.

This app is the home for calendar views, personal and recurring events, shared calendars, the central task engine, priorities, categories, deadlines, progress, assignees, task allocation, study sessions, and potential goals or habits features.

## Does not own

The university timetable remains part of `academics`, even when timetable items are displayed in calendar-style views. Assignments remain academic objects in `academics`, but assignment planning data should use this app's task and deadline behaviour.

## Example database schema

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Calendar event | A personal or shared calendar item | Owner user reference; title as short text; description as long text; starts at datetime; ends at datetime; all-day flag as boolean; location as short text; recurrence rule as structured text | Title and start time required; end time must be after start time unless all-day rules allow otherwise |
| Task | The shared planning engine used across Ceres | Owner user reference; title as short text; description as long text; priority as choice text; status as choice text; progress as integer percentage; due datetime; completed timestamp; created and updated timestamps | Title required; progress between 0 and 100; status limited to planned, active, blocked, completed, or archived |
| Task assignment | Who is responsible for a task | Task reference; assigned user reference; assigned by user reference; role as choice text; assigned timestamp | One assignment per task and user; assignee must have access to the linked context |
| Task link | A generic link between a task and another app's object | Task reference; linked app label as short text; linked object type as short text; linked object identifier as positive integer | One link per task and target object; target must be checked before display |
| Study session | A planned or completed study session | Owner user reference; title as short text; starts at datetime; ends at datetime; location as short text; session status as choice text; notes summary as long text | Title and start time required; end time must be after start time when provided |
| Study session participant | A participant invited to a study session | Study session reference; user reference; response status as choice text; invited timestamp; responded timestamp | One participant per session and user; status limited to invited, accepted, declined, or attended |
| Deadline | A central deadline record that can point to another object | Owner user reference; title as short text; due datetime; source app label as short text; source object type as short text; source object identifier as positive integer; reminder enabled flag as boolean | Due date required; source object should be unique when the deadline mirrors another app's object |
| Goal | A personal academic goal | Owner user reference; title as short text; goal type as choice text; target value as decimal number; current value as decimal number; start and end dates | Current value should not be negative; end date should be after start date |

## Cross-app linking

Tasks should be reusable across assignments, modules, lectures, study sessions, group projects, and notes. Deadlines may point to assignment, task, calendar event, group project, or revision plan objects in their respective apps.
