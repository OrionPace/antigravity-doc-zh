---
layout: doc
---

# 记忆桥接：Codex 与 Antigravity 协同

当你在同一个开发机或团队中同时使用 **Codex CLI** 与 **Google Antigravity CLI** 时，如何避免知识割裂？

## 知识割裂的痛点

- Codex 解决过的复杂 Bug 方案保存在 `~/.codex/sessions/` 中；
- Antigravity 沉淀的架构决策保存在 `~/.gemini/antigravity-cli/` 中；
- 开发者在不同工具间切换时，新 Agent 往往需要重新探索代码库。

## 统一知识中枢模式 (Obsidian Wiki)

最佳实践是将两个 Agent 的会话经验沉淀到一个统一的 Markdown 知识库（如 Obsidian Wiki）中：

1. **统一 Ingest 归档**：使用专用 history-ingest 工具定期将各 Agent 的会话摘要写入共享的 `concepts/` 与 `projects/` 笔记。
2. **跨 Agent 检索**：通过规则文件（`AGENTS.md` 或 `rules`），让 Antigravity 与 Codex 在启动时都以该笔记库作为外部上下文（External Context）。
3. **互补调用**：让 Codex 负责快速局部编辑，让 Antigravity 负责复杂多步骤子代理编排（Subagents），实现双引擎驱动。
