# Antigravity CLI 功能特性

### Plugins

**Plugin 的工作原理**
Plugin 是带命名空间的打包单元，可以将 skill、agent、rule、MCP server 和 hook 作为单个可部署单元打包在一起。

当你安装一个 plugin 时，CLI 会将文件暂存到你的主目录下的 `~/.gemini/antigravity-cli/plugins/<plugin_name>/`。Antigravity Agent 会自动发现并加载这些暂存的自定义配置。

```
~/.gemini/antigravity-cli/
├── plugins/
│   └── <plugin_name>/
│       ├── plugin.json         # 必需的标记文件
│       ├── mcp_config.json     # 可选的 MCP server 定义
│       ├── hooks.json          # 可选的 event hook 定义
│       ├── skills/             # 可选的 skill
│       ├── agents/             # 可选的 subagent
│       └── rules/              # 可选的 rule
└── import_manifest.json        # 跟踪清单
```

**访问 Plugin 组件**
一旦暂存并加载完成，你可以在 CLI 中使用 slash command 与 plugin 组件进行交互。

### Terminal Sandbox

Terminal Sandbox 是一种轻量级安全隔离机制，当 agent 执行本地 shell 命令时，它保护你的宿主系统免受潜在的破坏性文件操作或未经授权的出站网络请求的影响。

CLI 不运行重量级虚拟机或容器，而是利用操作系统的原生功能（Linux 上的 `nsjail`、macOS 上的 `sandbox-exec` 以及 Windows 上的 `AppContainer`）来实施严格的隔离边界，且零启动开销。

**配置**
你可以在 `settings.json` 文件（位于 `~/.gemini/antigravity-cli/settings.json`）中配置 sandbox 行为：

```
{
    "enableTerminalSandbox": true
}
```

*   **`enableTerminalSandbox`**（boolean，默认值：`false`）：对所有本地 agent 进程启用通用执行隔离屏障。

**交互式审批**
当 agent 提出需要你确认的终端命令时，CLI prompt 会根据你的设置动态调整：

*   **当 Sandbox 已启用时**：确认 prompt 将包含一个特定选项 **Yes, and run without sandbox restrictions**，以便你在需要为单条受信任命令临时绕过隔离边界时使用。
*   **当 Sandbox 已禁用时**：prompt 将包含一个选项 **Yes, and run in sandbox**，以便你强制将某条特定的、可能具有风险的命令在安全边界内执行。

### CLI Slash Commands 参考

Antigravity CLI 支持多种 slash command，可直接在 prompt 输入框中输入，用于管理对话、配置设置以及查看 agent 能力。

### 核心 Slash Commands

| Command | 类别 | 用途 |
| :-- | :-- | :-- |
| **`/resume`** _（别名 `/switch`）_ | Conversation | 打开对话选择器以恢复或切换会话。 |
| **[`/boost <task>`](/docs/boost)** | Reasoning | 针对复杂 bug、竞态条件和算法的多 agent 深度推理。 |
| **[`/teamwork-preview <task>`](/docs/teamwork)** | Reasoning | 为长周期项目启动[协作式多 agent 团队](/docs/teamwork)（付费计划）。 |
| **`/rewind`** _（别名 `/undo`）_ | Conversation | 将对话历史回滚到之前的检查点。 |
| **`/rename <name>`** | Conversation | 重命名当前活跃的对话线程，便于跟踪。 |
| **`/permissions`** | Configuration | 选择 agent 自主级别（`request-review`、`always-proceed` 或 `strict`）。 |
| **`/model`** | Configuration | 选择默认推理模型（跨会话持久化）。 |
| **`/keybindings`** | Configuration | 打开交互式键盘快捷键编辑器。 |
| **`/statusline`** | Configuration | 自定义 CLI 状态栏中显示的实时指示器。 |
| **`/tasks`** | Tools & Monitoring | 监控、查看日志或终止活跃的后台任务。 |
| **`/skills`** | Tools & Monitoring | 浏览本地和全局封装的 agent 工作流。 |
| **`/mcp`** | Tools & Monitoring | 打开面板以配置和管理 Model Context Protocol server。 |
| **`/open <path>`** | Utility | 立即在你首选的外部编辑器中打开文件。 |
| **`/diff`** | Utility | 打开[交互式 diff 查看器](/docs/cli/commands/diff)以审查更改并引导 agent。 |
| **[`/remote-control`](/docs/remote-control?tab=cli#interactive-mode)** | Utility | 为当前终端会话开启或关闭 Remote Control。 |
| **`/usage`** | Utility | 在终端内打开内联交互式帮助手册。 |
| **`/logout`** | Account | 退出你的 Google 会话并清除缓存的凭据。 |

### 通过 `settings.json` 进行高级自定义

对于高级用户，多个 slash command 支持通过 `~/.gemini/antigravity-cli/settings.json` 配置进行深度自定义：

*   **细粒度权限**：不局限于全局级别，可以定义具体的允许/拒绝命令：
    
    ```
    "permissions": {
      "allow": ["command(git)", "command(npm test)"],
      "deny": ["command(rm -rf)"]
    }
    ```
    
*   **自定义状态栏和窗口标题**：你可以将实时 agent 元数据（JSON 格式，包含 CWD、活跃模型、token 用量、状态等）直接管道传输到你自己的自定义 shell 脚本中，以生成动态状态栏或终端窗口标题。

### Antigravity CLI 中的 Subagents

Antigravity CLI 具备异步 subagent 框架，允许主 agent 委派并行工作、执行后台研究以及运行系统测试，而不会阻塞你当前的对话。

**什么是 Subagent？**
Subagent 是独立的并发 agent 会话，旨在与主对话并行处理特定的后台任务。

*   **目的**：主 agent 自动生成 subagent 来执行后台操作，例如查找文档、运行构建或验证修复。
*   **能力**：Subagent 拥有对代码搜索、文件编辑、终端命令和网络搜索等工具的完全访问权限，以完成其分配的任务。
    *   主 agent 决定 subagent 获得哪些工具和权限，包括是否可以使用 MCP 工具以及是否可以写入文件。

### 管理 Agent：`/agents` 面板

Antigravity CLI 提供交互式终端 UI，用于查看、管理运行中的 subagent 并审批其操作。

*   **访问方式**：在 prompt 中输入 `/agents` 打开 subagent 面板。
*   **概览**：面板显示活跃和已完成的 subagent 列表，包括其状态（running、done、killed 等）和当前正在执行的步骤等表层信息。

注意

从面板中选择一个 subagent 会打开全屏详情视图。该视图显示 subagent 对话的全部内容，包括其步骤、思考和 tool call 执行日志。

**Tool Call 确认与审批**
当 subagent 想要执行需要用户权限的 tool call（例如运行本地命令或写入文件）时，它会将请求呈现出来。你可以通过两种方式管理审批：

1.  **详情视图审批**
    Subagent 详情视图包含一个交互区域，其中列出了所有待处理的审批请求，你可以在其中选择性地批准或拒绝请求。

注意

**提示**：使用键盘快捷键 `ctrl+j` 从主对话“传送”到下一个等待你审批的 subagent 的详情视图。

2.  **快速路径提醒**
    为了让你保持专注，当 subagent 请求权限时，Antigravity CLI 会在你的 prompt 输入框正上方显示一个快速路径提醒。

注意

**提示**：你可以使用 `ctrl+k` 即时批准待处理的 subagent 权限请求，而无需离开主对话。