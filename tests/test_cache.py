import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from resource_pack_server.config import RpsConfig
from resource_pack_server.pack_merger import PackMerger
from resource_pack_server.server import ResourcePackHandler


def _make_config(pack_dir: Path) -> RpsConfig:
    config = RpsConfig.get_default()
    config.server.pack_dir = str(pack_dir)
    config.merge.enabled = True
    return config


def _write_pack(path: Path, description: str) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "pack.mcmeta",
            f'{{"pack":{{"pack_format":15,"description":"{description}"}}}}',
        )
        zf.writestr("assets/example/lang/en_us.json", f'{{"message":"{description}"}}')


class CacheFingerprintTest(unittest.TestCase):
    def test_sha1_cache_uses_file_size_in_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pack.zip"
            path.write_bytes(b"old")
            original_stat = path.stat()

            ResourcePackHandler._sha1_cache.clear()
            first_sha1 = ResourcePackHandler._cached_sha1(path)

            path.write_bytes(b"new content with different size")
            os.utime(path, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))

            second_sha1 = ResourcePackHandler._cached_sha1(path)

            self.assertNotEqual(second_sha1, first_sha1)

    def test_pack_merger_cache_uses_file_size_in_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_dir = Path(tmp)
            pack_path = pack_dir / "pack.zip"
            _write_pack(pack_path, "first")
            original_stat = pack_path.stat()

            merger = PackMerger(_make_config(pack_dir))
            first_data, first_sha1 = merger.build()

            _write_pack(pack_path, "second description with different size")
            os.utime(
                pack_path,
                ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns),
            )

            second_data, second_sha1 = merger.build()

            self.assertNotEqual(second_sha1, first_sha1)
            self.assertNotEqual(second_data, first_data)
            with zipfile.ZipFile(pack_path, "r") as zf:
                self.assertIn(
                    b"second description with different size",
                    zf.read("pack.mcmeta"),
                )


if __name__ == "__main__":
    unittest.main()
