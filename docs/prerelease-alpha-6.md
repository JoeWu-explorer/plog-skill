# v0.1.0-alpha.6 · 照片有话说 · Plog

仓库正式更名为 **plog-skill**，Skill 名称统一为 **plog**。从人物、儿童成长、多人相聚到山海、街景、美食和宠物，让照片自动配上有故事的文案、光色与艺术排版；支持对白互动、组图日记、自然语言修改与版本恢复。

## 快速开始

```sh
npx skills add https://github.com/JoeWu-explorer/plog-skill --skill plog
```

安装后发照片，说「用 plog 把这些照片做成一组中文日记」。需要支持 Skills、读图与照片编辑的 Agent。仓库保持私有，安装需要访问权限；完整 Agent／图像服务组合仍待逐项实测。

## 本版更新

- README 使用十组作品合集封面与可展开的前后对照，涵盖儿童、婴儿、多人和多宠互动等场景，扩充功能简介，保留简洁安装流程
- 仓库、Skill 入口、安装目录、CI 和当前文档统一新名称；历史版本和作品路径保持可追溯
- 安装器识别旧 photo-dialogue 包与安装清单，保留本地修改保护，阻止同目录新旧技能重复安装
- 文案不以句号收尾、文字张力与逐图艺术指导继续沿用；本版不更改原有作品记录格式

旧版用户按 [迁移说明](https://github.com/JoeWu-explorer/plog-skill/blob/v0.1.0-alpha.6/docs/install.md#从-photo-dialogue-迁移) 操作。固定版本使用本页 `plog-v0.1.0-alpha.6.zip` 与 `SHA256SUMS`。

## 验证范围

58 项确定性测试、类型检查、仓库引用与 70 项资产清单检查通过；Skill 格式检查、可复现构建、全新安装／自检／卸载、真实 alpha.5 发布包升级及目录迁移通过。Skills CLI 已在临时目录验证 Claude Code 复制安装。

本次未执行新的图像生成或多 Agent 端到端视觉验收；展示图片的来源与范围见仓库清单。托管 CI 状态和固定运行提交见 [版本清单](https://github.com/JoeWu-explorer/plog-skill/blob/v0.1.0-alpha.6/docs/release.json)。
