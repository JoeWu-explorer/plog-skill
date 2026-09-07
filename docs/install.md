# 安装、更新与卸载

[返回首页](../README.md) · [安装后的使用方法](guide.md)

## 让 Codex 帮你安装

适合不想手动运行命令的用户。将下面这段发给能访问本仓库的 Codex：

> 请帮我安装「照片有话说」的 v0.1.0-alpha.3。仓库是 JoeWu-explorer/photo-dialogue；使用该版本的安装包，核对 SHA256SUMS，检查 Python 和本地依赖，在独立环境安装并自检。这次允许下载版本文件和依赖。已有安装或本地修改时请先检查并保留。

仓库目前私有，需要仓库访问权限。这段话授权安装所需下载，**不授权外发你的照片**；做图时另按当前照片与用途确认。

## 手动安装

需要 Codex 的看图与内置图像生成能力，以及已安装的 CPython 3.11–3.13。已验证环境详情见 [版本与验收](README.md#版本与验收)。

1. 从 [v0.1.0-alpha.3](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.3) 下载 `photo-dialogue-v0.1.0-alpha.3.zip`、`SHA256SUMS`，以及同一标签的源码归档。
2. 在下载目录核对 ZIP 的 SHA-256：macOS 用 `shasum -a 256 -c SHA256SUMS`，Linux 用 `sha256sum -c SHA256SUMS`。通过后继续。
3. 解压源码归档，在解压后的仓库根目录运行以下命令。将第一行的 ZIP 路径替换为实际下载路径；下例统一使用 `python3.13`，也可统一改用已安装的合格版本。

```sh
python3.13 scripts/distribution.py install '/实际下载路径/photo-dialogue-v0.1.0-alpha.3.zip'
python3.13 -m venv ~/.local/share/photo-dialogue/venv
~/.local/share/photo-dialogue/venv/bin/python -m pip install --require-hashes -r ~/.agents/skills/photo-dialogue/requirements.lock
mkdir -p ~/Pictures/PhotoDialogue
~/.local/share/photo-dialogue/venv/bin/python ~/.agents/skills/photo-dialogue/scripts/self_check.py --workspace ~/Pictures/PhotoDialogue
```

默认安装到 `~/.agents/skills/photo-dialogue`。已有目录或本地修改会阻止覆盖，请先查看提示；不要通过删目录来绕过保护。已有专用 Python 环境时沿用合格解释器，不必重复创建。

自检通过表示本地读写和格式能力可用，不代表已验证图像服务权限。新开 Codex 对话，输入 `$photo-dialogue`；后续处理应使用上面的专用环境解释器，可将该路径告诉 Codex。

## 可选：读取 HEIC/HEIF

JPEG、PNG、WebP 不需要这一步。需要 HEIF 时，在同一环境安装并重新自检：

```sh
~/.local/share/photo-dialogue/venv/bin/python -m pip install --require-hashes -r ~/.agents/skills/photo-dialogue/requirements-heif.lock
~/.local/share/photo-dialogue/venv/bin/python ~/.agents/skills/photo-dialogue/scripts/self_check.py --workspace ~/Pictures/PhotoDialogue
```

## 更新与卸载

使用对应版本源码中的安装器，在源码根目录运行；把示例路径替换为实际路径：

```sh
python3.13 scripts/distribution.py update '/实际下载路径/新版本.zip'
python3.13 scripts/distribution.py uninstall --target ~/.agents/skills/photo-dialogue
```

更新前先校验新包；更新后在同一专用环境按新 lock 安装依赖并自检。安装器会保护已修改或未知的本地文件，不提供强制覆盖开关。

卸载只处理指定技能，不删除独立保存的作品及历史版本。专用 Python 环境也不会随技能卸载自动删除。
