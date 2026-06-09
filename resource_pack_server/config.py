from __future__ import annotations

import functools
from pathlib import Path
from typing import Optional

from mcdreforged.api.all import Serializable


class ServerConfig(Serializable):
    host: str = "0.0.0.0"
    port: int = 8080
    pack_dir: str = "./resource_packs"
    # Public URL prefix exposed to clients (e.g. "http://example.com:8080")
    # If empty, auto-detect from request
    public_url: str = ""


class CommandConfig(Serializable):
    enabled: bool = True
    prefix: str = "!!rps"
    permission_level: int = 1


class MergeConfig(Serializable):
    enabled: bool = True
    pack_priority: list[str] = []


class RpsConfig(Serializable):
    enabled: bool = True
    debug: bool = False
    server: ServerConfig = ServerConfig()
    command: CommandConfig = CommandConfig()
    merge: MergeConfig = MergeConfig()

    # --- Singleton ---

    @classmethod
    @functools.lru_cache
    def __get_default_instance(cls) -> RpsConfig:
        return RpsConfig.get_default()

    @classmethod
    def get(cls) -> RpsConfig:
        if _config is not None:
            return _config
        return cls.__get_default_instance()

    # --- Derived paths ---

    @property
    def pack_path(self) -> Path:
        return Path(self.server.pack_dir).resolve()


_config: Optional[RpsConfig] = None


def set_config_instance(cfg: RpsConfig) -> None:
    global _config
    _config = cfg
