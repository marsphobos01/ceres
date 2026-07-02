# Ceres Issue Workflow Skill Usage

This skill is for working through Ceres GitHub issues in a structured way.

It is not intended to take over the project. It should behave like the main Ceres mentor skill: guide, review, validate, and help with workflow, while leaving implementation ownership with the human contributors.

## What the skill is for

Use this skill when you want help with:

- understanding a specific issue
- checking whether an issue is ready to start
- understanding blockers
- breaking work into implementation steps
- reviewing your implementation against the issue
- preparing commit messages and PR text
- deciding whether work is ready for a PR

## What the skill should not do by default

Unless explicitly asked, the skill should not:

- write or change code
- proactively suggest code changes or patches
- commit work
- create or open pull requests
- take ownership of implementation decisions

The default mode should be mentor-style guidance, not autonomous execution.

## Recommended way to use it

A good workflow is:

1. Tell the skill which issue you are working on.
2. Ask it to summarise the implementation steps.
3. Implement the work yourself.
4. Show the result and ask it to review the implementation against the issue.
5. If the work is not valid yet, use the feedback to fix it.
6. Once valid, ask it to prepare a commit message and description, or ask it to commit if you want that.
7. When a sensible amount of related work is done, ask it whether the branch is ready for a PR.
8. If ready, ask it to prepare the PR title and body, making sure the PR includes `Closes #...` lines for each resolved sub-issue.

## Example prompts

- `I am working on issue #142. Can you summarise the implementation steps only?`
- `Is issue #142 actually ready, or is it blocked by schema work?`
- `Here is my implementation for issue #142. Does it satisfy the issue?`
- `Give me a commit message and commit description for this completed issue.`
- `Should I open a PR now, or finish one more related sub-issue first?`
- `Draft the PR title and body, including the correct Closes lines.`

## Best practices

- Use the skill on one issue at a time.
- Start from unblocked work.
- Keep branches focused.
- Prefer smaller PRs when unsure.
- Treat the skill as a reviewer and workflow assistant, not the owner of the repo.

## Relationship to the main Ceres mentor skill

The main Ceres mentor skill is broader and helps with architecture, ownership, product decisions, and project direction.

This issue workflow skill is narrower. It helps you move a specific issue from ready state through implementation review to commit and PR preparation.
