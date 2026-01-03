# git

Create a short, focused commit message, commit staged changes, then push the current branch to `origin`.

## Steps

**CRITICAL**: Always use `--no-pager` flag with git commands to prevent paging and ensure commands complete autonomously without requiring user interaction.

1.  **Review changes**
    - If staged: `git --no-pager diff --cached`
    - If unstaged: `git --no-pager diff`
    - Optional summary: `git --no-pager status`

2.  **Stage changes (if not already staged)**
    - Stage all: `git add -A`
    - Re-check: `git --no-pager status`

3.  **Create short commit message**
    - Base the message on the actual diff.
    - Prefer <= 72 chars, imperative mood, no trailing period.
    - Template:
      - `git commit -m "<type>(<scope>): <short summary>"`
      - With issue key: `git commit -m "<issue-key>: <type>(<scope>): <short summary>"`

5.  **Push current branch to origin**
    - Push current branch (and set upstream): `git push -u origin HEAD`

6.  **If push rejected due to remote updates**
    - Rebase and push:
      - `git pull --rebase`
      - `git push`

7.  **Force-push safety rule**
    - Only if explicitly requested and understood:
      - `git push --force-with-lease`

8.  **Always complete this workflow**
    - Do not ash for clarification. Complete this entire workflow. Commit and push to origin.
