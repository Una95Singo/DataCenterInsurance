import csv
from pathlib import Path

from dc_scs import manifest as manifest_mod


def test_sha256_file(tmp_path: Path):
    p = tmp_path / "x.txt"
    p.write_bytes(b"hello\n")
    digest = manifest_mod.sha256_file(p)
    # sha256 of "hello\n"
    assert digest == "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"


def test_append_manifest_row(tmp_path: Path, monkeypatch):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    fake_root = tmp_path
    manifest_path = raw_dir / "manifest.csv"

    monkeypatch.setattr(manifest_mod, "REPO_ROOT", fake_root)
    monkeypatch.setattr(manifest_mod, "RAW_DIR", raw_dir)
    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", manifest_path)

    payload = raw_dir / "sample.bin"
    payload.write_bytes(b"abc")

    row = manifest_mod.append_manifest_row(
        pull_id="t1",
        source_name="unit-test",
        source_url="https://example.invalid/",
        local_path=payload,
        notes="smoke",
    )

    assert row["bytes"] == 3
    assert row["local_path"] == "raw/sample.bin"

    with manifest_path.open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["pull_id"] == "t1"
    assert rows[0]["sha256"] == row["sha256"]
