# 统一文献知识库

inbox 保存待登记文件；sources 保存已登记原始材料（不要修改原件）；notes 保存各模式笔记与 evidence.json；synthesis 保存跨篇综合；runs 保存实际计算日志及环境，勿保存虚构运行记录。当前除说明与空索引外无真实论文。

| 路径约定 | 内容 |
| --- | --- |
| inbox/ | 用户提供论文，尚未登记 |
| sources/<paper_id>/manifest.json | source_id、path（相对项目根）、version、sha256、获取方式、可读范围 |
| sources/<paper_id>/ | 正文、补充材料、提取文本（保留页码映射） |
| notes/<paper_id>/screening.md | 筛选卡 |
| notes/<paper_id>/deep-reading.md | 精读 |
| notes/<paper_id>/method-reproduction.md | 方法计划 |
| notes/<paper_id>/evidence.json | 各模式共用证据账本，保持 claim_id 稳定 |
| synthesis/ | 主题、矛盾、方法对比；每项回链论文原文 |
| runs/<paper_id>/<run_id>/ | 已执行操作的环境、参数、输入校验、日志、输出 |

index.csv 每行一篇文献版本；paper_id 是本地稳定主键，identifier 可空。stage 建议 ingested/screened/deep-read/method-planned；不表示科学结论被证实。完整来源登记与更新规则见 [契约](../.agents/skills/_literature-shared/references/kb-contract.md)。

同 DOI 新版本：保持家族关联，使用版本后缀 ID 或独立版本记录，不覆盖旧文件；同文件重复导入按 sha256 检查；只有标题相似不能自动去重。更正、补充、撤稿信息需来源。建议定期备份原文与索引；重建索引时以来源 manifest 和人工审核笔记为准，不对原文做不可逆修改。
