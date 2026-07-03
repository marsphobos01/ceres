# core — Implemented Database Schema

This document describes the models as actually implemented in `core/models.py`, and how to use them. Unlike `Core Database plan.md`, which describes the intended design, this reflects the current code. Update this file (not the plan) whenever the models change.

Per the plan, this app owns only presentation/preference data for the shared dashboard experience — no schedules, deadlines, notes, assignments, notifications, friends, or project data live here.

## DashboardLayout

A user's saved dashboard arrangement.

| Field | Type | Notes |
| --- | --- | --- |
| `user` | `OneToOneField(AUTH_USER_MODEL)`, `primary_key=True` | The user's own PK is reused as this row's PK — no separate `id` column. `related_name='dashboard_layout'` — access via `user.dashboard_layout` |
| `layout_name` | `CharField(120)` | Required |
| `widget_order` | `JSONField(default=dict)` | Structured widget ordering |
| `is_default` | `BooleanField` | Default `False` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:** none needed — `OneToOneField(primary_key=True)` already guarantees at most one row per user at the database level.

**Usage:** access via `user.dashboard_layout`. Because the model structurally allows only one row per user, `is_default` currently has nothing to distinguish itself from — the plan's "one default layout per user" language implies a user might eventually have several named layouts with one marked default, but the current schema doesn't allow more than one layout per user at all. Worth confirming whether multiple layouts per user are actually planned before relying on `is_default`.

## DashboardWidget

Per-user, per-widget display settings.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='dashboard_widgets'` — access via `user.dashboard_widgets` |
| `widget_key` | `CharField(120)` | Identifies which dashboard widget this row configures |
| `enabled` | `BooleanField` | Default `True` |
| `display_size` | `CharField(120)`, choices | Nested `DisplaySizeChoices`: Small/Medium/Large. `max_length=120` is oversized for a one-character code |
| `configuration` | `JSONField`, nullable | `default=dict`, `blank=True`, `null=True` — structured per-widget config |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- `widget_key_unique` — unique on `(user, widget_key)`; one settings row per widget per user, matching the plan.

**Usage:** a user's widget settings are `user.dashboard_widgets.all()`.

## QuickActionPreference

The quick actions a user wants visible, and where.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `related_name='quick_action_preferences'` — access via `user.quick_action_preferences` |
| `action_key` | `CharField(120)` | Identifies which quick action this row configures |
| `position` | `PositiveIntegerField` | Required. Django's `PositiveIntegerField` permits `0`, satisfying the plan's "position must be zero or greater" despite the field name suggesting strictly positive |
| `enabled` | `BooleanField` | Default `True` |
| `pinned` | `BooleanField` | Default `False` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:**
- `action_key_unique` — unique on `(user, action_key)`; one preference row per action key per user, matching the plan.

**Usage:** a user's quick action preferences are `user.quick_action_preferences.all()`.

## UserInterfacePreference

Interface preferences not specific to `accounts` (theme, density, sidebar state).

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `BigAutoField` | Default primary key |
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `related_name='interface_preference'` — access via `user.interface_preference`. Unlike `DashboardLayout`, this doesn't use `primary_key=True` — it has its own `id` in addition to the unique `user` column, a different pattern for the same "one row per user" guarantee |
| `theme` | `CharField(6)`, choices | Nested `ThemeChoices`: Light/Dark/System |
| `density` | `CharField(11)`, choices | Nested `DensityChoices`: Compact/Comfortable/Spacious |
| `sidebar_collapsed` | `BooleanField` | Default `True` |
| `created_at`, `updated_at` | `DateTimeField` | Auto-set on create/update |

**Constraints:** none needed — `OneToOneField` already enforces uniqueness on `user`.

**Usage:** access via `user.interface_preference`.

## Known open items across this app

- **Two different "one row per user" patterns.** `DashboardLayout` collapses its primary key into the `user` FK (`primary_key=True`); `UserInterfacePreference` keeps its own `id` and relies on `OneToOneField`'s implicit uniqueness instead. Both work, but picking one convention would be more consistent.
- **`DashboardWidget.display_size` uses `max_length=120`** for a one-character code — the same oversized-`choices`-field pattern flagged in other apps' schema docs; worth a project-wide pass at some point.
- **`DashboardLayout.is_default`** may not mean anything yet given the model only allows one layout per user — see note above.

Resolved in migration `0002`: explicit `related_name`s added to all four models, and the unused `User` import was removed from `core/models.py`.

## How the models relate

```
User (Django auth)
  - dashboard_layout -> DashboardLayout (1:1, PK = user)
  - dashboard_widgets -> DashboardWidget (1:M, one row per widget_key)
  - quick_action_preferences -> QuickActionPreference (1:M, one row per action_key)
  - interface_preference -> UserInterfacePreference (1:1)
```
