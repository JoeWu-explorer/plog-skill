# 来源与许可

原创代码/文档按 MIT（LICENSE）。依赖由锁文件安装，未把第三方 wheel 或二进制打入技能包；安装的发行包携带各自完整许可与二进制组件通知。

| 范围 | 来源 | 许可 / 状态 |
| --- | --- | --- |
| 基础运行 Pillow 12.3.0 | https://pypi.org/project/pillow/12.3.0/ ; https://github.com/python-pillow/Pillow | HPND；安装发行包包含 LICENSE 与第三方组件通知 |
| 可选 pillow-heif（精确版见 requirements-heif.lock） | https://pypi.org/project/pillow-heif/ ; https://github.com/bigcat88/pillow_heif | BSD-3-Clause；其 wheel 还含 libheif 等组件，以发行包携带通知为准；不在本技能压缩包重分发 |
| 六张合成测试照 | tests/fixtures/source-photos/MANIFEST.md | 仅清单六个 PNG 适用该目录 CC0-1.0 dedication；不进运行包 |
| 历史 Look 研究图 | prototypes/look-system/generated/PROVENANCE.md | 来源已记录；尚未授予独立发布许可，公开发布被此项阻止 |
| 开发工具 mypy / jsonschema | tests/requirements-dev.txt | MIT；仅开发使用，不进运行包 |

运行依赖完整通知的本地副本在 `photo-dialogue/notices/`，它们来自实际安装的锁定发行包；不改变其许可。

六图 CC0 不覆盖新成图、用户照片或其他图片。正式 examples 尚未完成真人审阅和逐文件许可登记。参考项目只作为高层交付方式参考，未复制其代码、提示词或图像。未知、NC、ND 或未经审查的 SA 资产不得公开。
