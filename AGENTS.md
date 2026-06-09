# Resource Pack Server

Python-based Minecraft resource pack server. Supports standalone HTTP mode and MCDReforged plugin mode.

## Project

- Stack: Python 3.14+, mcdreforged>=2.0.0
- Entry point: `main.py` → `resource_pack_server.__main__:main`
- Author: Mooling0602
- Manifest: `pyproject.toml`
- Dual-mode: standalone HTTP server + MCDReforged plugin

## Commands

- Run standalone: `uv run python main.py [--port 8080] [--pack-dir ./resource_packs]`
- Run as module: `uv run python -m resource_pack_server`
- Install deps: `uv sync`
- Test: none configured yet
- Lint: none configured (Ruff suggested by `.gitignore`)

## Architecture

- `main.py` — root entry, delegates to `resource_pack_server.__main__`
- `resource_pack_server/__main__.py` — detects MCDR vs standalone, routes to correct entrypoint
- `resource_pack_server/server.py` — HTTP server core (shared by both modes), serves .zip packs
- `resource_pack_server/config.py` — `RpsConfig` (Serializable), `ServerConfig`, `CommandConfig`
- `resource_pack_server/cli/cli_entrypoint.py` — standalone argparse CLI with signal handling
- `resource_pack_server/mcdr/mcdr_entrypoint.py` — MCDR plugin hooks (`on_load`/`on_unload`), `!!rps` commands
- `resource_pack_server/hash_utils.py` — SHA1 hashing for pack identification
- `resource_pack_server/logger.py` — dual-mode logger (MCDR logger vs stdlib)

## Conventions

- Python 3.14+ required (`requires-python = ">=3.14"`)
- Use `uv` for package management (lockfile gitignored)
- Ruff intended for linting/formatting
- Config uses mcdreforged `Serializable` class for both modes
- No secrets, no committed credentials

## Notes

<!-- Quick-add notes below this line -->
