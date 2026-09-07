# 照片有话说 v0.1.0-alpha.5 · 让文字参与构图

把人物、山海、街景和日常照片做成中文 Plog，自动设计文案、光色、氛围与排版。

## 快速开始

```sh
npx skills add https://github.com/JoeWu-explorer/photo-dialogue --skill photo-dialogue
```

安装后发照片，说：“用 photo-dialogue 做一张中文 Plog，文字更有张力。”Agent 需具备读图、图片编辑和本地脚本能力。

npx 安装 main 分支源码；固定版本可下载本页 ZIP 与 SHA256SUMS，按 [安装指南](https://github.com/JoeWu-explorer/photo-dialogue/blob/v0.1.0-alpha.5/docs/install.md) 操作。仓库仍为私有，需要访问权限。

## 本次更新

- 将展示图的主视觉词组、字体细节、尺度差异与空间关系写入 Skill，逐图决定表达方式。
- 创作配文默认不加句末句号，按语气保留问号与感叹号；只改标点须核对画面与排版保持情况。
- 同步修整展示图的句末句号，保留原图、历史版本与修订记录。
- README 展示人物、人文、山海、街景、食物与宠物的自动创作前后对照，采用错落首图、等宽对照和按需展开的示例指令。

## 验证范围

56 项确定性测试、类型检查、Skill 格式及仓库检查通过。固定包重复构建一致，全新安装、自检、卸载与真实 alpha.4 发布包升级检查通过。

README 示例及编辑记录见 [素材说明](https://github.com/JoeWu-explorer/photo-dialogue/blob/v0.1.0-alpha.5/examples/readme/MANIFEST.md)。完整 Plog 视觉矩阵、各 Agent／图像服务全链路及新增视觉行为用例仍待正式执行；示例效果不代表全部组合已通过。

运行内容固定于 `9db3c16d6d6b2c8108b43e290245bab71cb76bf0`。ZIP 共 22 个文件、74,418 字节，SHA-256：`5b01222381817c25a3734034caf481333d10db9b387ae8e17796bd35ede27771`。附件仅含运行 ZIP 与校验文件。

历史原型图片许可仍待整理，仓库保持私有；本次预发布不代表稳定版或公开素材验收完成。详见 [版本清单](https://github.com/JoeWu-explorer/photo-dialogue/blob/v0.1.0-alpha.5/docs/release.json)。
