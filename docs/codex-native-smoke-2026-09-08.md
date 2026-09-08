# Codex 原生图片工具实测 · 2026-09-08

**结果：单样例的安装 → 出图 → 仅改文字 → 旧版恢复与交付已走通。** 使用真实 OpenAI 图片编辑工具，共两次调用、无重试。已保存两个版本及版本记录，恢复旧版未改写原图、两个 PNG 或记录。

这是当前源码的手动链路检查，不是 [完整发布验收](acceptance.md)。使用现有 Codex 会话显式读取新安装的技能；未验证全新 Agent 会话自动发现，未完成 14 次首次尝试、20 类行为、三类修改或真人评分。合成静物不证明真人照片保真。

## 固定候选与环境

| 项目 | 实测值 |
| --- | --- |
| 源码提交 | `1cae0e92e1188702d8c820cfb9ab0fc107f9d7cc` |
| 允许名单运行 ZIP SHA-256 | `94ab59543356182af5faeaf1441a01ad41cfdf9f915397390e5ad8a5bddf4dae` |
| 安装内容 | 从公开 GitHub main 复制安装；19 个文件与上述固定提交逐文件 SHA-256 一致 |
| Agent | Codex 桌面端当前会话；桌面应用版本 `26.901.51231 (8109)` |
| 读图 | 原生 `view_image` 与当前会话视觉能力 |
| 图片服务 | 原生 OpenAI `image_gen.imagegen`，实际图片编辑调用 |
| 服务模型版本／费用 | 工具未返回，均为 unavailable |
| 系统 | macOS 26.6.2 / arm64 |
| 安装工具 | Node.js 26.5.0；Skills CLI 1.5.24 |
| 本地依赖 | 独立环境；Python 3.13.13，Pillow 12.3.0，按锁文件校验安装 |
| 文件能力自检 | JPEG、PNG、WebP 通过；未安装可选 HEIF，未验证 HEIC/HEIF |

固定 ZIP 用于记录运行文件，不是重新发布的 alpha.6 附件。实测使用 CLI 安装的副本及其中的脚本，未用开发目录中的同名脚本替代。Codex CLI 未参与出图。

## 执行与结果

样例为仓库已有的 AI 生成早餐示例 `examples/readme/table/before.png`，1086 × 1448，无真人。生成前记录原图 SHA-256：`14f62263fb0ea60c6d60d075aa3f398409f7dccc6d51e184109b702cbf9c7d5d`。作品和详细证据保存在仓库外。

| 步骤 | 操作与证据 | 结果 |
| --- | --- | --- |
| 安装 | 在新项目目录禁用 Git credential helper、交互询问及 askpass 后执行下方 npx 命令；19 文件与固定源码一致 | 通过，无需仓库访问权限或 GitHub 登录 |
| 准备 | 显式读取安装后的 SKILL.md，独立 venv 按锁文件安装依赖，执行本地自检，查看原图并准备清洁副本 | 通过；原生工具可用，未配置兼容 API |
| 首次出图 | 原图清洁副本作为输入，配上两行早餐旁白和轻暖光色；真实编辑调用一次，约 62 秒 | 中文与画面核验后接受为 v001 |
| 仅改文字 | 只用已接受 v001 的清洁副本，替换第二行前两个字；真实编辑调用一次，约 69 秒 | 对照原图、v001、候选后接受为 v002，parent_id 为 v001 |
| 恢复与交付 | 独立脚本进程运行 recover、delivery，明确选择 v001；校验返回路径、旧文字及 PNG，并重显旧版 | 通过；原图、v001、v002、revision.json 前后 SHA-256 完全一致 |

耗时为工具调用前后计时的近似值，不是性能基准。恢复表示重新选择旧版作为查看／继续编辑基准，不改写 `current_version`；当前最新接受版本仍为 v002，没有凭空增加 v003。

视觉检查对照了原图、首图与修改图：杯子、餐盘、两片面包、鸡蛋和亚麻布的位置与主要结构保留；首图两行中文正确，修改图仅替换目标字词，未发现明显的字体、布局、光色或场景漂移。也查看了两版 390 像素宽的只读检查缩略图，文字可辨；这不是产品负责人的 390 CSS px 浏览器视图评分，不作为真人审阅完成。

## 重现这条路径

在空项目目录运行（`npx` 默认跟随 main；复核本记录时须再核对上述固定提交的文件哈希）：

```sh
GIT_TERMINAL_PROMPT=0 \
GIT_CONFIG_COUNT=2 \
GIT_CONFIG_KEY_0=credential.helper GIT_CONFIG_VALUE_0='' \
GIT_CONFIG_KEY_1=core.askPass GIT_CONFIG_VALUE_1='' \
npx --yes skills add https://github.com/JoeWu-explorer/plog-skill --skill plog --agent codex --copy --yes
```

随后按 [安装指南](install.md#准备-python-环境) 准备独立 Python，显式读取该项目 `.agents/skills/plog/SKILL.md`，确认当前会话有原生读图与图片编辑能力。按 [运行约定](../plog/references/runtime.md) 准备输入；实际生成后核验再 append，按 [修改与恢复约定](../plog/references/revisions.md) 用首版清洁副本修改，并以 `recover --version v001` 和 `delivery --version v001` 恢复与重显。

本次保留了安装文件哈希、环境、自检、两次生成、两次 append、恢复／交付返回及前后哈希证据；公开报告只记录范围与结论，不包含私人绝对路径或完整提示词。

## 尚未覆盖

- 干净 Agent 会话中的技能发现、自动选用，以及完整 Plog 场景和行为矩阵。
- 真人、宠物、密集人群、多图系列、HEIC/HEIF；仅氛围和仅移动文字修改。
- 产品负责人五项视觉评分、其他 Agent／provider、托管 CI 平台矩阵。

本轮仓库 58 项确定性测试通过，引用与资产清单检查通过。这些检查和本次真实图像结果分别记录，不互相替代。
