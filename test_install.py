import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import install


def archive(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as output:
        for name, data in files.items():
            output.writestr(name, data)
    return stream.getvalue()


class InstallationTests(unittest.TestCase):
    def test_traversal_rejected(self):
        for name in ("source/../escape", "/absolute", "source\\..\\escape"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                install.select_zip(archive({name: b"bad"}), "source/")

    def test_symlink_rejected(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as output:
            entry = zipfile.ZipInfo("source/link")
            entry.create_system = 3
            entry.external_attr = 0o120777 << 16
            output.writestr(entry, "../outside")
        with self.assertRaises(ValueError):
            install.select_zip(stream.getvalue(), "source/")

    def test_prefix_and_includes(self):
        data = archive({"source/SKILL.md": b"rules", "source/references/a.md": b"reference",
                        "source/corpus/large": b"exclude", "other/SKILL.md": b"exclude"})
        files = install.select_zip(data, "source/", ["SKILL.md", "references"])
        self.assertEqual(set(files), {"SKILL.md", "references/a.md"})

    def test_rerun_and_existing_customization(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "skill"
            files = {"SKILL.md": b"original"}
            self.assertEqual(install.install_tree(target, files), "installed")
            self.assertEqual(install.install_tree(target, files), "already_installed")
            (target / "SKILL.md").write_bytes(b"custom")
            self.assertEqual(install.install_tree(target, files), "kept_existing_not_verified")
            self.assertEqual((target / "SKILL.md").read_bytes(), b"custom")

    def test_hash_failure_changes_no_installation(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            cache = p / "cache"
            cache.mkdir()
            (cache / ("0" * 64)).write_bytes(b"tampered")
            with self.assertRaises(ValueError):
                install.payload({"name": "test", "sha256": "0" * 64, "url": "https://example.invalid"}, cache)
            self.assertEqual(set(p.iterdir()), {cache})

    def test_cli_isolated_install_and_dry_run(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            cache = p / "cache"
            cache.mkdir()
            data = archive({"source/SKILL.md": b"public rules", "source/references/r.md": b"ref"})
            digest = install.sha(data)
            (cache / digest).write_bytes(data)
            manifest = p / "manifest.json"
            manifest.write_text(json.dumps({"version": "test", "herdr": {}, "skills": [
                {"name": "example", "url": "https://example.invalid", "sha256": digest, "prefix": "source/"}]}))
            auth = p / ".codex" / "auth.json"
            auth.parent.mkdir()
            auth.write_bytes(b"test sentinel; not a credential")
            args = ["--skills-only", "--manifest", str(manifest), "--cache", str(cache),
                    "--root", str(p / "root"), "--skills-dir", str(p / "skills")]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(install.main(args + ["--dry-run"]), 0)
                self.assertFalse((p / "root").exists())
                self.assertFalse((p / "skills").exists())
                self.assertEqual(install.main(args), 0)
                self.assertEqual(install.main(args), 0)
            self.assertEqual((p / "skills/example/references/r.md").read_bytes(), b"ref")
            self.assertEqual(auth.read_bytes(), b"test sentinel; not a credential")
            receipt = json.loads((p / "root/receipt.json").read_text("utf-8"))
            self.assertEqual(receipt["results"][0]["status"], "already_installed")


if __name__ == "__main__":
    unittest.main()
