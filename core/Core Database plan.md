# core

Owns the overall Ceres experience and pages that combine information from several other apps.

This app is the home for the dashboard, landing page, main layout, shared navigation, shared page structure, general error pages, quick actions, and product-wide contextual actions.

## Does not own

Actual schedules, deadlines, notes, assignments, notifications, friends, or project data should not be stored here. The dashboard presents data from other apps rather than owning it — schedules and deadlines come from `planning`, notes from `content`, assignments from `academics`, notifications from `notifications`, and friends or projects from `collaboration`. Store only presentation choices and pull the underlying data from the owning apps.

## Example database schema

`core` contains very little product data. Its tables support the shared experience rather than duplicate records from other apps.

| Example table | What it represents | Example fields and data types | Example constraints and rules |
| --- | --- | --- | --- |
| Dashboard layout | A user's chosen dashboard arrangement | User reference; layout name as short text; widget order as structured JSON; default flag as boolean; created and updated timestamps | One default layout per user; layout name required; widget order must only reference supported dashboard widgets |
| Dashboard widget setting | Per-user settings for a dashboard widget | User reference; widget key as short text; enabled flag as boolean; display size as choice text; configuration as structured JSON | One setting per user and widget key; widget key must match a registered dashboard widget |
| Quick action preference | The quick actions a user wants visible | User reference; action key as short text; position as positive integer; pinned flag as boolean | One action key per user; position must be zero or greater |
| User interface preference | Shared interface preferences not specific to accounts | User reference; theme mode as choice text; density as choice text; sidebar collapsed flag as boolean | One preference record per user; choices should be restricted to supported interface options |

## Cross-app linking

This app queries all other apps for display purposes only. It should never become a data owner for content that has a more appropriate home elsewhere.
