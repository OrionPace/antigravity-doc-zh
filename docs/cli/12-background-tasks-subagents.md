# 后台任务与 subagent

将缓慢的构建、多文件代码生成以及深度调研任务委托给并行的后台 agent（智能体/代理），同时保持你活跃的编程心流。

> [!NOTE]
> **Antigravity 2.0 与 Hub 文档**：有关核心平台能力、subagent 生命周期状态图、agent 间消息传递以及嵌套深度限制，请参阅 [Antigravity 2.0 Subagents 文档](/docs/subagents)。

## 异步执行模型

为了最大化开发人员的研发速度，Antigravity CLI 采用了多线程异步执行架构。主 agent（primary agent）不会在耗时较长的构建、大规模代码库搜索扫描或复杂的多文件编辑期间锁定你的终端会话，而是将这些操作委托给并行的 **subagent** 或后台 **task（任务）**。

这种委托模型可确保你无需等待高延迟的 AI 处理过程。你可以继续编写代码、提交 prompt（提示词/交互）或检查文件，同时多个自主运行的后台线程会并行执行校验任务。

## 管理 agent：`/agents` 面板

当前活动的 agent 层级结构与自定义 agent 选择菜单是完全透明的，并可以通过交互式 [Agent 管理面板（`/agents`）](/docs/cli/commands/agents) 进行统一管理。

### 打开面板

在 prompt 输入框中键入 `/agents` 并按 Enter 即可打开交互式 **Agent 管理面板（Agent Manager Panel）**。

### 面板概览

该面板会实时显示所有处于活动（active）、已完成（completed）、已终止（killed）或失败（failed）状态的后台 agent 清单：

*   **Identifier（标识符）**：目标 subagent 的唯一 ID。
*   **Role（角色）**：agent 的专业分工角色（例如 “Codebase Researcher” 或 “Database Debugger”）。
*   **State（状态）**：实时状态指示器（running、done、killed 或 error）。
*   **Step（步骤）**：当前正在执行的 tool（工具）或推理步骤的实时摘要。

> [!TIP]
> 你也可以在该面板中选择并在自定义 agent 之间进行切换（或 fork 会话）。有关自定义 agent 发现与面板 keybindings 的完整详细信息，请参阅 [`/agents` 命令参考](/docs/cli/commands/agents)。

## 自定义 Agent（Markdown 格式）

除了内置 agent 之外，CLI 还会自动发现以 Markdown 格式（`.md`）并包含 YAML frontmatter 定义的自定义 agent：

*   **Workspace Agent**：`.agents/agents/<name>.md` 或 `.agents/agents/<name>/agent.md`
*   **全局 Agent**：`~/.gemini/config/agents/`

当自定义 agent 的 YAML frontmatter 中设置了 `subagent: true` 时，主 agent 即可通过 `invoke_subagent` 调用它。你也可以在 `/agents` 面板菜单中直接选择自定义 agent 作为主 agent。

有关完整的 schema、frontmatter 参数和代码示例，请参阅 [自定义 Subagent 规范](/docs/subagents#custom-subagents)。

## 深入监控

若要检查特定后台 agent 的内部推理、思考过程和日志：

1.  打开 `/agents` 面板，并使用 ↑/↓ 高亮选中目标 agent。
2.  按 Enter 打开 **Subagent 详情视图（Subagent Detail View）**。
3.  检查该 subagent 的完整推理日志，包括其私有内部思考、tool call（工具调用）和执行输出。
4.  按 Esc 退出并返回 Agent 管理器主列表。

## 使用 `/tasks` 监控后台任务

对于非 agent 类的后台操作（例如直接执行的 shell 命令、测试套件或通过 `/btw` 发起的简单后台查询），请使用 `/tasks` 命令。

```
/tasks
```

任务跟踪列表允许你：

*   跟踪标准的非交互式后台进程。
*   使用 ↑/↓ 选择任务并按 Enter 查看 stdout 标准输出日志。
*   安全终止失控的终端进程。

## 键盘工效与快捷操作

当 subagent 需要手动交互或 tool 授权时，为了减少上下文切换带来的摩擦，Antigravity CLI 集成了高效率的快捷路径。

### 深度“传送”导航（`Alt+J`）

当某个 subagent 遇到需要审批的 tool（例如写入文件或运行数据库迁移）时，状态栏通知会闪烁提示。

*   在主 prompt 面板内按 Alt + J，即可从当前会话即时“传送（teleport）”到下一个等待你审批的 subagent 详情视图中。
*   确认或拒绝该操作，然后按 Esc 即可传送回主线程。

### “快速路径”确认（`Ctrl+K`）

若要在不离开当前活动 workspace（工作区）的情况下即时授权 agent 操作：

1.  查看紧挨在当前活动 prompt 输入框上方显示的行内状态通知。它会概述待处理的操作（例如 `Subagent 12 asks to run "npm test"`）。
2.  按 Ctrl + K 即可即时批准待处理的快速路径操作，无需切换面板或打开浮层。

## 后续步骤

配置终端显示行为并定制你的配置文件：

*   **[Teamwork agent 团队（`/teamwork-preview`）](/docs/teamwork)**：为长期复杂项目启动协作式多 agent 团队。
*   **[设置、渲染与 Keybindings](/docs/cli/settings)**：自定义按键映射、缓冲区和 JSON 规则。
*   **[权限与 Sandbox](/docs/cli/sandbox)**：对后台进程实施安全隔离防护环。
*   **[Plugin 与 Skill](/docs/cli/plugins)**：创建你自己的自定义 skill（技能）和 slash command。