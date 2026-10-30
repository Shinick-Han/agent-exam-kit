"""Maintainer build only. Python is not needed by the resulting Unix installer."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import zipfile

import install

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text("utf-8"))
files = {}
for item in manifest["skills"]:
    data = install.payload(item, root / ".cache")
    selected = install.select_zip(data, item["prefix"], item.get("includes"))
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        license_path = item["prefix"].split("/")[0] + "/LICENSE"
        if license_path in archive.namelist():
            selected["UPSTREAM-LICENSE"] = archive.read(license_path)
    for name, content in selected.items():
        files["skills/" + item["name"] + "/" + name] = content
files["sources.json"] = json.dumps(manifest["skills"], indent=2).encode()
stream = io.BytesIO()
with tarfile.open(fileobj=stream, mode="w", format=tarfile.USTAR_FORMAT) as archive:
    for name, content in sorted(files.items()):
        item = tarfile.TarInfo(name)
        item.size = len(content)
        item.mode = 0o644
        item.mtime = 0
        archive.addfile(item, io.BytesIO(content))
compressed = gzip.compress(stream.getvalue(), mtime=0)
out = root / "release"
out.mkdir(exist_ok=True)
(out / "writing-skills.tar.gz").write_bytes(compressed)
digest = hashlib.sha256(compressed).hexdigest()
(out / "SHA256SUMS").write_text(digest + "  writing-skills.tar.gz\n", "utf-8")
(root / ".cache" / digest).write_bytes(compressed)
script = (root / "unix-install.sh.in").read_text("utf-8").replace("@BUNDLE_SHA@", digest)
(root / "install.sh").write_text(script, "utf-8", newline="\n")
print("Skill bundle:", len(compressed), "bytes; sha256:", digest)
