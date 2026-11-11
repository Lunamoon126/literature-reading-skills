# 官方兼容性依据

核对日期：2026-11-11。仅为格式与工作流依据，不作为科学文献。

- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)：name/description frontmatter、渐进加载、Codex 项目 .agents/skills、ChatGPT Skill 选择及平台差异。
- [OpenAI plugin skills concept](https://developers.openai.com/plugins/concepts/skills)：Skill 是指令和资源目录，可与工具结合。

本包采用直接项目目录，不提供插件发布声明、MCP 工具或跨客户端安装器。共享相对文件要求宿主能访问完整目录。官方能力说明不等于当前账户可用；本次未进行 ChatGPT 桌面端端到端导入验证。若导入流程要求自包含 Skill 或插件格式，需按当前官方流程封装整个资源依赖，不能把本项目 ZIP 当成保证兼容的插件。
