"""MCDReforged plugin hooks — on_load / on_unload / commands."""

import zipfile
from typing import Any

from mcdreforged.api.all import (
    CommandSource,
    Literal,
    PluginServerInterface,
    RColor,
    RText,
    RTextBase,
)

from resource_pack_server import constants
from resource_pack_server.config import RpsConfig, set_config_instance
from resource_pack_server.hash_utils import sha1_file
from resource_pack_server.logger import get as get_logger
from resource_pack_server.server import ResourcePackHttpServer

_http_server: ResourcePackHttpServer | None = None
_config: RpsConfig | None = None


def _reply(source: CommandSource, msg: str | RTextBase) -> None:
    prefix = RText("[RPS] ", RColor.gold)
    if isinstance(msg, str):
        msg = RText(msg)
    source.reply(RTextBase.join("", [prefix, msg]))


# --- MCDR Hooks ---


def on_load(server: PluginServerInterface, old):
    global _config, _http_server
    logger = get_logger()

    try:
        config = server.load_config_simple(
            target_class=RpsConfig,
            failure_policy="raise",
        )
    except (OSError, ValueError, TypeError):
        config = RpsConfig.get_default()
        server.save_config_simple(config)
        logger.info("Created default config file")

    assert isinstance(config, RpsConfig)
    _config = config
    set_config_instance(_config)

    if not _config.enabled:
        logger.warning("ResourcePackServer is disabled in config")
        return

    # Register commands
    prefix = _config.command.prefix

    def _cmd_list(source: CommandSource):
        try:
            packs: list[dict[str, Any]] = []
            for entry in sorted(_config.pack_path.iterdir()):
                if entry.is_file() and entry.suffix.lower() == ".zip":
                    packs.append(
                        {
                            "name": entry.name,
                            "size_mb": round(entry.stat().st_size / (1024 * 1024), 1),
                            "sha1": sha1_file(entry),
                        }
                    )
            if packs:
                lines = [
                    f"{p['name']} ({p['size_mb']} MB, {p['sha1'][:8]}…)" for p in packs
                ]
                _reply(source, "\n".join(lines))
            else:
                _reply(source, "No resource packs found.")
        except (OSError, ValueError) as e:
            _reply(source, f"Error listing packs: {e}")

    def _cmd_reload(source: CommandSource):
        server.reload_plugin(constants.PLUGIN_ID)
        _reply(source, "Plugin reloaded.")

    def _cmd_status(source: CommandSource):
        if _http_server is not None and _http_server.is_running:
            cfg = _config.server
            lines = [
                f"Server running on {cfg.host}:{cfg.port}",
                f"Pack dir: {cfg.pack_dir}",
            ]
            if _config.merge.enabled:
                try:
                    data, sha1 = _http_server.merger.build()
                    size_mb = len(data) / (1024 * 1024)
                    lines.append(f"Merged pack: {size_mb:.1f} MB, SHA1={sha1}")
                    if _config.merge.pack_priority:
                        lines.append(
                            f"Priority: {', '.join(_config.merge.pack_priority)}"
                        )
                except (OSError, zipfile.BadZipFile, ValueError) as e:
                    lines.append(f"Merge error: {e}")
            else:
                lines.append("Merge: disabled")
            _reply(source, "\n".join(lines))
        else:
            _reply(source, "Server not running.")

    def _cmd_merge_rebuild(source: CommandSource):
        if _http_server is None:
            _reply(source, "Server not running.")
            return
        try:
            data, sha1 = _http_server.merger.build(force=True)
            size_mb = len(data) / (1024 * 1024)
            _reply(source, f"Merged pack rebuilt: {size_mb:.1f} MB, SHA1={sha1}")
        except (OSError, zipfile.BadZipFile, ValueError) as e:
            _reply(source, f"Merge rebuild failed: {e}")

    def _cmd_help(source: CommandSource):
        _reply(
            source,
            f"{prefix} list          - List available packs\n"
            f"{prefix} status        - Show server status\n"
            f"{prefix} merge rebuild - Force rebuild merged pack\n"
            f"{prefix} reload        - Reload plugin\n"
            f"{prefix} help          - Show this help",
        )

    server.register_command(
        Literal(prefix)
        .runs(
            lambda src: _reply(
                src,
                f"ResourcePackServer v{constants.PLUGIN_VERSION}. Use {prefix} help",
            )
        )
        .then(Literal("list").runs(_cmd_list))
        .then(Literal("reload").runs(_cmd_reload))
        .then(Literal("status").runs(_cmd_status))
        .then(Literal("help").runs(_cmd_help))
        .then(Literal("merge").then(Literal("rebuild").runs(_cmd_merge_rebuild)))
    )

    server.register_help_message(
        prefix,
        RText("Resource Pack Server", RColor.gold).h("Manage and serve resource packs"),
    )

    _http_server = ResourcePackHttpServer(_config)
    _http_server.start()

    logger.info("ResourcePackServer MCDR plugin loaded")


def on_unload(server: PluginServerInterface):
    global _http_server
    if _http_server is not None:
        _http_server.stop()
        _http_server = None
    get_logger().info("ResourcePackServer unloaded")
