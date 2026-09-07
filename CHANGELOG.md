# 更新记录

## v0.1.0-alpha.3

- 首次确认说清照片处理方式和用途，支持自然回复，同一范围内修改和重试不重复确认。
- 统一生成、修改、旧版恢复、导出、失败和停止等各轮对话，简短说明实际结果与下一步。
- 对话指南随运行包分发，安装器兼容 alpha.1/alpha.2 的文件名单并继续保护本地修改。
- 42 项确定性测试、类型与仓库检查、可复现构建、独立安装和真实 alpha.2 升级验证通过；原型 11 个模拟场景及桌面/手机检查通过。
- 未重跑真实生成与完整视觉矩阵；历史结果不转移到本版本。

[下载](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.3) · [固定包与验证范围](docs/release.json)

## v0.1.0-alpha.2

- 文字按照片空间、人物动作和内容决定分量，支持醒目、平衡或克制的表达，不固定大字模板。
- 简化首次使用、授权、失败和恢复话术；首页、安装、使用与开发文档分开，历史报告归档。
- 工具直接生成同一版本的有效预览与下载链接，支持只读重显旧作品。
- 修复保存中断时可能误删被其他操作替换的 PNG。
- 38 项确定性测试通过。生成质量未进行新的完整视觉矩阵验收，原失败保留。

[下载](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.2) · [该版固定包与验证范围](https://github.com/JoeWu-explorer/photo-dialogue/blob/v0.1.0-alpha.2/docs/release.json)

## v0.1.0-alpha.1

首个可安装版本：首次成图、多人原话、定向修改、恢复导出、失败保护和安装维护。

固定 18 次首次生成中，11 次通过代理底线检查、7 次拒收；人工评分未完成。这是 alpha.1 的历史结果，不能用于宣称新版本通过。

[下载](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.1) · [历史验证](docs/person-fidelity-fixes.md)
