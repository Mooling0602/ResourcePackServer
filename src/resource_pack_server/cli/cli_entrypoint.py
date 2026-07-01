"""Standalone CLI entrypoint using argparse."""

import argparse
import signal
import threading

from resource_pack_server import __version__
from resource_pack_server.config import RpsConfig, set_config_instance
from resource_pack_server.constants import (
    DEFAULT_HOST,
    DEFAULT_PACK_DIR,
    DEFAULT_PORT,
)
from resource_pack_server.logger import get as get_logger
from resource_pack_server.server import ResourcePackHttpServer


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"Resource Pack Server v{__version__}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="Bind address")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port")
    parser.add_argument(
        "--pack-dir",
        default=DEFAULT_PACK_DIR,
        help="Directory containing .zip resource packs",
    )
    parser.add_argument(
        "--public-url",
        default="",
        help="Public URL prefix",
    )
    parser.add_argument(
        "--merge",
        action=argparse.BooleanOptionalAction,
        default=True,
        dest="merge",
        help="Enable/disable merged pack (default: enabled)",
    )
    parser.add_argument(
        "--priority",
        nargs="*",
        default=[],
        metavar="PACK.zip",
        help="Pack priority order for merging (highest first)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    return parser


def cli_entry() -> None:
    parser = create_parser()

    args = parser.parse_args()

    if args.version:
        print(f"Resource Pack Server v{__version__}")
        return

    logger = get_logger()
    if args.debug:
        import logging

        logger.setLevel(logging.DEBUG)

    config = RpsConfig.get_default()
    config.server.host = args.host
    config.server.port = args.port
    config.server.pack_dir = args.pack_dir
    config.server.public_url = args.public_url
    config.merge.enabled = args.merge
    config.merge.pack_priority = args.priority
    config.debug = args.debug
    set_config_instance(config)

    server = ResourcePackHttpServer(config)
    shutdown_event = threading.Event()

    def _shutdown(signum, frame):
        logger.info("Received signal, shutting down...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    server.start()
    logger.info(
        f"Server running. Press Ctrl+C to stop. "
        f"Open http://{args.host}:{args.port}/ to browse packs."
        + (" Merged pack at /merged.zip." if args.merge else "")
    )

    shutdown_event.wait()
    server.stop()
