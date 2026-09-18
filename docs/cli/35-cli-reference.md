# CLI reference

浏览可扫描的表格，其中列出了所有 TUI slash commands、默认键盘快捷键以及 JSON 配置参数。

## Core slash commands

在 prompt 输入框中输入 `/` 即可打开 typeahead 命令选择菜单。

| Command | Category | Alias | Execution Purpose |
| :-- | :-- | :-- | :-- |
| **`/add-dir <path>`** | Utilities | — | 将目录路径添加到当前 workspace。 |
| **[`/agents`](/docs/cli/commands/agents)** | Tools & Tasks | — | 打开 [Agent Manager Panel](/docs/cli/commands/agents)，以切换自定义 agent 并监控后台 subagent。 |
| **[`/boost`](/docs/boost)** `<task>` | Reasoning | — | 运行按需的多 agent 深度推理循环。 |
| **`/artifact`** | Tools & Tasks | — | 打开 Artifact Review Panel。 |
| **`/btw <query>`** | Utilities | — | 在后台提出一个附带问题，而不打断主对话。 |
| **`/clear`** | Utilities | `/new` | 清空终端并重置当前对话上下文。 |
| **`/config`** | Configurations | `/settings` | 打开交互式 Settings Editor Overlay。 |
| **`/context`** | Utilities | — | 打开上下文用量可视化面板。 |
| **`/copy`** | Utilities | — | 将最后一条 agent 回复复制到系统剪贴板。 |
| **[`/credits`](/docs/cli/commands/credits)** | Account | — | 查看剩余的 G1 credits 及购买链接。 |
| **[`/diff`](/docs/cli/commands/diff)** | Utilities | — | 打开 [Interactive Diff Viewer](/docs/cli/commands/diff)，以查看变更、turn 和提交。 |
| **`/exit`** | Core | `/quit` | 关闭 TUI 会话并恢复你的宿主 shell。 |
| **`/fast`** | Configurations | — | 启用 fast mode（绕过推理计划）以执行快速操作。 |
| **`/feedback`** | Utilities | — | 打开反馈提交面板。 |
| **`/fork`** | Conversations | `/branch` | 将当前对话线程克隆为一个新的并行会话。 |
| **`/help`** | Utilities | — | 打开帮助面板，显示命令和快捷键。 |
| **`/hooks`** | Tools & Tasks | — | 浏览当前生效的 pre-flight/post-format 脚本 hook。 |
| **`/keybindings`** | Configurations | — | 打开交互式 Keyboard Shortcut Editor。 |
| **`/logout`** | Account | — | 断开你的个人资料连接，并从安全 keyring 中清除认证 token。 |
| **`/mcp`** | Tools & Tasks | — | 打开 Model Context Protocol (MCP) server 管理器。 |
| **`/model`** | Configurations | — | 选择你偏好的推理模型（跨会话持久保存）。 |
| **`/open <path>`** | Utilities | — | 强制在系统默认编辑器中打开该路径。 |
| **[`/permissions`](/docs/cli/commands/permissions)** | Configurations | — | 打开交互式工具权限管理器面板。 |
| **`/planning`** | Configurations | — | 为复杂工程任务启用多 turn 计划生成模式。 |
| **`/rename <name>`** | Conversations | — | 重命名当前会话线程。 |
| **[`/remote-control`](/docs/remote-control?tab=cli#interactive-mode) \[on/off\]** | Utilities | — | 为当前终端会话切换 Remote Control。 |
| **[`/resume`](/docs/cli/commands/resume)** | Conversations | `/switch`, `/conversation` | 打开 [conversation picker overlay](/docs/cli/commands/resume)，以选择并加载之前的线程。 |
| **`/rewind`** | Conversations | `/undo` | 将你的对话历史回滚到之前的某条消息。 |
| **`/skills`** | Tools & Tasks | — | 浏览已加载的本地和全局 Agent Skills。 |
| **[`/statusline`](/docs/cli/commands/statusline)** | Configurations | — | 打开 Status Bar 自定义 overlay。 |
| **`/tasks`** | Tools & Tasks | — | 打开 Task Manager Panel，以监控后台 shell 执行日志。 |
| **[`/teamwork-preview`](/docs/teamwork)** `<task>` | Reasoning | `/teamwork` | 为长周期项目启动[协作式多 agent 团队](/docs/teamwork)（付费计划）。 |
| **[`/title`](/docs/cli/commands/title) \[on/off\]** | Configurations | — | 切换或设置终端窗口标题更新。 |
| **[`/usage`](/docs/cli/commands/usage)** | Utilities | `/quota` | 显示模型配额用量。 |
| **[`/voice`](/docs/cli/commands/voice)** | Utilities | `/record` | 使用麦克风口述 prompt。 |

## Default keybindings

键盘快捷键命令，映射全局、prompt、导航和审批操作。

### Global controls

无论当前聚焦于哪个面板、overlay 或 prompt，这些热键始终处于活动状态。

| Key | TUI Command | Action Behavior |
| :-- | :-- | :-- |
| **`Esc`** | `cli.escape` | 关闭当前活动面板、停止当前活动流，或清空空 prompt。 |
| **`Ctrl+C`** | `cli.exit` | 终止 CLI 会话（如果 agent 正在工作，会提示确认）。 |
| **`Ctrl+D`** | `cli.exit` | 退出 CLI 会话（仅当 prompt 输入框为空时）。 |
| **`Ctrl+L`** | `cli.clear_screen` | 刷新并清空可视终端缓冲区。 |

### Prompt focus keys

当你在 prompt 输入框中编写指令时，这些按键处于活动状态。

| Key | TUI Command | Action Behavior |
| :-- | :-- | :-- |
| **`Enter`** | `prompt.submit` | 将你的 prompt 或当前菜单选择提交给 agent。 |
| **`Shift+Enter`** / **`Ctrl+J`** | `prompt.newline` | 插入一个干净的换行符而不提交。 |
| **`Ctrl+V`** | `prompt.paste` | 将图形媒体文件或剪贴板内容块粘贴到 prompt 中。 |
| **`Ctrl+O`** | `prompt.toggle_trajectory` | 展开或折叠详细的工具推理输出。 |
| **`Ctrl+R`** | `prompt.open_review` | 打开 Artifact Review Panel。 |
| **`Ctrl+G`** | `prompt.external_editor` | 启动你的默认 `$EDITOR` shell 来编写 prompt。 |
| **`Alt+J`** | `prompt.teleport_agent` | 立即将焦点切换到下一个等待确认的 subagent。 |
| **`Ctrl+K`** | `prompt.fast_approve` | 立即批准状态提醒中列出的待处理 subagent 操作。 |
| **`Ctrl+A`** | `prompt.cursor_start` | 将 prompt 插入光标移动到行首。 |
| **`Ctrl+E`** | `prompt.cursor_end` | 将 prompt 插入光标移动到行尾。 |
| **`Ctrl+Z`** | `prompt.undo_text` | 撤销上一次编辑。 |
| **`Ctrl+Shift+Z`** | `prompt.redo_text` | 重做上一次撤销的文本操作。 |
| **`Ctrl+D`** | — | 向前删除（仅当 prompt 输入框非空时）。 |
| **`F5`** | `voice.start_dictation` | 开始或停止[语音听写](/docs/cli/commands/voice)。 |

### Navigation & scrolling

用于选择面板、菜单和可滚动文本框中。

| Key | TUI Command | Action Behavior |
| :-- | :-- | :-- |
| **`↑`** / **`↓`** | `navigation.up` / `navigation.down` | 将高亮选择向上或向下滚动一项。 |
| **`PgUp`** / **`Shift+↑`** | `navigation.page_up` | 将当前活动文本视口向上滚动一页。 |
| **`PgDn`** / **`Shift+↓`** | `navigation.page_down` | 将当前活动文本视口向下滚动一页。 |
| **`←`** / **`→`** | `navigation.left` / `navigation.right` | 在多页结构中切换页面（例如 Session Picker）。 |
| **`Tab`** | `navigation.tab` | 确认高亮的 slash-command 自动填充选项。 |

### Tool confirmations

在确认提示期间处于活动状态。

| Key | TUI Command | Action Behavior |
| :-- | :-- | :-- |
| **`y`** | `confirm.yes` | 授权提议的 tool、命令或当前 artifact。 |
| **`n`** | `confirm.no` | 拒绝提议的 tool、命令或当前 artifact。 |
| **`A`** | — | （在 Review Panel 内）一次性批准所有生成的 artifact（内置快捷键）。 |

## Configuration keys (`settings.json`)

主要设置键名、数据类型、系统默认值以及预期参数。

### Example `settings.json`

```
{
    "colorScheme": "tokyo night",
    "altScreenMode": "always",
    "toolPermission": "request-review",
    "notifications": true,
    "enableTerminalSandbox": true
}
```

| Option Key Name | Value Type | System Default | Parameter Characteristics & Options |
| :-- | :-- | :-- | :-- |
| **`colorScheme`** | string | `"terminal"` | 颜色主题：`"light"`、`"solarized light"`、`"colorblind-friendly light"`、`"dark"`、`"solarized dark"`、`"colorblind-friendly dark"`、`"tokyo night"` 或 `"terminal"`（继承原生 shell 颜色）。 |
| **`altScreenMode`** | string | `"default"` | 屏幕缓冲区使用方式：`"default"`（自适应 inline/altscreen）、`"always"`（强制使用备用屏幕缓冲区）或 `"never"`（强制使用 inline 顺序输出）。 |
| **`toolPermission`** | string | `"request-review"` | 全局安全预设：`"request-review"`（对 write/bash/web tool 进行提示）、`"proceed-in-sandbox"`（在 sandbox 内自动继续）、`"always-proceed"`（从不提示）或 `"strict"`（对所有非读取类 tool 进行提示）。 |
| **`artifactReviewPolicy`** | string | `"asks-for-review"` | 代码审查策略：`"asks-for-review"`（写入代码前始终提示）、`"agent-decides"`（动态提示）或 `"always-proceed"`（从不提示）。 |
| **`notifications`** | boolean | `false` | 在任务完成时发出系统桌面通知和终端铃声提醒。 |
| **`showTips`** | boolean | `true` | 在生成 turn 期间，在 prompt 面板上方显示有用的 agentic 提示。 |
| **`showFeedbackSurvey`** | boolean | `true` | 在活动任务完成时，定期显示质量反馈调查。 |
| **`editor`** | string | `"auto"` | 目标文本编辑器工具：`"auto"`（参考系统 `$EDITOR`）、`"vim"`、`"emacs"` 或自定义文本标签。 |
| **`editorMode`** | string | `"default"` | Prompt 编辑模式：`"default"`（纯文本编辑）或 `"vim"`（模态编辑）。与 `editor` 不同，后者用于选择外部程序。参见 [Vim Editor Mode](/docs/cli/vim-editor-mode)。 |
| **`vimInsertFirst`** | boolean | `false` | 以 Insert 模式启动 Vim 编辑，并使单独的 `Enter` 执行提交。需要将 `editorMode` 设置为 `"vim"`。 |
| **`allowNonWorkspaceAccess`** | boolean | `false` | 允许 agent 的文件读写 tool 访问已识别的 Git/workspace 根目录之外的路径。 |
| **`enableTerminalSandbox`** | boolean | `false` | 将 agent 启动的所有本地执行命令限制在操作系统隔离环内。 |
| **`useG1Credits`** | boolean | `false` | _仅限外部构建版本。_ 当计划配额耗尽后，使用个人 AI credits 进行模型调用。 |
| **`enableTelemetry`** | boolean | `true` | 允许收集指标和流式传输崩溃日志，以提升工具可靠性。 |
| **`verbosity`** | string | `"high"` | 可视详细程度：`"high"`（渲染完整思考和 tool 输出）或 `"low"`（仅显示最少的可视进度指示器）。 |
| **`runningLightSpeed`** | string | `"medium"` | 可视 running light 进度动画速度：`"fast"`、`"medium"`、`"slow"` 或 `"off"`。 |

## Next steps

了解如何安全地部署权限策略、sandbox，以及自定义 plugin：

*   **[Permissions & Sandbox](/docs/cli/sandbox)**：强制执行命令行隔离规则。
*   **[Plugins & Skills](/docs/cli/plugins)**：创建你自己的自定义 skill slash commands。
*   **[Installation & Auth](/docs/cli/install)**：更新你的 CLI 安装。