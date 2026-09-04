# CLI 参考

浏览列出所有 TUI（终端界面）Slash Commands、默认键盘快捷键以及 JSON 配置参数的速查表。

## 核心 Slash Commands

在 prompt 输入框内输入 `/` 即可打开命令先输入后选择（typeahead）菜单。

| 命令 | 类别 | 别名 | 执行用途 |
| :-- | :-- | :-- | :-- |
| **`/add-dir <path>`** | Utilities | — | 将目录路径添加到当前活跃的 workspace（工作区）中。 |
| **[`/agents`](/docs/cli/commands/agents)** | Tools & Tasks | — | 打开 [Agent 管理面板](/docs/cli/commands/agents) 以切换自定义 agent 并监控后台 subagent（子代理）。 |
| **[`/boost`](/docs/boost)** `<task>` | Reasoning | — | 按需运行多 agent 深度推理闭环。 |
| **`/artifact`** | Tools & Tasks | — | 打开 Artifact 审查面板。 |
| **`/btw <query>`** | Utilities | — | 在后台发起旁枝提问，不打断主对话流程。 |
| **`/clear`** | Utilities | `/new` | 清屏并重置当前对话上下文。 |
| **`/config`** | Configurations | `/settings` | 打开交互式设置编辑器浮层。 |
| **`/context`** | Utilities | — | 打开上下文用量可视化面板。 |
| **`/copy`** | Utilities | — | 将最后一条 agent 响应复制到系统剪贴板。 |
| **[`/credits`](/docs/cli/commands/credits)** | Account | — | 查看剩余 G1 积分及购买链接。 |
| **[`/diff`](/docs/cli/commands/diff)** | Utilities | — | 打开 [交互式 Diff 查看器](/docs/cli/commands/diff) 查看变更、turn（轮次）与 commit。 |
| **`/exit`** | Core | `/quit` | 关闭 TUI 会话并恢复宿主 shell。 |
| **`/fast`** | Configurations | — | 启用快速模式（跳过推理计划）以执行快捷操作。 |
| **`/feedback`** | Utilities | — | 打开反馈提交面板。 |
| **`/fork`** | Conversations | `/branch` | 将当前对话线程克隆到一个新的并行会话中。 |
| **`/help`** | Utilities | — | 打开展示命令与快捷键的帮助面板。 |
| **`/hooks`** | Tools & Tasks | — | 浏览活跃的前置/后置格式化脚本 hook（钩子）。 |
| **`/keybindings`** | Configurations | — | 打开交互式键盘快捷键编辑器。 |
| **`/logout`** | Account | — | 断开用户配置连接并从安全 keyring 中清除认证令牌。 |
| **`/mcp`** | Tools & Tasks | — | 打开 Model Context Protocol (MCP) 服务器管理器。 |
| **`/model`** | Configurations | — | 选择偏好的推理模型（跨会话持久保存）。 |
| **`/open <path>`** | Utilities | — | 强制在系统默认编辑器中打开指定路径。 |
| **[`/permissions`](/docs/cli/commands/permissions)** | Configurations | — | 打开交互式工具权限管理器面板。 |
| **`/planning`** | Configurations | — | 为复杂工程任务启用多轮计划生成模式。 |
| **`/rename <name>`** | Conversations | — | 重命名当前会话线程。 |
| **[`/resume`](/docs/cli/commands/resume)** | Conversations | `/switch`, `/conversation` | 打开 [会话选择器浮层](/docs/cli/commands/resume) 以选择并加载先前的线程。 |
| **`/rewind`** | Conversations | `/undo` | 将对话历史回滚到先前的某条消息。 |
| **`/skills`** | Tools & Tasks | — | 浏览已加载的本地和全局 Agent Skill（技能）。 |
| **[`/statusline`](/docs/cli/commands/statusline)** | Configurations | — | 打开 statusline（状态栏/状态行）自定义浮层。 |
| **`/tasks`** | Tools & Tasks | — | 打开任务管理器面板以监控后台 shell 执行日志。 |
| **[`/teamwork-preview`](/docs/teamwork)** `<task>` | Reasoning | `/teamwork` | 为长期演进项目启动 [多 Agent 协作团队](/docs/teamwork)（付费方案）。 |
| **[`/title`](/docs/cli/commands/title) \[on/off\]** | Configurations | — | 切换或设置终端窗口标题更新。 |
| **[`/usage`](/docs/cli/commands/usage)** | Utilities | `/quota` | 显示模型配额使用情况。 |
| **[`/voice`](/docs/cli/commands/voice)** | Utilities | `/record` | 使用麦克风进行语音听写 prompt。 |

## 默认按键绑定

映射全局、prompt、导航及审批操作的键盘快捷键命令。

### 全局控制

无论当前焦点位于哪个面板、浮层或 prompt，这些快捷键始终处于活跃状态。

| 按键 | TUI 命令 | 操作行为 |
| :-- | :-- | :-- |
| **`Esc`** | `cli.escape` | 关闭活跃面板、停止当前流式输出或清空空 prompt。 |
| **`Ctrl+C`** | `cli.exit` | 终止 CLI 会话（若 agent 正在工作中会提示确认）。 |
| **`Ctrl+D`** | `cli.exit` | 退出 CLI 会话（仅当 prompt 输入框为空时有效）。 |
| **`Ctrl+L`** | `cli.clear_screen` | 刷新并清空可视终端缓冲区。 |

### Prompt 焦点按键

在 prompt 输入框内编写指令时，这些按键生效。

| 按键 | TUI 命令 | 操作行为 |
| :-- | :-- | :-- |
| **`Enter`** | `prompt.submit` | 向 agent 提交 prompt 或当前选中的菜单项。 |
| **`Shift+Enter`** / **`Ctrl+J`** | `prompt.newline` | 插入换行符而不提交。 |
| **`Ctrl+V`** | `prompt.paste` | 将图形媒体文件或剪贴板内容粘贴到 prompt 中。 |
| **`Ctrl+O`** | `prompt.toggle_trajectory` | 展开或折叠详细的工具推理输出。 |
| **`Ctrl+R`** | `prompt.open_review` | 打开 Artifact 审查面板。 |
| **`Ctrl+G`** | `prompt.external_editor` | 启动系统默认的 `$EDITOR` shell 来编写 prompt。 |
| **`Alt+J`** | `prompt.teleport_agent` | 立即将焦点切换到下一个等待确认的 subagent（子代理）。 |
| **`Ctrl+K`** | `prompt.fast_approve` | 快速批准状态告警中列出的待处理 subagent 操作。 |
| **`Ctrl+A`** | `prompt.cursor_start` | 将光标移动到行首。 |
| **`Ctrl+E`** | `prompt.cursor_end` | 将光标移动到行尾。 |
| **`Ctrl+Z`** | `prompt.undo_text` | 撤销上一次编辑。 |
| **`Ctrl+Shift+Z`** | `prompt.redo_text` | 重做上一次撤销的文本操作。 |
| **`Ctrl+D`** | `—` | 向前删除字符（仅当 prompt 输入框非空时有效）。 |
| **`F5`** | `voice.start_dictation` | 开始或停止 [语音听写](/docs/cli/commands/voice)。 |

### 导航与滚动

在选择面板、菜单和可滚动的文本框内使用。

| 按键 | TUI 命令 | 操作行为 |
| :-- | :-- | :-- |
| **`↑`** / **`↓`** | `navigation.up` / `navigation.down` | 将高亮选区向上或向下移动一项。 |
| **`PgUp`** / **`Shift+↑`** | `navigation.page_up` | 将活跃文本视口向上滚动一整页。 |
| **`PgDn`** / **`Shift+↓`** | `navigation.page_down` | 将活跃文本视口向下滚动一整页。 |
| **`←`** / **`→`** | `navigation.left` / `navigation.right` | 在多页结构中切换页面（如会话选择器）。 |
| **`Tab`** | `navigation.tab` | 确认高亮的 slash command 自动补全选项。 |

### 工具确认

在确认提示浮层出现时生效。

| 按键 | TUI 命令 | 操作行为 |
| :-- | :-- | :-- |
| **`y`** | `confirm.yes` | 批准提议的工具、命令或当前 artifact。 |
| **`n`** | `confirm.no` | 拒绝提议的工具、命令或当前 artifact。 |
| **`A`** | `—` | （在 Review Panel 内）一次性批准所有生成的 artifact（内置快捷键）。 |

## 配置项 (`settings.json`)

主要的设置键名、数据类型、系统默认值以及预期参数。

### `settings.json` 示例

```json
{
    "colorScheme": "tokyo night",
    "altScreenMode": "always",
    "toolPermission": "request-review",
    "notifications": true,
    "enableTerminalSandbox": true
}
```

| 配置键名 | 取值类型 | 系统默认值 | 参数特性与可选值 |
| :-- | :-- | :-- | :-- |
| **`colorScheme`** | string | `"terminal"` | 颜色主题：`"light"`、`"solarized light"`、`"colorblind-friendly light"`、`"dark"`、`"solarized dark"`、`"colorblind-friendly dark"`、`"tokyo night"` 或 `"terminal"`（继承原生 shell 颜色）。 |
| **`altScreenMode`** | string | `"default"` | 屏幕缓冲区使用方式：`"default"`（自适应内联/备用屏幕）、`"always"`（强制使用备用屏幕缓冲区 altscreen）或 `"never"`（强制内联顺序输出）。 |
| **`toolPermission`** | string | `"request-review"` | 全局安全预设：`"request-review"`（在调用写入/bash/web 工具前提示）、`"proceed-in-sandbox"`（在 sandbox 内自动放行）、`"always-proceed"`（从不提示）或 `"strict"`（对所有非只读工具均提示）。 |
| **`artifactReviewPolicy`** | string | `"asks-for-review"` | 代码审查策略：`"asks-for-review"`（写入代码前始终提示）、`"agent-decides"`（动态提示）或 `"always-proceed"`（从不提示）。 |
| **`notifications`** | boolean | `false` | 任务完成时发出系统桌面通知及终端响铃提示音。 |
| **`showTips`** | boolean | `true` | 在生成 turn（轮次）期间在 prompt 面板上方显示实用的 agent 提示。 |
| **`showFeedbackSurvey`** | boolean | `true` | 在活跃任务完成时定期显示质量反馈调查。 |
| **`editor`** | string | `"auto"` | 目标文本编辑器工具：`"auto"`（查阅系统 `$EDITOR`）、`"vim"`、`"emacs"` 或自定义文本标识。 |
| **`editorMode`** | string | `"default"` | Prompt 编辑模式：`"default"`（扁平文本编辑）或 `"vim"`（模态编辑）。与用于选择外部程序的 `editor` 不同。请参阅 [Vim 编辑模式](/docs/cli/vim-editor-mode)。 |
| **`vimInsertFirst`** | boolean | `false` | 以 Insert 模式启动 Vim 编辑，并使直接按 `Enter` 提交。需要将 `editorMode` 设置为 `"vim"`。 |
| **`allowNonWorkspaceAccess`** | boolean | `false` | 允许 agent 的文件读取和写入工具导航访问所识别的 Git/workspace 根目录之外的文件。 |
| **`enableTerminalSandbox`** | boolean | `false` | 将 agent 发起的所有本地执行命令限制在操作系统级安全隔离环（sandbox）内。 |
| **`useG1Credits`** | boolean | `false` | _仅限外部构建版本。_ 当方案配额耗尽后，使用个人 AI 积分进行模型调用。 |
| **`enableTelemetry`** | boolean | `true` | 允许收集指标数据并回传崩溃日志以提升工具可靠性。 |
| **`verbosity`** | string | `"high"` | 视觉输出详细程度级别：`"high"`（渲染完整思考过程与工具输出）或 `"low"`（仅显示极简的视觉进度指示器）。 |
| **`runningLightSpeed`** | string | `"medium"` | 视觉流水灯进度动画速度：`"fast"`、`"medium"`、`"slow"` 或 `"off"`。 |

## 后续步骤

了解如何安全地部署权限策略、sandbox（沙箱）以及自定义 plugin（插件）：

*   **[权限与沙箱](/docs/cli/sandbox)**：强制执行命令行隔离规则。
*   **[插件与技能](/docs/cli/plugins)**：创建你自己的自定义 skill（技能）slash commands。
*   **[安装与认证](/docs/cli/install)**：更新你的 CLI 安装。