"""Sanity checks on the raw-sources registry.

These tests don't touch the network. They guarantee the YAML is
well-formed, every entry has the required fields, pull_ids are unique,
and local_paths are scoped under data/raw/.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REGISTRY = Path(__file__).resolve().parents[1] / "scripts" / "raw_sources.yaml"

REQUIRED_SOURCE_FIELDS = {"pull_id", "source_name", "url", "local_path"}
REQUIRED_TODO_FIELDS = {"pull_id", "source_name", "blocker"}


def _registry() -> dict:
    with REGISTRY.open() as f:
        return yaml.safe_load(f)


def test_registry_parses():
    r = _registry()
    assert isinstance(r.get("sources", []), list)
    assert isinstance(r.get("todo", []), list)


def test_active_sources_well_formed():
    for entry in _registry().get("sources", []):
        missing = REQUIRED_SOURCE_FIELDS - entry.keys()
        assert not missing, f"{entry.get('pull_id')} missing {missing}"
        assert entry["local_path"].startswith("data/raw/"), entry["local_path"]
        assert entry["url"].startswith("https://"), entry["url"]


def test_todo_entries_well_formed():
    for entry in _registry().get("todo", []):
        missing = REQUIRED_TODO_FIELDS - entry.keys()
        assert not missing, f"{entry.get('pull_id')} missing {missing}"


def test_pull_ids_globally_unique():
    r = _registry()
    ids = [e["pull_id"] for e in r.get("sources", [])] + [
        e["pull_id"] for e in r.get("todo", [])
    ]
    assert len(ids) == len(set(ids)), "duplicate pull_id in raw_sources.yaml"
