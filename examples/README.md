# 示例与验证范围

`harbor-clock/` 是之前四章短篇的创作与二稿流程示例，保留原文和历史报告。
原报告中的 “Structural validation passed” 指旧版检查，不代表通过当前协作验收。
它没有实际五角色分工记录，也没有新版 `workflow.json`；不要补造身份、审稿或验收。

可以只读测量它：

```sh
python3 -B skills/longform-fiction-studio/scripts/inspect_project.py examples/harbor-clock --json
```

实测正文纯汉字为 2,758，正文非空白字符（含标点）为 3,229；与旧报告使用
的整文件字符数不同。原要求的口径需澄清，不能为了通过而改成更宽松的口径。
按新版执行 `validate_project.py` 将明确要求迁移；这是预期行为。

可执行的三章协作状态回归样例在 `verification/test_project_validation.py`。
它在临时目录构造正文、角色、问题和审稿记录，测试分批接续、返修复核、
会话交接、版本失效、重复与字数边界。**这些是合成测试记录，不是真实文学
审稿，也不证明长篇创作质量。** 临时目录自动删除。

```sh
python3 -B -m unittest discover -s verification -v
```

真实作品请放在被忽略的 `novels/` 下，用真实角色执行审读并保存证据。
