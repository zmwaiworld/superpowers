# Installing Superpowers for Kiro

## Prerequisites

- [Kiro IDE](https://kiro.dev) installed

## Installation via Powers Panel (Recommended)

1. Open Kiro IDE
2. Open the Powers panel
3. Click "Import power from GitHub"
4. Enter: `https://github.com/obra/superpowers/tree/main/.kiro-power`
5. Install the power

The power activates automatically when you mention keywords like "debug", "plan", "brainstorm", or "tdd". On activation it locates the repo, loads the bootstrap skill via `discloseContext`, and loads other skills on demand from the repo — no file copying needed.

## Manual Installation

If you prefer not to use the Powers Panel, clone the repo and point the power at it manually.

### macOS / Linux

```bash
git clone https://github.com/obra/superpowers.git ~/superpowers
```

### Windows (PowerShell)

```powershell
git clone https://github.com/obra/superpowers.git "$env:USERPROFILE\superpowers"
```

Then tell the Kiro agent:

```text
Load the superpowers using-superpowers skill from ~/superpowers/skills/using-superpowers/SKILL.md
```

The agent will use `discloseContext` to load the skill and follow the workflow from there.

## How It Works

Superpowers uses Kiro's `discloseContext` tool to load skills directly from the repository on disk. There is no file copying, no symlinks, and no `~/.kiro/skills/` installation step.

- **Powers Panel install:** Kiro clones the repo into `~/.kiro/powers/repos/`. POWER.md locates the repo and bootstraps via `discloseContext`.
- **Manual install:** You clone the repo yourself. The agent loads skills from wherever you cloned it.

**Trade-off:** Skills are not available as `/` slash commands (Kiro only discovers those from `~/.kiro/skills/`). Instead, the power activates on keyword match and the agent loads skills on demand. You can also ask the agent directly: "use the brainstorming skill".

## Updating

### Powers Panel Install

Update from the Powers panel in Kiro, or:

```bash
cd ~/.kiro/powers/repos/*superpowers* && git pull
```

### Manual Install

```bash
cd ~/superpowers && git pull
```

Skills load from the repo directly, so updates take effect immediately — no re-copying needed.

## Uninstalling

Remove the power from the Powers panel in Kiro. For manual installs, delete the cloned repo:

**macOS / Linux:**
```bash
rm -rf ~/superpowers
```

**Windows (PowerShell):**
```powershell
Remove-Item "$env:USERPROFILE\superpowers" -Recurse -Force
```

## Troubleshooting

### Power not activating

1. Verify the power is installed in the Powers panel
2. Try mentioning a keyword like "debug" or "brainstorm" in chat
3. Check that POWER.md exists in the installed power directory

### Agent can't find skills

1. Check the repo exists: `ls ~/.kiro/powers/repos/*/skills/` or `ls ~/superpowers/skills/`
2. Verify the repo has a `skills/using-superpowers/SKILL.md` file
3. Try telling the agent the repo path explicitly

### Tool mapping issues

If the agent uses Claude Code tool names instead of Kiro equivalents, remind it:
```text
Use Kiro tools: discloseContext for skills, invokeSubAgent for subagents, executeBash for shell commands
```

## Getting Help

- Report issues: https://github.com/obra/superpowers/issues
- Main documentation: https://github.com/obra/superpowers
