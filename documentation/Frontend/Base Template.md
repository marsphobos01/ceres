# Base Template

## Purpose

The base template provides the shared authenticated Ceres application shell. It follows the structure and visual language in `Design/Mockups/application-prototype` while keeping feature-specific content inside Django template blocks.

It contains:

- the Ceres SVG logo and shared icon sprite
- grouped sidebar navigation
- responsive mobile navigation and scrim
- signed-in user summary and logout control
- sticky top bar with search and notifications
- Django message banners
- page heading and main-content regions
- the shared CSS token and component stylesheets

## Location

```text
core/templates/base.html
```

Pages extend the template with:

```django
{% extends "base.html" %}
```

## Template blocks

### `title`

Sets the browser-tab title.

```django
{% block title %}Dashboard - Ceres{% endblock %}
```

The default is `Ceres`.

### `nav`

Contains the grouped primary navigation. Most pages should use the shared navigation and should not override this block.

### `breadcrumb`

Sets the current-page label in the desktop top bar.

```django
{% block breadcrumb %}Dashboard{% endblock %}
```

### `header`

Contains the visible page heading and optional actions. Use the shared `page-header-copy` and `page-actions` classes.

```django
{% block header %}
    <div class="page-header-copy">
        <span class="eyebrow">Workspace</span>
        <h1>Dashboard</h1>
        <p>A short description of the page.</p>
    </div>
    <div class="page-actions">
        <a class="button button--primary" href="#">Primary action</a>
    </div>
{% endblock %}
```

### `content`

Contains the page's main content. It is rendered inside `main#main-content.screen`.

```django
{% block content %}
    <section class="card">
        <div class="card__body">Page content</div>
    </section>
{% endblock %}
```

### `scripts`

Loads JavaScript required only by an individual page. Keep JavaScript in static files rather than writing it inline.

```django
{% load static %}

{% block scripts %}
    <script src="{% static 'js/dashboard.js' %}" defer></script>
{% endblock %}
```

## Shared static files

```text
static/css/tokens.css
static/css/base.css
static/css/components/buttons.css
static/css/components/forms.css
static/css/components/messages.css
static/css/components/empty.css
static/js/base.js
static/img/
```

`tokens.css` owns the semantic theme colours. `base.css` owns the reset, typography, layout utilities, icon rules and application shell. Component files own reusable controls and states.

## Responsive behaviour

The full sidebar is shown on wide screens. It collapses to an icon rail on medium screens and becomes an off-canvas drawer below 900px. `static/js/base.js` manages the drawer's expanded state, focus return, scrim, Escape-key handling, `aria-hidden` and `inert` state.

## Accessibility conventions

- Keep the skip link as the first focusable control.
- Give icon-only controls an accessible name with `aria-label`.
- Mark decorative SVGs with `aria-hidden="true"`.
- Use visible labels for form controls.
- Connect help and error text using `aria-describedby`.
- Use `aria-invalid="true"` for invalid fields.
- Do not remove the global `:focus-visible` outline.
- Use real links for navigation and real buttons for actions.
