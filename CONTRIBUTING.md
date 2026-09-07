# 开发与维护

[产品首页](README.md) · [文档导航](docs/README.md)

## 提交贡献与合并权限

欢迎通过 Issue 报告问题，也欢迎 Fork 本仓库后，在自己的分支修改并向 `main` 提交 Pull Request（PR）。较大的功能改动请先开 Issue 说明需求。

PR 请说明解决的问题、实际改动和验证结果。不要提交密钥、私人照片、私人提示词或未经授权的素材；原创代码和文档贡献沿用仓库 MIT 许可证，图片必须单独登记来源与使用范围。

`JoeWu-explorer` 是唯一拥有仓库写入和合并权限的维护者。贡献者不需要协作者权限；PR 由维护者检查后决定是否合并。维护者自己的修改也通过分支和 PR 进入 `main`。

主分支要求 PR，必需审批人数为 0，以允许唯一维护者合并自己的 PR；禁止强制推送和删除主分支。提交 PR 不会自动修改主分支，也不会自动发布新版本。

## 仓库地图

| 位置 | 职责 |
| --- | --- |
| `plog/` | 可安装 Skill：入口、条件参考、文件处理、版本记录及依赖 |
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
.venv/bin/python -m pip install --require-hashes -r plog/requirements.lock -r tests/requirements-dev.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -m mypy --ignore-missing-imports plog/scripts scripts
.venv/bin/python scripts/check_repository.py
```

测试文件与版本记录的公开行为、真实输出、调用次数及原图保护；不固定自由创作文案或用像素完全相等代替人物核验。真实成图与人工评分另按 [验收标准](docs/acceptance.md) 执行。

## 构建运行包

```sh
.venv/bin/python scripts/distribution.py build dist/plog-local.zip
```

目标文件必须尚不存在。安装器采用固定允许名单；添加运行资源时同步检查打包边界。首页保留一条 npx 安装命令与简短使用示例；详细安装、环境配置和维护步骤放在 [安装指南](docs/install.md)。

运行内容变更后重新构建并核对固定版本；定向测试与完整视觉矩阵分开记录。更新本机开发安装不等于替换已发布附件。发布前检查 [清单](docs/release-checklist.md)；`check_repository.py --release` 会检查资产许可，图片使用范围见 `docs/image-rights.md`。

## 文档与素材

使用说明写给普通用户：先说明发生了什么，再给必要的下一步；内部字段名留在开发文档。运行技能的说明按 [SKILL.md](plog/SKILL.md) 与其条件参考维护。

当前使用入口放在首页和 `docs/`，过时报告归档到 `docs/history/` 并修复引用。保留固定版本的历史结果，不跨批次选优，也不把缺失的人工评分写成通过。

私密原图、成图、提示词及宿主事件放在仓库外。仓库图片逐项登记来源、许可和校验值；六张合成测试照的 CC0 不自动覆盖其他图片。
