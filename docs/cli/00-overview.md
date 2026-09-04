# Antigravity CLI 概览

Antigravity CLI 是 Antigravity 的轻量级终端用户界面（TUI，Terminal User Interface）前端。它将与 Antigravity 2.0 相同的核心 agent 能力（如多步推理、多文件编辑、tool calling 以及对话历史）直接带入你的终端。

## 为什么选择 Antigravity CLI？

Antigravity CLI 将我们共享的 agent harness 具备的推理、执行与编排能力直接带入你的本地 Shell。虽然 Antigravity 2.0 提供了全面的可视化编辑器界面，但 CLI 是专门为极速响应、轻量化运行以及与终端优先工作流无缝集成而量身打造的。

### 平台对比

| 特性 | Antigravity CLI | Antigravity 2.0 |
| :-- | :-- | :-- |
| **主要交互界面** | 键盘驱动的 TUI | 可视化桌面编辑器 / IDE |
| **性能开销** | 趋近于零，极度轻量 | 标准桌面 IDE 资源占用 |
| **工作流侧重** | 快速本地迭代、SSH、headless | 完整项目管理、可视化 workspace |
| **交互导航** | 通用键盘快捷键 | 鼠标与多面板布局 |
| **远程可用性** | 原生支持 SSH、tmux 与终端复用器 | 本地 workspace 或远程开发容器 |

## 集成特性

Antigravity CLI 与 Antigravity 2.0 协同工作，共享配置并支持在不同界面之间无缝切换：

*   **共享 agent harness**：两个环境运行在完全相同的 agent 核心之上。针对多步推理、tool call 或代码理解的任何优化均在两个平台上通用。
*   **共享配置同步**：你的核心偏好、权限以及安全配置会在两个界面之间自动同步。在一个平台上更新权限 rule 或标准配置，另一方将立即生效。
*   **对话导出**：在不同平台间无缝转移正在进行的会话。如果终端中的会话变得复杂且需要可视化编排，可将对话导出到 Antigravity 2.0 中，在可视化编辑器界面中继续进行。

## 从 Gemini CLI 迁移

如果你正在从 Gemini CLI 迁移过来，初始化引导流程支持一次性导入，可自动迁移现有的 Gemini CLI 扩展插件、skills 和设置。欲了解更多信息，请阅读 [从 Gemini CLI 迁移](/docs/cli/gcli-migration)。

## 后续步骤

浏览以下指南以配置你的环境，并开始与自主 agent 协同工作：

*   **[安装与认证（Installation & Auth）](/docs/cli/install)**：配置 CLI、配置企业参数并完成静默身份认证。
*   **[入门指南（Getting Started）](/docs/cli/getting-started)**：了解上手路线图、首次启动设置及核心概念模型。
*   **[上手教程（Tutorial）](/docs/cli/tutorial)**：配合活跃的 agent 运行你的第一个多文件生成任务。
*   **[Prompt 编写与交互（Prompting & Interaction）](/docs/cli/prompting)**：掌握多行编写、prompt 编辑及终端媒体粘贴技巧。
*   **[审查 Artifact（Reviewing Artifacts）](/docs/cli/artifacts)**：利用透明度特性审查 agent 规划、diff 以及测试运行。
*   **[AI 额度点数（AI Credits）](/docs/cli/credits)**：配置和监控 AI Premium 额度回退机制、定价链接与配置项。
*   **[插件与 Skill（Plugins & Skills）](/docs/cli/plugins)**：创建自定义 skill 对应的 Slash Command、管理 hook 并配置 MCP 服务器。
*   **[最佳实践（Best Practices）](/docs/cli/best-practices)**：掌握工作流管道、验证循环以及会话纠偏技巧。