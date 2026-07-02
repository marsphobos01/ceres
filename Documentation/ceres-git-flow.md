# Ceres Git Flow

This document describes a simple Git workflow for two people working on Ceres.

## Goal

Keep `main` stable while both contributors work in parallel. A feature branch workflow is useful because each change happens on a separate branch and is merged back through a pull request rather than direct pushes to `main`.

## Core rules

- `main` should always stay in a working state.
- Do not commit feature work directly to `main`; create a branch for each feature or bug fix.
- Merge work into `main` through a pull request so the other person can review it.
- Keep branches short-lived and focused on one task where possible.

## Normal workflow

1. Pull the latest `main`.
2. Create a new branch from `main`, for example `feature/auth-pages` or `fix/login-redirect`.
3. Make commits on that branch.
4. Push the branch to GitHub.
5. Open a pull request into `main`.
6. The other contributor reviews it, changes are made if needed, and then the PR is merged.
7. Delete the branch after merge to keep the repo tidy.

## When a branch is behind

It is normal for one person to merge a feature into `main` while the other person is still working on an older branch. In that case, the older branch is behind `main` and should be updated before it is merged.

Do not ignore the newer `main`. Bring the latest `main` into the feature branch and resolve conflicts there before merging the branch back into `main`.

## Recommended update flow

If `main` has moved on while your branch is still in progress:

```bash
git fetch origin
git checkout feature/your-branch
git merge origin/main
```

This updates the feature branch with the newest changes from `main`. If Git reports conflicts, fix them in the branch, stage the resolved files, commit, test, and continue with the pull request.

Some teams use `git rebase origin/main` instead of `git merge origin/main`. Rebase gives a cleaner linear history, while merge is usually simpler and easier for beginners because it does not rewrite branch history.

## Practical team rule

Before opening a pull request, update your branch from the latest `main`, fix conflicts if needed, run the project, and then push the updated branch. This helps catch integration problems before they reach `main`.

## Dependency syncing

Ceres uses a `requirements.txt` at the repo root to track Python packages. Each contributor should work inside their own virtual environment (`venv` locally, or PyCharm's interpreter settings) rather than a shared or global environment.

- If you install a new package, run `pip freeze > requirements.txt` and commit the updated file as part of your branch/PR.
- After pulling changes that touch `requirements.txt`, install the update before running the app: `pip install -r requirements.txt` (or, in PyCharm, right-click `requirements.txt` and choose "Install requirements").
- Don't rely on PyCharm's automatic install prompt alone — make re-installing after a pull a habit.

## Pre-PR checklist — DB / schema work

Before opening a pull request that adds or changes models, check all of these — they're easy to forget individually, but any one of them can break the app for the other person after they pull:

- [ ] If you added a new app, is it registered in `INSTALLED_APPS` in `config/settings.py`?
- [ ] If you installed a new package, did you regenerate `requirements.txt` (delete the old file first, then `pip freeze > requirements.txt` from a shell that writes UTF-8 — PowerShell's default redirection writes UTF-16, which breaks `pip install -r requirements.txt` for everyone else)?
- [ ] Does `pip install -r requirements.txt` run cleanly from a fresh check of that file?
- [ ] Are the new or changed models registered in that app's `admin.py` (and does the class name in `admin.py` actually match the model name)?
- [ ] Did you run `makemigrations` and actually read the generated migration file before applying it?
- [ ] Did you run `migrate` locally and confirm it applies without errors?
- [ ] Are the new migration files committed along with the model changes? Migrations are part of the code, not a generated artifact to ignore.
- [ ] Are any secrets (DB passwords, API keys) coming from `.env` via `python-dotenv`, rather than hardcoded in `settings.py`? Check `.env` isn't accidentally un-ignored.
- [ ] Does the app actually start and run without errors before you push?
- [ ] Did you ask Claude to generate/update a `<App> Database Implementation` file for your models? This is separate from writing the models themselves, and it helps the other person understand your schema.

## Pre-PR checklist — feature work

Before opening a pull request that builds a feature on top of existing models, check these:

- [ ] If you installed a new package, did you regenerate `requirements.txt` the same way as above (delete first, UTF-8 shell) and confirm `pip install -r requirements.txt` runs cleanly?
- [ ] Did this feature need a new field or model change? If so, did you go through the DB/schema checklist above for that part, rather than assuming the schema is already finished?
- [ ] Are there tests for the new behavior, and do they pass?
- [ ] Did you manually run the feature end-to-end at least once, not just read the code?
- [ ] Are any secrets coming from `.env`, not hardcoded?
- [ ] Does the app actually start and run without errors before you push?
- [ ] Did you ask Claude to generate/update a '<App> Features' file for your feature? This is separate from writing the feature itself, and it helps the other person understand your work.

## Suggested branch names

- `feature/auth-pages`
- `feature/profile-model`
- `feature/dashboard-layout`
- `fix/login-redirect`
- `docs/git-flow`

Short, descriptive branch names make pull requests easier to understand and review.

## Team agreement

- One branch per feature or bug fix.
- Pull request required before merge.
- No direct pushes to `main` unless both contributors explicitly agree.
- Update your branch from latest `main` before merging.
- Delete merged branches after the PR is complete.

## Current workflow checklist

Right now each person is building out the database schema for their own app(s). Once the schema work is merged, the same team will move on to building features on top of it. The steps below are the practical version of the rules above for each phase.

### Schema phase

```bash
git checkout main
git pull origin main
git checkout -b accounts-db   # or your app's branch
# ...write models...
python manage.py makemigrations
python manage.py migrate
```

Before opening the PR, sync with `main` again in case it moved on while you worked:

```bash
git fetch origin
git merge origin/main
# resolve conflicts if any, re-run makemigrations/migrate, retest
```

Then open the PR, get it reviewed, merge, and delete the branch.

### Feature phase

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature
# ...build the feature...
# ...write/run tests...
```

Sync with `main` again before opening the PR:

```bash
git fetch origin
git merge origin/main
# resolve conflicts if any, retest
```

Then open the PR, get it reviewed, merge, and delete the branch.

Because schema work is currently split by app, migrations from different branches land in different app directories and merge without conflict. Conflicts only become a risk once two people edit models in the same app at the same time.

## Example

1. Morgan creates `feature/auth-pages` from `main`.
2. Their friend creates `feature/profile-model` from the same `main`.
3. Morgan finishes first and merges `feature/auth-pages` into `main` through a pull request.
4. Their friend is still on `feature/profile-model`, which is now behind `main`.
5. Before opening or merging their PR, they update their branch:

```bash
git fetch origin
git checkout feature/profile-model
git merge origin/main
```

6. If conflicts appear, they resolve them in `feature/profile-model`, test the app, commit the resolution, and push again.
7. Once the branch is clean and reviewed, it gets merged into `main`.
