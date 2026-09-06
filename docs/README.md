# 文档导航

[返回产品首页](../README.md)

## 使用产品

- [使用指南](guide.md)：首次做图、修改、返回旧版、导出与排错。
- [安装指南](install.md)：安装、HEIF 支持、更新和卸载。

## 版本与验收

**已发布：v0.1.0-alpha.1。** 运行包固定为 `2a6156c`，仍是试用版；18 次首次生成中 11 次通过代理底线检查、7 次拒收，人工评分未完成。原始失败保留，尚未达到完整发布验收要求。

- [下载已发布版本](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.1) · [发布包校验与统计](candidate.json)
- [完整视觉验证记录](person-fidelity-fixes.md) · [生成限制诊断](generation-limit-diagnosis.md)
- [预发布后的交付与保存修复](delivery-and-save-fixes.md) · [该次开发候选校验](development-candidate.json)
- [上手引导与文档整理](onboarding-update.md)：本分支新增变化及验证范围。
- [验收标准](acceptance.md) · [公开前清单](release-checklist.md)

运行目标为 macOS/Linux 与 CPython 3.11–3.13，基础格式 JPEG/PNG/WebP，HEIF 可选。原包目标宿主实测 Codex 0.153.3；依赖版本与各批次证据以上述清单为准。Windows 和所有客户端兼容性未作承诺。新分支或本机开发安装不能沿用旧版视觉成绩宣称通过。

## 开发与维护

- [开发指南与仓库地图](../CONTRIBUTING.md)
- [领域词汇](../CONTEXT.md) · [issue 与规格入口](agents/issue-tracker.md)
- [行为验收用例](../tests/cases.md) · [素材清单](assets.json)
- [历史记录](history/README.md) · [历史网页原型](../prototypes/README.md)

历史原型、工程检查通过和代理底线检查，都不能替代产品负责人的视觉审阅。
