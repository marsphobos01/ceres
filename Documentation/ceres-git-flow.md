# Ceres Git Flow

This document describes a simple Git workflow for two people working on Ceres.

## Goal

Keep `main` stable while both contributors work in parallel. A feature branch workflow is commonly used for this because each change happens on a separate branch and is merged back through a pull request rather than direct pushes to `main`.[web:59][web:60]

## Core rules

- `main` should always stay in a working state.[web:60]
- Do not commit feature work directly to `main`; create a branch for each feature or bug fix.[web:59][web:60]
- Merge work into `main` through a pull request so the other person can review it.[web:60][web:92]
- Keep branches short-lived and focused on one task where possible.[web:66][web:89]

## Normal workflow

1. Pull the latest `main`.[web:59]
2. Create a new branch from `main`, for example `feature/auth-pages` or `fix/login-redirect`.[web:59][web:66]
3. Make commits on that branch.[web:59]
4. Push the branch to GitHub.[web:59]
5. Open a pull request into `main`.[web:59][web:92]
6. The other contributor reviews it, changes are made if needed, and then the PR is merged.[web:59][web:92]
7. Delete the branch after merge to keep the repo tidy.[web:66][web:83]

## When a branch is behind

It is normal for one person to merge a feature into `main` while the other person is still working on an older branch. In that case, the older branch is behind `main` and should be updated before it is merged.[web:59][web:69]

Do not ignore the newer `main`. Bring the latest `main` into the feature branch and resolve conflicts there before merging the branch back into `main`.[web:69][web:93]

## Recommended update flow

If `main` has moved on while your branch is still in progress:

```bash
git fetch origin
git checkout feature/your-branch
git merge origin/main
```

This updates the feature branch with the newest changes from `main`. If Git reports conflicts, fix them in the branch, stage the resolved files, commit, test, and continue with the pull request.[web:69][web:93]

Some teams use `git rebase origin/main` instead of `git merge origin/main`. Rebase gives a cleaner linear history, while merge is usually simpler and easier for beginners because it does not rewrite branch history.[web:68][web:93]

## Practical team rule

Before opening a pull request, update your branch from the latest `main`, fix conflicts if needed, run the project, and then push the updated branch. This helps catch integration problems before they reach `main`.[web:69][web:59]

## Suggested branch names

- `feature/auth-pages`
- `feature/profile-model`
- `feature/dashboard-layout`
- `fix/login-redirect`
- `docs/git-flow`

Short, descriptive branch names make pull requests easier to understand and review.[web:66][web:81]

## Team agreement

- One branch per feature or bug fix.[web:59][web:60]
- Pull request required before merge.[web:60][web:92]
- No direct pushes to `main` unless both contributors explicitly agree.[web:60]
- Update your branch from latest `main` before merging.[web:69][web:93]
- Delete merged branches after the PR is complete.[web:66][web:83]

## Example

1. Morgan creates `feature/auth-pages` from `main`.[web:59]
2. Their friend creates `feature/profile-model` from the same `main`.[web:59]
3. Morgan finishes first and merges `feature/auth-pages` into `main` through a pull request.[web:59][web:92]
4. Their friend is still on `feature/profile-model`, which is now behind `main`.[web:69]
5. Before opening or merging their PR, they update their branch:

```bash
git fetch origin
git checkout feature/profile-model
git merge origin/main
```

This is the normal way to bring the latest `main` changes into an in-progress feature branch.[web:69][web:93]

6. If conflicts appear, they resolve them in `feature/profile-model`, test the app, commit the resolution, and push again.[web:69]
7. Once the branch is clean and reviewed, it gets merged into `main`.[web:59][web:92]
