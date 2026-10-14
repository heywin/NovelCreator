# Novel Creator

Novel Creator 是一套可移植的 AI 长篇小说协作流程和技能包。主控编辑拆解任务，故事策划设计场景，正文作者写作，两类编辑独立审读，主控根据证据验收。可以每次完成一章或一个批次，再由其他会话接续。

项目文件是长期记忆；正文存在、字数达到或模型声称完成，都不等于已经验收。

## 快速开始

把仓库交给 AI，并使用下面的指令：

```text
请读取 AI_START_HERE.md。
我要创作一部现实悬疑小说，共 10 章，每章 6000—8000 个汉字，
全书 60000—80000 个汉字。先完成故事设计、角色分工和前三章的场景任务。
我确认设计后，再完成前三章的写作、双编辑审读、修订和主控验收，随后停下交接。
```

已有项目可以这样继续：

```text
读取 AI_START_HERE.md，接手 novels/<项目名>。
先核对实际正文与任务状态，修复当前批次的未解决问题，再完成下一批 3 章。
沿用已确认的创作合同，批次验收后汇报并停止。
```

角色可由不同会话承担；具备且获准使用代理委派时，也可以由主控协调代理。流程本身不自动启动 AI、不提供后台调度，也不额外授予外部操作权限。

## 五个角色如何配合

| 角色 | 交付 | 权限边界 |
| --- | --- | --- |
| 主控编辑 `supervisor` | 任务拆解、分配、冲突裁决、验收和交接 | 唯一负责合并正式状态与验收记录 |
| 故事策划 `planner` | 全书结构、人物弧线、章节卡、场景预算 | 提议设定变更，由主控合入 |
| 正文作者 `writer` | 当前任务的正文、偏离计划说明、状态变更建议 | 不验收自己的正文 |
| 连续性编辑 `continuity_editor` | 时间、知识、物件、动机与因果检查 | 问题必须定位到正文，修后复查 |
| 文学编辑 `literary_editor` | 可读性、声音、情感、节奏和重复检查 | 同时承担冷读和文字编辑视角 |

执行顺序：任务与场景设计 → 写作 → 字数和重复检查 → 两类编辑审读 → 修订 → 复查 → 主控验收并回写状态。依赖前文的章节顺序写；获准委派时，两类审读可以并行。详见[协作协议](skills/longform-fiction-studio/references/collaboration-protocol.md)。

## 项目文件与工具

新作品默认放在 `novels/<项目名>/`，该目录由 `.gitignore` 排除，避免私人正文误入技能仓库。`examples/` 是公开的流程示例，不能作为未核实作品已经验收的依据。

每个项目保留人物、关系、时间线、情节线、连续性和风格 Markdown 文件，并新增 `workflow.json` 作为创作合同、任务、角色、审读、问题与验收的结构化台账。详见[项目模板](skills/longform-fiction-studio/references/project-template.md)和[字段规范](skills/longform-fiction-studio/references/workflow-schema.md)。

所有脚本只使用 Python 标准库，在仓库根目录运行：

```bash
# 只读检查旧项目：真实字数、正文哈希和重复情况
python3 -B skills/longform-fiction-studio/scripts/inspect_project.py novels/<项目名> --json

# 创建 workflow.json 和任务；不覆盖正文、不补造审读或验收记录
python3 -B skills/longform-fiction-studio/scripts/init_workflow.py novels/<项目名> --chapters 10 --chapter-min 6000 --chapter-max 8000 --total-min 60000 --total-max 80000 --count-mode han

# 检查当前批次：尚未完成后续章节不等于交付失败
python3 -B skills/longform-fiction-studio/scripts/validate_project.py novels/<项目名> --stage progress

# 全书交付检查
python3 -B skills/longform-fiction-studio/scripts/validate_project.py novels/<项目名> --stage release --json
```

初始化后，由主控按实际参与者分配角色并填充任务；初始化本身不表示可以开始写作。`han` 统计正文汉字，`nonspace` 统计正文非空白字符并含标点。两种口径都排除 Markdown 标题；开始前锁定口径、单章范围与总量，不能在不达标时悄悄切换。

## 验收要求

- 场景任务说明进入状态、冲突、选择、后果、预算和完成条件；不足字数通过补全场景扩写。
- 检查章内及跨章重复，禁止复制段落填充字数。
- 审读记录绑定实际正文版本；改稿后重新审读，不能沿用过期通过结论。
- 作者提出修复，编辑复查，主控验收；高严重度和致命问题不能靠延期绕过。
- 主控回写连续性、时间线、人物关系、当前状态和下一任务，之后才能写依赖这些状态的章节。
- 每批次总结文学质量；全书交付还需要两类编辑对全书当前版本的最终审读和发布校验。

程序能检查可执行约束与记录一致性，不能证明审稿人真的读过正文，也不能保证文学感染力。主控需核对审读证据、场景因果和修复效果，质量报告应区分程序结果与编辑判断。

## 回归验证

无需安装第三方包，建议 Python 3.10 或更新版本：

```bash
python3 -B -m unittest discover -s verification -v
```

测试使用临时三章项目验证阶段交接、修订复查、审稿版本失效、角色接手、字数与重复反例。测试记录为合成数据，不代表真实文学审稿。[历史示例说明](examples/README.md)解释旧作品与新版验收的区别。

仓库附带 [GitHub Actions 配置模板](verification/github-actions.example.yml)，目前尚未启用自动测试。拥有 workflow 写入权限的维护者可将它复制为 `.github/workflows/validate.yml` 后提交，启用 Python 3.10 / 3.13 的推送及 PR 检查。当前上传凭据缺少该权限，所以模板按普通文件交付。
