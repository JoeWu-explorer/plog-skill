# 安装、更新与卸载

[返回首页](../README.md) · [Agent 适配](agent-compatibility.md) · [使用指南](guide.md)

**当前预发布：[v0.1.0-alpha.5](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.5)。** npx 安装 main 分支源码；需要固定版本可下载该 Release 的 ZIP 与 `SHA256SUMS`。仓库当前为私有，需要仓库访问权限和可供 Git 使用的认证。

## 推荐：npx 安装

需要 Node.js/npm。在你希望使用技能的项目目录执行，按 CLI 提示选择 Agent：

```sh
npx skills add https://github.com/JoeWu-explorer/photo-dialogue --skill photo-dialogue
```

也可以把这段话交给 Agent：

```text
请运行 npx skills add https://github.com/JoeWu-explorer/photo-dialogue --skill photo-dialogue 安装「照片有话说」。
安装后读取 SKILL.md，在独立环境准备必要依赖并自检，检查读图与图片编辑工具是否可用。
```

CLI 安装技能文件；Python 依赖与图像服务由 Agent 按 `SKILL.md` 及其引用文档检查。已有本地修改先保留，已有安装沿用原管理器更新。准备好后，按宿主要求刷新技能或新开会话，上传照片即可开始。

## 使用 Skills CLI

上面的命令采用 CLI 默认的安装范围和方式。需要明确指定时，例如安装独立副本到当前项目的 Claude Code 目录：

```sh
npx skills add https://github.com/JoeWu-explorer/photo-dialogue --skill photo-dialogue --agent claude-code --copy
```

- 想装到用户范围可加 `--global`；其他宿主先用 `npx skills add --help` 核对 CLI 支持的 Agent 名称。尚未列出的宿主可用下方完整包安装器。
- `--copy` 安装独立副本。已有同名技能时先保留本地修改，再决定更新方式。
- 手动准备运行环境时，接着看 [准备 Python 环境](#准备-python-环境) 和 [检查图像能力](#检查图像能力)。

仓库 URL 与本地目录均为 [Skills CLI 支持的来源](https://github.com/vercel-labs/skills#supported-sources)。已验证远端技能发现，以及临时项目中的 Claude Code 目录复制安装、19 个技能文件内容一致和本地自检；这不等于完成了真实 Agent 图片创作验证。

试用自己的本地改动时，在源码根目录将命令中的仓库 URL 换成 `./photo-dialogue`。GitHub 安装只包含已推送的内容。

## 手动安装完整包

需要 macOS/Linux（Windows 可用 WSL）及 CPython 3.11–3.13。以下使用 `python3.13`，也可统一换成已有合格版本。该方式不依赖 Node.js。

先取得源码（已有检出目录时使用它）：

```sh
git clone --branch v0.1.0-alpha.5 https://github.com/JoeWu-explorer/photo-dialogue.git
cd photo-dialogue
```

使用 Release 附件时，先在下载目录运行 `shasum -a 256 -c SHA256SUMS`（Linux 可用 `sha256sum -c SHA256SUMS`），再用该版本源码的安装器安装：

```sh
python3.13 scripts/distribution.py install '/下载目录/photo-dialogue-v0.1.0-alpha.5.zip' --agent hermes
```

也可自行构建。在源码根目录运行；每次使用新的临时构建目录，避免同名 ZIP 已存在导致构建失败：

```sh
PD_BUILD_DIR="$(mktemp -d)"
python3.13 scripts/distribution.py build "$PD_BUILD_DIR/photo-dialogue-plog.zip"
python3.13 scripts/distribution.py install "$PD_BUILD_DIR/photo-dialogue-plog.zip" --agent hermes
```

将 `hermes` 换成你使用的宿主：

| 宿主 | 安装选项 |
| --- | --- |
| OpenClaw | `--agent openclaw` |
| Hermes | `--agent hermes` |
| Claude Code | `--agent claude-code` |
| DeepSeek Harness | `--agent deepseek-harness` |
| Codex | `--agent codex` |
| 其他 Agent | `--target '/实际技能根目录/photo-dialogue'` |

`--target` 不能与 `--agent` 同时使用。默认目录、环境变量和通用目录选项见 [适配表](agent-compatibility.md)。已有安装用 [更新步骤](#更新与卸载)，不要直接覆盖。

## 准备 Python 环境

无论选择哪种安装方式，只需为技能准备一次独立环境。将 `PD_SKILL` 替换成安装结果中**包含 SKILL.md 的绝对目录**：

```sh
PD_SKILL='/实际安装目录/photo-dialogue'
python3.13 -m venv ~/.local/share/photo-dialogue/venv
PD_PYTHON="$HOME/.local/share/photo-dialogue/venv/bin/python"
"$PD_PYTHON" -m pip install --require-hashes -r "$PD_SKILL/requirements.lock"
mkdir -p ~/Pictures/PhotoDialogue
"$PD_PYTHON" "$PD_SKILL/scripts/self_check.py" --workspace ~/Pictures/PhotoDialogue
```

将 `PD_SKILL` 和 `PD_PYTHON` 的实际路径告诉 Agent，后续运行沿用这个解释器。远程 Agent 要在它实际执行代码的环境里安装；本机 Python 就绪不代表远程容器已就绪。

只有完整的技能目录才能工作，单独复制 `SKILL.md` 会缺少脚本与参考文件。自检不联网、不生成图片，也不能替代真实图片服务测试。

### 可选：读取 HEIC/HEIF

需要处理手机 HEIC/HEIF 照片时，在同一环境中运行：

```sh
"$PD_PYTHON" -m pip install --require-hashes -r "$PD_SKILL/requirements-heif.lock"
"$PD_PYTHON" "$PD_SKILL/scripts/self_check.py" --workspace ~/Pictures/PhotoDialogue
```

未安装时使用 JPEG、PNG 或 WebP 即可。

## 检查图像能力

安装后可以把这句话发给 Agent：

```text
检查 photo-dialogue 是否已就绪：能否读图、以我的照片为输入编辑图片，
并把结果保存和交付给我？先检查现有工具与配置，不要发起图片生成。
```

优先使用 Agent 已有的视觉与图片编辑工具。缺少其中一项时，可以接入已有 MCP／CLI 或随包兼容 API，见 [图像接入说明](../photo-dialogue/references/agents.md)。普通聊天 API 不代表支持看图或图片编辑。

使用随包 API 适配器时，可额外执行：

```sh
"$PD_PYTHON" "$PD_SKILL/scripts/image_backend.py" doctor
```

`doctor` 只做离线配置检查。`configured_not_tested` 表示配置完整但尚未验证服务；使用原生图片工具时无需为它另外配置 API。

密钥留在宿主环境或密钥管理器中，不写进技能或作品记录。模型、额度和费用由所选服务决定；第一次实际创作前，Agent 会核对接收照片的服务与已有授权。

## 更新与卸载

沿用最初的安装方式维护，同一份安装不要混用管理器。

### 使用本仓库安装器的安装

从新的源码构建新 ZIP，再使用原来的宿主选项或目标目录：

```sh
python3.13 scripts/distribution.py update '/实际新包.zip' --agent hermes
python3.13 scripts/distribution.py uninstall --target '/实际技能目录/photo-dialogue'
```

安装器能识别原 alpha.1／alpha.2／alpha.3 清单并更新。发现本地修改或未知文件时停止覆盖，保留后人工处理。更新后按新 lock 检查依赖并自检。

### 使用 Skills CLI 或其他管理器的安装

通过原管理器更新／移除。当前 `--copy` 本地源码安装不会自动跟随源码变化：先保留本地修改，确认新源码，再用相同来源、Agent 与安装范围重新安装；刷新后重新自检。远端源安装的维护命令见 [Skills CLI 文档](https://github.com/vercel-labs/skills#available-commands)。

没有本仓库安装器清单的目录不能用 `distribution.py update/uninstall` 接管，也不能伪造清单绕过保护。卸载技能时保留独立的作品目录、原图和专用 Python 环境。
