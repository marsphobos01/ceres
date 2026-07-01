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
