import json
from pathlib import Path

PLUGIN_ID = "resource_pack_server"

_plugin_json = Path(__file__).parent.parent / "mcdreforged.plugin.json"
PLUGIN_VERSION = json.loads(_plugin_json.read_text(encoding="utf-8"))["version"]

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
DEFAULT_PACK_DIR = "./resource_packs"
DEFAULT_COMMAND_PREFIX = "!!rps"

MCDR_COMMAND_PERMISSION_LEVEL = 1
