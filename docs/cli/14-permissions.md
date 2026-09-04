# Permissions（权限）

保护你的本地工作站、限制绝对文件路径、配置自定义 allow / deny / ask 策略，并管理交互式审批。你还可以使用 **[Permissions 命令（`/permissions`）](/docs/cli/commands/permissions)** 交互式管理这些 rule（规则）。

## 细粒度权限

为了在支持自主工作流的同时保护你的工作站安全，Antigravity CLI 集成了强大的**细粒度权限引擎（Fine-Grained Permissions Engine）**。agent 执行的每一项敏感操作都被表示为一个**权限资源（permission resource）**，格式为 `action(target)`。

权限会根据全局设置中配置的三个独立访问控制列表进行评估：

```
~/.gemini/antigravity-cli/settings.json
```

*   **`deny`**：该操作立即被阻止。
*   **`ask`**：agent 会暂停并在继续执行前提示请求你的明确批准。
*   **`allow`**：该操作无需提示自动获批。

> [!NOTE]
> **优先级规则（Precedence Rule）**：存在冲突的 rule 会严格按照优先级顺序评估：**Deny > Ask > Allow**。例如，如果你在 `ask` 列表中配置了 `command(*)`，并在 `allow` 列表中配置了 `command(git)`，则 `ask` rule 具有更高优先级，会在执行每条命令前进行提示。

## 支持的 action 与匹配规则

细粒度权限遵循标准的 schema 模式：

```
action(target)
```

支持的 action、目标格式规范和匹配算法如下：

| Action | 目标格式 | 匹配行为 | 默认回退 |
| :-- | :-- | :-- | :-- |
| **`read_file`** | `read_file(/path)`、`read_file(dir)` 或 `read_file(*)` | 匹配绝对路径或相对于 workspace 根目录的相对路径。递归授予对其包含的所有文件/文件夹的读取权限。`read_file(*)` 匹配系统上的所有文件。 | **Ask**（在 workspace 内自动允许） |
| **`write_file`** | `write_file(/path)` 或 `write_file(*)` | 与 `read_file` 相同。对完全相同的目标路径隐式授予 `read_file` 权限。 | **Ask**（在 workspace 内自动允许） |
| **`read_url`** | `read_url(domain)` 或 `read_url(*)` | 匹配主机名和子域名（例如 `google.com` 覆盖 `mail.google.com`）。忽略 URL 路径段。`read_url(*)` 匹配任何域名。 | **Ask** |
| **`execute_url`** | `execute_url(domain)` 或 `execute_url(*)` | 在某个域名上操作网页元素（点击、输入）或驱动交互式浏览器工作流。 | **Ask** |
| **`command`** | `command(prefix)`、`command(regex)` 或 `command(*)` | 按精确的单词/token（标记）前缀匹配命令。每个由空格分隔的 token 都作为锚定的正则表达式（`^(?:pattern)$`）进行评估。<br><br>例如，`command(npm run (build\|lint\|test))` 匹配 `npm run build` 和 `npm run test`。 | **Ask** |
| **`unsandboxed`** | `unsandboxed(prefix)` 或 `unsandboxed(*)` | 按精确的单词/token 前缀匹配命令。匹配此授权的命令将在容器隔离外部执行（仅在启用终端 sandbox 时适用）。 | **Ask** |
| **`mcp`** | `mcp(server/tool)` 或 `mcp(*)` | 匹配具体的 MCP tool 或指定服务器上的所有 tool（适用于本地 `mcp` 服务器和远程连接）。`mcp(*)` 匹配任何 tool。 | **Ask** |

### 全局通配符语法

在所有支持的 action 类型中，传入全局通配符 `*`（例如 `read_file(*)`、`command(*)`、`mcp(*)`）将匹配该整个 action 命名空间下的所有目标。

### 隐式权限规则

*   **写入隐含读取（Write implies Read）**：在某个路径上允许 `write_file` 会自动授予该路径上的 `read_file` 权限。
*   **拒绝读取隐含拒绝写入（Deny Read implies Deny Write）**：在某个路径上拒绝 `read_file` 会立即阻止该路径上的 `write_file` 权限。

### 跨平台路径归一化

Antigravity 可确保你的权限 rule 在 macOS、Linux 或 Windows 上开发时均能完美运行。在 macOS 和 Linux 上，路径使用标准正斜杠（`/`）。在 Windows 上，Antigravity 会在 rule 评估之前自动归一化路径：去除盘符（例如 `C:`）并将所有反斜杠（`\`）转换为正斜杠（`/`）。

* * *

## 默认系统行为与安全护栏

当某个操作未明确列在你的 `allow`、`deny` 或 `ask` 列表中时，系统会回退到安全的系统默认行为：

1.  **Workspace 自动允许**：在标准操作中，当前活动项目目录内的文件读写是自动允许的。
2.  **网页浏览默认为 Ask**：`read_url` 和 `execute_url` 操作默认为 **Ask**。除非配置了 allow 规则，否则在 agent 导航到任何网页或在网页上执行操作之前，都会暂停并提示请求你的批准。
3.  **未配置的操作默认为 Ask**：所有其他未配置的操作（`command`、`mcp`、`execute_url`、非 workspace 文件）均默认为 **Ask**。

* * *

## 交互式权限提示

当 agent 遇到需要审批的操作（**Ask** 模式）时，TUI 中会出现一张交互式 prompt 卡片。

在为文件、URL 或 MCP 权限确认 **Allow** 之前，你可以直接在 prompt 卡片中编辑目标字符串以扩大授予的范围（例如，将针对单个文件的请求 `/project/file.txt` 扩大为其父目录 `/project`）。CLI 会验证你编辑后的目标是否安全地涵盖了该操作，并在当前 turn（轮次）的剩余时间中应用扩展后的授权，避免对相关操作重复弹出提示。*（注意：终端命令不支持作用域编辑）。*

* * *

## 配置示例

将以下 rule 添加到你的 `~/.gemini/antigravity-cli/settings.json` 文件中：

```json
{
    "permissions": {
        "allow": [
            "command(git)",
            "command(npm run (build|lint|test))",
            "unsandboxed(git push)",
            "read_file(/var/log/app)",
            "write_file(src/)",
            "read_url(google.com)",
            "mcp(linter/*)"
        ],
        "deny": [
            "command(rm -rf)",
            "command(curl .*)",
            "command(sudo)",
            "write_file(.git/)",
            "write_file(/home/user/.ssh)"
        ],
        "ask": ["command(*)", "execute_url(aws.amazon.com)", "mcp(sql/execute_mutation)"]
    }
}
```

## 参见

*   **[Permissions 命令](/docs/cli/commands/permissions)**：在 TUI 中交互式管理 rule。
*   **[Sandbox 定制](/docs/cli/sandbox)**：实施操作系统级容器隔离边界。
*   **[Plugin 与 Skill](/docs/cli/plugins)**：创建你自己的自定义 skill 和 slash command。
*   **[设置、渲染与 Keybindings](/docs/cli/settings)**：自定义键盘快捷键与缓冲区。