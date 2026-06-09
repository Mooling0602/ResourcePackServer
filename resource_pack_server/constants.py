import uuid

PLUGIN_ID = "resource_pack_server"
PLUGIN_VERSION = "0.1.0"
INSTANCE_ID = uuid.uuid4().hex[:4]

DEFAULT_PORT = 8080
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PACK_DIR = "./resource_packs"
DEFAULT_COMMAND_PREFIX = "!!rps"

MCDR_COMMAND_PERMISSION_LEVEL = 1
