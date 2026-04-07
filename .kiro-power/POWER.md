---
name: "superpowers"
displayName: "Superpowers"
description: "Complete software development workflow with composable skills: TDD, systematic debugging, brainstorming, planning, code review, and subagent-driven development"
keywords: ["tdd", "test driven development", "debug", "brainstorm", "plan", "code review", "workflow", "skills", "subagent", "refactor", "git worktree", "implementation", "testing", "verification"]
author: "Jesse Vincent"
---

# Superpowers

Superpowers is a complete software development workflow built on composable skills. It starts before you write code — brainstorming designs, writing plans, then executing with TDD, systematic debugging, code review, and subagent-driven development.

Bootstrap and tool mapping are handled by the bundled steering file (`steering/superpowers-bootstrap.md`), which loads automatically in every conversation.

## Available Skills

Load any skill with `discloseContext` from `$SUPERPOWERS_REPO/skills/<name>/SKILL.md`:

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
