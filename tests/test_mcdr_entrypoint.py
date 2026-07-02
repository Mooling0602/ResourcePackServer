import unittest
from unittest.mock import patch

from resource_pack_server.config import RpsConfig
from resource_pack_server.mcdr import mcdr_entrypoint


class _Logger:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.infos: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def info(self, message: str) -> None:
        self.infos.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


class _Server:
    def __init__(self, config: RpsConfig) -> None:
        self.config = config
        self.logger = _Logger()
        self.commands: list[object] = []
        self.help_messages: list[tuple[str, object]] = []

    def load_config_simple(self, **kwargs) -> RpsConfig:
        return self.config

    def save_config_simple(self, config: RpsConfig) -> None:
        self.config = config

    def register_command(self, command: object) -> None:
        self.commands.append(command)

    def register_help_message(self, prefix: str, message: object) -> None:
        self.help_messages.append((prefix, message))

    def reload_plugin(self, plugin_id: str) -> None:
        pass


class McdrEntrypointTest(unittest.TestCase):
    def test_mcdr_on_load_records_http_startup_error(self) -> None:
        config = RpsConfig.get_default()
        server = _Server(config)

        class _FailingHttpServer:
            def __init__(self, config: RpsConfig) -> None:
                self.config = config

            def start(self) -> None:
                raise OSError("address already in use")

        with patch.object(
            mcdr_entrypoint, "ResourcePackHttpServer", _FailingHttpServer
        ):
            mcdr_entrypoint.on_load(server, None)

        self.assertEqual(mcdr_entrypoint._startup_error, "address already in use")
        self.assertIsNone(mcdr_entrypoint._http_server)
        self.assertTrue(server.commands)


if __name__ == "__main__":
    unittest.main()
