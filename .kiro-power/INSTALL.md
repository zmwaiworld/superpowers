# Installing Superpowers in Kiro

There are two ways to install: a one-line script (recommended) or fully manual.

The script exists because Kiro's "Add Custom Power" panel currently can't install this power. It fails when:
- the branch contains a slash (e.g., `feat/kiro-support`)
- the power lives in a subdirectory (`.kiro-power/`)

## Option A: Install Script (Recommended)

```bash
git clone -b feat/kiro-support https://github.com/gaumondp/superpowers-kiro.git
./superpowers-kiro/.kiro-power/install.py
```

Then reload the Kiro window: `cmd-shift-P` → "Developer: Reload Window".

The script registers the cloned `.kiro-power/` directory as a `type: local`
custom power in `~/.kiro/powers/`. POWER.md and any `steering/` files are
mirrored into `~/.kiro/powers/installed/superpowers/`.

### Skills setup

Superpowers expects skill folders directly under `~/.kiro/skills/`. After
installing the power, run:

```bash
mkdir -p ~/.kiro/skills
for skill in superpowers-kiro/skills/*/; do
  cp -R "$skill" ~/.kiro/skills/"$(basename "$skill")"
done
```

### Updating

```bash
./superpowers-kiro/.kiro-power/install.py --update superpowers
```

This runs `git fetch + ff-merge` on the clone and re-mirrors POWER.md.

To update every user-added power Kiro tracks:

```bash
./superpowers-kiro/.kiro-power/install.py --update-all
```

### Uninstalling

```bash
./superpowers-kiro/.kiro-power/install.py --uninstall superpowers
```

## Option B: Fully Manual

If you'd rather not run a script, you can wire up the same state by hand.

1. Clone the repo somewhere persistent:

   ```bash
   git clone -b feat/kiro-support https://github.com/gaumondp/superpowers-kiro.git ~/.kiro/powers/repos/superpowers-kiro
   ```

2. Add an entry to `~/.kiro/powers/registries/user-added.json` (create the file
   if it doesn't exist):

   ```json
   {
     "powers": [
       {
         "name": "superpowers",
         "description": "Superpowers skills system",
         "source": {
           "type": "local",
           "path": "/Users/YOU/.kiro/powers/repos/superpowers-kiro/.kiro-power"
         },
         "autoInstall": false
       }
     ]
   }
   ```

3. Add an entry to `~/.kiro/powers/installed.json`:

   ```json
   {
     "version": "1.0.0",
     "installedPowers": [
       { "name": "superpowers", "registryId": "user-added" }
     ],
     "dismissedAutoInstalls": []
   }
   ```

4. Mirror `POWER.md` so the panel finds it:

   ```bash
   mkdir -p ~/.kiro/powers/installed/superpowers/steering
   cp ~/.kiro/powers/repos/superpowers-kiro/.kiro-power/POWER.md \
      ~/.kiro/powers/installed/superpowers/POWER.md
   ```

5. Copy skills (same as Option A):

   ```bash
   mkdir -p ~/.kiro/skills
   for skill in ~/.kiro/powers/repos/superpowers-kiro/skills/*/; do
     cp -R "$skill" ~/.kiro/skills/"$(basename "$skill")"
   done
   ```

6. Reload the Kiro window: `cmd-shift-P` → "Developer: Reload Window".

## Notes

- Use `source.type: "local"` rather than `"repo"`. Kiro's registry validator
  silently drops `type: repo` entries that didn't go through its install pipeline.
- The clone can live anywhere; pointing at `~/.kiro/powers/repos/` matches the
  location Kiro itself uses for cached repos.
- Kiro's "Install updates" button on a `type: local` power re-mirrors files but
  doesn't pull from git. Use `install.py --update` for real upstream updates.
