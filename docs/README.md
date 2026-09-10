# 文档导航

[返回产品首页](../README.md)

## 使用产品

- [使用指南](guide.md)：首次做图、修改、返回旧版、导出与排错。
- [安装指南](install.md)：安装、HEIF 支持、更新和卸载。

## 版本与验收

**当前预发布：v0.1.0-alpha.7。** 新增可开合、翻页的 Plog 故事书与翻书动画导出；根据每册照片、故事和用户偏好独立设计装帧，保留单张 Plog 的修改与版本流程。

- [下载](https://github.com/JoeWu-explorer/plog-skill/releases/tag/v0.1.0-alpha.7) · [固定包与验证范围](release.json) · [更新记录](../CHANGELOG.md)
- [本次发布说明](prerelease-alpha-7.md) · [适配与证据状态](agent-compatibility.md) · [Plog 开发检查](plog-development.md)
- [Codex 原生图片工具单样例实测](codex-native-smoke-2026-09-08.md)：安装、出图、文字修改与旧版恢复。
- [验收标准](acceptance.md) · [发布检查](release-checklist.md)
- [alpha.4 发布说明](prerelease-alpha-4.md) · [alpha.3 发布说明](prerelease-alpha-3.md) · [alpha.1 历史视觉验证](person-fidelity-fixes.md) · [历史固定包记录](candidate.json)

运行目标为 macOS/Linux 与 CPython 3.11–3.13，基础格式 JPEG/PNG/WebP，HEIF 可选。58 项确定性测试及安装升级检查通过；Codex 原生图片工具已完成单样例手动链路实测，完整 Plog 场景视觉矩阵、新会话技能发现及真人评分仍待执行。旧版成绩不转移到本版本。

## 开发与维护

- [开发指南与仓库地图](../CONTRIBUTING.md)
- [文字表现力设计方向](typography-direction.md)
- [领域词汇](../CONTEXT.md) · [issue 与规格入口](agents/issue-tracker.md)
- [行为验收用例](../tests/cases.md) · [素材清单](assets.json)
- [历史记录](history/README.md) · [历史网页原型](../prototypes/README.md)

历史原型、工程检查通过和代理底线检查，都不能替代产品负责人的视觉审阅。
