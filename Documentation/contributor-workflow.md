# Contributor Workflow

This document replaces `ceres-git-flow.md`. It covers everything a new contributor needs to start working in Ceres: how work is tracked in GitHub Issues and Projects, how to find something you're actually allowed to start (nothing blocking it), and the Git branching/PR process around it.

If you're brand new to the repo, read this top to bottom once. After that, the section you'll come back to most is [Finding work to do](#finding-work-to-do).

---

## 1. Environment setup

Full setup steps (clone, venv, `requirements.txt`, `.env`, migrations, `runserver`) are in the [README](../README.md#local-setup) — do that first if you haven't.

One habit worth calling out early: **after pulling any change that touches `requirements.txt`, re-run `pip install -r requirements.txt` before running the app.** PyCharm's install prompt is not reliable enough to depend on alone.

---

## 2. How work is organized

Every piece of work in Ceres is a GitHub Issue with a `type:` label:

| Label | Meaning |
|---|---|
| `type:epic` | A large outcome spanning many issues (e.g. `[Epic] Notifications`) |
| `type:db-epic` | The DB-schema counterpart to a feature epic (e.g. `[Epic] notifications DB Schema`) |
| `type:feature` | A user-facing capability, sub-issue of a feature epic |
| `type:db-schema` | A model/migration/constraint, sub-issue of a DB epic |
| `type:bug` | Broken behavior |
| `type:task` | Small implementation/admin work |

Each issue also carries one `area:*` label (which Django app it belongs to) and one `priority:*` label (`p0`–`p3`, most to least urgent).

Full label taxonomy, epic body template, and PR-closing conventions are in [issue-management-approach.md](issue-management-approach.md) — this section is just the practical summary.

**The rule that matters most day to day:** feature work is blocked by the DB schema work it depends on. A feature issue like "Requests for Friends" may be marked **Blocked by** the DB schema issue that defines the `FriendRequest` model. You cannot productively start a feature issue until its blockers are closed because the model shape it needs to write code against may still change.

---

## 3. Finding work to do

Don't scroll the issue list looking for something that looks unblocked — GitHub can tell you exactly, and it's always accurate because it's computed live from the real dependency graph.

### The fast way: native `is:blocked` filters

In the repo's **Issues** tab or in the **Ceres Issue System** project's filter bar, these qualifiers work directly:

| Filter | Shows |
|---|---|
| `-is:blocked` | Issues with no open blockers — safe to start now |
| `is:blocked` | Issues waiting on something else to close first |
| `is:blocking` | Issues that other work is waiting on (fixing these unblocks the most people) |
| `blocked-by:#123` | Everything waiting on issue #123 specifically |
| `blocking:#123` | Everything that #123 is waiting on |

These are live — the moment a blocking issue closes, the blocked issue drops out of `is:blocked` automatically. There is no manual field to keep in sync and no risk of it going stale.

### The saved view: "Ready to Start"

The **Ceres Issue System** project has (or should have — see below if it doesn't exist yet) a saved view filtered to `-is:blocked`. Open the project, switch to that view, and everything in it is fair game to pick up right now.

If the view doesn't exist yet:
1. Open the **Ceres Issue System** project.
2. **+ New view** → Table or Board layout.
3. Filter bar → type `-is:blocked`.
4. Name it "Ready to Start" and save.

> **Don't build a custom "Readiness" field for this.** It was tried and removed — a custom single-select field has to be manually recomputed every time a dependency closes, while the native filter is always correct because GitHub computes it from the actual blocked-by graph. If you ever see a "Readiness" or "Blocked Status" custom field reappear in the project, it's redundant with `is:blocked` and should be deleted rather than maintained.

### Picking something up

1. Open the "Ready to Start" view.
2. Filter further by `area:*` if you want to stay in one Django app, or by `priority:` if you want the most urgent thing.
3. Read the issue body — schema issues list exact fields/constraints; feature issues describe the capability and link back to their parent epic.
4. Assign yourself and move it to "In Progress" (or your project's equivalent status) so nobody else duplicates the work.
5. If it's a feature issue, skim its parent epic and its DB schema blocker (even though it's closed) — the model's boundary notes often explain what belongs in which app.

---

## 4. Git branching workflow

### Core rules

- `main` always stays in a working state.
- Never commit directly to `main`; create a branch per issue or task.
- Merge through a pull request so someone else reviews it.
- Keep branches short-lived and focused on one issue where possible.

### Normal flow

```bash
git checkout main
git pull origin main
git checkout -b feature/your-branch   # see naming below
# ...do the work...
git push -u origin feature/your-branch
```

Open a pull request into `main`. Once reviewed and merged, delete the branch.

### Branch naming

- `feature/auth-pages`, `feature/friend-requests`
- `db-schema/notifications` (or just the app name, e.g. `notifications-db`, for schema-phase branches)
- `fix/login-redirect`
- `docs/contributor-workflow`

Short and descriptive — branch names should make the PR's purpose obvious without opening it.

### Keeping your branch current

If `main` has moved on while you're still working, don't ignore it — bring it in before you open or merge your PR:

```bash
git fetch origin
git checkout feature/your-branch
git merge origin/main
# resolve conflicts if any, re-test, commit the resolution
```

(`git rebase origin/main` is an alternative if you want linear history — merge is simpler and doesn't rewrite branch history, which is the safer default if you're not comfortable with rebase yet.)

**Practical rule:** update from `main`, resolve conflicts, run the app, *then* push and open/update the PR. Catch integration problems on your branch, not after merge.

### Example

1. Morgan creates `feature/auth-pages` from `main`.
2. A teammate creates `feature/profile-model` from the same `main`.
3. Morgan finishes first and merges into `main`.
4. The teammate's branch is now behind. Before opening their PR:
   ```bash
   git fetch origin
   git checkout feature/profile-model
   git merge origin/main
   ```
5. If conflicts appear, resolve them on `feature/profile-model`, re-test, commit, push.
6. Once clean and reviewed, merge.

### PR closing convention

Reference the issue in the PR description so merging auto-closes it and keeps the project in sync:

```
Closes #123
```

---

## 5. Pre-PR checklists

These catch the mistakes that break the app for whoever pulls next — check every box, not just the ones that feel relevant.

### DB / schema work

- [ ] New app registered in `INSTALLED_APPS` in `config/settings.py`?
- [ ] New package installed → regenerated `requirements.txt` (delete the old file first, then `pip freeze > requirements.txt` from a shell that writes UTF-8 — PowerShell's default redirection writes UTF-16, which breaks `pip install -r requirements.txt` for everyone else)?
- [ ] `pip install -r requirements.txt` runs cleanly from a fresh check of that file?
- [ ] New/changed models registered in that app's `admin.py`, and the class name there actually matches the model name?
- [ ] Ran `makemigrations` and actually read the generated migration file before applying it?
- [ ] Ran `migrate` locally and confirmed it applies without errors?
- [ ] Migration files committed alongside the model changes — migrations are part of the code, not a generated artifact to ignore?
- [ ] Secrets (DB passwords, API keys) coming from `.env` via `python-dotenv`, not hardcoded in `settings.py`? `.env` isn't accidentally un-ignored?
- [ ] App starts and runs without errors before you push?
- [ ] Asked Claude to generate/update a `<App> Database Implementation` doc for these models — separate from writing the models, and it's what helps the next person understand your schema?
- [ ] Is the matching feature work actually unblocked now? If this schema issue was blocking feature issues, closing it should flip them to `-is:blocked` — spot-check the "Ready to Start" view after merge.

### Feature work

- [ ] New package installed → same `requirements.txt` regeneration process as above, confirmed clean install?
- [ ] Did this feature need a new field or model change? If so, did you go through the DB/schema checklist above for that part, rather than assuming the schema is already finished?
- [ ] Tests exist for the new behavior and pass?
- [ ] Manually ran the feature end-to-end at least once, not just read the code?
- [ ] Secrets coming from `.env`, not hardcoded?
- [ ] App starts and runs without errors before you push?
- [ ] Asked Claude to generate/update a `<App> Features` doc for this feature — separate from writing the feature, and it's what helps the next person understand your work?

---

## 6. Team agreement

- One branch per issue or bug fix.
- Pull request required before merge; no direct pushes to `main` unless explicitly agreed.
- Update your branch from latest `main` before merging.
- Delete merged branches after the PR completes.
- Feature work stays blocked-by its DB schema dependency until that schema is merged — don't start the feature branch early "to save time," the model shape can and does change during schema review.
- Check `-is:blocked` before picking up new work, not the raw issue list.
