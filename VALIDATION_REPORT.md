# 交付验证报告

日期：2026-11-11。运行环境：Windows / Python 3.14.7；完整 YAML 检查使用 PyYAML 6.0.3。

## 已执行并通过

- 项目静态检查：恰好三个指定 Skill、必需文件、name/description frontmatter、本包使用的 Markdown 相对链接和代码围栏、JSON 文件语法。
- 完整 YAML 解析：研究档案与全部 Markdown frontmatter 使用 PyYAML SafeLoader，并拒绝重复键。
- Codex 随附 skill-creator 的 quick_validate.py：三个 Skill 均返回 `Skill is valid!`。在 Windows 下需 `python -X utf8`，避免校验器默认 GBK 解码中文导致错误。
- Python unittest：17 项通过。包含账本有效输入、缺失/伪造引用、重复 ID、非法字段、缺少来源文件、路径逃逸、行号越界等负向测试，以及故意破坏相对链接的测试。
- 合成 expected-evidence.json：结构与 source_id、文件、行范围检查通过。玩具词元计数结果为 2，属于测试值，不是科学结果。
- 发布打包：ZIP CRC、归档内容与已解压项目文件清单、SHA256 逐文件一致性检查；清单见 MANIFEST.json（清单不对自身哈希）。

## 已审阅的设计约束

研究档案包含用户提供的 S. pombe、Killer Meiotic Drive、Tdk1/Tdk210/Tdk203/Tdk11、蛋白进化与互作、生信、TurboID/邻近标记、AI4BIO；均明确为可编辑偏好，不能作为论文证据。三种模式可独立调用，共享规则和资源须随项目保留。测试数据标为 SYNTHETIC，未进入真实知识库。

## 未执行的验收及限制

未使用真实论文测试，未独立调用模型执行行为验收 case，未验证当前 ChatGPT 账户的 Skill 导入/持久化能力。未实施生物实验、下载或执行作者代码。tests/TEST_PLAN.md 提供这些后续验收的方法与禁止项；不宣称它们已经通过。

自动工具检查的是结构和引用可解析性，不能证明声明与引用语义一致、科学结论正确、图像读取正确或实验可复现。页码/section 等非 L 行号定位仍需人工核对。完整 CommonMark 渲染与任意 YAML 方言不属于基础静态检查范围。

## 本次检查中修正的问题

初轮静态检查发现验证报告链接指向尚未生成的文件，报告生成后重跑通过。完整 YAML 库安装后在受限进程中不可读，改在获准进程完成解析。Codex 校验器首次采用系统 GBK 读取中文失败，改用 UTF-8 后三个 Skill 均通过。以上均不是论文内容验证。
