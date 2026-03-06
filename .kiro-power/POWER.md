---
name: "superpowers"
displayName: "Superpowers"
description: "Complete software development workflow with composable skills: TDD, systematic debugging, brainstorming, planning, code review, and subagent-driven development"
keywords: ["tdd", "test driven development", "debug", "brainstorm", "plan", "code review", "workflow", "skills", "subagent", "refactor", "git worktree", "implementation", "testing", "verification"]
author: "Jesse Vincent"
---

# Superpowers

Superpowers is a complete software development workflow built on composable skills. It starts before you write code — brainstorming designs, writing plans, then executing with TDD, systematic debugging, code review, and subagent-driven development. Skills trigger automatically based on what you're doing.

## Onboarding

When this power is first activated, set up skill access so the user can invoke skills via `/` slash commands.

### Step 1: Determine power installation path

This POWER.md is located inside the superpowers repository. The `skills/` directory is at the same level as the `.kiro-power/` directory that contains this file.

### Step 2: Check if skills are already installed

```bash
ls ~/.kiro/skills/brainstorming/SKILL.md 2>/dev/null
```

### Step 3: Copy skills if needed

If the skills are not yet installed, copy each skill directory into `~/.kiro/skills/`. Kiro requires skills to be directly under the skills directory (no nesting).

**macOS / Linux:**
```bash
mkdir -p ~/.kiro/skills
for skill in <path-to-superpowers-repo>/skills/*/; do
  target=~/.kiro/skills/"$(basename "$skill")"
  rm -rf "$target"
  cp -R "$skill" "$target"
done
```

Where `<path-to-superpowers-repo>` is the parent directory of `.kiro-power/` (the root of this repository).

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.kiro\skills"
Get-ChildItem "<path-to-superpowers-repo>\skills" -Directory | ForEach-Object {
    $target = "$env:USERPROFILE\.kiro\skills\$($_.Name)"
    if (Test-Path $target) { Remove-Item $target -Recurse -Force }
    Copy-Item $_.FullName $target -Recurse
}
```

### Step 4: Verify

```bash
ls ~/.kiro/skills/
```

You should see skill directories like `brainstorming/`, `systematic-debugging/`, `test-driven-development/`, etc. directly under `~/.kiro/skills/`.

After setup, skills are available as `/` slash commands in all Kiro workspaces.

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


## Bootstrap

When this power activates, IMMEDIATELY use `discloseContext` to load the `using-superpowers` skill before taking any other action. That skill contains the complete workflow rules, skill priority, red flags table, and decision flowchart that govern all agent behavior.

Do not proceed without loading it first.

Skills are also available as `/` slash commands — the user can type `/brainstorming`, `/systematic-debugging`, etc. to activate a skill directly.

## Tool Mapping for Kiro

When skills reference Claude Code tools, substitute Kiro equivalents:

| Claude Code Tool | Kiro Equivalent | Notes |
|-----------------|-----------------|-------|
| `Skill` tool | `discloseContext` | Load a skill by name |
| `TodoWrite` | Markdown checklist | Use `- [ ] item` format in responses |
| `Task` (subagent) | `invokeSubAgent` | Dispatch work to sub-agents |
| `Read` | `readFile` / `readCode` | `readCode` preferred for code files |
| `Write` | `fsWrite` / `fsAppend` | Use `fsAppend` for large files |
| `Edit` | `editCode` / `strReplace` | `editCode` preferred for AST-based edits |
| `Bash` | `executeBash` | Same functionality |
| `WebFetch` | `webFetch` | Same functionality |
| `WebSearch` | `remote_web_search` | Same functionality |
