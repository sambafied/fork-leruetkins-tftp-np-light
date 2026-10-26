"""Read-only donor reference check; never renders or executes source text."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text())
assert manifest["source_commit"] == "1b6be33569b47972bf939a2a332b0c533fd2cccf"
expected = {"LICENSE", "public/menu.txt", "public/boot/soft/ipxes/memtest/memtest.ejs"}
assert len(manifest["files"]) == len(expected)
assert {entry["path"] for entry in manifest["files"]} == expected
assert not (root / "source").is_symlink()
actual = set()
for path in (root / "source").rglob("*"):
    assert not path.is_symlink(), path
    if path.is_file():
        actual.add(path.relative_to(root / "source").as_posix())
assert actual == expected, (actual - expected, expected - actual)
for entry in manifest["files"]:
    path = root / "source" / entry["path"]
    mode = path.stat().st_mode
    assert stat.S_ISREG(mode) and not mode & 0o111, path
    content = path.read_bytes()
    assert len(content) == entry["bytes"], path
    assert hashlib.sha256(content).hexdigest() == entry["sha256"], path
    blob = subprocess.check_output(["git", "hash-object", "--stdin"], input=content,
                                   cwd=root).decode().strip()
    assert blob == entry["git_blob"], path
print("PASS: 3 selected donor files; exact set, pin, sizes, SHA-256, Git blobs and modes")
