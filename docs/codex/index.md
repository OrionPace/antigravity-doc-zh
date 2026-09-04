---
layout: doc
---

# Codex CLI 中文指南

> **Codex CLI** 是 OpenAI 推出的终端 AI 编程助手与 Agentic 编码工具，支持在本地 shell 中自主执行跨文件编辑、命令运行和项目构建。
> 本专区为社区整理的中文核心参考，方便与 Google Antigravity CLI 对照使用。

## 核心导航

<div class="feature-grid">

### 核心概念
- [快速上手](./getting-started) — 安装、认证与初次会话
- [配置指南](./configuration) — 环境变量、配置文件与参数调整
- [记忆桥接](./memory-bridge) — Codex 与 Antigravity 的协同与知识互通

### 关键特性
- **自主 Multi-turn 循环**：多步推理、工具链调度与自动错误自愈
- **非侵入式代码修改**：以最小 Diff 进行安全替换
- **上下文感知**：本地代码库深度索引与符号跳转

</div>

## 与 Antigravity CLI 的定位对比

| 维度 | Antigravity CLI | Codex CLI |
| :--- | :--- | :--- |
| **底层生态** | Google Gemini 2.5 / Vertex AI | OpenAI o-series / GPT-4o |
| **交互界面** | 终端 TUI（带多面板/状态栏/Vim模式） | 终端命令行 / 交互式 Shell |
| **可扩展性** | 原生 Plugin / Skill / MCP / Hook | Tools / MCP / Custom Scripts |
| **协同模式** | 支持与 Antigravity 2.0 桌面端会话互通 | 聚焦极简终端原生闭环 |

---

> 如需补充内容或提交改进建议，欢迎访问 [GitHub 仓库](https://github.com/OrionPace/antigravity-doc-zh) 提交 PR。
