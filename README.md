# Novel Creator

Novel Creator 是一套可移植的 AI 长篇小说创作流程和技能包。

它的目标不是让 AI 一次性靠超长上下文写完整部小说，而是让 AI 像一个小型创作生产组一样工作：先规划，再分章写作，再持续更新人物、关系、时间线、情节线和连续性记录，最后做整体验收。

核心原则：不要依赖某个 AI 的隐藏记忆。项目文件才是长期记忆。

## 给 AI 的启动指令

无论是新项目还是旧项目，都先让 AI 读取统一入口：

```text
请先读取 AI_START_HERE.md。你需要自动判断这是新项目还是已有项目：
如果是新项目，按我的题材、字数和章节数创建完整小说项目，先给我故事设计；
等我说“开始”后，再逐章完成正文，并在最后完成校对、质量评估和交付。
如果是已有项目，检测 PROJECT_ENTRY.md，然后从当前状态接手，直到完成剩余章节和最终 QA。
```

## 新项目使用方式

你可以这样对 AI 说：

```text
读取 AI_START_HERE.md。
我要写一部中篇小说，现实悬疑题材，10 个章节，每章 6000-8000 字。
请先构建完整项目文件和故事设计，等我确认后再开始逐章写作。
```

AI 应该先创建：

```text
novels/<作品名或 slug>/
```

然后填充项目控制文件、章节卡和入口文件。你修改完故事设计后，说“开始”，AI 就应该逐章写作，并在每章或每批章节后更新状态。

## 旧项目接手方式

如果另一个 AI 已经写到一半，你可以这样说：

```text
读取 AI_START_HERE.md。
这是已有项目：novels/<项目名>。
请检测 PROJECT_ENTRY.md，并根据项目当前状态继续完成剩余章节，最后做整体验收和交付。
```

如果项目里有 `PROJECT_ENTRY.md`，AI 会知道这是旧项目，并按入口文件接手。

如果没有 `PROJECT_ENTRY.md`，但已经有 `00-project-overview.md`、`chapters/`、`chapter-cards/` 等文件，AI 应该先补入口文件，再继续。

## 仓库结构

```text
AI_START_HERE.md
README.md
skills/
  longform-fiction-studio/
    SKILL.md
    references/
```

生成的小说项目默认放在：

```text
novels/
```

`novels/` 默认被 `.gitignore` 忽略，避免把正文草稿和测试作品误提交到技能包仓库。

## 使用方式

clone 仓库后，可以直接让 AI 读取：

```text
AI_START_HERE.md
```

AI 会根据入口文件创建 `novels/<项目名>/` 以及所有 Markdown 控制文件和目录。

项目验收按 `AI_START_HERE.md` 和 `SKILL.md` 里的清单检查。

## 这套流程会强制维护什么

- 统一启动入口：`AI_START_HERE.md`
- 每个小说项目自己的入口：`PROJECT_ENTRY.md`
- 项目概览：`00-project-overview.md`
- 人物设定表：`01-cast-bible.md`
- 人物关系图谱：`02-relationship-map.md`
- 时间线：`03-timeline.md`
- 主线和支线：`04-plot-lines.md`
- 章节路线图：`05-chapter-roadmap.md`
- 连续性账本：`06-continuity-ledger.md`
- 风格与叙事声音：`07-style-and-voice.md`
- 当前状态与情节线热度：`08-active-state.md`
- 批次文学修订：`09-literary-revision.md`
- 每章任务卡：`chapter-cards/`
- 正文目录：`chapters/`
- 最终质量报告：`QUALITY_REPORT.md`
- 叙事边界检查：防止正文出现作者说明、读者称呼、控制卡术语或写作意图说明

## 工作标准

一个小说项目不是“有正文”就算完成。它至少要满足：

- 所有计划章节都存在
- 字数符合用户要求
- 人物关系、时间线和情节线没有明显断裂
- 关键事实有证据状态：`observed`、`claimed`、`inferred`、`confirmed`、`contradicted`
- 支线没有无计划冷掉
- 每 3-6 章做一次文学修订检查
- 正文没有突破第四面墙
- 完成最终质量报告
- 手动验收清单通过

## 重要规则

不要让 AI 靠隐藏记忆继续写。每次新 AI 接手时，都先读：

```text
AI_START_HERE.md
```

然后由它自动判断是新项目还是旧项目。旧项目再读取对应的：

```text
PROJECT_ENTRY.md
```
