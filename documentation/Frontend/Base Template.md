# Base Template

## Purpose

The base template provides the shared application structure used by authenticated Ceres pages.

It contains the main navigation, user information, logout control, message display, page header and main content area.

## Location

```text
core/templates/base.html
```

Pages should extend the template using:

```django
{% extends "base.html" %}
```

## Template blocks

### `title`

Sets the text displayed in the browser tab.

```django
{% block title %}Dashboard - Ceres{% endblock %}
```

If the block is not overridden, the title defaults to `Ceres`.

### `nav`

Contains the main application navigation.

Most pages should use the navigation supplied by `base.html` and should not override this block.

### `header`

Contains the page-level heading or breadcrumbs.

```django
{% block header %}
    <h1>Dashboard</h1>
{% endblock %}
```

### `content`

Contains the main content of the page.

```django
{% block content %}
    <p>Welcome to your dashboard.</p>
{% endblock %}
```

### `scripts`

Loads JavaScript required only by an individual page.

JavaScript should remain in separate static files rather than being written inline.

```django
{% load static %}

{% block scripts %}
    <script src="{% static 'core/js/dashboard.js' %}" defer></script>
{% endblock %}
```

The shared `base.js` file is loaded by `base.html` and should contain behaviour used across the application.

## Static files

Shared application-shell assets are located at:

```text
core/static/core/css/base.css
core/static/core/js/base.js
```

## Responsive navigation

The application shell displays the navigation beside the page content on larger screens.

On smaller screens, the navigation is collapsed and can be opened using the Navigation control.

## Example page

```django
{% extends "base.html" %}

{% block title %}Dashboard - Ceres{% endblock %}

{% block header %}
    <h1>Dashboard</h1>
{% endblock %}

{% block content %}
    <p>Welcome to your dashboard.</p>
{% endblock %}
```
