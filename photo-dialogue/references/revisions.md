# 定向修改、恢复与附加导出

## 选择基准

用户说改文字、减轻氛围、移动文字或从旧版继续时，先读取其明确指定的作品目录。默认当前最新 Accepted Version；指定旧版则 `select --version v001`，使用那个版本的确切文字、声音归属及 visual_intent。选择是只读操作，不会把“看过旧版”当成新接受版本。找不到所选版本就说明缺口，不换成最新。

`recover` 还需要用户提供/指定的原图 `--source`。记录中的路径可展示给用户确认，却不是任意读取其他私人目录的授权；仅当当前上下文已明确指定该原图时直接承接。原图 SHA-256 相同才可更新移动后的引用；缺失/变更请用户提供正确原图，不扫描、不用生成图替代。记录缺失时已有 PNG 可继续查看；精确修改需原图、所选成图、必要文字/视觉说明。未知 schema、坏父子关系、越界/符号链接输出引用都停止恢复。

## 执行修改

简述理解到的范围后执行，无实质歧义不重复批准。仅文案：保留人物、光色、主要构图，文字变长时只调整必要排版。仅氛围：保留确切文字、人物及主要构图。移动文字：保留文案、声音归属与整体 Look，避开用户指出的手/脸/互动。多项明确要求可合并。

以原图和所选旧版共同约束宿主编辑，准确区分二者用途；原图始终是人物真值。成功候选需重查身份、中文、目标变化和未请求变化的重要决定；不要求逐像素不变，也不能接受实质无关改动。失败不追加、不改变 current_version。明确重试才增加一次调用；停止后不接受迟到结果。

## 最小记录与命令

下面命令使用已选解释器与本技能绝对目录（`PD_PYTHON`、`PD_SKILL`），变量内容来自实际环境。所有命令的 `--help` 提供参数细节。

```sh
"$PD_PYTHON" "$PD_SKILL/scripts/revision_record.py" select "$PD_WORK" --version v001
"$PD_PYTHON" "$PD_SKILL/scripts/revision_record.py" recover "$PD_WORK" --source "$PD_SOURCE" --version v001
"$PD_PYTHON" "$PD_SKILL/scripts/revision_record.py" append "$PD_WORK" --source "$PD_SOURCE" --source-sha256 "$PD_SOURCE_SHA256" --candidate "$PD_CANDIDATE" --details "$PD_DETAILS" --version v001
```

PD_SOURCE_SHA256 必须是本次生成前 inspect 返回的原图校验，不能在生成后重新取值绕过变化检测。首次 append 省略 --version；修改省略则基于当前最新接受版本。append 仅供已完成视觉核验的候选使用，脚本本身不判定人物或文字正确。PD_DETAILS 是本次私密临时区的 JSON，成功/失败后清理，只含：

```json
{
  "change_target": "仅移动文字，避开手部",
  "voice_elements": [
    {"text": "茶先喝一口", "kind": "narration", "attribution": "narrator"}
  ],
  "visual_intent": "保持冷色窗光、人物和茶杯；旁白移至右上留白"
}
```

kind 为 confirmed_quote / creative_dialogue / inner_voice / narration。刻意留白用空数组。确切文本与最小归属按版本记录；视觉意图包含需保持的重要决定。完整结构见 [schema](../schemas/revision-record.schema.json)。文件和记录成功后才宣布完成；出现孤立未登记文件时停止并说明，不把它当成当前版本或删除用户文件。

## 按需附加交付

默认只有版本 PNG 和 revision.json。用户要纯文字时运行 export-text，指定新文件，可用 --version；同名目标不会覆盖。无障碍说明依据指定成图的可见内容与必要中性背景生成，存到用户指定的新文件。完整提示词仅当用户要求时提供；历史原文未保留就明确说不可得，若重建必须标“重建提示词，非历史原文”。附加文件不扩展记录 schema，不记永久授权或完整对话。
