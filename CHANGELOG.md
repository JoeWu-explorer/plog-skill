# 更新记录

## v0.1.0-alpha.6 · Plog 新入口

- 仓库改名 `plog-skill`，Skill 与 npx 调用名统一为 `plog`；补齐旧安装迁移说明，作品与版本记录保留原路径
- 丰富功能简介，README 展示十组作品合集、儿童与多人／多宠互动、原图与成图对照
- 安装器兼容旧包和旧清单，继续保护本地改动，拒绝混合根目录或名称不匹配的包
- 58 项测试、类型与仓库检查、可复现构建、实际 alpha.5 包升级和本地 Skills CLI 复制安装通过

[下载](https://github.com/JoeWu-explorer/plog-skill/releases/tag/v0.1.0-alpha.6) · [验证范围](docs/release.json)

## v0.1.0-alpha.5 · 字体表现力与画内标点

- 展示图与封面先确定主视觉词组，再逐图设计字形、尺度、断行与图文关系；增强文字不自动加重滤镜。
- 画内创作配文默认不用句末句号，保留有意义的问号、感叹号；只改标点时核对其他文字、排版与摄影内容。
- README 重排六类 Plog 前后对照，突出自动文案、色调、氛围与排版；保留简洁的 npx 快速开始。
- 56 项确定性测试、类型与仓库检查、可复现构建、全新安装和真实 alpha.4 发布包升级检查通过。新增视觉行为用例待正式执行，不宣称所有 Agent 或照片均已通过。

[下载](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.5) · [固定包与验证范围](docs/history/release-alpha-5.json)

## v0.1.0-alpha.4 · Plog / 多 Agent

- 主定位改为中文 Plog，覆盖人物、山海、街景、食物、静物与宠物；多张照片逐张创作和保存，取消人数硬门槛。
- 通用 Skill 按实际能力选择原生工具或兼容 API；支持 OpenClaw、Hermes、Claude Code、DeepSeek Harness、Codex 与自定义安装目录。
- 新增图片编辑与视觉分析接口，密钥留在宿主环境；显式外发、元数据清理、单次请求、失败保护与候选核验分开。
- 交付适配本地链接与当前聊天附件；旧版本记录不变，安装器兼容 alpha.1–3 更新。
- 重写 README 与安装指南，加入 Plog 组图示例、Agent 安装口令和 Skills CLI 安装路径。
- 新增 Plog 场景与宿主验收矩阵，保留历史人物矩阵。实际各 Agent／图像服务全链路和新场景视觉验收待执行。

- 56 项确定性测试、类型／仓库检查、可复现构建、全新安装和真实 alpha.3 发布包升级验证通过。

[下载](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.4) · [固定包与验证范围](docs/release.json)

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
