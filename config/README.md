# config

Project-wide Django configuration for Ceres.

This package contains settings, root URL routing, ASGI/WSGI startup, app registration, and environment-level configuration. It is not a product feature app and should not contain dashboard, academic, planning, content, collaboration, file, notification, or search functionality.

## Example database schema

`config` should not own product database tables.

Any environment-specific configuration should normally live in Django settings, environment variables, deployment configuration, or admin-managed records owned by the relevant feature app. If a future database-backed project setting is needed, keep it limited to operational configuration and avoid storing user, academic, content, planning, collaboration, file, notification, or search data here.
