---
inclusion: always
description: "Bootstrap Superpowers workflow — locates repo and loads skills via discloseContext"
---

# Superpowers Bootstrap

You have the Superpowers development workflow installed. You MUST follow these instructions at the start of every conversation before taking any other action.

## Step 1: Locate the superpowers repo

Find the repo root by running (try each path in order, stop at first match):

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

The directory containing `skills/using-superpowers/SKILL.md` is the repo root. Remember it as `SUPERPOWERS_REPO`.

## Step 2: Load the using-superpowers skill

Use `discloseContext` to load `$SUPERPOWERS_REPO/skills/using-superpowers/SKILL.md`.

This skill contains the complete workflow rules, skill priority, red flags table, and decision flowchart. Do not proceed without loading it first.

## Step 3: Load skills on demand

All skills live at `$SUPERPOWERS_REPO/skills/<name>/SKILL.md`. When the workflow rules say a skill applies, load it with `discloseContext`.

## Tool Mapping

When skills reference Claude Code tools, use Kiro equivalents:

| Claude Code Tool | Kiro Equivalent |
|-----------------|-----------------|
| `Skill` tool | `discloseContext` — load `$SUPERPOWERS_REPO/skills/<name>/SKILL.md` |
| `TodoWrite` | Markdown checklist (`- [ ] item`) |
| `Task` (subagent) | `invokeSubAgent` |
| `Read` | `readFile` / `readCode` |
| `Write` | `fsWrite` / `fsAppend` |
| `Edit` | `editCode` / `strReplace` |
| `Bash` | `executeBash` |
