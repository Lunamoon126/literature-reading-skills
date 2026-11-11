# 科研文献阅读 Skill 系统 · 1.0.0

三个独立 Codex Agent Skills，共用可编辑研究档案和可追溯知识库。默认中文输出，保留英文术语；不包含真实科学结论、预装模型、PDF 解析器或自动文献检索服务。

## 快速安装

1. 完整解压 ZIP，保留隐藏目录 `.agents`。将本文件所在的 `literature-reading-system` 文件夹作为 Codex 项目打开，并在该目录开始会话。无需管理员权限、API 密钥或网络即可阅读本地文本并运行基础检查。
2. 在 Skill 选择器检查三个名称。可输入 `$literature-screening`、`$literature-deep-reading`、`$literature-method-reproduction`。若未刷新，重新打开会话或重启 Codex。
3. 阅读并修改 [研究档案](research-profile.yaml)，将真实论文放进 `knowledge-base/inbox/`。不要把测试文本当作论文。
4. 在项目根目录运行 `python scripts/validate.py` 和 `python -m unittest discover -s tests -v`。Python 3.10+；基础测试仅用标准库。完整 YAML 解析检查另需 `python -m pip install -r requirements-validation.txt`，然后 `python scripts/validate.py --full-yaml`。

合并到已有项目时，将 `.agents/skills/` 下三个完整目录、`research-profile.yaml`、`knowledge-base/`、`scripts/`、`tests/`、验证依赖文件及本 README 一起复制。先处理同名文件冲突，勿盲目覆盖已有档案。共享资源位于 `.agents/skills/_literature-shared/`，该目录没有 SKILL.md，因此不是第四个 Skill。不要只复制三个入口文件。回退时移除本包新增文件即可；先备份自己的论文与笔记。

## 平台兼容性

Codex 项目约定为 `.agents/skills/<skill-name>/SKILL.md`，包含 YAML `name` 和 `description`。每个 Skill 能单独调用，不要求先运行另一个 Skill。它们依赖同一份随包资源，不要求外部 Skill、Zotero 或 MCP。

ChatGPT 桌面端仅在当前账户/版本支持 Skill 导入或使用时适用。若有 Skill 选择功能，可选择导入后可见的 Skill（官方文档描述 `@` 选择）；本项目 ZIP **不是已发布插件，也不保证是任何客户端的一键导入格式**。请按客户端支持的流程导入/打包，并一并提供共享资源、档案和论文。ChatGPT 不会因为本机存在 `.agents/skills` 就自动扫描，也不保证运行 Python、持久写入本地知识库或读取相对路径。没有对应能力时，可把相关 Skill 和共享规则、模板、档案作为文件上下文手动使用并下载结果，这属于手动工作流，不等于安装成功。不得声称已写入无法访问的本地文件。

兼容性依据仅核对官方 OpenAI 文档，日期 2026-11-11，见 [来源与范围](.agents/skills/_literature-shared/references/compatibility.md)。没有验证实际 ChatGPT 账户导入或真实论文行为。

## 调用与编排

| 目标 | 调用 | 产出 |
| --- | --- | --- |
| 多篇快速筛选 | `$literature-screening 对 inbox 中每篇论文按研究档案分流；标记仅摘要可见。` | 筛选卡、依据、可解释分流 |
| 单篇精读 | `$literature-deep-reading 精读指定论文，逐图梳理证据链，区分作者主张与数据支持。` | 精读笔记、声明—证据表、局限 |
| 方法复现 | `$literature-method-reproduction 根据该论文和补充材料形成复现计划，缺参不得补造。` | 参数表、步骤依赖、缺口、验证计划 |

推荐流程：登记来源 → 筛选 → 用户选择精读对象 → 精读 → 对关键方法制定复现计划 → 人工审核 → 知识库综合。也可直接精读或直接复现；不强制三级流水线。筛选结论是工作优先级，不是科研质量排名；不自动下载、执行作者代码或实施实验。

跨篇综合时，按 paper_id 检索已有笔记与证据表，先查覆盖范围，再按研究问题比较相同实验对象/条件。相互矛盾的结果并列记录，不能用多数投票消除。关联笔记写入 `knowledge-base/synthesis/`，保留各论文定位符，不能用档案或旧笔记替代原文证据。重读或新增材料时新增版本/变更记录，并将依赖旧证据的综合笔记标记需复核。

## 知识库与更新

详见 [知识库说明](knowledge-base/README.md)。每篇使用稳定 paper_id；优先复用 DOI/预印本编号匹配，但不同版本保留来源版本与校验值，不盲目合并。没有编号时用本地 ID，禁止虚构 DOI。原文和原始提取文本留在 sources，生成内容写在 notes；测试数据只在 tests。

研究档案的 `context` 来自用户陈述，是默认兴趣；Tdk1/Tdk210/Tdk203/Tdk11 仅为用户提供的标识，不默认是别名、同源物或已证实功能。修改档案时更新 `profile_version` 与 `updated`，在新笔记记录版本和变动；旧笔记不静默改写。修改偏好不构成论文事实变化。可按实际需求增删关键词、预算及优先问题。

## 验证与限制

[测试计划](tests/TEST_PLAN.md) 区分静态检查、工具测试及需要实际模型执行的验收。自动检查验证结构、引用完整性和部分证据约束，无法证明论文理解正确。交付检查结果见 [验证报告](VALIDATION_REPORT.md)。科学性须结合原文人工审阅；本包不提供任何真实 Tdk 功能结论。
