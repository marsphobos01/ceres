# Ceres URL Conventions

Ceres uses namespaced Django URL names.

Each app-level URL configuration must define an `app_name`:

```python
app_name = "academics"
```

URLs should be reversed using their full namespace:

```python
reverse("academics:index")
```

In templates:

```django
{% url "academics:index" %}
```

## Standard route names

Use the following names consistently where appropriate:

| Purpose          | Route name     |
| ---------------- | -------------- |
| App landing page | `<app>:index`  |
| Object list      | `<app>:list`   |
| Object details   | `<app>:detail` |
| Object creation  | `<app>:create` |
| Object editing   | `<app>:edit`   |
| Object deletion  | `<app>:delete` |

## Feature-specific route names

When one Django app owns several types of object, include the feature name in the route name.

Examples:

```text
academics:module-list
academics:module-detail
academics:assignment-create
academics:assignment-edit
planning:task-detail
planning:task-delete
content:note-edit
```

This avoids ambiguous names such as:

```text
academics:detail
academics:create
```

Conceptual product areas such as modules, assignments, notes, tasks, and calendar events remain inside their owning Django apps. They do not receive separate Django app namespaces.

For example:

```text
academics:module-detail
```

should be used instead of creating a separate `modules` app and namespace.

## URL path conventions

URL paths should:

* Use lowercase letters.
* Use hyphens between multiple words.
* Include trailing slashes.
* Use clear nouns for collection routes.
* Use an object identifier for detail routes.

Examples:

```python
path("study-sessions/", views.study_session_list, name="study-session-list")
path("tasks/<int:pk>/", views.task_detail, name="task-detail")
path("tasks/<int:pk>/edit/", views.task_edit, name="task-edit")
path("tasks/<int:pk>/delete/", views.task_delete, name="task-delete")
```

## App index routes

Each participating app should provide an `index` route where appropriate.

Example:

```python
from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("", views.index, name="index"),
]
```

This route can then be reversed with:

```python
reverse("academics:index")
```

and resolves to:

```text
/academics/
```

## Recommended CRUD structure

A standard set of CRUD routes should follow this structure:

```python
urlpatterns = [
    path("", views.task_list, name="task-list"),
    path("create/", views.task_create, name="task-create"),
    path("<int:pk>/", views.task_detail, name="task-detail"),
    path("<int:pk>/edit/", views.task_edit, name="task-edit"),
    path("<int:pk>/delete/", views.task_delete, name="task-delete"),
]
```

This produces:

```text
/planning/tasks/
/planning/tasks/create/
/planning/tasks/12/
/planning/tasks/12/edit/
/planning/tasks/12/delete/
```

## Project-level URL configuration

The project-level `config/urls.py` file should only connect top-level URL prefixes to their owning Django apps.

Example:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("academics/", include("academics.urls")),
    path("collaboration/", include("collaboration.urls")),
    path("content/", include("content.urls")),
    path("files/", include("files.urls")),
    path("notifications/", include("notifications.urls")),
    path("planning/", include("planning.urls")),
    path("search/", include("search.urls")),
]
```

Feature-specific routes should remain inside the URL configuration of the app that owns them.

For example:

```text
/academics/modules/
```

belongs in `academics/urls.py`, not `config/urls.py`.

## Ownership rules

Routes should follow the established Ceres app responsibilities:

| Feature                                        | Owning app      |
| ---------------------------------------------- | --------------- |
| Dashboard and landing shell                    | `core`          |
| Login, logout, registration, and profiles      | `accounts`      |
| Modules, lectures, timetable, and assignments  | `academics`     |
| Calendar, tasks, deadlines, and study sessions | `planning`      |
| Notes and whiteboards                          | `content`       |
| Study groups, group projects, and discussions  | `collaboration` |
| Uploaded files and attachments                 | `files`         |
| Alerts and reminders                           | `notifications` |
| Global search                                  | `search`        |

A navigation item or product page does not automatically require a separate Django app.
