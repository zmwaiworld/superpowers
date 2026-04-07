---
inclusion: always
---

# Superpowers

At the start of every conversation, you MUST complete these steps IN ORDER before doing anything else:

## Step 1: Locate the SKILL.md file

Use `listDirectory` or `executeBash` (NOT `discloseContext`) to find the file at one of these paths:
- `~/.kiro/powers/repos/*/skills/using-superpowers/SKILL.md`
- `~/superpowers/skills/using-superpowers/SKILL.md`

## Step 2: Read the SKILL.md file

Use `executeBash` with `cat <path>` or `readFile` to read the full content of the file you found in Step 1. Do NOT use `discloseContext` — it cannot load files by path.

## Step 3: Follow the SKILL.md instructions

The SKILL.md content defines your complete workflow for the session. Follow it, including loading other skills on demand from the same repo.

## Tool Mapping (for interpreting SKILL.md instructions)

SKILL.md was written for Claude Code. In Kiro, map these tools:

| SKILL.md says | In Kiro, use |
|---|---|
| `Skill` (load a skill) | `executeBash` with `cat` to read `SKILL.md` from the same repo |
| `TodoWrite` | markdown checklist |
| `Task` | `invokeSubAgent` |
| `Read` | `readFile` / `readCode` |
| `Write` | `fsWrite` |
| `Edit` | `strReplace` |
| `Bash` | `executeBash` |

## Critical Notes

- `discloseContext` only works for skills registered in `~/.kiro/skills/`. The superpowers repo skills are NOT registered there — they live on the filesystem and must be read directly.
- If Step 1 finds no file at either path, skip this workflow and proceed normally.
