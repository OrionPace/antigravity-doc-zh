# 权限（Permissions）

保护您的本地工作站安全，限制绝对文件路径，配置自定义的允许/拒绝/询问策略，并管理交互式审批。您也可以使用 **[权限命令（Permissions Command）](/docs/cli/commands/permissions)** 以交互方式管理这些规则。

## 细粒度权限（Fine-grained permissions）

为了在启用自主工作流的同时保护工作站安全，Antigravity CLI 集成了强大的 **细粒度权限引擎（Fine-Grained Permissions Engine）**。agent 执行的每一项敏感操作都表示为一个 **权限资源（permission resource）**，其格式为 `action(target)`。

权限在全局设置中配置的三个不同的访问列表中进行评估：

```
~/.gemini/antigravity-cli/settings.json
```

*   **`deny`**：该操作被立即阻止。
*   **`ask`**：agent 暂停并提示您明确批准后再继续。
*   **`allow`**：该操作自动批准，无需提示。

注意

**优先级规则**：冲突规则严格按优先级顺序评估：**Deny > Ask > Allow**。例如，如果您在 `ask` 列表中配置了 `command(*)`，并在 `allow` 列表中配置了 `command(git)`，则 `ask` 规则优先，会在每条命令执行前进行提示。

## 支持的操作与匹配规则

细粒度权限遵循标准模式结构：

```
action(target)
```

支持的操作、目标格式规范及匹配算法如下：

| 操作 | 目标格式 | 匹配行为 | 默认回退 |
| :-- | :-- | :-- | :-- |
| **`read_file`** | `read_file(/path)`、`read_file(dir)` 或 `read_file(*)` | 匹配绝对路径或相对于 workspace 根目录的路径。授予对所有包含的文件/文件夹的递归读取权限。`read_file(*)` 匹配系统上的所有文件。 | **Ask**（workspace 内自动允许） |
| **`write_file`** | `write_file(/path)` 或 `write_file(*)` | 与 `read_file` 相同。隐式授予对完全相同目标路径的 `read_file` 权限。 | **Ask**（workspace 内自动允许） |
| **`read_url`** | `read_url(domain)` 或 `read_url(*)` | 匹配主机名和子域名（例如，`google.com` 涵盖 `mail.google.com`）。忽略 URL 路径段。`read_url(*)` 匹配任何域名。 | **Ask** |
| **`execute_url`** | `execute_url(domain)` 或 `execute_url(*)` | 在网页元素上执行操作（点击、输入）或驱动某个域名上的交互式浏览器工作流。 | **Ask** |
| **`command`** | `command(prefix)`、`command(regex:pattern)` 或 `command(*)` | 默认按字面逐词匹配命令前缀。如果要使用正则表达式，请添加 `regex:` 前缀（例如，`command(regex:npm run (build|lint|test))`）。 | **Ask** |
| **`unsandboxed`** | `unsandboxed(prefix)`、`unsandboxed(regex:pattern)` 或 `unsandboxed(*)` | 默认按字面逐词匹配命令前缀（或使用 `regex:`）。匹配此规则的命令在启用终端 sandbox 时可在容器隔离之外执行。 | **Ask** |
| **`mcp`** | `mcp(server/tool)`、`mcp(server/*)` 或 `mcp(*)` | 匹配指定的 MCP 工具或指定服务器上的所有工具（适用于本地和远程 MCP 服务器）。`mcp(*)` 匹配任何工具。 | **Ask** |

### 全局通配符语法

在所有支持的操作类型中，传递全局通配符 `*`（如 `read_file(*)`、`command(*)`、`mcp(*)`）将匹配该操作命名空间内的所有目标。

### 隐式权限规则

*   **写入隐含读取**：允许对某个路径执行 `write_file` 会自动授予对该路径的 `read_file` 权限。
*   **拒绝读取隐含拒绝写入**：拒绝某个路径的 `read_file` 会立即阻止对该路径的 `write_file`。

### 跨平台路径规范化

Antigravity 确保无论您是在 macOS、Linux 还是 Windows 上进行开发，权限规则都能完美运行。在 macOS 和 Linux 上，路径使用标准正斜杠（`/`）。在 Windows 上，Antigravity 会在规则评估之前自动规范化路径：去除驱动器号（如 `C:`）并将所有反斜杠（`\`）转换为正斜杠（`/`）。

### 跨平台命令匹配

在 Windows shell（如 PowerShell 或 Command Prompt）中，无法干净地拆分为独立单词的命令默认需要精确匹配。要在 Windows 上匹配命令及其子命令，请使用 `regex:` 前缀（例如，使用 `command(regex:git .*)` 允许任何 `git` 命令）。

* * *

## 默认系统行为与安全护栏

当某个操作未明确列在您的 `allow`、`deny` 或 `ask` 列表中时，系统将回退到安全的系统默认值：

1.  **Workspace 自动允许**：在标准操作中，在您的活动项目目录内读写文件是自动允许的。
2.  **Web 浏览默认 Ask**：`read_url` 和 `execute_url` 的操作默认 **Ask**。在 agent 导航到或操作任何网页之前，它会暂停并提示您批准，除非已配置 allow 规则。
3.  **未配置操作默认 Ask**：所有其他未配置的操作（`command`、`mcp`、`execute_url`、非 workspace 文件）默认 **Ask**。

* * *

## 交互式权限提示

当 agent 遇到需要批准的操作（**Ask** 模式）时，TUI 中会出现一个交互式提示卡片。

在确认 **Allow** 文件、URL 或 MCP 权限之前，您可以直接编辑提示卡片中的目标字符串以扩大授予范围（例如，将 `/project/file.txt` 这样的单个文件请求扩展到父目录 `/project`）。CLI 会验证您编辑的目标是否安全地覆盖了该操作，并在当前 turn 的剩余时间内应用扩展后的授权，避免对相关操作重复提示。_（注意：终端命令不支持范围编辑。）_

* * *

## 配置示例

将这些规则添加到您的 `~/.gemini/antigravity-cli/settings.json` 文件中：

```
{
    "permissions": {
        "allow": [
            "command(git)",
            "command(regex:npm run (build|lint|test))",
            "unsandboxed(git push)",
            "read_file(/var/log/app)",
            "write_file(src/)",
            "read_url(google.com)",
            "mcp(linter/*)"
        ],
        "deny": [
            "command(rm -rf)",
            "command(regex:curl .*)",
            "command(sudo)",
            "write_file(.git/)",
            "write_file(/home/user/.ssh)"
        ],
        "ask": ["command(*)", "execute_url(aws.amazon.com)", "mcp(sql/execute_mutation)"]
    }
}
```

## 另请参阅

*   **[权限命令（Permissions Command）](/docs/cli/commands/permissions)**：在 TUI 中以交互方式管理规则。
*   **[Sandbox 自定义](/docs/cli/sandbox)**：强制实施操作系统级容器隔离边界。
*   **[Plugins 与 Skills](/docs/cli/plugins)**：创建您自己的自定义 skills 斜杠命令。
*   **[设置、渲染与按键绑定](/docs/cli/settings)**：自定义键盘快捷键和缓冲区。