"""Shared HTTP server core — usable from both CLI and MCDR modes."""

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from resource_pack_server.config import RpsConfig
from resource_pack_server.hash_utils import sha1_file
from resource_pack_server.logger import get as get_logger
from resource_pack_server.pack_merger import PackMerger


class ResourcePackHandler(BaseHTTPRequestHandler):
    """Serves .zip files and a merged pack."""

    pack_dir: Path
    public_url: str
    merger: PackMerger

    def log_message(self, format: str, *args) -> None:
        get_logger().info(format % args)

    def _send_zip(self, data: bytes, name: str, sha1: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Disposition", f'attachment; filename="{name}"')
        self.send_header("X-Resource-Pack-SHA1", sha1)
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, title: str, body: str) -> None:
        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
<h1>{title}</h1>
{body}
<p><em>ResourcePackServer v0.1.0</em></p>
</body>
</html>"""
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.lstrip("/")

        if path == "merged.zip":
            return self._serve_merged()
        if path == "" or path == "index.html":
            return self._list_packs()
        if path.endswith(".zip"):
            return self._serve_pack(path)
        self.send_error(404, "Not Found")

    def _serve_merged(self) -> None:
        try:
            data, sha1 = self.merger.build()
        except Exception as e:
            self.send_error(500, f"Merge failed: {e}")
            return
        self._send_zip(data, "merged.zip", sha1)

    def _list_packs(self) -> None:
        rows: list[str] = []

        # Merged pack link (always shown if merge enabled)
        try:
            data, sha1 = self.merger.build()
            size_mb = len(data) / (1024 * 1024)
            rows.append(
                '<tr style="background:#e8f5e9">'
                '<td><b><a href="/merged.zip">merged.zip</a></b> '
                '<small>(all packs combined)</small></td>'
                f"<td>{size_mb:.1f} MB</td>"
                f"<td><code>{sha1}</code></td>"
                "</tr>"
            )
        except Exception:
            rows.append(
                '<tr><td colspan="3">Merge unavailable</td></tr>'
            )

        # Individual packs
        try:
            for entry in sorted(self.pack_dir.iterdir()):
                if entry.is_file() and entry.suffix.lower() == ".zip":
                    sha1 = sha1_file(entry)
                    size = entry.stat().st_size
                    size_mb = size / (1024 * 1024)
                    url = f"/{entry.name}"
                    rows.append(
                        f'<tr><td><a href="{url}">{entry.name}</a></td>'
                        f"<td>{size_mb:.1f} MB</td>"
                        f"<td><code>{sha1}</code></td></tr>"
                    )
        except FileNotFoundError:
            self.send_error(503, "Pack directory not found")
            return

        if not rows:
            body = "<p>No resource packs found.</p>"
        else:
            body = (
                "<table border='1' cellpadding='6' cellspacing='0'>"
                "<tr><th>File</th><th>Size</th><th>SHA1</th></tr>"
                + "".join(rows)
                + "</table>"
            )
        self._send_html("Resource Packs", body)

    def _serve_pack(self, path: str) -> None:
        safe_name = Path(path).name
        if safe_name != path or ".." in path:
            self.send_error(400, "Bad Request")
            return
        file_path = self.pack_dir / safe_name
        if not file_path.is_file():
            self.send_error(404, "Pack not found")
            return
        data = file_path.read_bytes()
        sha1 = sha1_file(file_path)
        self._send_zip(data, safe_name, sha1)


def _handler_factory(
    pack_dir: Path, public_url: str, merger: PackMerger
) -> type[ResourcePackHandler]:
    handler = type(
        "BoundHandler",
        (ResourcePackHandler,),
        {"pack_dir": pack_dir, "public_url": public_url, "merger": merger},
    )
    return handler


class ResourcePackHttpServer:
    def __init__(self, config: RpsConfig):
        self._config = config
        self._httpd: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.logger = get_logger()
        self.merger = PackMerger(config)

    @property
    def is_running(self) -> bool:
        return self._httpd is not None

    def start(self) -> None:
        cfg = self._config
        pack_dir = cfg.pack_path
        pack_dir.mkdir(parents=True, exist_ok=True)

        host = cfg.server.host
        port = cfg.server.port
        handler_cls = _handler_factory(pack_dir, cfg.server.public_url, self.merger)

        self._httpd = HTTPServer((host, port), handler_cls)
        self.logger.info(f"Resource pack server starting on {host}:{port}")
        self.logger.info(f"Serving packs from: {pack_dir}")

        # Pre-build merged pack
        self.merger.build()

        self._thread = threading.Thread(
            target=self._httpd.serve_forever,
            name="rps-http-server",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        if self._httpd is not None:
            self.logger.info("Shutting down resource pack server...")
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None
