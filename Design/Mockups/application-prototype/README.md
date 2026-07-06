# Ceres Connected Product Prototype

This is a standalone, connected product prototype for the Ceres academic workspace. It expands the approved dashboard and identity direction into a consistent application-wide UI.

## Open it

Open `index.html` in a modern browser. No server, Django installation or build step is required.

Navigation is hash-based, so every screen can be linked directly, for example:

- `index.html#dashboard`
- `index.html#calendar`
- `index.html#module-detail`
- `index.html#note-editor`
- `index.html#settings`

## Theme selector

The palette button in the global top bar opens the theme selector inside the actual application shell. Appearance Settings contains the same controls in a larger format.

Three dark and three light themes are included:

### Dark

- Forest
- Moonlit
- Clay

### Light

- Daybreak
- Linen
- Harvest

The selection is stored in browser local storage and applies to every route, including authentication and onboarding previews.

## Screen inventory

### Foundation and account

- Dashboard
- Login
- Registration
- Onboarding
- Profile
- Settings and appearance
- Notifications
- Global search

### Organisation and planning

- Calendar
- Timetable
- Tasks
- Study Sessions

### Academic

- Modules
- Module detail
- Lecture Hub
- Assignments
- Assignment detail and linked task checklist
- Revision overview
- Flashcard review

### Content and library

- Notes library
- Rich-text / Markdown note editor
- Files library
- File preview and sharing detail
- Whiteboard

### Collaboration

- Friends and friend requests
- Study Groups and Group Projects
- Group Project workspace
- Messaging

## Repository grounding

The prototype was mapped from:

- `Documentation/Ceres Vision Document.md`
- `Documentation/Django App Structure.md`
- Foundation issues `#237`, `#238`, `#239`, and `#242`
- Product epics `#8` through `#25`
- The current Django models in `accounts`, `academics`, `planning`, `content`, `collaboration`, `files`, `notifications`, and `search`

Important boundaries represented in the UI:

- Dashboard aggregates data but does not own it.
- Assignments use linked Planning Tasks for checklist, priority, status and progress.
- Notes and Files are reusable objects linked into Modules, Lectures, Assignments, Sessions and Projects.
- Lecture Hub is a connected view rather than a second Notes or Files system.
- Group Projects coordinate Tasks, Notes and Files from their owning apps.
- Search groups permission-aware results without becoming their source of truth.
- Goals, Habits and Placement are not included because they remain future modules.
- Timetable import is not presented as a committed core workflow.

## Prototype interactions

- Use the sidebar to navigate between top-level screens.
- Click cards and rows to open common detail screens.
- Press `/` to open Search.
- Use the palette button for the compact theme selector.
- Change themes from Settings for the full appearance view.
- Filter tabs, segmented controls and switches provide lightweight prototype interactions.
- Login, registration and onboarding previews are accessible from Settings.

## Implementation boundary

This is a design prototype only. It does not change Django routes, models, templates or production static files.
