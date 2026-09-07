# 文档导航

[返回产品首页](../README.md)

## 使用产品

- [使用指南](guide.md)：首次做图、修改、返回旧版、导出与排错。
- [安装指南](install.md)：安装、HEIF 支持、更新和卸载。

## 当前开发源码

Plog 与多 Agent 适配正在当前源码中开发，支持无人场景、日常物件和组图逐张处理；新增原生图像工具路由、兼容 API 与各宿主安装选项。参见 [适配与证据状态](agent-compatibility.md) 和 [本轮开发检查](plog-development.md)。此变更尚未发布，不能把下方 alpha.3 包当作通用 Plog 包。

## 版本与验收

**当前预发布：v0.1.0-alpha.3。** 首次确认与后续修改、失败、恢复等对话已统一为简短日常表达，保留已有交付、保存和逐图设计能力；完整视觉验收仍未通过，新版没有重跑完整视觉矩阵。

- [下载](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.3) · [当前固定包与验证范围](release.json) · [更新记录](../CHANGELOG.md)
- [本次发布说明](prerelease-alpha-3.md) · [对话表达](../photo-dialogue/references/conversation.md)
- [文字设计方向](typography-direction.md) · [引导与文档整理](onboarding-update.md) · [交付与保存修复](delivery-and-save-fixes.md)
- [验收标准](acceptance.md) · [公开前清单](release-checklist.md)
- [alpha.1 历史视觉验证](person-fidelity-fixes.md) · [历史固定包记录](candidate.json) · [生成限制诊断](generation-limit-diagnosis.md)

运行目标为 macOS/Linux 与 CPython 3.11–3.13，基础格式 JPEG/PNG/WebP，HEIF 可选。原包目标宿主实测 Codex 0.153.3；依赖版本与各批次证据以上述清单为准。Windows 和所有客户端兼容性未作承诺。新分支或本机开发安装不能沿用旧版视觉成绩宣称通过。

## 开发与维护

- [开发指南与仓库地图](../CONTRIBUTING.md)
- [文字表现力设计方向](typography-direction.md)
- [领域词汇](../CONTEXT.md) · [issue 与规格入口](agents/issue-tracker.md)
- [行为验收用例](../tests/cases.md) · [素材清单](assets.json)
- [历史记录](history/README.md) · [历史网页原型](../prototypes/README.md)

历史原型、工程检查通过和代理底线检查，都不能替代产品负责人的视觉审阅。
