# Base Template

## Purpose

`core/templates/base.html` is the shared authenticated Ceres shell. Its markup and active CSS class names mirror `Design/Mockups/application-prototype/index.html` rather than approximating the prototype.

It provides:

- the Ceres SVG logo and shared icon sprite
- the exact prototype sidebar, navigation groups and profile area
- the exact prototype sticky top bar, search control and notification control
- responsive icon-rail and mobile drawer behaviour
- Django message rendering
- page heading and main-content template blocks

Only routes and controls that currently exist are active. Future controls such as Settings and the theme panel remain commented in the template until their owning issues are implemented.

## Extending the template

```django
{% extends "base.html" %}
```

## Template blocks

### `title`

Sets the browser title.

```django
{% block title %}Dashboard - Ceres{% endblock %}
```

### `nav`

Contains the shared grouped sidebar navigation. Most pages should not override this block.

### `breadcrumb`

Sets the final label in the prototype top-bar breadcrumb.

```django
{% block breadcrumb %}Dashboard{% endblock %}
```

### `header`

Use the prototype page-header structure inside this block.

```django
{% block header %}
<header class="page-header">
    <div class="page-header-copy">
        <span class="eyebrow">Workspace</span>
        <h1>Dashboard</h1>
        <p>A short description of the page.</p>
    </div>
    <div class="page-actions">
        <a class="button primary" href="#">Primary action</a>
    </div>
</header>
{% endblock %}
```

### `content`

Contains page content rendered inside `main#screen.screen`.

```django
{% block content %}
<section class="card">
    <div class="card-body">Page content</div>
</section>
{% endblock %}
```

### `scripts`

Loads JavaScript required by one page. Keep JavaScript in a static file.

```django
{% load static %}

{% block scripts %}
<script src="{% static 'js/dashboard.js' %}" defer></script>
{% endblock %}
```

## Active static files

```text
static/css/tokens.css
static/css/prototype-foundation.css
static/js/base.js
```

`tokens.css` mirrors the prototype theme tokens. `prototype-foundation.css` contains the exact shared foundation and responsive CSS from the connected prototype, followed only by small Django integration rules.

The older approximation files remain in the branch but their `<link>` elements are commented in `base.html`, so they do not affect rendering.

## Future prototype styles

The feature-specific prototype stylesheet imports are listed and commented at the top of `static/css/prototype-foundation.css`. Do not enable them under issue #239. Enable or migrate each file only when its owning feature issue is implemented.

## Accessibility conventions

- Keep the skip link as the first focusable control.
- Give icon-only controls an `aria-label`.
- Mark decorative SVGs with `aria-hidden="true"`.
- Use visible labels for form controls.
- Do not remove the shared focus outline.
- Use links for navigation and buttons for actions.
- Preserve the mobile drawer's `aria-expanded`, `aria-hidden` and `inert` behaviour.
