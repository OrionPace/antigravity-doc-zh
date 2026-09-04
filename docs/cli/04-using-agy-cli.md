# 使用 AGY CLI

### 配置（Settings）

Antigravity CLI 提供了灵活的配置系统，用于自定义 workspace 行为、安全限制、编辑器偏好、视觉样式以及性能表现。

*   **配置文件**：存储在纯 JSON 文件 `~/.gemini/antigravity-cli/settings.json` 中。
*   **设置面板**：输入 `/config` 或 `/settings` 可打开全屏浮层菜单，列出所有可用选项。
    *   选择某项配置即可打开其选项列表或文本输入字段。
    *   立即将你的选择保存到磁盘并返回主列表。
*   **覆盖配置**：部分配置可在启动时通过 CLI flags 进行覆盖（例如 `--sandbox` 或 `--dangerously-skip-permissions`）。
    *   设置菜单中会显示一个指示器，标明该覆盖项的来源（例如：_Sandbox Mode on overridden by `--sandbox`_）。
    *   你仍然可以编辑磁盘上的持久化配置，但当前会话将强制执行命令行覆盖规则，直到重新启动。

### 快捷技巧（Quick Tips）

| 操作 / 功能 | 技巧 / 命令 |
| :-- | :-- |
| **自动补全文件路径** | 输入 `@` 将触发路径补全建议 |
| **清空 Prompt** | 连按两下 `esc esc` 即可清空 prompt 输入框（在无流式输出时有效） |
| **终端命令** | 在 prompt 开头输入 `!` 可直接运行终端命令 |
| **帮助** | 输入 `?` 获取帮助并列出所有 Slash Command |
| **减少 Tool Call 干扰** | 在 `/config` 中将详细程度（verbosity）设置为 **low**，以最大限度减少大量 tool call 产生的输出干扰 |
| **管理权限** | 通过 `/config` 或 `/permissions` 管理权限 |
| **回退对话** | 使用 `/rewind` 或 `/undo` 回退对话历史 |
| **分叉对话** | 使用 `/fork` 启动一个独立的 workspace，并从之前的节点分支对话 |
| **清空对话** | 使用 `/clear` 清空 prompt 并开启全新对话会话 |
| **恢复对话** | 使用 `/resume` 列出并恢复之前的对话日志 |
| **自动保存恢复** | 当你关闭 CLI 时，它会自动打印恢复该特定会话所需的精确命令 |

### 快捷键（Keybindings）

AGY CLI 支持自定义快捷键。你可以通过输入 `/keybindings` 或直接修改 JSON 文件来进行编辑。

*   **文件路径**：`~/.gemini/antigravity-cli/keybindings.json`。
*   **重置**：若要重置为默认值，只需删除 `keybindings.json` 文件。

**默认快捷键**

| 操作 / 命令 | 按键 | 用途 |
| :-- | :-- | :-- |
| **清空 TUI 屏幕** | `ctrl+l` | 清除终端输出 |
| **确认 / 提交** | `enter` | 提交 prompt 或选择项 |
| **退出 / 取消** | `ctrl+c`, `esc` | 停止流式输出、关闭菜单或清空 prompt |
| **退出 CLI** | `ctrl+d` | 终止 CLI TUI 会话 |
| **挂起 CLI** | `ctrl+z` | 将 CLI 会话推到终端后台运行 |
| **编辑命令** | `e` | 打开编辑器以编辑提议的终端命令 |
| **确认拒绝 (No)** | `n` | 拒绝执行终端命令 |
| **确认同意 (Yes)** | `y` | 批准执行终端命令 |
| **打开外部编辑器** | `ctrl+g` | 在你的默认 Shell 编辑器中编辑 prompt |
| **粘贴文本** | `ctrl+v` | 从剪贴板粘贴文本 |
| **重做文本编辑** | `ctrl+shift+z` | 重做上一次撤销的文本更改 |
| **撤销文本编辑** | `ctrl+_`, `ctrl+shift+-` | 撤销上一次文本更改 |
| **复制 (Yank)** | `ctrl+y` | 复制选中的文本 |
| **向下导航** | `down` | 在菜单列表中向下滚动 |
| **跳至底部** | `ctrl+end` | 将 TUI 视图直接跳转到底部 |
| **跳至顶部** | `ctrl+home` | 将 TUI 视图直接跳转到顶部 |
| **向左移动** | `left` | 将 prompt 光标向左移动 |
| **向下翻页** | `pgdown`, `shift+down` | 向下滚动 TUI 页面 |
| **向上翻页** | `pgup`, `shift+up` | 向上滚动 TUI 页面 |
| **向右移动** | `right` | 将 prompt 光标向右移动 |
| **Tab / 切换焦点** | `tab` | 自动补全选项或切换组件焦点 |
| **向上导航** | `up` | 在菜单列表中向上滚动 |
| **换行** | `alt+enter`, `ctrl+j`, `shift+enter` | 在 prompt 中插入换行而不提交 |

你可以在 JSON 文件中将单个操作映射到多个快捷键。若要禁用某个快捷键，请将列表设为空（例如 `[]`）。如果文件格式损坏，CLI 将使用有效的部分，并在损坏的操作上回退到默认快捷键。

注意

**重要说明**：快捷键 `cli.exit` 与 `cli.enter` 无法被禁用。