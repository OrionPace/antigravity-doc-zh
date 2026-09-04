# 从 Gemini CLI 迁移

转换您的旧版配置、将 Gemini CLI 扩展导入为原生 plugin（插件）、适配自定义 skill（技能）路径，并重新格式化 Model Context Protocol（MCP）配置。

## 概述

Antigravity CLI 保持了对 Gemini CLI 所普及的核心开发者体验机制的向后兼容性。为确保无缝升级，CLI 提供了自动初始化迁移引导以及明确的 CLI 迁移命令序列。

## 首次启动引导

当您在包含旧版配置的环境中首次执行 `agy` 时，CLI 会自动检测您现有的配置文件。交互式检查清单会提示您选择要迁移的资产：

1. **自动转换（Auto-conversion）**：选择您希望转换的扩展与全局配置。
2. **密钥环存储（Keyring storage）**：CLI 会安全地将您活跃的会话 token 迁移至操作系统的原生密钥环（keyring）存储中。
3. **设置对齐（Settings alignment）**：默认视觉参数和渲染缓冲区将自动映射到您的新设置配置文件中。

> [!NOTE]
> **部分对齐（Partial Parity）**：虽然我们保留了对 workspace skill、rule 以及 MCP 服务器的支持，但 Gemini CLI 中某些自定义终端主题或实验性视觉叠加层可能不受支持。

## 将扩展转换为 plugin

自 Gemini CLI 发布以来，行业已将此类扩展标准化称为 **plugin（插件）**。您可以通过执行以下命令，将旧版 Gemini 扩展手动转换为原生 Antigravity plugin：

```
agy plugin import gemini
```

该实用工具会搜索您的旧版本地目录，解析扩展 manifest 清单，并将文件转换为原生布局块。

### 预期导入输出

```
[ok]   conductor-tools
       - skills     : skipped (none detected)
       - agents     : skipped (none detected)
       ✔ commands   : 4 legacy commands converted to skills
       - mcpServers : skipped (none detected)
[ok]   google-workspace
       ✔ skills     : 5 skills processed
       - agents     : skipped (none detected)
       ✔ commands   : 2 legacy commands converted to skills
       ✔ mcpServers : 1 server definition migrated to mcp_config.json
```

## 上下文文件与 workspace rule

两个 CLI 平台使用完全相同的 workspace 上下文 rule（规则）。您现有的 rule 文档无需进行任何修改：

* **Workspace 本地上下文**：agent 继续解析并强制执行当前活动目录中 `GEMINI.md` 和 `AGENTS.md` 文件内定义的 rule 约束。
* **全局开发者上下文**：agent 自动查阅并强制执行位于 `~/.gemini/GEMINI.md` 的全局约束。

## 更新后的 skill 路径

虽然全局共享 skill 仍保留在您的用户主目录中，但本地特定于 workspace 的 skill 目标文件夹路径已更新。

| 配置 | Gemini CLI | Antigravity CLI |
| :-- | :-- | :-- |
| **全局共享路径** | `~/.gemini/skills/` | `~/.gemini/antigravity-cli/skills/` |
| **Workspace 项目路径** | `.gemini/skills/` | `.agents/skills/` |

> [!NOTE]
> **需要操作**：如果您的项目中包含在 `.gemini/skills/` 中定义的自定义 workspace skill，您必须手动重命名或将该文件夹移动至 `.agents/skills/`，以便 Antigravity agent 将其识别为活跃的 slash command。

## MCP 配置格式变更

Antigravity CLI 将 Model Context Protocol（MCP）服务器分离到独立的轻量级 JSON 配置文件中，而不是嵌套在主偏好设置配置中。

### 目录映射

* **旧版 Gemini 配置**：服务器以内联方式声明在 `~/.gemini/settings.json` 中。
* **Antigravity CLI 配置**：服务器定义在独立的 `mcp_config.json` 配置文件中：
    * 全局服务器：`~/.gemini/config/mcp_config.json`
    * Workspace 服务器：`.agents/mcp_config.json`

### 必需的 Schema 更新

手动迁移远程 WebSocket 或 SSE 服务器定义时，请更新 URI 键参数以匹配当前标准：

* **旧版 Schema 键**：`url` 或 `httpUrl`
* **现代 Schema 键**：`serverUrl`

```
{
    "mcpServers": {
        "remote-indexer": {
            "serverUrl": "https://mcp.internal.enterprise.com/sse",
            "env": {
                "AUTH_TOKEN": "secure_alpha_token"
            }
        }
    }
}
```

## 后续步骤

开始配置您的新视觉参数并排查任何设置异常：

* **[设置、渲染与键位绑定](/docs/cli/settings)**：自定义键盘快捷键、主题与屏幕缓冲区。
* **[问题排查](/docs/cli/troubleshooting)**：了解如何解决身份验证锁定或路径问题。
* **[CLI 参考](/docs/cli/reference)**：查阅标准参数列表与 slash command 映射。