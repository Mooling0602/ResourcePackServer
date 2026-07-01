# Repository Guidelines

## Project Structure & Module Organization

Python 3.12+ Minecraft resource pack server with two runtime modes: standalone HTTP server and MCDReforged plugin.

- `main.py` and `src/__main__.py` delegate to `resource_pack_server.__main__:main`.
- `src/resource_pack_server/` contains the package source.
- `src/resource_pack_server/server.py` is the shared HTTP server.
- `src/resource_pack_server/cli/` contains the standalone argparse entrypoint.
- `src/resource_pack_server/mcdr/` contains MCDReforged hooks and commands.
- `src/resource_pack_server/pack_merger.py` merges `.zip` packs by priority.
- `src/mcdreforged.plugin.json` is the MCDR manifest and packaging version source.
- `docs/` contains Sphinx documentation. Runtime test assets should stay under ignored local directories such as `resource_packs/`.

## Build, Test, and Development Commands

- `uv sync --all-groups` installs runtime, dev, and docs dependencies.
- `uv run python main.py --port 8080 --pack-dir ./resource_packs` runs standalone mode.
- `uv run python -m resource_pack_server` runs the package entrypoint.
- `python check.py` runs pytest, `ty check src`, `ruff check src`, and `ruff format --check src` when those tools are installed.
- To build the `.pyz`, copy `src/.` and `LICENSE` into `build/mcdr_pack/`, then run `uv run mcdreforged pack -i build/mcdr_pack -o ./dist --ignore-patterns "__pycache__" "*.pyc" "*.pyo" ".gitignore" --shebang "/usr/bin/env python3"`.
- `cd docs && uv run ./build_docs.sh` builds documentation.

## Coding Style & Naming Conventions

Use Ruff formatting and keep code type-check friendly for ty. Follow standard Python naming: modules and functions in `snake_case`, classes in `PascalCase`, constants in `UPPER_SNAKE_CASE`. Prefer explicit `Path` handling for filesystem operations and keep request-path validation in the HTTP layer. Avoid hidden global state unless it is required for MCDR integration and guarded clearly.

## Testing Guidelines

Add focused pytest coverage for bug fixes and run `python check.py`. Manually verify the affected entrypoint with `uv run` when changing CLI or server startup behavior. Cover standalone and MCDR behavior when changing shared modules such as `server.py`, `config.py`, or `pack_merger.py`.

## Commit & Pull Request Guidelines

Recent history uses conventional prefixes such as `fix:`, `docs:`, and `release:`. Keep commits small and behavior-focused, for example `fix: honor merge disabled config`. Pull requests should describe the user-visible change, list verification commands, note MCDR compatibility risks, and link related issues when available.

## Configuration & Security Notes

Config classes use `mcdreforged.api.all.Serializable`, so changes must remain compatible with MCDR config loading. Do not commit resource packs, generated `.pyz` files, caches, virtual environments, or credentials. Be careful with `.zip` serving and merging paths; preserve traversal protections and SHA1 behavior because Minecraft clients rely on stable pack hashes.
