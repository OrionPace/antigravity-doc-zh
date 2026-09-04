# Agents 命令 (/agents)

直接在交互式 TUI 面板中浏览、选择并切换自定义 agent，或监控活动与已完成的后台 subagent（子代理）。

## 开始之前

*   [安装 Antigravity CLI](/docs/cli/install)
*   了解[异步执行模型](/docs/cli/subagents)

## 概述

`/agents` 命令会打开交互式的 **Agent Manager Panel（Agent 管理面板）**。该界面主要有两个核心用途：

1.  **自定义 Agent 选择与发现**：在默认 agent 与特定工作流的自定义 agent 之间进行选择，或了解如何在本地与全局定义新的 agent。
2.  **Subagent 监控与控制**：跟踪、检查或终止在当前活动会话期间并发运行的后台 subagent。

> [!NOTE]
> **Subagent 规范**：有关 subagent 生命周期状态、agent 间通信以及自定义 Markdown agent 规范（`.md`）的完整细节，请参阅 [Antigravity 2.0 Subagents 文档](/docs/subagents) 与 [CLI Subagents 指南](/docs/cli/subagents)。

要在 TUI 中打开该面板，输入 `/agents` 并按 Enter：

```bash
/agents
```

![Interactive Agents Panel](/assets/image/docs/cli/agents-panel.png)

* * *

## 自定义 Agent 选择与发现

Antigravity CLI 支持加载带有专属系统指令与工具权限的自定义 agent 定义。**Available Agents（可用 Agent）** 区域列出了当前会话可用的所有 agent。

### 1. 在 Agent 之间切换

*   **选择**：使用 ↑/↓ 在 **Available Agents** 下高亮选中某个 agent（`Default agent` 或自定义 agent），然后按 Enter。
*   **状态指示器**：绿色圆圈（`●`）表示当前激活或已准备就绪的 agent。
*   **应用并退出**：按 Esc 关闭面板并应用您的选择。

> [!NOTE]
> 如果您当前处于活动会话中，切换自定义 agent 会自动分叉（fork）当前会话（`[ Switch will fork the current conversation on exit ]`），以确保上下文不会丢失。如果您是从新会话开始，则切换会直接生效（`[ Switch will create a new conversation on exit ]`）。

### 2. 创建自定义 Agent

`/agents` 面板的顶部标头显示了创建新自定义 agent 的准确模板位置：

```
Create New Agents
  Workspace: {workspace}/.agents/agents/{agent_name}/agent.md
  Global: ~/.gemini/config/agents/{agent_name}/agent.md
```

要创建可在所有 workspace 和项目中通用的自定义 agent，请将其放置在全局自定义目录下（`~/.gemini/config/agents/`）。创建一个与您的 agent 名称匹配的目录，并添加带有 YAML frontmatter 的 `agent.md` 文件：

```bash
mkdir -p ~/.gemini/config/agents/code-reviewer
cat << 'EOF' > ~/.gemini/config/agents/code-reviewer/agent.md
---
name: code-reviewer
description: Rigorous code review specialist focusing on edge cases and security.
---
You are an expert code reviewer. Analyze diffs carefully and verify edge cases.
EOF
```

当您重新打开 `/agents` 时，CLI 会自动发现 `code-reviewer` 并将其列在 **Available Agents** 下。如果您需要将 agent 严格限定在单个项目代码库内，请将其放置在对应 workspace 的 `.agents/agents/` 目录下（例如 `/home/user/projects/my-app/.agents/agents/code-reviewer/agent.md`）。您也可以将自定义 agent 打包并在 [Plugins](/docs/cli/plugins) 中进行分发。

* * *

## Subagent 监控与控制

当主 agent 分发委托任务时（例如运行测试或查询大型代码库），衍生的执行线程会按触发它们的 prompt 进行分组，显示在 `/agents` 面板的 **Subagents** 下。

### 1. 检查 Subagent 进度

*   **分组展开/折叠**：在 subagent 分组标题（`▸ Subagents (1 running, 2 done)`）上按 Enter 即可展开或折叠（`▾`）该分组。
*   **状态指示器**：每行 subagent 都会显示实时的生命周期状态：
    *   `running`：正在活跃地执行工具或生成推理步骤。
    *   `done`：已成功完成分配的后台任务。
    *   `error`：在执行过程中遇到了致命故障。
    *   `killed`：被用户或父进程手动终止。
*   **详情视图**：高亮选中特定的 subagent 行并按 Enter，可打开全屏的 **Subagent Detail View（Subagent 详情视图）**。该视图展示了 subagent 完整的内部思考（thoughts）、tool calls（工具调用）和执行 stdout 输出。按 Esc 返回列表。

### 2. 终止活动中的 Subagent

如果某个后台 subagent 陷入死循环或运行时间超过预期，您可以立即终止它而无需退出当前会话：

1.  打开 `/agents` 并高亮选中正在运行的 subagent 行。
2.  按 K 即可立即终止该活动的 subagent 及其所有子线程。

### 3. 行内工具审批

如果 subagent 尝试执行受保护的操作（例如修改文件或在沙箱环境中运行 shell 命令），授权 prompt 会直接在 `/agents` 面板中以内联方式显示。您可以直接在列表中按 A 批准或按 D 拒绝。

* * *

## 面板快捷键参考

当焦点位于 `/agents` 面板内时，适用以下快捷键：

| 按键 | 操作 | 行为 |
| :-- | :-- | :-- |
| ↑ / ↓ | 导航 | 在标头、subagents 以及可用 agents 之间移动光标。 |
| Enter | 选择 / 切换 | 展开/折叠分组、打开 Subagent Detail View，或选择自定义 agent。 |
| K | 终止活动 Subagent | 立即取消（`CancelSubagent`）高亮选中的正在运行的 subagent。 |
| Esc | 返回 | 退出面板，返回 prompt 输入框，并应用任何已准备的 agent 切换。 |

* * *

## 常见错误

| 常见错误 | 失败原因 | 解决方法 |
| :-- | :-- | :-- |
| 期望切换自定义 agent 时能修改 turn（轮次）历史记录 | 切换 agent 会对会话进行分叉（fork）以保持历史记录的完整性 | 在新分叉出的会话中继续您的工作流 |
| 将 agent 文件直接放在配置根目录下 | 扫描器专门在 `agents/` 目录下查找定义 | 将定义移动到 `.agents/agents/<name>/agent.md` |
| 对已完成的 subagent 按 K 键 | 终止操作仅针对活跃（`running`）的 subagent 进程 | 按 Enter 键检查已完成任务的日志 |

* * *

## 后续步骤

*   [后台任务与 subagents](/docs/cli/subagents)：深入了解多线程异步执行架构。
*   [Plugins 与 Skills](/docs/cli/plugins)：了解如何将自定义 agent、skill 和 MCP 配置打包到可共享的 plugin 中。
*   [权限与 Sandbox](/docs/cli/sandbox)：为后台 subagent 配置安全护栏与审批规则。