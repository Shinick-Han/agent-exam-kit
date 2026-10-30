#!/usr/bin/env python3
"""Download pinned public tools. Never read credentials or project files."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import sys
import tempfile
import urllib.request
import zipfile

BASE = "https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0"
MAX_DOWNLOAD = 150 * 1024 * 1024


def download(url):
    if not url.startswith("https://"):
        raise ValueError("HTTPS required")
    req = urllib.request.Request(url, headers={"User-Agent": "agent-exam-kit/0.1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("Download exceeds size limit")
    return data


def sha(data):
    return hashlib.sha256(data).hexdigest()


def payload(item, cache):
    cached = cache / item["sha256"] if cache else None
    data = cached.read_bytes() if cached and cached.is_file() else download(item["url"])
    if sha(data) != item["sha256"]:
        raise ValueError("SHA-256 mismatch: " + item["name"])
    if cached and not cached.exists():
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_bytes(data)
    return data


def select_zip(data, prefix, includes=None):
    """Return selected regular files; reject path traversal and symbolic links."""
    files = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            name = entry.filename
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name:
                raise ValueError("Unsafe archive path")
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Archive symlinks are unsupported")
            if entry.is_dir() or not name.startswith(prefix):
                continue
            relative = name[len(prefix):]
            if not relative:
                continue
            if includes and relative.split("/")[0] not in includes:
                continue
            if relative in files:
                raise ValueError("Duplicate archive path")
            files[relative] = archive.read(entry)
    if not files:
        raise ValueError("Selected archive directory is empty")
    return files


def host_key():
    system = {"Linux": "linux", "Darwin": "macos", "Windows": "windows"}.get(platform.system())
    machine = platform.machine().lower()
    arch = {"amd64": "x86_64", "x86_64": "x86_64", "arm64": "aarch64", "aarch64": "aarch64"}.get(machine)
    return f"{system}-{arch}"


def install_tree(target, files):
    """Never replace an existing tree; all identical files mean an idempotent rerun."""
    if target.exists() or target.is_symlink():
        if target.is_dir() and not target.is_symlink() and all(
            (target / name).is_file() and (target / name).read_bytes() == data
            for name, data in files.items()
        ):
            return "already_installed"
        return "kept_existing_not_verified"
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".exam-kit-", dir=target.parent) as temp:
        staged = Path(temp) / "tree"
        staged.mkdir()
        for name, data in files.items():
            destination = staged / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        staged.rename(target)
    return "installed"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.home() / ".agent-exam-kit")
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--cache", type=Path, help="Optional download cache; every cached file is hash-checked")
    parser.add_argument("--skills-only", action="store_true")
    parser.add_argument("--herdr-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.skills_only and args.herdr_only:
        parser.error("Choose at most one component filter")
    manifest = json.loads(args.manifest.read_text("utf-8") if args.manifest else download(BASE + "/manifest.json"))
    key = host_key()
    selected = []
    if not args.skills_only:
        if key not in manifest["herdr"]:
            raise ValueError("Unsupported Herdr platform: " + key)
        selected.append(("herdr", manifest["herdr"][key], args.root / "bin"))
    if not args.herdr_only:
        selected.extend(("skill", item, args.skills_dir / item["name"]) for item in manifest["skills"])
    if args.dry_run:
        print(json.dumps({"version": manifest["version"], "platform": key, "plan": [
            {"kind": kind, "name": item["name"], "destination": str(dest), "url": item["url"], "sha256": item["sha256"]}
            for kind, item, dest in selected]}, ensure_ascii=False, indent=2))
        return 0
    results = []
    # Verify every download before changing any installation directory.
    fetched = [(kind, item, dest, payload(item, args.cache)) for kind, item, dest in selected]
    for kind, item, dest, data in fetched:
        if kind == "skill":
            files = select_zip(data, item["prefix"], item.get("includes"))
            if "SKILL.md" not in files:
                raise ValueError("Missing SKILL.md: " + item["name"])
        elif item.get("zip_member"):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                files = {"herdr.exe": archive.read(item["zip_member"])}
        else:
            files = {"herdr": data}
        status = install_tree(dest, files)
        if kind == "herdr" and status != "kept_existing_not_verified" and os.name != "nt":
            (dest / "herdr").chmod(0o755)
        results.append({"name": item["name"], "destination": str(dest), "status": status,
                        "source": item["url"], "sha256": item["sha256"]})
        print(item["name"] + ": " + status + " -> " + str(dest))
    args.root.mkdir(parents=True, exist_ok=True)
    receipt = {"bundle_version": manifest["version"], "results": results}
    (args.root / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), "utf-8")
    (args.root / "USAGE.md").write_text(
        "# Agent exam kit\n\nInvoke writing skills only when editing documents. "
        "Preserve facts, numbers, tests, commands and uncertainty. "
        "Apply stop-slop-ko last for Korean text. Resolve scanner/reference paths relative to each installed skill.\n\n"
        "Use the supplied Codex and authorized models/account unchanged. "
        "Herdr installation does not install Codex or its integration hooks, start agents, modify auth, "
        "or connect to an external model. Start with one coordinator and one worker. "
        "Check CPU/RAM and actual task completion. Follow the exam's tool restrictions. "
        "During AI-prohibited follow-up questions, stop AI use.\n", "utf-8")
    if not args.skills_only:
        executable = args.root / "bin" / ("herdr.exe" if os.name == "nt" else "herdr")
        print("Start Herdr: " + str(executable))
    print("Receipt: " + str(args.root / "receipt.json"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print("Install failed: " + str(error), file=sys.stderr)
        sys.exit(1)
