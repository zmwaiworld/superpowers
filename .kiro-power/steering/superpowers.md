---
inclusion: always
---

# Superpowers

At the start of every conversation, locate the superpowers repo (`~/.kiro/powers/repos/*/skills/using-superpowers/SKILL.md` or `~/superpowers/skills/using-superpowers/SKILL.md`) and use `discloseContext` to load that file. It contains the complete workflow. Load other skills on demand from the same repo with `discloseContext`.

Tool mapping: `Skill` → `discloseContext`, `TodoWrite` → markdown checklist, `Task` → `invokeSubAgent`, `Read` → `readFile`/`readCode`, `Write` → `fsWrite`, `Edit` → `editCode`/`strReplace`, `Bash` → `executeBash`.
