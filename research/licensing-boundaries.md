# Photo Dialogue v1 字体、素材与示例许可边界

> 研究日期：2026-09-04
>
> 目的：为仓库日后由 Private 转为 Public 建立一套可执行、可审计的来源与许可政策。
>
> 说明：这是产品与仓库治理建议，不是针对特定司法辖区的法律意见。

## 决策建议

v1 采用 **原创优先、允许名单、逐文件溯源、人物另行授权** 的政策：代码、文档、气泡和装饰均原创；中文字体只使用官方来源且保持未修改的 OFL-1.1 字体；公开示例优先使用无真实人物原型的合成照片；任何第三方文件、真实人物照片或生成式内容必须先进入来源清单并通过对应许可、肖像与隐私检查。无明确许可证的项目只能作为高层方法参考，不能复制代码、文字或资产。

为了与 `guizang-yingzao-skill` 保持用户所要求的“完成度一致性”，Photo Dialogue 可以采用同等级的交付层次——`SKILL.md`、`agents/openai.yaml`、`assets/`、`references/`、`scripts/`、`tests/`、README 和检查脚本——但这些目录中的表达、实现和素材必须由本项目原创或具有明确的可再分发许可。目录分层是一种功能组织方式；不应借“一致性”复制对方的文件内容、参考图或代码。

## 发布时的许可结构

| 层级 | v1 政策 | 发布所需证据 |
| --- | --- | --- |
| 本项目代码、测试、原创文档 | 在根目录使用一个明确的软件许可证；建议 MIT，以便 Skill 被安装、修改和再分发 | 根 `LICENSE`；每位外部贡献者通过 Git 提交同意按该许可证贡献 |
| 原创气泡、边框、纹理与装饰 | 与项目代码一起按 MIT 发布；只提交源 SVG、参数或生成脚本，不提交来源不明的“素材包” | Git 作者记录；`assets/provenance.yml` 标为 `project-original` |
| 中文字体文件 | 字体自身继续使用 OFL-1.1，不受根许可证覆盖 | 每个字体目录保留上游版权声明、完整 OFL 文本、来源 URL、版本与 SHA-256 |
| 示例图与 README 作品展示 | 建议使用 CC0-1.0；若包含第三方 CC BY 4.0 内容，则该文件保留 CC BY 4.0 并满足署名，不由根许可证覆盖 | `assets/ATTRIBUTION.md` 与 `assets/provenance.yml`；若是真人，另有非公开授权记录 |
| 外部视觉参考 | 默认只保存链接、书目信息和本项目原创的抽象分析，不缓存图片或缩略图 | `references/sources.md` 中记录标题、作者、URL、访问日期和可否再分发 |

根许可证必须明确排除另有许可的字体和媒体文件，避免让一个 `LICENSE` 看起来像是在重许可第三方内容。GitHub 官方说明也提醒：仓库没有许可证时，默认版权规则适用，其他人不能复制、分发或制作衍生作品；因此“公开可见”不等于“可复用” [GitHub Docs：Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。

## 1. 中文字体

### v1 允许名单

只内置以下官方上游发布的、**未经修改**的字体文件：

- Noto Sans CJK SC，来自 `notofonts/noto-cjk` 的正式 release；其 Sans 目录附有 [OFL-1.1 许可证](https://github.com/notofonts/noto-cjk/blob/main/Sans/LICENSE)。
- Noto Serif CJK SC，来自同一官方仓库的正式 release；其 Serif 目录附有 [OFL-1.1 许可证](https://github.com/notofonts/noto-cjk/blob/main/Serif/LICENSE)。

Noto 官方文档明确说明 Noto 字体采用 OFL，可与应用一起分发并用于商业项目，但不能把字体单独出售 [Noto：Use Noto fonts](https://github.com/notofonts/noto-docs/blob/main/docs/website/use.md)。OFL-1.1 允许使用、复制、嵌入、修改和再分发字体，也允许字体随软件一起销售；分发字体时须保留版权声明与许可证，修改版还必须遵守 Reserved Font Name 条款 [OFL-1.1 正文](https://opensource.org/license/OFL-1.1)。用 OFL 字体生成的图片不会因此自动变成 OFL；SIL 的官方 FAQ 明确区分了“使用字体制作图形”和“分发字体软件” [OFL FAQ 1.1–1.3](https://openfontlicense.org/ofl-faq/)。

### 实施约束

1. v1 不做字体子集化、格式转换、字形修改或合并；SIL 将子集化视为修改，可能触发改名和 RFN 要求 [OFL FAQ 2.6](https://openfontlicense.org/ofl-faq/#2.6)。若仓库体积不可接受，宁可让依赖检查器从固定的官方 release 下载并验证校验和，也不要提交未经审计的“精简版”。
2. 每个被分发的字体文件旁必须有对应版权声明与完整 OFL 文本；不能只在 README 中笼统写“免费字体”。
3. `fonts.lock.yml` 固定上游仓库、release/tag、具体文件、SHA-256、许可证和是否修改。升级字体必须走一次许可与字形覆盖复核。
4. 不提交系统自带字体、从设计软件导出的字体、网盘“免费商用”字体或只有下载页宣传语却没有许可证正文的字体。
5. 若未来必须修改字体，单开审计票据：检查是否声明 RFN、按需要改内部和外部字体名、保留 OFL，并记录修改。

## 2. 气泡与装饰资产

### 默认策略

气泡、尾巴、旁白框、分隔线、纸纹和几何装饰均由本项目以 SVG、路径参数或确定性脚本原创生成。优先保存“生成规则”而不是一批不明来源 PNG，这既便于不同画幅适配，也使来源最清楚。

第三方装饰只允许：

- CC0-1.0：许可方在法律允许范围内放弃版权及相关权利，可用于商业复制、修改和再分发 [CC0-1.0 法律文本](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en)。
- CC BY 4.0：可商业分享和改编，但必须保留作者、版权与许可信息、链接原作，并说明是否修改 [CC BY 4.0 法律文本，第 3 节](https://creativecommons.org/licenses/by/4.0/legalcode.en)。

v1 禁止引入：

- 无许可证、来源无法回溯、仅写“free”或“个人使用”的素材；
- NC（非商业）或 ND（禁止改编）素材；
- BY-SA 素材，除非另开兼容性审查并愿意让改编素材遵守相同许可。CC BY-SA 4.0 的 ShareAlike 条款要求公开改编物时使用相同或兼容许可 [CC BY-SA 4.0，第 3(b) 节](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en)；
- 从 Canva、Figma 社区、商业素材库或其他应用导出的元素，除非该具体文件的条款明确允许源码仓库中的再分发，而不仅仅允许制作终端设计；
- 商标、品牌吉祥物、影视角色或明显仿制某位在世艺术家代表性作品的资产。

CC BY 文件必须逐项署名；不能把一个素材站首页链接当作许可证明。若上游删除文件，仓库仍应保留当时下载的许可证文本、版本和校验和。

## 3. Look 与视觉参考

### 可用作研究，不可默认入库

公开仓库中的 `references/` 只保存：

- 外部页面链接和书目信息；
- 对构图、色彩、层级、留白、前后遮挡等**抽象机制**的本项目原创描述；
- 本项目原创的示意图与测试夹具。

不保存外部网页截图、社交媒体图片、摄影作品缩略图、对方 moodboard、扫描书页或“仅供参考”的复制件，除非每个文件已有明确允许再分发和改编的许可证并登记在来源清单中。只写出处或致谢并不能替代许可。

这一边界允许我们学习一般思路而不复制具体表达。美国版权法明确把“思想、程序、过程、系统、操作方法、概念、原则或发现”排除在版权保护之外，但具体文字、图形和代码表达仍可能受保护 [17 U.S.C. §102(b)](https://www.copyright.gov/title17/92chap1.html#102)；美国版权局的 Circular 33 也明确区分了思想／方法与对它们的原创表达 [Circular 33](https://www.copyright.gov/circs/circ33.pdf)。这是一个保守的工程边界，不代表所有司法辖区的完整法律结论。

### `guizang-yingzao-skill` 的处理

截至 2026-09-04 检查的提交 [`58c9b8738858bae0ab2c669d0a0fead90d4a80c9`](https://github.com/op7418/guizang-yingzao-skill/tree/58c9b8738858bae0ab2c669d0a0fead90d4a80c9)，GitHub 仓库元数据没有检测到许可证，许可证 API 返回 404，仓库树中也没有 `LICENSE`、`COPYING` 或 `NOTICE`。依 GitHub 的无许可证说明，应按“保留所有权利”处理，而不能因为仓库公开就假定可复制。

Photo Dialogue 可以：

- 在 README 的“灵感与致谢”中按名称链接该项目；
- 记录并独立落实高层能力，例如照片预检、稀疏排版规划、设计 Token、生成前门控、脚本与回归测试；
- 采用同等级的仓库完整度和通用目录分层，以回应 Q14 的“一致性”要求。

Photo Dialogue 不可以：

- 复制、翻译或近似改写其 `SKILL.md`、README、参考文档、JSON Token 文案、提示词或代码；
- 下载、裁切、调色、描摹或重新发布其 `reference-plates`、缩略图、英雄图等资产；
- 以其输出图为 image-to-image 输入、风格参考图或测试 fixture；
- 将它的具体表达换几个名词后作为“原创实现”。

实践上使用 clean-room 记录：研究笔记只写“需要解决什么”和可观察的高层机制，生产实现从 Photo Dialogue 自己的人物叙事需求、测试和领域词汇出发重新设计。若未来确实需要复用任何具体文件，先取得版权方书面许可或等待上游添加覆盖该文件的明确许可证。

## 4. 示例照片与人物授权

### v1 默认：不公开真实可识别人物

公开 README、测试、样例集和作品墙优先使用：

1. 无真实人物原型、未使用真实人物参考图的合成人物照片；
2. 不可识别人物的本项目原创照片；
3. 只有在确有必要时，使用项目方拥有照片版权且所有可识别人物均完成书面授权的摆拍照片。

真实照片至少涉及两条相互独立的权利链：摄影作品的版权，以及照片中人物可能享有的肖像、隐私或人格权。CC0 与 CC BY 也不会自动清除所有第三方人物权利；CC0 法律文本明确将人物图像相关的 publicity/privacy rights 列为可能存在的权利，而其限制条款不影响他人的这些权利 [CC0-1.0，第 1(c) 与 4(a) 节](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en)。CC BY 4.0 同样提示许可可能没有覆盖公开使用所需的隐私、人格或精神权利 [CC BY 4.0，第 2(b) 节](https://creativecommons.org/licenses/by/4.0/legalcode.en)。因此，“来自 CC0/CC BY 图库”不能代替人物授权。

如以后加入真实人物示例，发布门槛是：

- 摄影者签署或明确授予全球、长期、可公开、可修改、可再分发、可用于项目推广及商业用途的许可；
- 每位可识别成年人同意这些具体用途；未成年人由具备资格的父母或法定监护人签署，并避免暴露姓名、学校、住址、定位、医疗等信息；
- 授权原件存放在私有、访问受控的位置，公开清单只记录 release ID、覆盖文件和审核日期，不公开签名、地址等个人信息；
- 发布前移除 EXIF、GPS、设备序列号和不必要的文件名信息；
- 用户在实际使用 Skill 时提供的 Source Photo 永远不进入仓库、遥测、测试夹具、README 或作品墙，除非用户另行、明确地授权该发布用途。

## 5. 生成式示例

生成示例不是“自动无风险”。v1 只发布满足以下条件的成品：

- 基础照片由无真实人物参考的文本提示生成，或输入照片已经通过上一节的权利检查；
- 不要求复现真实人物、公众人物、商标、角色或特定在世艺术家的风格；
- 生成后由项目方完成人工文案、气泡、构图与排版，并进行相似性和身份检查；
- 清单记录生成日期、工具／模型、适用条款版本、提示词或提示词摘要、输入资产、人工修改和审核者；
- README 明确标注“AI-generated demonstration / AI 生成示例”，不暗示其中是真实家庭或真实事件。

以 OpenAI 为例，当前条款在用户与 OpenAI 之间把输出权利归给用户，但同时要求用户对输入所需权利负责，并提示输出可能不唯一 [OpenAI Terms of Use：Content](https://openai.com/policies/row-terms-of-use/)。OpenAI 当前图像与视频条款还禁止在没有明确同意和必要权利时复现任何人的肖像 [OpenAI Service Terms，第 6 节](https://openai.com/policies/service-terms/)。换用其他生成服务时必须重新读取该服务当时的官方条款，不能把 OpenAI 的条款推定给其他供应商。

“服务商把输出权利让给用户”也不等于该输出一定获得排他的著作权。美国版权局 2025 年报告认为，生成式输出只有在人类决定了足够的表达性要素时才可能受到版权保护；仅提供提示词通常不够，但人类的创造性选择、安排或修改可能受到保护 [美国版权局 AI 报告 Part 2 公告](https://www.copyright.gov/newsnet/2025/1060.html)。因此公开示例建议使用 CC0-1.0，并写成“在贡献者拥有或可许可的权利范围内适用”；不要宣称对纯 AI 像素拥有排他版权。

## 6. 来源清单与自动门控

公开前应新增两个机器／人可读入口：

- `assets/provenance.yml`：每个被提交的二进制资产一条记录；
- `assets/ATTRIBUTION.md`：供用户阅读的字体、照片、装饰与生成式内容说明。

建议最小字段：

```yaml
- path: assets/examples/family-dialogue-01.webp
  kind: generated-example
  creator: Photo Dialogue contributors
  source_url: null
  upstream_version: null
  sha256: "..."
  license: CC0-1.0
  license_file: assets/licenses/CC0-1.0.txt
  modified: true
  modification_note: "Original dialogue, layout, and deterministic overlays"
  ai:
    provider: OpenAI
    model: "record-exact-model"
    generated_at: "YYYY-MM-DD"
    real_person_reference: false
    terms_url: https://openai.com/policies/terms-of-use/
  people:
    identifiable: false
    release_id: null
  reviewed_by: "..."
  reviewed_at: "YYYY-MM-DD"
```

CI 或发布前检查脚本应当：

1. 枚举 `assets/` 和 `fonts/` 中所有二进制文件，要求每个文件在清单中唯一出现；
2. 比对 SHA-256；
3. 拒绝空许可证、`unknown`、`personal-use`、NC、ND 和未经例外批准的 SA；
4. 要求字体具备本地许可证文件和固定上游版本；
5. 要求所有 `identifiable: true` 的照片有 release ID，且未成年人记录 guardian approval；
6. 扫描 JPG/HEIC/TIFF 等文件的 EXIF/GPS 并在发现时失败；
7. 要求生成式示例有供应商、模型、生成日期、条款 URL 与真实人物参考标志；
8. 检查 README 所嵌入的每个本地图片也存在于清单。

## 7. Public 切换前的硬门槛

- [ ] 根目录已有明确许可证，并声明字体和单独标注媒体不受根许可证覆盖。
- [ ] 所有字体来自允许名单、版本固定、校验和通过、OFL 与版权声明齐全。
- [ ] 所有气泡和装饰为原创、CC0 或已正确署名的 CC BY 4.0；没有来源不明素材。
- [ ] 仓库中没有从 `guizang-yingzao-skill` 或其他无许可证来源复制的代码、文字、图片、缩略图或测试数据。
- [ ] 所有视觉参考默认仅以链接和原创抽象分析存在。
- [ ] 所有示例图已登记；默认没有真实可识别人物。
- [ ] 若存在真实人物，照片版权与人物授权均已核验，授权原件留在私有受控位置。
- [ ] 所有图片已清理 EXIF/GPS；生成式示例已披露来源并核验当时供应商条款。
- [ ] 来源检查脚本和 CI 在干净 clone 中通过。

## 结论

这项政策不会妨碍 Photo Dialogue 做到与参考项目同等级的目录完整度、排版研究深度、Look 系统和自动检查；它只把“学习”限定在高层机制，把每一份实际表达和资产重新原创或置于明确许可之下。对 v1 而言，最稳的组合是：**MIT 的原创 Skill 实现 + 未修改的 Noto CJK/OFL-1.1 + 原创程序化气泡 + CC0 合成示例 + 强制 provenance 清单**。
