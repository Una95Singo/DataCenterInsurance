"""Fetch-layer tests. Patch requests; no network."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from dc_scs.inventory import fetch as fetch_mod
from dc_scs.inventory.fetch import fetch_metro, scrape_metros
from dc_scs.inventory.metros import Metro


class _FakeResponse:
    def __init__(self, content: bytes, status: int = 200):
        self.content = content
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def _fake_session(body: bytes = b"<html>hi</html>") -> MagicMock:
    sess = MagicMock()
    sess.get.return_value = _FakeResponse(body)
    return sess


@pytest.fixture()
def isolated_manifest(tmp_path: Path, monkeypatch):
    raw = tmp_path / "raw"
    raw.mkdir()
    manifest_path = raw / "manifest.csv"

    from dc_scs import manifest as manifest_mod

    monkeypatch.setattr(manifest_mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(manifest_mod, "RAW_DIR", raw)
    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(fetch_mod, "MANIFEST_PATH", manifest_path)
    return raw


def test_fetch_metro_writes_file_and_manifest(isolated_manifest: Path):
    m = Metro("virginia", "manassas")
    sess = _fake_session(b"<html>payload</html>")

    result = fetch_metro(m, isolated_manifest, already_logged=set(), session=sess)

    assert result.status.startswith("fetched")
    dest = m.local_path(isolated_manifest)
    assert dest.read_bytes() == b"<html>payload</html>"
    sess.get.assert_called_once()
    (url_arg,) = sess.get.call_args.args
    assert url_arg == "https://www.datacentermap.com/usa/virginia/manassas/"


def test_fetch_metro_is_cached_on_second_run(isolated_manifest: Path):
    m = Metro("virginia", "manassas")
    sess = _fake_session(b"<html>payload</html>")

    fetch_metro(m, isolated_manifest, already_logged=set(), session=sess)
    already = {m.pull_id}
    result2 = fetch_metro(m, isolated_manifest, already_logged=already, session=sess)

    # Second call did not hit network again (status starts with 'cached'),
    # did not write a duplicate manifest row (already in already_logged).
    assert result2.status.startswith("cached")
    assert "manifest row already present" in result2.status
    assert sess.get.call_count == 1


def test_fetch_metro_on_failure_does_not_corrupt_destination(isolated_manifest: Path):
    m = Metro("texas", "dallas")
    sess = MagicMock()
    sess.get.return_value = _FakeResponse(b"", status=500)

    result = fetch_metro(m, isolated_manifest, already_logged=set(), session=sess)

    assert result.status.startswith("FAIL")
    assert not m.local_path(isolated_manifest).exists()


def test_scrape_metros_sleep_skipped_between_cached(isolated_manifest: Path, monkeypatch):
    # Pre-populate both files so every iteration takes the `cached` path.
    metros = [Metro("virginia", "manassas"), Metro("texas", "dallas")]
    for mx in metros:
        p = mx.local_path(isolated_manifest)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"<html>cached</html>")

    calls: list[float] = []
    monkeypatch.setattr(fetch_mod.time, "sleep", lambda s: calls.append(s))

    scrape_metros(metros, isolated_manifest, delay_s=2.0, session=_fake_session())

    assert calls == []  # no sleeps between cached results


def test_scrape_metros_sleeps_between_fetches(isolated_manifest: Path, monkeypatch):
    metros = [Metro("virginia", "manassas"), Metro("texas", "dallas")]
    calls: list[float] = []
    monkeypatch.setattr(fetch_mod.time, "sleep", lambda s: calls.append(s))

    scrape_metros(metros, isolated_manifest, delay_s=2.0, session=_fake_session())

    # First fetch: no prior network → no sleep. Second fetch: sleeps 2 s.
    assert calls == [2.0]
