# Statusline 自定义

定义自定义脚本配置并格式化动态 JSON 状态 payload，以自定义您的 TUI statusline（状态栏）。

> [!NOTE]
> 要在 TUI 中切换 statusline 的开启/关闭或对其进行配置，请参阅 **[Status Line 命令](/docs/cli/commands/statusline)**。

## 概述

Statusline 位于 TUI prompt 面板的底部。它提供了一目了然的上下文信息，涵盖活动的 agent 循环、workspace 环境、上下文 token 窗口使用情况以及后台执行任务。

## 自定义 Statusline 脚本编写

针对高级终端布局或自定义状态栏显示，您可以将活动的 agent 元数据路由到自定义脚本中。

### 配置

将 `statusLine` 配置块添加到您的 `~/.gemini/antigravity-cli/settings.json` 文件中：

```json
{
    "statusLine": {
        "type": "command",
        "command": "~/.gemini/antigravity-cli/statusline.sh"
    }
}
```

每当 agent 状态发生变化时，TUI 就会执行您的命令脚本，将详细的状态 JSON payload 直接通过管道传输到该脚本的 `stdin`，从 `stdout` 读取您格式化后的字符串，并将结果渲染在 prompt 的 statusline 中。完全支持 ANSI 颜色代码。

该配置块还接受另外三个可选键：`padding` 用于在 statusline 上方添加空行；`enabled` 设置为 `false` 可暂停执行脚本同时保留文件中的命令；`stack_with_default` 设置为 `true` 则会将您的脚本渲染在内置 statusline 的下方，而不是替换它。

### 可用的 JSON 字段

通过管道传输给脚本的 JSON payload 包含以下顶级字段：

| 字段 | 类型 | 描述 |
| :-- | :-- | :-- |
| `cwd` | string | 启动 CLI 时的当前工作目录。 |
| `session_id` | string | `conversation_id` 的向后兼容别名。 |
| `conversation_id` | string | 当前唯一的会话 ID。 |
| `transcript_path` | string | 活动会话记录日志文件的绝对路径（可选）。 |
| `model` | object | 包含当前活动模型的 `id` 和 `display_name`。 |
| `workspace` | object | 包含 `current_dir` 和 `project_dir` 路径。 |
| `version` | string | CLI 版本字符串。 |
| `context_window` | object | 包含 token 使用详情：`total_input_tokens`、`total_output_tokens`、`context_window_size`、`used_percentage`、`remaining_percentage` 以及 `current_usage` 子对象。 |
| `exceeds_200k_tokens` | bool | 会话上下文是否已超过 200k tokens（在首次 API 调用前为 null）。 |
| `product` | string | 应用程序名称（例如 `antigravity`）。 |
| `quota` | object | 将模型/存储桶 ID 映射到其配额状态，包含 `remaining_fraction`、`reset_time` 和 `reset_in_seconds`（可选）。 |
| `agent_state` | string | 当前状态：`idle`、`thinking`、`working`、`tool_use`、`initializing`。 |
| `vcs` | object | 版本控制信息：`type`（git/jj/hg）、`branch`、`client`、`dirty`（可选）。 |
| `sandbox` | object | Sandbox（沙箱）配置：`enabled`、`allow_network`（可选）。 |
| `artifact_count` | int | 在该会话中生成的 artifact（成果物/工件）数量。 |
| `plan_tier` | string | 已认证用户的订阅等级（可选）。 |
| `email` | string | 已认证用户的 Email/LDAP。 |
| `pending_input_count` | int | 队列中排队等待的用户消息数量。 |
| `tool_confirmation_pending` | bool | 当显示工具确认对话框时为 true。 |
| `task_count` | int | 正在运行的后台任务数量。 |
| `terminal_width` | int | 交互式终端的实时宽度。 |
| `execution_mode` | string | 当前活动的 prompt 执行模式（例如 `planning`、`fast`）。 |
| `vim` | object | Vim 编辑状态：`mode` 为 `NORMAL`、`INSERT`、`VISUAL` 或 `VISUAL LINE`。仅在启用 [Vim 编辑器模式](/docs/cli/vim-editor-mode) 时存在。 |

### JSON Payload 示例

以下是传递给您的 statusline 脚本的一个完整脱敏典型 JSON payload：

```json
{
    "cwd": "/home/user/my-project",
    "session_id": "12345678-abcd-ef01-2345-6789abcdef01",
    "conversation_id": "12345678-abcd-ef01-2345-6789abcdef01",
    "transcript_path": "/home/user/.gemini/antigravity/brain/12345678-abcd-ef01-2345-6789abcdef01/.system_generated/logs/transcript.jsonl",
    "model": {
        "id": "Gemini 3.5 Flash (High)",
        "display_name": "Gemini 3.5 Flash (High)"
    },
    "workspace": {
        "current_dir": "/home/user/my-project",
        "project_dir": "/home/user/my-project"
    },
    "version": "1.0.13",
    "context_window": {
        "total_input_tokens": 88244,
        "total_output_tokens": 61074,
        "context_window_size": 1048576,
        "used_percentage": 14.24,
        "remaining_percentage": 85.76,
        "current_usage": {
            "input_tokens": 63382,
            "output_tokens": 346,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 20857
        }
    },
    "exceeds_200k_tokens": false,
    "product": "antigravity",
    "quota": {
        "gemini-weekly": {
            "remaining_fraction": 0.9378,
            "reset_time": "2026-07-06T07:50:32Z",
            "reset_in_seconds": 560580
        }
    },
    "agent_state": "idle",
    "vcs": {
        "type": "git",
        "branch": "main",
        "dirty": false
    },
    "sandbox": {
        "enabled": false
    },
    "artifact_count": 2,
    "plan_tier": "Pro",
    "email": "developer@email.com",
    "task_count": 1,
    "terminal_width": 111,
    "execution_mode": "planning"
}
```

### 示例脚本

您可以从 GitHub 上的官方 [statusline.sh 示例](https://github.com/google-antigravity/antigravity-cli/blob/main/examples/statusline/statusline.sh) 下载完整的、自适应布局的脚本。该脚本可动态渲染状态徽章、处理活动分支，并格式化上下文窗口进度条。

将该脚本保存到 `~/.gemini/antigravity-cli/statusline.sh` 并赋予其可执行权限：

```bash
chmod +x ~/.gemini/antigravity-cli/statusline.sh
```

## 另请参阅

*   **[Status Line 命令](/docs/cli/commands/statusline)**：以交互方式切换 statusline 元素。
*   **[终端标题自定义](/docs/cli/title)**：配置动态窗口标题。
*   **[设置、渲染与键位绑定](/docs/cli/settings)**：自定义键盘快捷键与缓冲区。
*   **[权限与 Sandbox](/docs/cli/sandbox)**：管理安全目录权限。