#!/usr/bin/env python3
"""Install this power (or any Kiro power) into Kiro.

Why this script exists:
  Kiro's "Add Custom Power" panel currently fails to install a power when:
    - the branch name contains a slash (e.g. feat/kiro-support)
    - the power lives in a repo subdirectory (.kiro-power)
    - the registry entry uses source.type = "repo"
  This script wires up Kiro's powers state directly using source.type = "local",
  which the panel accepts.

Self-install (no arguments):
  When run from inside a Kiro power directory (next to a POWER.md), it
  registers the local path as the power source. Use this when you've cloned
  the repo and want to install without going through Kiro's panel.

  Example:
    git clone -b feat/kiro-support https://github.com/gaumondp/superpowers-kiro.git
    ./superpowers-kiro/.kiro-power/install.py

Other modes:
  Install from GitHub URL:
    install.py <github-tree-url> [--name NAME]

  Install from a local power directory:
    install.py --from-local /path/to/.kiro-power [--name NAME]

  Update / uninstall:
    install.py --update NAME
    install.py --update-all
    install.py --uninstall NAME

After install/update, reload the Kiro window:
  cmd-shift-P -> Developer: Reload Window
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

KIRO_HOME = Path.home() / ".kiro"
POWERS_DIR = KIRO_HOME / "powers"
REPOS_DIR = POWERS_DIR / "repos"
INSTALLED_DIR = POWERS_DIR / "installed"
REGISTRY_FILE = POWERS_DIR / "registries" / "user-added.json"
INSTALLED_JSON = POWERS_DIR / "installed.json"


# ---------- power dir helpers ----------

def read_power_metadata(power_dir: Path) -> dict[str, str]:
    """Parse YAML frontmatter from POWER.md. Returns {} if no frontmatter found.

    Only supports simple `key: "value"` lines — no nested YAML, no lists.
    """
    power_md = power_dir / "POWER.md"
    if not power_md.is_file():
        return {}
    text = power_md.read_text()
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.+?)\s*$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        meta[key] = value
    return meta


def power_name_from_metadata(power_dir: Path, fallback: str) -> str:
    meta = read_power_metadata(power_dir)
    name = meta.get("name") or meta.get("displayName") or fallback
    # Normalize: lowercase, replace spaces with dashes.
    return re.sub(r"\s+", "-", name.strip().lower())


# ---------- GitHub URL parsing ----------

def parse_tree_url(url: str) -> tuple[str, str, str | None]:
    """Return (clone_url, branch, subdir) from a github tree URL.

    Resolves ambiguous branch/path splits by listing remote branches and
    finding the longest prefix match. Handles branches with slashes.
    """
    parsed = urlparse(url)
    if parsed.netloc != "github.com":
        sys.exit(f"Not a github.com URL: {url}")
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        sys.exit(f"URL must include owner/repo: {url}")
    owner, repo = parts[0], parts[1]
    clone_url = f"https://github.com/{owner}/{repo}.git"

    if len(parts) < 4 or parts[2] not in ("tree", "blob"):
        return clone_url, _default_branch(owner, repo), None

    rest = parts[3:]
    branch_candidates = _list_branches(owner, repo)
    for length in range(len(rest), 0, -1):
        candidate = "/".join(rest[:length])
        if candidate in branch_candidates:
            branch = candidate
            subdir = "/".join(rest[length:]) or None
            return clone_url, branch, subdir
    branch = rest[0]
    subdir = "/".join(rest[1:]) or None
    return clone_url, branch, subdir


def _list_branches(owner: str, repo: str) -> set[str]:
    out = subprocess.check_output(
        ["git", "ls-remote", "--heads", f"https://github.com/{owner}/{repo}.git"],
        text=True,
    )
    return {
        m.group(1)
        for m in (re.match(r"^[0-9a-f]+\s+refs/heads/(.+)$", line) for line in out.splitlines())
        if m
    }


def _default_branch(owner: str, repo: str) -> str:
    out = subprocess.check_output(
        ["git", "ls-remote", "--symref", f"https://github.com/{owner}/{repo}.git", "HEAD"],
        text=True,
    )
    m = re.search(r"^ref: refs/heads/(\S+)\s+HEAD$", out, re.MULTILINE)
    if not m:
        sys.exit(f"Could not determine default branch for {owner}/{repo}")
    return m.group(1)


def clone_or_update(clone_url: str, branch: str, dest: Path) -> None:
    if dest.exists():
        print(f"Updating existing clone at {dest}")
        subprocess.check_call(["git", "-C", str(dest), "fetch", "origin", branch])
        subprocess.check_call(["git", "-C", str(dest), "checkout", branch])
        subprocess.check_call(["git", "-C", str(dest), "reset", "--hard", f"origin/{branch}"])
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"Cloning {clone_url} ({branch}) -> {dest}")
        subprocess.check_call(["git", "clone", "--branch", branch, clone_url, str(dest)])


# ---------- registry / installed.json / mirroring ----------

def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def upsert_registry_entry(name: str, source_path: Path, description: str) -> None:
    data = load_json(REGISTRY_FILE, {"powers": []})
    data.setdefault("powers", [])
    data["powers"] = [p for p in data["powers"] if p.get("name") != name]
    data["powers"].append(
        {
            "name": name,
            "description": description,
            "source": {"type": "local", "path": str(source_path)},
            "autoInstall": False,
        }
    )
    save_json(REGISTRY_FILE, data)


def upsert_installed_entry(name: str) -> None:
    data = load_json(INSTALLED_JSON, {"version": "1.0.0", "installedPowers": [], "dismissedAutoInstalls": []})
    data.setdefault("installedPowers", [])
    data["installedPowers"] = [p for p in data["installedPowers"] if p.get("name") != name]
    data["installedPowers"].append({"name": name, "registryId": "user-added"})
    save_json(INSTALLED_JSON, data)


def mirror_into_installed(name: str, source_path: Path) -> None:
    target = INSTALLED_DIR / name
    target.mkdir(parents=True, exist_ok=True)
    power_md = source_path / "POWER.md"
    if not power_md.is_file():
        sys.exit(f"POWER.md not found at {power_md}")
    shutil.copy2(power_md, target / "POWER.md")
    steering_src = source_path / "steering"
    steering_dst = target / "steering"
    if steering_src.is_dir():
        if steering_dst.exists():
            shutil.rmtree(steering_dst)
        shutil.copytree(steering_src, steering_dst)
    else:
        steering_dst.mkdir(exist_ok=True)


def register_local(power_dir: Path, name_override: str | None, description: str) -> str:
    """Register a local power directory and return the chosen name."""
    if not (power_dir / "POWER.md").is_file():
        sys.exit(f"No POWER.md at {power_dir}. Is this a Kiro power directory?")
    fallback = power_dir.name.lstrip(".") or power_dir.parent.name
    name = name_override or power_name_from_metadata(power_dir, fallback)
    upsert_registry_entry(name, power_dir, description)
    upsert_installed_entry(name)
    mirror_into_installed(name, power_dir)
    return name


def print_install_summary(name: str, source_path: Path) -> None:
    print()
    print(f"Installed '{name}'")
    print(f"  registry:       {REGISTRY_FILE}")
    print(f"  installed.json: {INSTALLED_JSON}")
    print(f"  source:         {source_path}")
    print(f"  mirrored:       {INSTALLED_DIR / name}")
    print()
    print("Reload Kiro: cmd-shift-P -> 'Developer: Reload Window'")


# ---------- modes ----------

def derive_name_from_url(repo_name: str, subdir: str | None) -> str:
    if subdir and subdir not in (".", ""):
        last = subdir.rstrip("/").split("/")[-1]
        if not last.startswith(".") and last not in ("power", "kiro-power", ".kiro-power"):
            return last
    return repo_name


def install_from_url(url: str, name_override: str | None) -> None:
    clone_url, branch, subdir = parse_tree_url(url)
    repo_name = clone_url.rstrip("/").split("/")[-1].removesuffix(".git")
    repo_dir = REPOS_DIR / repo_name
    clone_or_update(clone_url, branch, repo_dir)

    source_path = repo_dir if not subdir else repo_dir / subdir
    if not source_path.is_dir():
        sys.exit(f"Subdir not found in repo: {source_path}")

    fallback_name = derive_name_from_url(repo_name, subdir)
    name = name_override or power_name_from_metadata(source_path, fallback_name)
    register_local(source_path, name, description=f"Custom power from {url}")
    print_install_summary(name, source_path)


def install_self(script_path: Path, name_override: str | None) -> None:
    """Install the power that this script lives inside of."""
    power_dir = script_path.resolve().parent
    if not (power_dir / "POWER.md").is_file():
        sys.exit(
            f"No POWER.md next to {script_path}. "
            "Self-install expects this script to live inside a power directory."
        )
    fallback = power_dir.name.lstrip(".") or power_dir.parent.name
    name = name_override or power_name_from_metadata(power_dir, fallback)
    description = f"Local install from {power_dir}"
    register_local(power_dir, name, description)
    print_install_summary(name, power_dir)


def install_from_local(path: Path, name_override: str | None) -> None:
    power_dir = path.expanduser().resolve()
    if not power_dir.is_dir():
        sys.exit(f"Not a directory: {power_dir}")
    fallback = power_dir.name.lstrip(".") or power_dir.parent.name
    name = name_override or power_name_from_metadata(power_dir, fallback)
    register_local(power_dir, name, description=f"Custom power from {power_dir}")
    print_install_summary(name, power_dir)


def find_git_root(path: Path) -> Path | None:
    p = path.resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def update(name: str) -> bool:
    data = load_json(REGISTRY_FILE, {"powers": []})
    entry = next((p for p in data.get("powers", []) if p.get("name") == name), None)
    if not entry:
        sys.exit(f"No registry entry for '{name}' in {REGISTRY_FILE}")
    source = entry.get("source", {})
    if source.get("type") != "local":
        sys.exit(f"'{name}' has source type {source.get('type')!r}, only 'local' is supported by --update")
    source_path = Path(source["path"]).expanduser()
    if not source_path.is_dir():
        sys.exit(f"Source path missing: {source_path}")

    git_root = find_git_root(source_path)
    changed = False
    if git_root is None:
        print(f"[{name}] not a git checkout, skipping pull (path: {source_path})")
    else:
        before = subprocess.check_output(
            ["git", "-C", str(git_root), "rev-parse", "HEAD"], text=True
        ).strip()
        try:
            branch = subprocess.check_output(
                ["git", "-C", str(git_root), "rev-parse", "--abbrev-ref", "HEAD"], text=True
            ).strip()
            subprocess.check_call(["git", "-C", str(git_root), "fetch", "origin", branch])
            subprocess.check_call(
                ["git", "-C", str(git_root), "merge", "--ff-only", f"origin/{branch}"]
            )
        except subprocess.CalledProcessError as e:
            print(f"[{name}] git update failed: {e}")
            return False
        after = subprocess.check_output(
            ["git", "-C", str(git_root), "rev-parse", "HEAD"], text=True
        ).strip()
        if before == after:
            print(f"[{name}] already up to date ({after[:7]})")
        else:
            print(f"[{name}] {before[:7]} -> {after[:7]}")
            changed = True

    mirror_into_installed(name, source_path)
    return changed


def update_all() -> None:
    data = load_json(REGISTRY_FILE, {"powers": []})
    names = [p["name"] for p in data.get("powers", [])]
    if not names:
        print("No user-added powers found")
        return
    any_changed = False
    for name in names:
        try:
            if update(name):
                any_changed = True
        except SystemExit as e:
            print(f"[{name}] skipped: {e}")
    if any_changed:
        print()
        print("Reload Kiro: cmd-shift-P -> 'Developer: Reload Window'")


def uninstall(name: str) -> None:
    data = load_json(REGISTRY_FILE, {"powers": []})
    before = len(data.get("powers", []))
    data["powers"] = [p for p in data.get("powers", []) if p.get("name") != name]
    save_json(REGISTRY_FILE, data)
    removed_registry = before - len(data["powers"])

    data = load_json(INSTALLED_JSON, {"version": "1.0.0", "installedPowers": [], "dismissedAutoInstalls": []})
    before = len(data.get("installedPowers", []))
    data["installedPowers"] = [p for p in data.get("installedPowers", []) if p.get("name") != name]
    save_json(INSTALLED_JSON, data)
    removed_installed = before - len(data["installedPowers"])

    target = INSTALLED_DIR / name
    if target.exists():
        shutil.rmtree(target)

    print(f"Uninstalled '{name}'")
    print(f"  registry entries removed:  {removed_registry}")
    print(f"  installed entries removed: {removed_installed}")
    print(f"  removed dir: {target}")
    print()
    print("Reload Kiro: cmd-shift-P -> 'Developer: Reload Window'")


# ---------- main ----------

def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("url", nargs="?", help="GitHub tree URL pointing at the power directory")
    p.add_argument("--name", help="Override the installed power name")
    p.add_argument("--from-local", metavar="PATH", help="Install from a local directory containing POWER.md")
    p.add_argument("--uninstall", metavar="NAME", help="Uninstall a power by name")
    p.add_argument("--update", metavar="NAME", help="Pull latest for a power's source repo and re-mirror")
    p.add_argument("--update-all", action="store_true", help="Update every user-added power")
    args = p.parse_args()

    if args.update_all:
        update_all()
        return
    if args.update:
        if update(args.update):
            print()
            print("Reload Kiro: cmd-shift-P -> 'Developer: Reload Window'")
        return
    if args.uninstall:
        uninstall(args.uninstall)
        return
    if args.from_local:
        install_from_local(Path(args.from_local), args.name)
        return
    if args.url:
        install_from_url(args.url, args.name)
        return

    # No args: self-install if this script is inside a power dir.
    install_self(Path(__file__), args.name)


if __name__ == "__main__":
    main()
