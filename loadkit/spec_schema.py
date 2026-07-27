"""Universal spec schema for all Ripple data pours.

Every dataset — regardless of loader tier (bridge_fuel, server_side, portal,
onboard) — gets one spec dict validated against this schema. The pour router
reads the `loader` field to dispatch; everything else is consumed by the loader
and the post-land lifecycle (log, register, scaffold, connect).

Backwards-compatible: existing specs in bridge_fuel_specs.py and
server_side_specs.py are valid PourSpecs (missing fields get defaults).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import urlparse


# Valid loader backends -- the pour router dispatches on this.
LOADERS = ("bridge_fuel", "server_side", "portal", "onboard")

# Valid source kinds (file shape on download).
KINDS = ("csv", "zip", "zip_csv", "json", "xml", "tsv", "dbf")


@dataclass
class KeyCol:
    """A single key-column mapping: source column name -> canonical key name."""
    col: str       # column name in the raw file (case-sensitive as downloaded)
    alias: str     # canonical name the connect engine detects (EIN, NPI, CIK, etc.)

    @classmethod
    def from_dict(cls, d: dict) -> "KeyCol":
        return cls(col=d["col"], alias=d.get("as", d.get("alias", d["col"])))

    def to_dict(self) -> dict:
        return {"col": self.col, "as": self.alias}


@dataclass
class Resolver:
    """For sources with rotating download links (e.g. GLEIF metadata API)."""
    url: str
    type: str = "json"  # json | regex
    path: str = ""      # dot-path into JSON response (e.g. "data.full_file.csv.url")

    @classmethod
    def from_dict(cls, d: dict) -> "Resolver":
        return cls(url=d["url"], type=d.get("type", "json"), path=d.get("path", ""))

    def to_dict(self) -> dict:
        return {"url": self.url, "type": self.type, "path": self.path}


@dataclass
class PourSpec:
    """Canonical spec for a single dataset pour.

    All fields after `source_id` and `name` have sensible defaults so a minimal
    spec can be written in 3 lines for a plain CSV download.
    """

    # --- Identity (required) ---
    source_id: str
    name: str

    # --- Acquisition ---
    download_url: str = ""        # direct URL to fetch (or human fallback if resolver set)
    url: str = ""                 # alternate field name (bridge_fuel uses 'url' for portal link)
    kind: str = "csv"
    loader: str = "bridge_fuel"   # which backend runs it

    # --- Publisher / metadata ---
    publisher: str = ""
    description: str = ""
    jurisdiction: str = ""
    category: str = ""
    subcategory: str = ""
    unit_of_observation: str = ""
    geographic_scope: str = ""
    access_method: str = "bulk"
    format: str = "csv"
    update_cadence: str = ""
    license_terms: str = ""
    accountability_relevance: str = ""
    priority_tier: str = "2"
    notes: str = ""

    # --- CSV/file options ---
    delimiter: str = ","
    encoding: str = "utf-8"
    has_header: bool = True
    member_pattern: str = ""      # for zip: regex to select the member file
    csv_opts: dict = field(default_factory=dict)

    # --- Scale control ---
    chunked: bool = False
    chunk_rows: int = 500_000

    # --- Key columns (what connects this to the graph) ---
    key_cols: list = field(default_factory=list)  # list of KeyCol or dicts
    join_keys: str = ""           # comma-separated canonical keys for SOURCE_REGISTRY

    # --- Resolver (rotating download links) ---
    resolver: dict | None = None

    # --- Optional extras ---
    provider_data_id: str = ""    # CMS provider-data dataset ID
    filter: Any = None            # row-filter callable applied before load
    smoke_referee: dict | None = None  # reconciliation config

    # --- Computed at validation time ---
    _effective_url: str = field(default="", init=False, repr=False)

    def __post_init__(self):
        self.source_id = self.source_id.upper()
        if not self.download_url and self.url:
            self._effective_url = self.url
        else:
            self._effective_url = self.download_url or self.url
        # Normalize key_cols to list of KeyCol
        self.key_cols = [
            KeyCol.from_dict(k) if isinstance(k, dict) else k
            for k in self.key_cols
        ]

    @property
    def effective_url(self) -> str:
        return self._effective_url

    @property
    def hosts(self) -> set[str]:
        """All hostnames this spec needs egress access to."""
        urls = set()
        if self._effective_url:
            urls.add(urlparse(self._effective_url).hostname)
        if self.resolver:
            r = self.resolver if isinstance(self.resolver, dict) else self.resolver.__dict__
            if r.get("url"):
                urls.add(urlparse(r["url"]).hostname)
        urls.discard(None)
        return urls

    @classmethod
    def from_dict(cls, d: dict) -> "PourSpec":
        """Construct from an existing spec dict (bridge_fuel_specs or server_side_specs format)."""
        # Handle the key_cols field which may use "as" (a reserved word in dataclass)
        kw = dict(d)
        # Don't pass unknown fields to __init__ — collect them and discard
        known = {f.name for f in cls.__dataclass_fields__.values()}
        extras = {k: v for k, v in kw.items() if k not in known}
        clean = {k: v for k, v in kw.items() if k in known}
        return cls(**clean)

    def to_registry_dict(self) -> dict:
        """Fields needed for SOURCE_REGISTRY upsert."""
        return {
            "source_id": self.source_id,
            "name": self.name,
            "publisher": self.publisher,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "unit_of_observation": self.unit_of_observation,
            "update_cadence": self.update_cadence,
            "join_keys": self.join_keys,
            "accountability_relevance": self.accountability_relevance,
            "priority_tier": self.priority_tier,
        }


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class SpecError(ValueError):
    """Raised when a spec fails validation."""


def validate_spec(spec: dict | PourSpec) -> PourSpec:
    """Validate and return a PourSpec. Raises SpecError on problems."""
    if isinstance(spec, dict):
        spec = PourSpec.from_dict(spec)

    errors = []

    if not spec.source_id:
        errors.append("source_id is required")
    if not spec.name:
        errors.append("name is required")
    if not spec.effective_url and not spec.resolver:
        errors.append("download_url (or url) or resolver is required")
    if spec.loader not in LOADERS:
        errors.append(f"loader must be one of {LOADERS}, got '{spec.loader}'")
    if spec.kind not in KINDS:
        errors.append(f"kind must be one of {KINDS}, got '{spec.kind}'")

    if errors:
        raise SpecError(f"Spec '{spec.source_id}': " + "; ".join(errors))

    return spec


def validate_specs(specs: list[dict]) -> list[PourSpec]:
    """Validate a list of spec dicts. Raises on first error."""
    return [validate_spec(s) for s in specs]


# ---------------------------------------------------------------------------
# Queue manifest
# ---------------------------------------------------------------------------

@dataclass
class QueueManifest:
    """A sprint-level batch of sources to pour."""
    sprint: str
    sources: list[str]           # source_ids in execution order
    spec_files: list[str] = field(default_factory=list)  # paths to spec modules
    created: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "QueueManifest":
        sources = []
        for entry in d.get("sources", []):
            if isinstance(entry, str):
                sources.append(entry)
            elif isinstance(entry, dict):
                sources.append(entry["source_id"])
        return cls(
            sprint=d.get("sprint", ""),
            sources=sources,
            spec_files=d.get("spec_files", []),
            created=d.get("created", ""),
            notes=d.get("notes", ""),
        )
