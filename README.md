# 照片有话说 · Photo Dialogue

把一张人物照片做成中文叙事成图，再用自然语言修改。它是可安装的 Codex Skill：上传照片，可补一句场景，技能按当前照片决定叙事、光色、字体与构图；生成后对照原图和确切中文核验，成功保存后给出 PNG 预览、下载入口和最小修改记录。

**当前为可安装的开发候选，尚未通过发布验收。** 首次成图、多人原话、定向修改、恢复导出、失败保护和安装维护已实现。最终保留包完成新的 18 次真实首次生成：11 次通过代理底线核验、7 次拒收，接受的成图中未观察到人物误交付；人工评分未填写。三种自然语言修改通过；15 类行为执行完毕，14 类通过，一类因相对下载链接保留失败。34 项本机测试与检查通过。完整证据及限制见 [最新验证记录](docs/person-fidelity-fixes.md)。

开发分支另有 [交付与保存优化](docs/delivery-and-save-fixes.md)，与已发布 alpha 的版本及验收统计分开记录。

## 使用体验

- 发一张照片：“把这张照片做成中文叙事图。” 也可以显式调用 `$photo-dialogue`。只有照片且动作清楚时，可直接采用中性叙事。
- 补充已知背景：“夫妻俩一起包饺子。” 照片负责可见动作，用户说明负责关系和原话。
- 定向修改：“只改这句话”“氛围淡一点，字别动”“从第一版继续，把字移开手部”。旧版本保留，失败不会替换已有成图。
- 新会话提供作品目录和原图，可恢复所选版本继续。原图缺失或校验变化会请求正确来源。

外发前说明照片、Codex 内置图像服务和本次用途；已有明确授权直接承接。成图在本地保存，不等于整个生成过程都在本地执行。

## 候选安装与维护

当前固定候选为 `2a6156c5369a30c8ad28ec1e79533c4aa286671c`，作为 `v0.1.0-alpha.1` 预发布交付，仓库保持私有；这不是通过完整发布验收的稳定版。制品为 `dist/photo-dialogue-2a6156c.zip`，校验信息见 [候选清单](docs/candidate.json)。该包已独立完成全部 18 次影像矩阵；更严格的提示词试验 `142b30e` 因效果未达标撤回，当前运行内容与此固定包逐字节一致。可从 [预发布页面](https://github.com/JoeWu-explorer/photo-dialogue/releases/tag/v0.1.0-alpha.1) 下载固定 ZIP 与 SHA256SUMS（需要仓库访问权限）。下面命令可从该版本源码构建并安装。使用已安装的合格 CPython 3.11–3.13，将 `python3.13` 替换为你选择的同一个解释器。

```sh
python3.13 scripts/distribution.py build dist/photo-dialogue-candidate.zip
python3.13 scripts/distribution.py install dist/photo-dialogue-candidate.zip
python3.13 -m venv ~/.local/share/photo-dialogue/venv
~/.local/share/photo-dialogue/venv/bin/python -m pip install --require-hashes -r ~/.agents/skills/photo-dialogue/requirements.lock
export CAP_PYTHON="$HOME/.local/share/photo-dialogue/venv/bin/python"
```

安装默认目标 `~/.agents/skills/photo-dialogue`；`--target` 可指定独立测试位置。发现旧安装位置或已有目录时不会默默覆盖/重复安装。包不包含测试照、原型、环境、私人输出或开发机路径。联网装依赖需用户已授权，包构建/安装器本身不联网。

在已有可写私密目录运行 `self_check.py --workspace <目录>`，使用同一 venv 的解释器。它检查本地格式和文件能力，不探测收费生成，也不能证明宿主图像权限。具体参数见 [运行说明](photo-dialogue/references/runtime.md)。

更新用 `scripts/distribution.py update <新包> --target <安装目录>`；卸载用 `scripts/distribution.py uninstall --target <安装目录>`。新增/修改/缺失本地文件会阻止替换或删除；先自行保留并处理修改，不提供强制覆盖开关。生成的已知 Python 字节码缓存可清理。作品独立保存在 `~/Pictures/PhotoDialogue/` 或用户指定位置，更新/卸载不处理作品。

## 范围与限制

支持目标是一张含 1–6 名参与者的静态 JPEG、PNG、WebP；HEIC/HEIF 为可选依赖，安装后必须通过功能自检。原方向默认保留，可按要求调整画幅。动画、多页、RAW、超人数或无法核验的人物图会说明问题。

已验证 macOS arm64 与 Linux arm64 / CPython 3.11–3.13 / Pillow 12.3.0；HEIF 在 macOS Python 3.13 与 Linux 三个 Python 版本上通过 pillow-heif 1.6.0 实测，缺失依赖时正确说明不支持。目标宿主实测为 Codex 0.153.3；旧 CLI 0.146.0 无法运行当前配置模型，不能据此承诺兼容。Windows、其他 Python 和所有 Agent 客户端不作兼容承诺。

生成式人物细节和中文仍可能失败。技能要求失败不作为成品交付，不自动重试、换服务或退回贴字；前一视觉候选实测发生 1 次人物漂移误交付，已在独立核验中判为失败，不能依赖技能自检作保真保证。不能承诺完全本地、无限免费、零错字、像素不变或任意照片必成功。普通非露骨照护场景可克制表达；隐私、人物尊严、未成年人和不支持用途边界见 [人物与隐私](photo-dialogue/references/people-and-privacy.md)。

## 示例、验收与许可

[历史网页原型](prototypes/)仅作规划评审记录，不能代表正式 Skill 成绩。正式三场景效果展示还未通过真人审阅，暂不把历史试验或失败候选当产品效果宣传。

原始六张合成测试照迁至 [测试素材目录](tests/fixtures/source-photos/MANIFEST.md)，内容和 SHA-256 保持不变。只有清单中的六张 PNG 适用 CC0；其他图片需逐项许可。原创代码/文档 MIT，见 [LICENSE](LICENSE) 和 [第三方通知](THIRD_PARTY_NOTICES.md)。

[验收方法](docs/acceptance.md) · [行为用例](tests/cases.md) · [公开前清单](docs/release-checklist.md) · [发布文案草稿](docs/release-draft.md)
