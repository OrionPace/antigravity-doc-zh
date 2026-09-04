# 终端标题自定义

配置动态窗口标题、映射自定义脚本配置，并格式化 JSON 状态输出以自定义终端窗口标题栏。

> [!NOTE]
> 要以交互方式切换或设置终端标题，请参阅 **[窗口标题命令](/docs/cli/commands/title)**。

## 概述

终端窗口标题功能可在您的终端模拟器标题栏中显示 agent 详情、活动 workspace 基础目录名称以及当前会话参数。这样即使终端窗口处于最小化或非焦点状态，您也能够监控 agent 的执行进度。

## 自定义标题脚本编写

针对定制化的窗口标题格式，您可以将当前活动的 TUI 状态详情路由到自定义 shell 脚本中。

### 配置

将 `title` 配置块添加到您的 `~/.gemini/antigravity-cli/settings.json` 文件中：

```json
{
    "title": {
        "type": "command",
        "command": "~/.gemini/antigravity-cli/title.sh"
    }
}
```

每当 agent 状态发生变化时，TUI 就会执行您的命令脚本，将详细的状态 JSON payload 直接通过管道传输到该脚本的 `stdin`，从 `stdout` 读取格式化后的字符串，并更新您的终端窗口标题。不可打印字符和 ANSI 转义序列在渲染前会被自动去除。

### JSON 状态 Payload Schema

该 JSON 状态 payload 与发送给自定义 statusline 脚本的 payload 相同。它包含表示 `cwd`、`conversation_id`、`agent_state`、`vcs` 详情等的完整属性。完整属性列表请参阅 **[Statusline Schema](/docs/cli/statusline#available-json-fields)**。

### 示例脚本

您可以从 GitHub 上的官方 [title.sh 示例](https://github.com/google-antigravity/antigravity-cli/blob/main/examples/title/title.sh) 下载完整的、自适应布局的脚本。该脚本可提取当前活动的 workspace 文件夹基名，并渲染包含实时 agent 状态与会话 session 前缀的结构化终端标题。

将该脚本保存到 `~/.gemini/antigravity-cli/title.sh` 并赋予其可执行权限：

```bash
chmod +x ~/.gemini/antigravity-cli/title.sh
```

## 另请参阅

*   **[窗口标题命令](/docs/cli/commands/title)**：以交互方式切换或设置终端标题。
*   **[Statusline 自定义](/docs/cli/statusline)**：自定义动态 TUI 状态栏。
*   **[设置、渲染与键位绑定](/docs/cli/settings)**：自定义键盘快捷键与缓冲区。
*   **[权限与 Sandbox](/docs/cli/sandbox)**：管理安全目录权限。