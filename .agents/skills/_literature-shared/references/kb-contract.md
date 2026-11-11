# 知识库写入契约

完整项目中，从 Skill 目录向上三级找到项目根，再读 research-profile.yaml 和 knowledge-base/README.md。若移动过 Skill 或环境不能读取文件，先定位用户指定知识库根；无法定位时请求档案或使用显式标记的会话内临时档案。不能假装已读档案。共同规则与模板位于 Skill 同级的 `_literature-shared`。单独调用不依赖其他 Skill 的产出。

为论文分配稳定 paper_id，检查 index.csv 中 DOI/其他标识与版本。新增 sources/<paper_id>/、notes/<paper_id>/，在 sources/<paper_id>/manifest.json 登记文件相对项目路径、sha256、来源版本、获取方式及可读范围；可从 [来源模板](../templates/source-manifest.json) 开始。复制/登记用户提供材料，避免覆盖原件。notes 下按模式创建 screening.md、deep-reading.md、method-reproduction.md；已有内容保留并用版本后缀或变更记录更新。共享 evidence.json 中合并声明时检查 ID 冲突，旧证据失效应标注并保留历史快照。不要改写其他模式的结论以制造一致性。

每条笔记头记录 paper_id、mode、profile_version、source_version、日期、材料覆盖、生成方式及审核状态（draft/reviewed）。筛选后更新 index.csv 的 stage 与 note 路径；精读和复现完成仅表示文档完成，不能标记为实验已成功。方法复现的执行状态独立记录。多篇 synthesis 使用 [综合模板](../templates/synthesis.md) 建立独立文件，链接各来源与版本，禁止无来源跨篇合并。

无本地写入能力时在会话中返回相同结构并说明“未持久化”；不要声称保存成功。可用 Python 时运行 `python scripts/check_evidence.py <evidence.json>`；校验通过只表示结构与引用可解析，不保证语义正确。实际 source path 相对项目根，fixture path 相对 fixture 根，调用 --base 明确指定。验证完成后人工回查 locator。
