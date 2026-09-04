# Sandbox（沙箱）

在隔离环境中运行 agent 的 shell 命令，保护你的文件系统和工作站。

## 工作原理

启用终端 sandbox 后，Antigravity CLI 会在操作系统级别的隔离边界内执行命令。命令可以对你的 workspace、临时目录和常用构建缓存进行写入，并可读取 `/usr` 和 `/etc` 等系统目录以保证你的工具正常运行。类似 `~/.ssh` 和 `.env` 这样的敏感文件将被阻止访问，任何未明确挂载的内容在 sandbox 内部都是不可见的，并且网络访问受限于你已批准的域名。

sandbox 基于原生操作系统底层机制构建，因此无需管理虚拟机或 Docker 镜像，也没有任何启动延迟：

| 操作系统 | 技术方案 | 详细说明 |
| :-- | :-- | :-- |
| **Linux** | Namespaces | 内核命名空间（Kernel namespaces）用于隔离文件系统、隐藏宿主进程并切断网络连接。 |
| **macOS** | `sandbox-exec` | Seatbelt 配置方案（SBPL）用于限制文件系统访问和套接字（socket）连接。 |

## 配置

在 `~/.gemini/antigravity-cli/settings.json` 中启用 sandbox，或通过 `/config` 交互式启用：

```json
{
    "enableTerminalSandbox": true,
    "toolPermission": "proceed-in-sandbox"
}
```

*   **`enableTerminalSandbox`**（布尔值，默认值：`false`）：在 sandbox 内运行 agent 命令。
*   **`toolPermission`**（字符串，默认值：`"request-review"`）：将其设置为 `"proceed-in-sandbox"` 可让处于 sandbox 内的命令自动运行，而需要运行在 sandbox 外部的命令仍会提示进行审核。有关其他模式，请参阅 [设置](/docs/cli/settings)。

### CLI 命令行参数

你也可以在启动 CLI 时控制 sandbox 行为：

```bash
# 在当前会话中强制启用 sandbox
antigravity --sandbox
```

*   **`--sandbox`**：在当前会话中启用 sandbox，覆盖 `settings.json` 中的配置。

## 权限集成

sandbox 会从你的 **[Permissions（权限）](/docs/cli/permissions)** 配置中推导其访问边界：

*   **文件系统**：workspace 文件夹以及在 `write_file` 下允许的路径均以读写方式挂载。在默认系统挂载之上，在 `read_file` 下允许的路径以只读方式挂载。被拒绝的路径将被阻止，其他所有路径均无法访问。
*   **网络**：默认情况下，sandbox 内部的命令在无网络访问权限下运行。在 `read_url` 下允许的域名会被添加到 sandbox 的出站允许列表中。
*   **逃生舱机制（`unsandboxed`）**：匹配 `unsandboxed` 允许 rule（规则）的命令无需提示即可在 sandbox 外部运行。这对于无法在隔离边界内运行的工具非常有用，例如 Docker 或与系统服务通信的命令。

agent 也可以主动请求在 sandbox 外部运行命令——例如，重试因 sandbox 限制而失败的命令。除非该命令匹配 `unsandboxed` 允许 rule，否则这些请求始终需要你的批准。

### 示例

```json
{
    "permissions": {
        "allow": [
            "command(npm test)",
            "command(git diff)",
            "unsandboxed(git push)",
            "read_file(/var/log/app)",
            "write_file(src/)"
        ],
        "deny": [
            "command(rm -rf /)",
            "command(sudo *)",
            "write_file(/home/user/.ssh)"
        ]
    }
}
```

在此配置下：

*   `npm test` 和 `git diff` 在 sandbox 内部运行。
*   `git push` 通过 `unsandboxed(git push)` 在 sandbox 外部运行。
*   `rm -rf /` 和 `sudo` 始终被阻止。

## 交互式提示

当命令需要审核时，你可以单次批准它，也可以将此次批准转换为长期有效的 rule：

```
Do you want to proceed?
1. Yes
2. Yes, and always allow in this conversation for commands that start with 'npm test'
3. Yes, and always allow for commands that start with 'npm test' (Persist to settings.json)
4. No
```

当 agent 请求绕过 sandbox 时，prompt 会明确指出，以便你评估风险：

```
🔓 Allow sandbox bypass for command execution?
⚠️ Confirm the command is safe to run outside of the sandbox with full network and disk access.
```

在此处批准“始终允许”（always allow）将记录一条 `unsandboxed(...)` rule，而不是普通的 `command(...)` rule。

## 参见

*   **[Hub Sandbox](/docs/sandbox)**：了解 Antigravity 2.0 中的 sandbox 工作原理。
*   **[Permissions](/docs/cli/permissions)**：配置 allow、deny 和 ask 规则。
*   **[Settings](/docs/cli/settings)**：全局 CLI 偏好设置与配置。