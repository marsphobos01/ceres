# Ceres

Ceres is an academic workspace designed to help university students organise, manage, and collaborate throughout their degree.

## Tech stack

- **Python / Django 6.0**
- **PostgreSQL**
- **Pillow** (image handling)
- **django-timezone-field**

## Local setup

1. Clone the repo
2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your settings — database credentials are required; `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are optional and fall back to development defaults
   ```bash
   cp .env.example .env
   ```
5. Apply migrations
   ```bash
   python manage.py migrate
   ```
6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server
   ```bash
   python manage.py runserver
   ```

> After pulling changes that touch `requirements.txt`, re-run `pip install -r requirements.txt` before running the app.

## Documentation

- [Vision](Documentation/Ceres%20Vision%20Document.md)
- [App Structure](Documentation/Django%20App%20Structure.md)
- [Database Schema Overview](Documentation/database-schema-overview.md)
- [Feature List](Documentation/feature_list.md)
- [Contributor Workflow](Documentation/contributor-workflow.md)
- [Issue Management Approach](Documentation/issue-management-approach.md)
