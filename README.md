# Resource Pack Server

A python based Minecraft resource pack server, also supports running in MCDReforged.

**English** | **[中文](README_zh_CN.md)**

## Documentation

📖 **[https://docs.staringplanet.top/resource-pack-server](https://docs.staringplanet.top/resource-pack-server)**

## Installation

Download the latest `.pyz` file from [GitHub Releases](https://github.com/Mooling0602/ResourcePackServer/releases).

**Standalone mode:**

```bash
python ResourcePackServer-v0.1.1.pyz --port 8080 --pack-dir ./resource_packs
```

**MCDReforged plugin mode:**

Place the `.pyz` file into your MCDR `plugins/` directory. The plugin will auto-load.

## Usage

Place `.zip` resource packs in `./resource_packs`, then open `http://localhost:8080/` to view download URLs and SHA1 hashes.

```bash
uv run python main.py --port 8080 --pack-dir ./resource_packs
uv run python -m resource_pack_server --no-merge
uv run python -m resource_pack_server --priority base.zip addon.zip
```

By default, the server exposes `/merged.zip`, which combines all packs into a single resource pack. Use `--no-merge` or set `merge.enabled` to `false` in MCDR config to serve individual packs only.

## Develop

```bash
uv sync --all-groups
python check.py
mkdir -p build/mcdr_pack
cp -r src/. build/mcdr_pack/
cp LICENSE build/mcdr_pack/LICENSE
uv run mcdreforged pack -i build/mcdr_pack -o ./dist --ignore-patterns "__pycache__" "*.pyc" "*.pyo" ".gitignore" --shebang "/usr/bin/env python3"
```

`check.py` runs pytest, ty, Ruff linting, and Ruff format checks when the tools are installed.

## License

[GPL-3.0](LICENSE)
