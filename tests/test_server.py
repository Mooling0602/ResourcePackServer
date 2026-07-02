import tempfile
import unittest
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


class ResourcePackHttpServerTest(unittest.TestCase):
    def test_merged_endpoint_is_not_served_when_merge_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_dir = Path(tmp)
            _write_pack(pack_dir / "one.zip")
            server = ResourcePackHttpServer(_make_config(pack_dir, merge_enabled=False))
            try:
                server.start()
                self.assertIsNotNone(server.port)
                url = f"http://127.0.0.1:{server.port}/merged.zip"

                with self.assertRaises(urllib.error.HTTPError) as cm:
                    urllib.request.urlopen(url, timeout=5)
                self.assertEqual(cm.exception.code, 404)
            finally:
                server.stop()

    def test_index_uses_public_url_and_hides_merged_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_dir = Path(tmp)
            _write_pack(pack_dir / "one.zip")
            server = ResourcePackHttpServer(_make_config(pack_dir, merge_enabled=False))
            try:
                server.start()
                self.assertIsNotNone(server.port)
                url = f"http://127.0.0.1:{server.port}/"
                with urllib.request.urlopen(url, timeout=5) as response:
                    body = response.read().decode("utf-8")

                self.assertNotIn("merged.zip", body)
                self.assertIn("https://packs.example.test/base/one.zip", body)
            finally:
                server.stop()

    def test_can_download_pack_with_url_encoded_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_dir = Path(tmp)
            _write_pack(pack_dir / "pack with space.zip")
            server = ResourcePackHttpServer(_make_config(pack_dir, merge_enabled=False))
            try:
                server.start()
                self.assertIsNotNone(server.port)
                index_url = f"http://127.0.0.1:{server.port}/"
                with urllib.request.urlopen(index_url, timeout=5) as response:
                    body = response.read().decode("utf-8")

                self.assertIn("/pack%20with%20space.zip", body)

                pack_url = f"http://127.0.0.1:{server.port}/pack%20with%20space.zip"
                with urllib.request.urlopen(pack_url, timeout=5) as response:
                    data = response.read()

                self.assertGreater(len(data), 0)
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["Content-Type"], "application/zip")
            finally:
                server.stop()

    def test_can_download_pack_with_non_ascii_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_dir = Path(tmp)
            _write_pack(pack_dir / "中文.zip")
            server = ResourcePackHttpServer(_make_config(pack_dir, merge_enabled=False))
            try:
                server.start()
                self.assertIsNotNone(server.port)
                index_url = f"http://127.0.0.1:{server.port}/"
                with urllib.request.urlopen(index_url, timeout=5) as response:
                    body = response.read().decode("utf-8")

                self.assertIn("/%E4%B8%AD%E6%96%87.zip", body)

                pack_url = f"http://127.0.0.1:{server.port}/%E4%B8%AD%E6%96%87.zip"
                with urllib.request.urlopen(pack_url, timeout=5) as response:
                    data = response.read()
                    content_disposition = response.headers["Content-Disposition"]

                self.assertGreater(len(data), 0)
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["Content-Type"], "application/zip")
                self.assertIn(
                    "filename*=UTF-8''%E4%B8%AD%E6%96%87.zip", content_disposition
                )
            finally:
                server.stop()


if __name__ == "__main__":
    unittest.main()
