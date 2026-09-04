# Antigravity CLI 特性

### 插件（Plugins）

**Plugin 工作原理**  
Plugin 是带有命名空间的组件包，可将 skills、agents、rules、MCP 服务器以及 hooks 作为单一的可部署单元进行打包。

当你安装 plugin 时，CLI 会将相关文件暂存到你的用户主目录下：`~/.gemini/antigravity-cli/plugins/<plugin_name>/`。Antigravity Agent 会自动发现并加载这些已暂存的自定义扩展。

```
~/.gemini/antigravity-cli/
├── plugins/
│   └── <plugin_name>/
│       ├── plugin.json         # 必需的标记文件
│       ├── mcp_config.json     # 可选的 MCP 服务器定义
│       ├── hooks.json          # 可选的事件 hooks 定义
│       ├── skills/             # 可选的 skills
│       ├── agents/             # 可选的 subagents
│       └── rules/              # 可选的 rules
└── import_manifest.json        # 跟踪清单文件
```

**访问 Plugin 组件**  
一旦完成暂存并加载后，你可以在 CLI 中使用 Slash Command 与 plugin 组件进行交互。

### 终端沙箱（Terminal Sandbox）

终端沙箱（Terminal Sandbox）是一种轻量级安全隔离机制，用于在 agent 执行本地 Shell 命令时，保护你的宿主系统免受潜在破坏性文件操作或未授权外部网络请求的影响。

CLI 并未采用笨重的虚拟机或容器，而是直接利用原生操作系统特性（Linux 上的 `nsjail`、macOS 上的 `sandbox-exec` 以及 Windows 上的 `AppContainer`）来实施严格的隔离边界，实现零启动开销。

**配置**  
你可以在 `settings.json` 文件（位于 `~/.gemini/antigravity-cli/settings.json`）中配置 sandbox 行为：

```json
{
    "enableTerminalSandbox": true
}
```

*   **`enableTerminalSandbox`**（布尔值，默认值：`false`）：在所有本地 agent 进程上启用通用的执行隔离屏障。

**交互式审批（Interactive Approvals）**  
当 agent 提议执行需要你确认的终端命令时，CLI 的 prompt 会根据你的配置动态调整：

*   **启用 Sandbox 时**：确认 prompt 会包含一个特定选项 **Yes, and run without sandbox restrictions**（是，并在无沙箱限制下运行），以便你在需要时针对单个受信命令临时绕过隔离边界。
*   **禁用 Sandbox 时**：prompt 会包含选项 **Yes, and run in sandbox**（是，并在沙箱中运行），以便你想强制在安全边界内执行某个特定且具有潜在风险的命令。

### CLI Slash Command 参考

Antigravity CLI 支持直接在 prompt 输入框中输入多种 Slash Command，用以管理对话、调整配置并检查 agent 能力。

### 核心 Slash Command

| 命令 | 分类 | 用途 |
| :-- | :-- | :-- |
| **`/resume`** _(别名 `/switch`)_ | 对话 | 打开对话选择器以恢复或切换会话。 |
| **[`/boost <task>`](/docs/boost)** | 推理 | 多 agent 深度推理，针对复杂 Bug、竞态条件与算法问题。 |
| **[`/teamwork-preview <task>`](/docs/teamwork)** | 推理 | 为长周期项目启动 [协作式多 agent 团队](/docs/teamwork)（付费方案）。 |
| **`/rewind`** _(别名 `/undo`)_ | 对话 | 将对话历史回滚到之前的检查点。 |
| **`/rename <name>`** | 对话 | 重命名当前活跃对话线程，以便于跟踪。 |
| **`/permissions`** | 配置 | 选择 agent 自主权级别（`request-review`、`always-proceed` 或 `strict`）。 |
| **`/model`** | 配置 | 选择默认推理模型（跨会话持久保存）。 |
| **`/keybindings`** | 配置 | 打开交互式快捷键编辑器。 |
| **`/statusline`** | 配置 | 自定义 CLI 状态栏中显示的实时指示器。 |
| **`/tasks`** | 工具与监控 | 监控、查看日志或终止后台运行的活跃任务。 |
| **`/skills`** | 工具与监控 | 浏览本地与全局封装的 agent 工作流。 |
| **`/mcp`** | 工具与监控 | 打开面板以配置和管理 Model Context Protocol（MCP）服务器。 |
| **`/open <path>`** | 工具 | 立即在你偏好的外部编辑器中打开指定文件。 |
| **`/diff`** | 工具 | 打开 [交互式 diff 查看器](/docs/cli/commands/diff) 以审查变更并引导 agent。 |
| **`/usage`** | 工具 | 在终端内打开内置交互式帮助手册。 |
| **`/logout`** | 账号 | 退出你的 Google 会话并清除缓存凭据。 |

### 通过 `settings.json` 进行高级自定义

对于高级用户，部分 Slash Command 支持通过 `~/.gemini/antigravity-cli/settings.json` 配置文件进行深度自定义：

*   **细粒度权限（Fine-Grained Permissions）**：无需使用全局权限级别，而是定义具体的允许/拒绝命令：
    
    ```json
    "permissions": {
      "allow": ["command(git)", "command(npm test)"],
      "deny": ["command(rm -rf)"]
    }
    ```
    
*   **自定义状态栏（Status Line）与窗口标题**：你可以将实时 agent 元数据（包含 CWD、当前模型、token 消耗、状态等的 JSON 格式）直接通过管道传输给你自己的自定义 Shell 脚本，从而生成动态状态栏或终端窗口标题。

### Antigravity CLI 中的 Subagent

Antigravity CLI 具备异步 subagents 架构，允许主 agent 分发并行工作、执行后台调研以及运行系统测试，而不会阻塞你当前的活跃对话。

**什么是 Subagent？**  
Subagent 是独立的并发 agent 会话，旨在与主对话并行处理特定的后台任务。

*   **定位与目的**：主 agent 会自动生成（spawn）subagent 来执行后台操作，例如查阅文档、运行构建或验证修复方案。
*   **功能能力**：Subagent 拥有代码搜索、文件编辑、终端命令和网络搜索等工具的完整访问权限，以完成分配给它们的任务。
    *   主 agent 决定赋予 subagent 哪些工具与权限，包括它们是否可以使用 MCP 工具以及是否可以写入文件。

### 管理 Agent：`/agents` 面板

Antigravity CLI 提供了交互式终端 UI，用于查看、管理并审批正在运行的 subagents 的操作。

*   **访问方式**：在 prompt 输入框中输入 `/agents` 即可打开 subagents 面板。
*   **概览**：面板显示活跃和已完成的 subagents 列表，包括基础摘要详情，例如其状态（running、done、killed 等）以及它们当前正在执行的步骤。

注意

在面板中选择某个 subagent 会打开全屏详情视图。该视图显示该 subagent 对话的完整内容，包括其步骤、思考过程（thoughts）以及 tool call 执行日志。

**工具确认与审批（Tool Confirmations & Approvals）**  
当 subagent 想要执行需要用户权限的工具时（例如运行本地命令或写入文件），它会发起请求。你可以通过两种方式管理审批：

1.  **详情视图审批（Detail View Approvals）**  
    Subagent 详情视图包含一个交互操作区域，列出所有待审批的请求，你可以在其中选择性地批准或拒绝请求。

注意

**提示**：使用快捷键 `ctrl+j` 可以从主对话直接“瞬间跳转（teleport）”到下一个等待你审批的 subagent 详情视图。

2.  **快捷通路提示（Fast Path Alerts）**  
    为了不打断你的工作心流，当 subagent 请求权限时，Antigravity CLI 会直接在你的 prompt 输入框上方显示快捷通路提示（Fast Path Alert）。

注意

**提示**：你可以使用 `ctrl+k` 立即批准待处理的 subagent 权限请求，而完全无需切换离开主对话。