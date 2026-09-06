# 开发与维护

[产品首页](README.md) · [文档导航](docs/README.md)

## 仓库地图

| 位置 | 职责 |
| --- | --- |
| `photo-dialogue/` | 可安装 Skill：入口、条件参考、文件处理、版本记录及依赖 |
| `scripts/` | 仓库检查、打包、验收统计与宿主验证工具 |
| `tests/` | 公开操作回归、行为用例、合成夹具 |
| `docs/` | 使用与安装指南、版本证据、验收标准 |
| `docs/history/` | 历史实施、审查与发布草稿 |
| `prototypes/` | 设计历史，不随运行包分发 |
| `CONTEXT.md` | 项目领域词汇 |

## 本地检查

使用合格的 CPython 3.11–3.13 创建独立环境，然后运行：

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r photo-dialogue/requirements.lock -r tests/requirements-dev.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -m mypy --ignore-missing-imports photo-dialogue/scripts scripts
.venv/bin/python scripts/check_repository.py
```

测试文件与版本记录的公开行为、真实输出、调用次数及原图保护；不固定自由创作文案或用像素完全相等代替人物核验。真实成图与人工评分另按 [验收标准](docs/acceptance.md) 执行。

## 构建运行包

```sh
.venv/bin/python scripts/distribution.py build dist/photo-dialogue-local.zip
```

目标文件必须尚不存在。安装器采用固定允许名单；添加运行资源时同步检查打包边界。用户安装与维护步骤统一放在 [安装指南](docs/install.md)，不在首页复制命令。

运行内容变更后重新构建并核对固定版本；定向测试与完整视觉矩阵分开记录。更新本机开发安装不等于替换已发布附件。发布前检查 [清单](docs/release-checklist.md)；`check_repository.py --release` 会检查资产许可，目前历史图仍有未清项。

## 文档与素材

使用说明写给普通用户：先说明发生了什么，再给必要的下一步；内部字段名留在开发文档。运行技能的说明按 [SKILL.md](photo-dialogue/SKILL.md) 与其条件参考维护。

当前使用入口放在首页和 `docs/`，过时报告归档到 `docs/history/` 并修复引用。保留固定版本的历史结果，不跨批次选优，也不把缺失的人工评分写成通过。

私密原图、成图、提示词及宿主事件放在仓库外。仓库图片逐项登记来源、许可和校验值；六张合成测试照的 CC0 不自动覆盖其他图片。
