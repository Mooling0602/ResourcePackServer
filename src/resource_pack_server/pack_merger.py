"""Merge multiple Minecraft resource packs into a single zip.

Strategy:
  - List packs in priority order (config-driven or alphabetical).
  - Later packs override earlier ones on file-level within assets/.
  - pack.mcmeta: use the highest-priority pack's mcmeta; append descriptions
    from lower-priority packs into the description field.
  - pack.png: use the highest-priority pack that has one.
  - Result cached to memory; regenerated when any source fingerprint changes.
"""

import io
import json
import threading
import zipfile
from pathlib import Path

from resource_pack_server.config import RpsConfig
from resource_pack_server.hash_utils import sha1_hex
from resource_pack_server.logger import get as get_logger

PackFingerprint = tuple[int, int]


def _pack_fingerprint(path: Path) -> PackFingerprint:
    stat = path.stat()
    return stat.st_mtime_ns, stat.st_size


def _list_packs(pack_dir: Path) -> list[Path]:
    """Return sorted list of .zip pack files in pack_dir."""
    packs = sorted(
        p for p in pack_dir.iterdir() if p.is_file() and p.suffix.lower() == ".zip"
    )
    return packs


def _apply_priority(packs: list[Path], priority_names: list[str]) -> list[Path]:
    """Reorder packs so those in priority_names come first (in that order),
    then any remaining packs alphabetically. Lower index = higher priority."""
    name_to_path = {p.name: p for p in packs}
    result: list[Path] = []
    seen: set[str] = set()

    for name in priority_names:
        if name in name_to_path:
            result.append(name_to_path[name])
            seen.add(name)

    # Append remaining in alphabetical order
    for p in packs:
        if p.name not in seen:
            result.append(p)

    return result


def _read_zip_manifest(zf: zipfile.ZipFile) -> dict[str, bytes]:
    """Read entire zip into a dict of {filename: bytes}."""
    return {info.filename: zf.read(info) for info in zf.infolist() if not info.is_dir()}


def _merge_pack_mcmeta(manifests: list[dict[str, bytes]]) -> bytes:
    """Merge pack.mcmeta: take highest-priority mcmeta as base, append
    descriptions from lower-priority packs."""
    base: dict | None = None
    descriptions: list[str] = []

    for manifest in manifests:
        if "pack.mcmeta" in manifest:
            try:
                meta = json.loads(manifest["pack.mcmeta"].decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            if base is None:
                base = meta
            pack_section = meta.get("pack", {})
            desc = pack_section.get("description", "")
            if isinstance(desc, str) and desc.strip():
                descriptions.append(desc.strip())

    if base is None:
        base = {
            "pack": {
                "pack_format": 9999,
                "description": "Merged Resource Pack",
                "supported_formats": [0, 9999],
                "min_format": 0,
                "max_format": 9999,
            }
        }

    if descriptions:
        combined = " | ".join(descriptions)
        base.setdefault("pack", {})["description"] = combined

    return json.dumps(base, indent=2, ensure_ascii=False).encode("utf-8")


def _merge_pack_png(manifests: list[dict[str, bytes]]) -> bytes | None:
    """Return the first pack.png found, from highest priority to lowest."""
    for manifest in manifests:
        if "pack.png" in manifest:
            return manifest["pack.png"]
    return None


class PackMerger:
    """Thread-safe, cached pack merger."""

    def __init__(self, config: RpsConfig):
        self._config = config
        self._lock = threading.Lock()
        self._cache: tuple[bytes, str] | None = None  # (zip_data, sha1)
        self._cache_fingerprints: dict[str, PackFingerprint] = {}
        self.logger = get_logger()

    def _needs_rebuild(self, packs: list[Path]) -> bool:
        """Check if any pack fingerprint has changed since last build."""
        for p in packs:
            try:
                fingerprint = _pack_fingerprint(p)
            except FileNotFoundError:
                return True
            if p.name not in self._cache_fingerprints:
                return True
            if fingerprint != self._cache_fingerprints[p.name]:
                return True
        # Also check if packs were added/removed
        return set(self._cache_fingerprints.keys()) != {p.name for p in packs}

    def build(self, force: bool = False) -> tuple[bytes, str]:
        """Return (merged_zip_bytes, sha1_hex). Cached unless force=True
        or source packs changed."""
        pack_dir = self._config.pack_path
        packs = _list_packs(pack_dir)

        if not packs:
            # No packs — return minimal valid zip
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                meta = json.dumps(
                    {
                        "pack": {
                            "pack_format": 9999,
                            "description": "No packs loaded",
                            "supported_formats": [0, 9999],
                            "min_format": 0,
                            "max_format": 9999,
                        }
                    },
                    indent=2,
                ).encode("utf-8")
                zf.writestr("pack.mcmeta", meta)
            data = buf.getvalue()
            return data, sha1_hex(data)

        # Apply priority ordering
        priority = self._config.merge.pack_priority
        packs = _apply_priority(packs, priority)

        # Check cache
        with self._lock:
            if not force and not self._needs_rebuild(packs) and self._cache is not None:
                return self._cache

            self.logger.info(
                f"Rebuilding merged pack from {len(packs)} packs: "
                f"{[p.name for p in packs]}"
            )

            # Read all manifests
            manifests: list[dict[str, bytes]] = []
            for p in packs:
                try:
                    with zipfile.ZipFile(p, "r") as zf:
                        manifests.append(_read_zip_manifest(zf))
                except (zipfile.BadZipFile, OSError, KeyError) as e:
                    self.logger.warning(f"Skipping {p.name}: {e}")
                    continue

            if not manifests:
                self.logger.warning("All packs failed to read, returning empty pack")
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                    meta = json.dumps(
                        {
                            "pack": {
                                "pack_format": 9999,
                                "description": "No valid packs",
                                "supported_formats": [0, 9999],
                                "min_format": 0,
                                "max_format": 9999,
                            }
                        },
                        indent=2,
                    ).encode("utf-8")
                    zf.writestr("pack.mcmeta", meta)
                data = buf.getvalue()
                sha1 = sha1_hex(data)
                self._cache = (data, sha1)
                self._cache_fingerprints = {}
                return data, sha1

            # Merge: lower index = higher priority
            # We iterate from lowest priority to highest, overwriting
            merged: dict[str, bytes] = {}

            # Lowest priority first
            for manifest in reversed(manifests):
                for filename, content in manifest.items():
                    merged[filename] = content

            # Now apply special merge for pack.mcmeta and pack.png
            merged["pack.mcmeta"] = _merge_pack_mcmeta(manifests)
            png = _merge_pack_png(manifests)
            if png is not None:
                merged["pack.png"] = png

            # Write merged zip
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for filename, content in sorted(merged.items()):
                    zf.writestr(filename, content)

            data = buf.getvalue()
            sha1 = sha1_hex(data)

            # Update cache
            self._cache_fingerprints = {p.name: _pack_fingerprint(p) for p in packs}
            self._cache = (data, sha1)

            self.logger.info(
                f"Merged pack built: {len(data) / (1024 * 1024):.1f} MB, SHA1={sha1}"
            )
            return data, sha1

    def invalidate(self) -> None:
        """Force next build() to regenerate."""
        with self._lock:
            self._cache_fingerprints.clear()
