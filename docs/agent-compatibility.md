# Agent 适配与验证状态

本页对应 Plog v0.1.0-alpha.6 及当前 main 的验证状态，不代表旧版 alpha.3 的能力。保留 `plog` 技能 ID 与版本记录格式，旧作品仍可查看和恢复。

## 安装与运行

同一运行包使用标准 name/description frontmatter，无宿主专属必需工具声明。安装器提供以下选项；非默认配置、项目级路径和远程容器用 `--target` 指定实际技能目录。

| Agent | 安装选项 | 默认目录 | 图像执行路径 |
| --- | --- | --- | --- |
| OpenClaw | `--agent openclaw` | `~/.openclaw/skills/plog` | 当前视觉工具 + 支持编辑的 `image_generate`；也可用兼容 API。 |
| Hermes | `--agent hermes` | `~/.hermes/skills/plog` | `vision_analyze` + 支持编辑的 `image_generate`；也可用兼容 API。 |
| Claude Code | `--agent claude-code` | `~/.claude/skills/plog` | 当前模型看图 + 已配置的图片 MCP／CLI／兼容 API。 |
| DeepSeek Harness | `--agent deepseek-harness` | `~/.dsh/skills/plog` | 视觉／编辑插件或兼容 API；文本模型需独立视觉分析。 |
| Codex | `--agent codex` | `~/.agents/skills/plog` | 可用的原生图片工具或兼容 API。 |
| 其他 Agent | `--agent generic` 或 `--target` | `~/.agents/skills/plog` | 同一能力契约；检查该宿主实际扫描目录。 |

安装器读取 `OPENCLAW_STATE_DIR`、`HERMES_HOME`、`CLAUDE_CONFIG_DIR`、`DSH_HOME` 的显式配置。它只安装用户指定的一处，不擅自安装 Agent、插件或修改认证。宿主在另一台机器／沙箱运行时，在那个环境安装并准备 Python；Windows 可在 WSL 中运行本地文件工具，原生 Windows 未适配。

运行前读 [接入契约](../plog/references/agents.md)。原生工具可满足全部能力时不需要兼容 API。兼容 API 是可执行的协议适配器，需要用户选定支持相应端点的服务和模型；不会将 DeepSeek 聊天模型当作图像编辑模型。

## 证据分层

- **静态适配**：技能结构、官方发现目录、运行提示、工具选择与交付方式。
- **确定性检查**：安装／升级／卸载、API 请求格式、配置缺失、外发开关、错误与超时、原图保护、无人物图片文件处理和版本恢复。
- **宿主实测**：真实 Agent 发现技能并执行完整创作、修改、恢复和附件交付。必须记录 Agent 版本、模型、图像服务、候选包及场景，逐环境验证。

2026-09-08 已在 Codex 桌面会话中，用原生 OpenAI 图片工具完成一个早餐合成样例的匿名干净安装、真实出图、仅改文字、旧版恢复与 PNG 交付，见 [实测记录](codex-native-smoke-2026-09-08.md)。这次显式读取了安装后的技能，但沿用已有会话，未验证新会话自动发现技能。其他宿主的真实图像链路，以及所有组合的完整 Plog 矩阵仍待实测。

Codex 的 alpha.1–3 历史测试不能作为本次 Plog 版的通过证明。不能把单样例检查、本地服务替身或 doctor 的 `configured_not_tested` 改写成完整兼容性认证。

当前 Plog 验收使用 `evaluation.py init --suite plog`，覆盖山海、街景、食物静物、宠物、人物、密集人群和组图中的单张。每个 Agent／provider 组合分别记录；安装渠道不是模型供应商，也不是同一测试环境。

本轮本地检查和开发包校验值见 [开发检查记录](plog-development.md)。

## 官方依据

核对日期：2026-09-07。这里记录文档接口，实际会话工具 schema 优先。

- [OpenClaw Skill 目录](https://docs.openclaw.ai/tools/skills) 与 [图片生成／编辑](https://docs.openclaw.ai/tools/image-generation)。
- [Hermes Skill 系统](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) 与 [图像编辑](https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation)。
- [Claude Code Skills](https://code.claude.com/docs/en/skills)。
- [DeepSeek Harness Skills](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)。
- 兼容 API 的 [图片编辑契约](https://developers.openai.com/api/reference/resources/images) 与 [视觉消息格式](https://developers.openai.com/api/docs/guides/images-vision)。供应商宣称兼容不证明每个模型都支持这些端点。
