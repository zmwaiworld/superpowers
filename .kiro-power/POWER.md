---
name: "superpowers"
displayName: "Superpowers"
description: "Complete software development workflow with composable skills: TDD, systematic debugging, brainstorming, planning, code review, and subagent-driven development"
keywords: ["tdd", "test driven development", "debug", "brainstorm", "plan", "code review", "workflow", "skills", "subagent", "refactor", "git worktree", "implementation", "testing", "verification"]
author: "Jesse Vincent"
---

# Superpowers

Superpowers is a complete software development workflow built on composable skills. It starts before you write code — brainstorming designs, writing plans, then executing with TDD, systematic debugging, code review, and subagent-driven development. Skills trigger automatically based on what you're doing.

## Bootstrap

When this power activates, you MUST do two things before taking any other action:

### 1. Locate the superpowers repo

Find the repo root by checking these paths in order:

**macOS / Linux:**
```bash
ls ~/.kiro/powers/repos/*/skills/using-superpowers/SKILL.md 2>/dev/null
ls ~/superpowers/skills/using-superpowers/SKILL.md 2>/dev/null
```

**Windows (PowerShell):**
```powershell
Get-ChildItem "$env:USERPROFILE\.kiro\powers\repos\*\skills\using-superpowers\SKILL.md" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\superpowers\skills\using-superpowers\SKILL.md" -ErrorAction SilentlyContinue
```

The first match tells you the repo root. For example, if the match is `~/.kiro/powers/repos/-kiro-power/skills/using-superpowers/SKILL.md`, then the repo root is `~/.kiro/powers/repos/-kiro-power`. Remember this as `SUPERPOWERS_REPO`.

### 2. Load the using-superpowers skill

Use `discloseContext` to load `$SUPERPOWERS_REPO/skills/using-superpowers/SKILL.md`. That skill contains the complete workflow rules, skill priority, red flags table, and decision flowchart that govern all agent behavior.

Do not proceed without loading it first.

## Loading Skills On Demand

All skills live in the repo at `$SUPERPOWERS_REPO/skills/<name>/SKILL.md`. Load them with `discloseContext` when needed — no copying or installation required. `git pull` in the repo directory picks up updates instantly.

## Available Skills

| Skill | When to use |
|-------|-------------|
| `brainstorming` | Before any creative work — features, components, design |
| `writing-plans` | When you have a spec and need an implementation plan |
| `executing-plans` | When you have a plan to execute task-by-task |
| `subagent-driven-development` | Execute plans with independent tasks using subagents |
| `test-driven-development` | When implementing any feature or bugfix |
| `systematic-debugging` | When encountering bugs, test failures, unexpected behavior |
| `requesting-code-review` | Before merging, to verify work meets requirements |
| `receiving-code-review` | When handling code review feedback |
| `verification-before-completion` | Before claiming work is done |
| `using-git-worktrees` | When starting feature work that needs isolation |
| `finishing-a-development-branch` | When implementation is complete, deciding merge/PR/cleanup |
| `dispatching-parallel-agents` | When facing 2+ independent tasks |
| `writing-skills` | When creating or editing skills |

## Tool Mapping for Kiro

When skills reference Claude Code tools, substitute Kiro equivalents:

| Claude Code Tool | Kiro Equivalent | Notes |
|-----------------|-----------------|-------|
| `Skill` tool | `discloseContext` | Load `$SUPERPOWERS_REPO/skills/<name>/SKILL.md` |
| `TodoWrite` | Markdown checklist | Use `- [ ] item` format in responses |
| `Task` (subagent) | `invokeSubAgent` | Dispatch work to sub-agents |
| `Read` | `readFile` / `readCode` | `readCode` preferred for code files |
| `Write` | `fsWrite` / `fsAppend` | Use `fsAppend` for large files |
| `Edit` | `editCode` / `strReplace` | `editCode` preferred for AST-based edits |
| `Bash` | `executeBash` | Same functionality |
| `WebFetch` | `webFetch` | Same functionality |
| `WebSearch` | `remote_web_search` | Same functionality |
