# 照片有话说 v0.1.0-alpha.4 · Plog

把人物、山海、街景和日常小事做成中文 Plog。单张记录一个瞬间，组图串起一天，每张独立保存版本；支持自然语言修改和从旧版继续。

## 快速开始

```sh
npx skills add https://github.com/JoeWu-explorer/photo-dialogue --skill photo-dialogue
```

安装后，在支持读图、图片编辑和本地脚本的 Agent 中发照片，说：“用 photo-dialogue 把这些照片做成一组中文 Plog，文字自然一点。”首次读取 SKILL.md，准备隔离依赖并自检。

npx 命令安装 main 分支源码。需要固定版本时，下载本页的 `photo-dialogue-v0.1.0-alpha.4.zip` 和 `SHA256SUMS`，按 [安装指南](https://github.com/JoeWu-explorer/photo-dialogue/blob/v0.1.0-alpha.4/docs/install.md) 核对、安装。仓库仍为私有，需要访问权限。

## 本次更新

- 场景扩展到山海、街景、食物、静物、宠物与人物，取消人数硬门槛，支持组图逐张叙事和版本维护。
- 为 OpenClaw、Hermes、Claude Code、DeepSeek Harness、Codex 提供安装与能力接入路径，新增可选图片编辑和视觉分析 API。
- 精简 README 快速开始为安装命令、使用示例和 Agent 代装口令。
- 安装器兼容 alpha.1–3 清单，继续保护本地修改、原图与历史版本。

## 验证与限制

56 项确定性测试、类型和仓库检查通过；发布包重复构建一致，全新安装、自检、卸载及真实 alpha.3 发布包升级检查通过。Skills CLI 远端发现、临时项目复制安装和本地自检通过。

本版未执行真实图片生成、各 Agent 的完整创作／修改／附件交付或 Plog 视觉矩阵。上述安装与脚本验证不代表所有 Agent 开箱即用，历史视觉成绩不移作新版通过证据。详见 [版本清单](https://github.com/JoeWu-explorer/photo-dialogue/blob/v0.1.0-alpha.4/docs/release.json)。

运行内容固定于 `46b8bb0bebee53a0254d64b44b31d87826511d46`；后续发布提交只更新文档。ZIP 共 22 个文件、73,311 字节，SHA-256：`52ce673156dc6b3dd7f24d9f6e223f17ec7b0487cc3fb8310caf2cfa43d9df90`。

附件仅含运行 ZIP 与校验文件，不含私人照片、作品或提示词。历史原型图片许可尚未清理，仓库保持私有；本次预发布不代表稳定版或公开素材验收完成。
