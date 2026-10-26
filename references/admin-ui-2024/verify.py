"""Read-only historical reference inventory check; never executes recovered content."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text())
assert manifest["source_commit"] == "b0aeaa128c16d70a29ccbba841ff9dcfbdaa53fc"
assert len(manifest["files"]) == 8
expected = {entry["path"] for entry in manifest["files"]}
assert expected == {"LICENSE", "public/config.ejs", "public/console.ejs",
                    "public/index.ejs", "public/menu.ejs", "public/menu_editor.ejs",
                    "public/assets/css/index.css", "public/assets/js/index.js"}
actual = {p.relative_to(root / "source").as_posix()
          for p in (root / "source").rglob("*") if p.is_file()}
assert actual == expected, (actual - expected, expected - actual)
for entry in manifest["files"]:
    path = root / "source" / entry["path"]
    assert not path.is_symlink() and not path.stat().st_mode & 0o111
    content = path.read_bytes()
    assert len(content) == entry["bytes"]
    assert hashlib.sha256(content).hexdigest() == entry["sha256"]
    original = subprocess.check_output(["git", "show",
        manifest["source_commit"] + ":" + entry["path"]], cwd=root)
    assert content == original, entry["path"]
    blob = subprocess.check_output(["git", "hash-object", "--stdin"], input=content,
                                   cwd=root, text=False).decode().strip()
    assert blob == entry["git_blob"]
print("PASS: 8 reference files; exact set, sizes, SHA-256, Git bytes/blob IDs and modes")
