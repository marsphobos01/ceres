# Ceres

Cultivate your academic life.

Version: Vision 1.0

## Vision

Ceres is an academic workspace designed to help university students organise, manage and collaborate throughout their degree.

Rather than attempting to replace a single application, Ceres provides one cohesive environment where students can manage lectures, assignments, notes, revision, group projects and day-to-day academic life.

The goal is not simply to increase productivity, but to reduce the mental overhead of university by giving every piece of academic work a logical place to live.

Ceres should become the workspace students naturally open whenever they attend lectures, revise, complete coursework or collaborate with others.

## Name

Ceres is named after both:

- The Roman goddess of agriculture, growth and cultivation.
- The largest dwarf planet in the asteroid belt.

The name reflects the philosophy of the application. Students are not simply completing assignments; they are cultivating knowledge, skills and long-term growth.

## Vision Statement

Create the most intuitive academic workspace for students by bringing organisation, learning and collaboration into a single, thoughtfully designed experience.

## Core Principles

### Cultivate, don't overwhelm

The application should encourage progress rather than punish procrastination.

### Everything belongs somewhere

Students should never wonder where information should be stored. Every lecture, assignment, note and file should have a natural home.

### Connected information

Nothing exists in isolation.

- Lectures connect to notes.
- Notes connect to revision.
- Revision connects to assignments.
- Assignments connect to modules.

Everything should naturally flow together.

### Calm by default

The interface should reduce stress. Visual clutter should be avoided, information should be prioritised, and animations should feel subtle rather than distracting.

### Collaboration first

University is increasingly collaborative. Where appropriate, every academic object should support collaboration.

### Progressive complexity

Essential features should be immediately accessible. Advanced features should reveal themselves naturally over time.

## Target Users

### Primary

- Undergraduate students

### Secondary

- Postgraduate students

### Future

- Colleges
- Sixth forms
- Apprenticeships
- Independent learners

## Problems Ceres Solves

Students currently juggle many disconnected applications.

### Typical workflow

```text
University Portal
-> Google Calendar
-> Notion
-> Word
-> Discord
-> Google Drive
-> Email
-> Quizlet
-> GitHub
```

Every context switch creates friction. Ceres aims to reduce these interruptions by creating a single academic workspace.

## Product Pillars

### Organisation

- Timetables
- Assignments
- Tasks
- Files
- Calendar

### Learning

- Lecture notes
- Revision
- Flashcards
- Study sessions
- Confidence tracking

### Collaboration

- Group projects
- Messaging
- Shared notes
- Study groups
- Shared whiteboards

### Personal Growth

- Habits
- Progress
- Achievements
- Statistics
- Placement tracking

## User Journey

### First Launch

```text
Create account
-> Choose university (optional)
-> Choose course
-> Import timetable (optional)
-> Complete onboarding
-> Dashboard
```

### Daily Flow

```text
Open Ceres
-> View Dashboard
-> Attend Lecture
-> Take Notes
-> Review Assignment Progress
-> Complete Study Session
-> Update Progress
-> End of Day Summary
```

## Features

This section is the canonical feature reference. Each feature lists what it includes. Anything not listed here is out of scope for the current vision.

### Dashboard

- Daily schedule
- Deadlines
- Assignment progress
- Study reminders
- Notes
- Quick actions
- Calendar overview
- Summary

### Calendar

- Normal calendar functionality
- Recurring events
- Colour categories
- Academic events
- Personal events
- Shared calendars
- Deadline integration

### Timetable

- Weekly timetable
- Modules
- Lectures
- Basic room information

### Modules

- General module details
- Lectures as a linked list; full lecture content lives in Lecture Hub
- Assignments
- Resources

### Lecture Hub

- Notes linked from Notes and tagged to the lecture
- Attachments linked from Files and tagged to the lecture
- Related assignments
- Discussions

### Assignments

- General details
- Checklist or general planner
- Group members
- Sorting, such as upcoming, active, and completed
- Priority, status, and progress inherited from the Tasks engine

### Notes

- Rich text
- Markdown
- Images
- Tables
- Checklists
- Mathematical notation
- Code blocks
- Search
- Organisation

### Revision

- Topics
- Confidence
- Flashcards
- Study sessions
- Weak areas
- Progress
- Practice questions
- Mock exams

### Whiteboard

- Canvas
- Drawing
- Sticky notes
- Shapes
- Images
- Collaboration
- Exporting

### Study Sessions

- Create sessions
- Invite others
- Track time
- Share notes through links into Notes
- Collaborate
- Location
- History and attachment links into Files

### Friends

- Profiles
- Requests
- Shared work
- Study groups

### Messaging

- Direct messages
- Group conversations
- Reactions
- Replies
- File sharing
- Search

### Group Projects

- Workspace
- Shared files through links into Files
- Shared notes through links into Notes
- Task boards
- Meeting notes
- Timeline
- Progress
- Job allocation

### Tasks

Tasks are the core planning engine. Assignments are a specialised view built on top of this.

- Quick creation
- Priorities
- Categories
- Deadlines
- Recurring tasks
- Progress
- Job allocation

### Files

- Storage
- Organisation
- Tags
- Search
- Preview
- Sharing
- Recent files

### Notifications

- Assignment reminders
- Lecture reminders
- Calendar reminders
- Group updates
- Friend requests
- Configurable preferences

### Search

- Modules
- Lectures
- Notes
- Assignments
- Files
- Friends
- Messages
- Tasks
- Events

## Potential Future Modules

These are not in scope for the current build but are planned for later.

- Goals
- Habits
- Placement Tracker
- User Profiles

## User Stories

### Dashboard

As a student, I want to immediately understand what requires my attention today, so I can begin work without searching through multiple applications.

### Assignments

As a student, I want to monitor coursework progress, so deadlines never become overwhelming.

### Notes

As a student, I want all lecture notes organised by module, so revision becomes effortless.

### Revision

As a student, I want to identify my weakest topics, so I can spend my revision time effectively.

### Collaboration

As a student, I want to work with classmates in shared spaces, so group projects remain organised.

### Habits

As a student, I want to build consistent study habits, so I improve over the duration of my degree.

## Non-Functional Requirements

### Performance

The application should remain responsive during normal use.

### Reliability

Student work should never be lost.

### Accessibility

The application should be usable by students with a wide range of accessibility requirements.

### Security

Personal and academic information should remain protected.

### Scalability

The platform should support future growth without requiring architectural redesign.

### Maintainability

Features should evolve independently without negatively impacting existing functionality.

### Extensibility

Future modules should integrate naturally into the existing workspace.

## Information Architecture

```text
Dashboard
|-- Calendar
|-- Timetable
|-- Modules
|   |-- Lectures
|   |-- Assignments
|   |-- Notes
|   `-- Revision
|-- Tasks
|-- Files
|-- Whiteboard
|-- Study Sessions
|-- Friends
|-- Messages
|-- Group Projects
|-- Goals
|-- Habits
|-- Placement
|-- Search
`-- Settings
```

## Long-Term Vision

Ceres should become more than an organisational tool.

It should become the digital academic workspace students rely on throughout their education: a place where they think, learn, collaborate and grow.

The product should be recognised not because it offers more features than competing applications, but because it provides a calmer, more coherent experience that genuinely helps students cultivate their academic journey.
