"""Extract facility records from a saved datacentermap.com metro HTML page.

A metro page (e.g. `/usa/virginia/manassas/`) is a Next.js document whose
`<script id="__NEXT_DATA__">` tag embeds the full page state as JSON. The
facility roster for the metro sits under `props.pageProps.mapdata.dcs`
as a list of GeoJSON Features. No HTML parsing is needed beyond the one
regex that extracts the script body.

Observed `maptype` values on the Manassas fixture:
  - `dc`              93  mapped facilities (real coords)
  - `dc-unmapped`     3   facilities shown at an approximate metro-centroid
                          location; the records are real, the coords are
                          synthetic. Preserved but flagged.
  - `market-unmapped` 1   sentinel at the metro centroid that groups the
                          unmapped ones in the UI. Dropped.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from typing import Any

_NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json"[^>]*>(.*?)</script>',
    re.DOTALL,
)

FACILITY_MAPTYPES = frozenset({"dc", "dc-unmapped"})

# Fields lifted directly from each GeoJSON Feature's `properties` dict.
_PROPERTY_FIELDS = (
    "id",
    "maptype",
    "listingtype",
    "capacitytype",
    "name",
    "companyname",
    "companylink",
    "address",
    "postal",
    "city",
    "state",
    "country",
    "url",
    "parent",
)


def extract_next_data(html: str) -> dict[str, Any]:
    """Parse the embedded __NEXT_DATA__ payload from a metro page's HTML."""
    match = _NEXT_DATA_RE.search(html)
    if not match:
        raise ValueError("no __NEXT_DATA__ script tag found in HTML")
    return json.loads(match.group(1))


def flatten_features(
    next_data: dict[str, Any],
    *,
    source_state: str,
    source_metro: str,
) -> Iterator[dict[str, Any]]:
    """Yield one flat dict per real facility on the page.

    Feature-level fields (id, name, address, …) are lifted from the GeoJSON
    `properties` dict; coordinates are lifted from `geometry.coordinates`;
    the enclosing metro page's slug is attached as `source_state` /
    `source_metro` so downstream code can audit which page a record came
    from. The sentinel `market-unmapped` row is dropped.
    """
    page_props = next_data.get("props", {}).get("pageProps", {})
    features = page_props.get("mapdata", {}).get("dcs") or []
    for feature in features:
        props = feature.get("properties") or {}
        if props.get("maptype") not in FACILITY_MAPTYPES:
            continue
        geom = feature.get("geometry") or {}
        coords = geom.get("coordinates") or (None, None)
        lon = coords[0] if len(coords) > 0 else None
        lat = coords[1] if len(coords) > 1 else None

        record = {k: props.get(k) for k in _PROPERTY_FIELDS}
        record["latitude"] = lat
        record["longitude"] = lon
        record["source_state"] = source_state
        record["source_metro"] = source_metro
        yield record
