# Resource Pack Server

基于 Python 的 Minecraft 资源包服务器，同时支持以 MCDReforged 插件模式运行。

**[English](README.md)** | **中文**

## 文档

📖 **[https://docs.staringplanet.top/resource-pack-server](https://docs.staringplanet.top/resource-pack-server)**

## 安装

从 [GitHub Releases](https://github.com/Mooling0602/ResourcePackServer/releases) 下载最新的 `.pyz` 文件。

**独立模式：**

```bash
python ResourcePackServer-v0.1.0.pyz --port 8080 --pack-dir ./resource_packs
```

**MCDReforged 插件模式：**

将 `.pyz` 文件放入 MCDR 的 `plugins/` 目录中，插件将自动加载。

## 开发

代码由小米 MiMo-V2.5-Pro 生成。

## 许可证

[GPL-3.0](LICENSE)
