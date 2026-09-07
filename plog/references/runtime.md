# 环境、格式和失败处理

## 选择环境

目标为 macOS/Linux 的 CPython 3.11–3.13，基础 Pillow>=12,<13。依次检查当前可用解释器、用户明确的 CAP_PYTHON、当前目录向上最近的 .venv；只有版本与功能自检通过才使用，全程保持同一解释器。缺依赖时说明需要隔离安装；已明确要求安装技能和必要依赖就承接授权，否则先取得安装授权。使用项目或用户指定的虚拟环境，不能全局装包或静默联网。

基础精确版本与哈希在 requirements.lock，HEIF 可选项在 requirements-heif.txt / requirements-heif.lock。用选定合格解释器创建 venv 后，安装锁定依赖，例如 `python -m pip install --require-hashes -r requirements.lock`（路径须解析为当前安装技能的文件）；无 pip 可用已存在的 uv 指定该 venv 安装。不把开发依赖装进运行环境。

设置 PD_PYTHON 为合格 venv 解释器、PD_SKILL 为当前 SKILL.md 所在绝对目录。先在已有可写私密目录执行：

```sh
"$PD_PYTHON" "$PD_SKILL/scripts/self_check.py" --workspace "$PD_PRIVATE"
```

自检真实写入/读取 JPEG、PNG、WebP、EXIF 方向与无元数据 PNG，再清理探测文件；HEIF 另作编解码探测。自检不联网、不做收费生成，host_image_service=unverified 是正常的独立状态。完整创作还需通过 [Agent 接入](agents.md) 确认读图、图片编辑、对照分析和当前会话文件交付。可用宿主原生工具或已配置的兼容 API；本地自检不证明远程服务可用。

## 输入与准备

只接受静态 JPEG、PNG、WebP；安装且功能自检通过的 pillow-heif 才启用 HEIC/HEIF。动画、多页、RAW、损坏图不默取首帧。HEIF 不可用时请用户提供基础格式，不调用系统转换器。仅支持可安全归一的色彩：有效 ICC 转换为 sRGB；无 profile 的常见 RGB/灰度按 sRGB 解释，未知 CMYK/高位深或损坏 ICC 明确请求 sRGB 替代图。

inspect 解码并返回归一方向尺寸及源 SHA-256。prepare 生成 RGB/RGBA、无源元数据的处理副本。所有准备/导出目标必须不存在。CLI prepare 输出由调用者在本次受控临时目录管理；Python prepare 上下文接口自动清理自己创建的副本。

```sh
"$PD_PYTHON" "$PD_SKILL/scripts/photo_files.py" inspect "$PD_SOURCE"
"$PD_PYTHON" "$PD_SKILL/scripts/photo_files.py" prepare "$PD_SOURCE" --destination "$PD_TEMP/prepared.png"
```

PD_TEMP 用私密工作区内新建的临时目录，权限 0700；只删除该次自己创建的文件。读图工具应检查归一后的原图；独立视觉服务也是照片接收方，须被当前授权覆盖；首次生成工具仅收到该处理副本与必要叙事。修改的唯一编辑底图按 [执行修改](revisions.md#执行修改) 准备。

## 输出和中断

候选先看图核验，再用 revision_record append 导出与提交。export 会清除所有源信息块（EXIF/IPTC/XMP/定位/设备/私有文字等），复读 PNG 并核对源校验；不会替换已有目标。所有导出保持候选尺寸；原方向、用户画幅和可读性由交付者核验，不能仅凭导出成功通过。

工作目录应在技能与仓库外。这里的本地指执行 Agent 所在的电脑、服务器或沙箱，不一定是用户手机。先确认会话与脚本能访问同一文件，沙箱退出后需保留的作品应放在已配置的持久位置。用户指定目录优先；默认在 ~/Pictures/PhotoDialogue 下创建日期加随机标识的新目录。无权限时报告并请用户指定位置，不能默存仓库。首次目录须为空，遇到未知内容不会覆盖。

append 先独占锁定作品目录，写入新 PNG，再原子替换记录。常规写入故障删除本次未登记 PNG、保留旧版和记录；操作系统突然终止可能留下未登记文件，下次停止并说明冲突，不能把孤立文件当作合格版本。已有登记版本仍可 select/recover；不擅自清理不明文件。没有持久诊断日志、源图备份或数据库。

## 失败与清理

超时、拒绝、不可用、损坏结果或核验失败时，说明实际问题并等待新指示；原因不明就说明不确定，不推断服务故障。可展示明确标为“未通过”的候选，但不标为成品或下载成功。失败不追加版本、不改变 current_version；调用次数按 [生成流程](../SKILL.md#5-生成与核验)，重试与停止按 [请求分流](../SKILL.md#1-分流请求) 执行。

成功、失败或停止均清理本次自建暂存源副本、细节 JSON、对照图及预览衍生物；保留用户原图、历史成图和宿主拥有的文件。私密照片、文字、提示词和审阅细节留在用户指定的本地私密位置，不写入技能目录、项目仓库、公共附件或遥测。持久内容仅为成图和最小版本记录；不保存原图副本、永久授权、源元数据、身份档案、敏感推断或全量对话。
