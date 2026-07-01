# Resource Pack Server

基于 Python 的 Minecraft 资源包服务器，同时支持以 MCDReforged 插件模式运行。

**[English](README.md)** | **中文**

## 文档

📖 **[https://docs.staringplanet.top/resource-pack-server](https://docs.staringplanet.top/resource-pack-server)**

## 安装

从 [GitHub Releases](https://github.com/Mooling0602/ResourcePackServer/releases) 下载最新的 `.pyz` 文件。

**独立模式：**

```bash
python ResourcePackServer-v0.1.2.pyz --port 8080 --pack-dir ./resource_packs
```

**MCDReforged 插件模式：**

将 `.pyz` 文件放入 MCDR 的 `plugins/` 目录中，插件将自动加载。

## 使用

将 `.zip` 资源包放入 `./resource_packs`，然后打开 `http://localhost:8080/` 查看下载地址和 SHA1。

```bash
uv run python main.py --port 8080 --pack-dir ./resource_packs
uv run python -m resource_pack_server --no-merge
uv run python -m resource_pack_server --priority base.zip addon.zip
```

默认会提供 `/merged.zip`，将多个资源包合并为一个资源包。使用 `--no-merge`，或在 MCDR 配置中将 `merge.enabled` 设为 `false`，即可只提供单独资源包。

## 开发

```bash
uv sync --all-groups
python check.py
mkdir -p build/mcdr_pack
cp -r src/. build/mcdr_pack/
cp LICENSE build/mcdr_pack/LICENSE
uv run mcdreforged pack -i build/mcdr_pack -o ./dist --ignore-patterns "__pycache__" "*.pyc" "*.pyo" ".gitignore" --shebang "/usr/bin/env python3"
```

`check.py` 会在工具已安装时运行 pytest、ty、Ruff lint 和 Ruff format 检查。

## 许可证

[GPL-3.0](LICENSE)
