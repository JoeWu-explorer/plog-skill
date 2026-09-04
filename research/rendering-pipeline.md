# v1 图像处理与渲染管线研究

研究日期：2026-09-04

对应决策票：[选择 v1 的图像处理与渲染管线](https://github.com/JoeWu-explorer/photo-dialogue/issues/2)

## 决策

v1 采用**原图像素为真源、本地确定性合成为正式路径、生成式编辑为显式 Strong Look 支线**的混合管线：

1. Codex 负责理解 Source Photo 与 Scene Description、生成 Voice Elements，并给出语义级的人物、视线、动作与负空间观察；它不单独裁定像素级禁排区。
2. 本地 Python 工具负责方向与色彩归一、轻量人脸检测、安全区合并、中文断行与字形覆盖检查、排版、Look、导出和验证。
3. 默认路径不调用图像生成模型，不重绘人物；所有中文、气泡、尾线与资料字均由 Pillow 从真实字符串确定性绘制。
4. 只有用户主动要求 Strong Look 时才调用 Codex 的图像生成能力；生成模型只产出**无字视觉底图**，最终中文仍在本地叠加。若身份、表情、人数或互动姿态漂移，废弃生成结果并降级为本地 Look。
5. 每次运行保存一份可重放的 `render-plan.json`。Directed Revision 只修改被点名的字段，并始终从归一后的 Source Photo 或已验收的无字 Strong Look 底图重新渲染，不在上一张有字成品上累积编辑。

这条边界同时满足 Identity Fidelity、中文准确性、本地交付和可定向修改；也与参考项目的“运行目录 + 分析清单 + 门控 + 脚本 + 最终文件”结构保持一致，但把人物照片的默认优先级改为“身份与真实文字先于生成式视觉增值”。

## 为什么不能把正式成图全部交给图像模型

Codex 内置图像生成使用 `gpt-image-2`，支持把参考图作为编辑或视觉指导；官方也建议定向修改时明确哪些内容要变、哪些保持不变。[OpenAI Codex 图像生成文档](https://learn.chatgpt.com/docs/image-generation)

但“高保真输入”不是像素锁定。OpenAI 的 API 文档说明 `gpt-image-2` 会以高保真处理输入，同时明确：蒙版只是提示引导，未必精确遵守形状；模型仍可能在文字放置与清晰度、重复角色的一致性、精确构图上失手。[OpenAI 图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)

视觉理解同样适合做语义判断，不适合单独做精确坐标真源。官方列出的限制包括精确空间定位、计数、旋转图像、非拉丁文字与输入缩放；对坐标敏感的任务应使用支持时的 `original` detail，并维护缩放后坐标到原图的映射。[OpenAI Images and vision](https://developers.openai.com/api/docs/guides/images-vision)

因此，以下能力不应委托给生成模型：

- 最终中文逐字准确性；
- 人脸与关键手势的硬禁排；
- 气泡边界、尾线落点和文字框的像素级碰撞；
- 隐私元数据剥离；
- Directed Revision 中“其他像素不变”的保证。

官方也建议对生产关键的密集文字逐字检查并在设计工具中完成。[OpenAI Codex 图像生成文档](https://learn.chatgpt.com/docs/image-generation) 对本 Skill 而言，这个“设计工具”应是仓库内可测试、可重放的本地合成器。

## 候选方案比较

| 方案 | Identity Fidelity | 中文准确性 | Directed Revision | 依赖与失败面 | v1 结论 |
| --- | --- | --- | --- | --- | --- |
| 全图生成式编辑 | 无法保证像素级身份与蒙版边界 | 模型仍可能错字或错位 | 可多轮，但有漂移风险 | 工具可用性、额度、延迟、审核、随机性 | 不作为正式默认路径 |
| Pillow 全本地合成 | 不改变人物几何，结果可重放 | 真字符串 + 字体 cmap + 实测边界 | 字段级修改后可重渲染 | 依赖小；需自建中文断行与版式求解 | **正式默认路径** |
| Pillow + OpenCV 本地合成 | 同上，且可提供人脸框与可选前景蒙版 | 同上 | 同上 | 增加 OpenCV 与模型资产；检测仍可能漏检 | **v1 标准安装路径** |
| MediaPipe 人脸/人像分割 + Pillow | 可输出人脸框或分割 mask | 同上 | 同上 | 另需任务模型与较重运行时 | v1 不纳入核心，后续评估 |
| 生成无字底图 + Pillow 字层 | Strong Look 有身份漂移风险，但中文与布局可控 | 准确 | 文字修改无需重新生成 | 生成工具失败时需降级 | **仅显式 Strong Look** |

## 推荐管线

### 1. 运行目录与不可变输入

沿用参考项目的产物分层：

```text
output/photo-dialogue/<run-id>/
  inputs/
    source-normalized.png
    strong-look-base.png        # 仅可选支线出现
  analysis/
    preflight.json
    scene.json
    safe-regions.json
    safe-regions-preview.png
    render-plan.json
    validation.json
    readback.md
  drafts/                       # 仅用户要求探索时使用
  final/
    finished.png
  revision-history.json
```

原始 Source Photo 只读。首先用 Pillow 的 `ImageOps.exif_transpose()` 应用 EXIF Orientation 并移除方向标签；如原图带 ICC profile，则用 `ImageCms` 转换或保留明确的 sRGB 输出配置。[Pillow ImageOps](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html) [Pillow ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html)

`preflight.json` 只记录尺寸、格式、方向变换、色彩处理、文件哈希和“是否发现隐私元数据”，不记录 GPS 值。分析缩图必须保存缩放比例；后续坐标统一换算回归一原图像素。

### 2. 场景理解与安全区域

Codex 读取高细节 Source Photo，并写 `scene.json`：可观察人物数量、粗略人物区域、脸部朝向、视线、手势、人物间动作、重要物件、候选负空间及置信度。人物关系只来自 Scene Description；图像观察不能升级为关系或身份事实。

像素级人脸框由 OpenCV `FaceDetectorYN` + YuNet 完成。OpenCV 的接口返回人脸边界、五个面部关键点与检测分数；官方示例所需检测模型约 338 KB。[OpenCV FaceDetectorYN 教程](https://docs.opencv.org/5.0/tutorials/dnn/dnn_face/dnn_face.html) YuNet 上游说明其模型目录采用 MIT License，并公开 WIDER Face 验证集结果；模型资产是否随仓库分发仍由许可证决策票最终确认。[OpenCV Zoo YuNet](https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/README.md)

v1 **只做检测，不做人脸识别、不生成 embedding、不跨照片比对人物**。每个人脸框按脸尺寸和输出尺寸膨胀为头部禁排区；再与 `scene.json` 中的身体、拥抱、牵手、抱婴儿等关键动作区合并。安全区的用途仅是版式避让，不是身份识别。

当版式确实需要人物前后层关系时，可用人工/模型给出的宽松矩形或多边形作为 GrabCut 种子生成候选 subject mask，并必须输出红色覆盖预览。OpenCV 官方将 GrabCut 定义为带矩形与修正笔画的交互式前景提取，且示例显示初次分割会漏掉头发等前景，因此它不能成为无复核的默认真源。[OpenCV GrabCut 教程](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html)

安全降级顺序：

1. 人脸框 + 语义动作区；
2. 只有可靠人脸框时，扩大禁排区并禁用穿插；
3. 检测不到脸、多人严重重叠或置信度不足时，改用无尾巴的边缘旁白栏或扩展画布，不猜 speaker anchor；
4. 没有合法空间时硬失败，不把文字压到脸上。

### 3. 可重放的 `render-plan`

`render-plan.json` 是 Directed Revision 的唯一渲染真源，至少包含：

```json
{
  "schema_version": 1,
  "source": {"sha256": "...", "size": [0, 0]},
  "canvas": {"size": [0, 0], "source_placement": [0, 0, 0, 0]},
  "safe_regions": [{"id": "face-1", "kind": "face", "polygon": []}],
  "voices": [{"id": "voice-1", "speaker": "person-1", "text": "...", "mode": "inner"}],
  "layout": {"recipe": "...", "elements": []},
  "look": {"id": "...", "parameters": {}, "seed": 0},
  "typography": {"font_ids": [], "locale": "zh-CN"},
  "output": {"format": "PNG", "strip_metadata": true}
}
```

自然语言修改必须先编译为字段补丁，例如“这句太肉麻”只改 `voices[voice-1].text`，“气泡别挡住奶奶”只增加或扩大对应安全区并重求该布局。没有被点名的 Voice Element、Look token、画幅和人物锚点保持不变。每次都从 `source-normalized.png` 重渲染，避免 JPEG 重压缩和编辑误差累积。

### 4. 中文与气泡的确定性排版

Pillow 可以在 RGBA 图层上绘制透明文字，随后 alpha composite；`rounded_rectangle`、`polygon`、`line` 可以构成气泡和尾线，`textbbox` / `multiline_textbbox` 可以用实际字体测量像素边界。[Pillow ImageDraw](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html)

渲染前必须完成四个硬检查：

1. 对文本做 NFC 归一化；Python `unicodedata.normalize()` 提供标准 Unicode 归一形式。[Python `unicodedata`](https://docs.python.org/3/library/unicodedata.html)
2. 用 FontTools `TTFont.getBestCmap()` 检查每个 code point 是否存在于主字体或声明的 fallback 中；缺字不得静默渲染为豆腐块。[FontTools `TTFont`](https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html)
3. 逐个候选字号计算真实 `textbbox`，再生成换行、内边距、尾线和气泡几何；不能按字符数估宽。
4. 中文断行遵守 UAX #14，并实现简体中文的基本行首行尾禁则。Unicode 把换行机会定义为有顺序的规则且允许语言定制；W3C CLREQ 明确列出了不能出现在行首的结束标点和不能出现在行尾的开始标点。[Unicode Line Breaking Algorithm](https://unicode.org/reports/tr14/) [W3C 中文排版需求](https://www.w3.org/International/clreq/)

当前 Codex bundled Python 的只读检查结果为 Pillow 12.3.0、NumPy 2.3.5，FreeType 与 LittleCMS 可用，但 RAQM、OpenCV、FontTools、MediaPipe 均不在同一运行时中。故 v1 只承诺**横排简体中文**；不能依赖 RAQM 自动解决中文断行，也不要在 v1 暗示完整竖排能力。

字体必须由 Skill 自带且通过许可证决策，不依赖用户机器恰好安装的系统字体。运行时的 fallback 顺序必须固定，实际字体文件哈希写入 `render-plan`；这样同一计划在兼容环境中才能得到相同字形与边界。

### 5. Look 与 Strong Look

默认 Look 是可重放的局部设计动作，不是给整图蒙一个不可解释的滤镜：从 Source Photo 采样色板，用固定参数控制色温、对比、饱和、暗角、颗粒、局部压暗/提亮、纸纹或背景模糊；随机颗粒必须把 seed 写入计划。Pillow 提供 3D LUT、Gaussian blur、UnsharpMask 等可组合的本地滤镜能力。[Pillow ImageFilter](https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html)

默认 Look 不改变人物几何、五官、表情、年龄线索、身体比例、服装或互动动作。需要遮罩的局部处理只能使用已验收的 mask；mask 不可靠时少做效果，而不是扩大生成式修改范围。

Strong Look 的固定顺序：

```text
Source Photo
  -> imagegen 生成无字 Strong Look 底图
  -> 人工/视觉 readback：人数、脸、表情、服装、手势、构图
  -> 通过才写 strong-look-base.png
  -> Pillow 叠加最终中文与图形
```

图像模型调用必须明确：Source Photo 是身份与内容真源；不得添加任何文字；点名需保持的人数、脸、表情、服装、手势和画幅。官方建议定向编辑一次只改一个元素并重复必须保持的要求；这能降低风险，但不是 Identity Fidelity 保证。[OpenAI Codex 图像生成文档](https://learn.chatgpt.com/docs/image-generation)

不要依赖图像模型蒙版保护脸，因为官方说明蒙版不一定精确遵守形状。[OpenAI 图像生成指南](https://developers.openai.com/api/docs/guides/image-generation) 若 Strong Look 失败，则回退到同名或相近的本地确定性 Look；没有安全的本地等价项时，报告无法满足，而不是交付身份已漂移的图。

### 6. 输出与隐私

默认输出 PNG，以避免对白边缘被有损压缩并保持跨次重渲染稳定；只有用户要求更小照片文件时才另导出 JPEG。输出保持 Source Photo 的方向与主体构图；平台比例适配优先 pad 或增加叙事边栏，不为填满画幅裁掉脸和关键动作。

成品不传递原 EXIF、XMP、GPS 或设备信息。Pillow 的格式文档说明，JPEG 与 PNG 的 EXIF/ICC 等元数据需要在保存时显式传入；实现应只显式写入经过确认的 sRGB ICC，不传原 EXIF/XMP，并在 `validation.json` 重新打开文件验证元数据为空。[Pillow 图像格式文档](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)

v1 核心输入承诺 JPEG、PNG、WebP。HEIF/HEIC 不是 Pillow 核心格式，官方把支持列为第三方插件；可提供 `pillow-heif` 可选适配器，缺失时清楚提示用户转为 JPEG/PNG，不静默调用系统专属转换工具。[Pillow 第三方插件](https://pillow.readthedocs.io/en/stable/handbook/third-party-plugins.html) [pillow-heif 上游](https://github.com/bigcat88/pillow_heif)

## 依赖边界

为与参考项目保持一致，标准 v1 环境采用同样的四层基础：

```text
Pillow>=10.0,<13
numpy>=1.26,<3
opencv-python-headless>=4.9,<5
fonttools>=4.55,<5
```

此外有一个经过许可证确认并固定哈希的 YuNet ONNX 检测模型。`pillow-heif` 是可选输入适配器，不进入核心依赖。MediaPipe、Torch、Transformers、云端分割服务和人脸识别模型均不进入 v1。

依赖策略也沿用参考项目：提供只读 `check_dependencies.py`；脚本优先使用当前解释器或调用者工作区的兼容 `.venv`；不得自动全局安装。缺 OpenCV 时仍可运行 Pillow 降级路径，但只能选边缘旁白类 Recipe；缺 Pillow、字体或 FontTools 时正式渲染硬失败。

## 门控与失败回退

| 失败 | 门控/检测 | 回退 |
| --- | --- | --- |
| 文件损坏、超大或方向不明 | 解码、像素上限、EXIF transpose 后尺寸 | 停止并要求可读副本 |
| HEIC 解码器缺失 | 格式能力检查 | 提示导出 JPEG/PNG；不改原文件 |
| 检测不到脸或人脸数量可疑 | YuNet 结果与 Codex 粗计数交叉检查 | 边缘旁白栏、Group Narration、无尾气泡 |
| 人脸/动作区无排版空间 | 气泡与膨胀安全区碰撞检测 | pad/扩画布；仍失败则缩短 Voice Element 或停止 |
| 字体缺字 | cmap 全覆盖检查 | 固定 fallback；仍缺字则硬失败，不替换原文 |
| 中文行首行尾违规或溢出 | 真实 bbox + CLREQ 规则 | 重断行、降字号到下限、换 Recipe；不裁字 |
| 背景对比不足 | 文本区域亮度/对比检查 | 提高气泡不透明度或使用实色旁白栏 |
| Strong Look 工具不可用、超时或被审核拦截 | 工具返回状态 | 本地确定性 Look；如无等价项则说明未完成 |
| Strong Look 身份/人数/表情/动作漂移 | 生成后视觉 readback | 丢弃生成底图，退回本地 Look |
| 只改文案却触发全图变化 | render-plan diff | 阻止提交；从原图只重画受影响元素 |
| 输出携带 EXIF/GPS/XMP | 保存后重新读取元数据 | 阻止交付并重新导出 |

## v1 验收标准

后续实现票应把以下内容变成自动测试或明确门控：

- 在同一锁定运行时与平台中，同一 Source Photo、`render-plan`、字体文件与 seed 重渲染得到相同像素哈希；跨 Pillow 或 FreeType 版本只比较结构与视觉门控，不承诺像素哈希一致。
- 测试语料中的每个中文 code point 都能由声明字体链覆盖；任何缺字都使命令非零退出。
- 每个 Voice Element 都有对应渲染 bbox，且位于画布内、不与硬安全区相交、不违反最小内边距。
- 断行测试覆盖逗号、句号、问号、引号、括号、书名号、破折号、省略号以及中西文混排。
- Directed Revision 的计划 diff 只包含被点名字段；文字修改不会调用 imagegen。
- 输出 PNG 重新打开后尺寸、方向、ICC 与预期一致，EXIF/GPS/XMP 均不存在。
- YuNet 缺失、零脸、低置信度、多人重叠、无负空间时都能得到可解释的降级结果或明确硬失败。
- Strong Look 测试只验证调用清单、无字约束、读图门控与失败回退；不把随机生成像素作为确定性单元测试。

## 明确不在本票决定的事项

- 具体字体家族、字体文件分发方式与第三方参考素材许可；由许可证决策票决定。
- Voice Element 的语言风格、关系推断规则和未成年人内容政策。
- Recipe 的视觉数量与具体气泡造型。
- 生产 Skill 的脚本文件名和最终 JSON Schema 细节。
- 动画、配音、嘴型驱动、云端服务与跨照片人物识别。

这些事项不会改变本票的核心能力边界：**默认保留原图并在本地准确合成；生成式编辑只负责可选无字底图；所有修改由可重放计划驱动。**
