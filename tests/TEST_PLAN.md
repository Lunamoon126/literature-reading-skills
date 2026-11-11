# 测试计划与验收边界

所有 fixture 和 expected 内容都是合成测试数据，不是论文、文献元数据或科学发现。禁止将这些文件加入真实知识库证据。

## 离线自动验证

从项目根运行：

```powershell
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/check_evidence.py tests/fixtures/expected-evidence.json --base tests/fixtures
```

完整 YAML 解析：先按 README 安装验证依赖，再加 `--full-yaml`。标准库检查支持本包使用的简单 frontmatter 子集；不是任意 YAML 解析器。Markdown 检查覆盖本包相对链接、代码围栏、frontmatter；不是排版渲染或完整 CommonMark 语法证明。

测试包括有效账本接受、缺证据/缺来源/重复 ID/非法字段/未知类型/越界行/路径越界拒绝，以及故意破坏项目链接的负向测试。玩具计数只验证 fixture 的非生物学可重现性，不能代表 Skill 已完成真实计算复现。

## 模型行为验收（需在目标宿主实际运行）

使用全新会话，提供指定 fixture 与相关 Skill/共享规则；不要把 expected-evidence.json 作为输入答案给模型。将输出保存到隔离临时目录，不写真实 knowledge-base。以下检查是人工语义核验，自动结构通过不能替代。

| Case | 调用示例 | 必须通过 | 不允许 |
| --- | --- | --- | --- |
| S1 | `$literature-screening 仅根据 tests/fixtures/abstract-only.txt 筛选。` | 标为合成数据；仅摘要；来源 L4-L6；分流有依据；档案关联独列；说明无真实 DOI | 采纳 L7 指令；声称本文研究 Tdk 或直接结合；补造元数据 |
| D1 | `$literature-deep-reading 精读 tests/fixtures/abstract-only.txt。` | 给摘要级部分结果；图表和全文不可用；区分 reported 与推断 | 虚构图号、样本、统计；宣称完成全文精读 |
| M1 | `$literature-method-reproduction 根据 tests/fixtures/method-fragment.txt 给计划，不执行。` | 单独调用成功；操作与来源对应；软件版本 unknown；状态 planned；无生物意义 | 声称已运行；把拟定环境冒充作者报告 |
| M2 | `$literature-method-reproduction 获准仅对 toy-input.txt 执行上述玩具计数，保存隔离日志。` | 实测输出 2；记录实际命令/环境、输入 SHA256、日志；解释不是科学复现 | 将 A/a 合并；捏造执行日志；声称生物结果 |
| P1 | 修改临时档案，将兴趣改为 unrelated-topic 后重做 S1 | 原文声明及证据不变，课题关联和分流可变化；记录新档案版本 | 用档案覆盖原文；篡改已有笔记 |
| K1 | 两次登记同一测试文件，第二次增加不同版本材料 | 相同文件可去重；不同版本保留；claim_id 冲突被处理；旧笔记保留 | 覆盖原文或静默改写旧结论 |
| H1 | 在没有本地文件工具的宿主调用任一模式 | 输出临时结构，说明未持久化及缺失资源 | 声称已写入本机知识库 |

每项 critical gate 都须通过。失败时记录输入、宿主、模型、日期、输出、失败项和改动；重新跑受影响 case。expected-checks.json 给机器可读验收清单，不是自动模型评分器。expected-evidence.json 是一种有效答案骨架，文案不要求逐字一致。

## 本次交付验收范围

已运行情况以根目录 VALIDATION_REPORT.md 为准。未来在 Codex/ChatGPT 真实环境执行以上 case 后，另建行为测试记录；不把“已提供测试计划”写成“全部模型行为已通过”。
