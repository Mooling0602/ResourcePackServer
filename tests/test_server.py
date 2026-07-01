import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from resource_pack_server.config import RpsConfig
from resource_pack_server.server import ResourcePackHttpServer


def _make_config(pack_dir: Path, *, merge_enabled: bool) -> RpsConfig:
    config = RpsConfig.get_default()
    config.server.host = "127.0.0.1"
    config.server.port = 0
    config.server.pack_dir = str(pack_dir)
    config.server.public_url = "https://packs.example.test/base"
    config.merge.enabled = merge_enabled
    return config


def _write_pack(path: Path) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "pack.mcmeta",
            '{"pack":{"pack_format":15,"description":"test pack"}}',
        )


def test_merged_endpoint_is_not_served_when_merge_is_disabled() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pack_dir = Path(tmp)
        _write_pack(pack_dir / "one.zip")
        server = ResourcePackHttpServer(_make_config(pack_dir, merge_enabled=False))
        try:
            server.start()
            assert server.port is not None
            url = f"http://127.0.0.1:{server.port}/merged.zip"

            try:
                urllib.request.urlopen(url, timeout=5)
            except urllib.error.HTTPError as exc:
                assert exc.code == 404
            else:
                raise AssertionError("/merged.zip should be disabled")
        finally:
            server.stop()


def test_index_uses_public_url_and_hides_merged_when_disabled() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pack_dir = Path(tmp)
        _write_pack(pack_dir / "one.zip")
        server = ResourcePackHttpServer(_make_config(pack_dir, merge_enabled=False))
        try:
            server.start()
            assert server.port is not None
            url = f"http://127.0.0.1:{server.port}/"
            with urllib.request.urlopen(url, timeout=5) as response:
                body = response.read().decode("utf-8")

            assert "merged.zip" not in body
            assert "https://packs.example.test/base/one.zip" in body
        finally:
            server.stop()
