# Plugins 与 Skills

扩展 agent 能力、安装第三方扩展包、封装自定义工作流 skill，并与 Model Context Protocol (MCP) server 交互。

## 可扩展性模型

Antigravity CLI 专为无限自定义而设计。您可以通过安装名为 **Plugin（插件）** 的结构化软件包模块，或创建名为 **Skill（技能）** 的本地化 Markdown 蓝图，来增强共享的 agent harness（代理底座）。

这些自定义功能允许 agent 访问专属的专有命令、调用特定领域的 subagent（子代理），并遵循定制的代码风格约束。

## Antigravity Plugins

Plugin 是具有命名空间的资源包，将自定义 skill、后台 subagent、代码检查（linting）rule、Model Context Protocol 定义以及事件 hook（钩子）打包为一个单一的可部署资产。

### Plugin 文件系统结构

当您安装或导入 plugin 时，CLI 会将资源包文件存放在全局配置路径中：

```
~/.gemini/antigravity-cli/plugins/<plugin_name>/
```

一个规范的 plugin 包含以下结构布局：

```
~/.gemini/antigravity-cli/plugins/<plugin_name>/
├── plugin.json                 # 必需的包标记清单文件
├── mcp_config.json             # 可选的 Model Context Protocol servers 配置
├── hooks.json                  # 可选的工具调用前/后事件 hooks
├── skills/                     # 可选的专用 skills 目录
├── agents/                     # 可选的 subagent 定义模板
└── rules/                      # 可选的自定义代码库 rules 文件
```

### Plugin 清单文件 (plugin.json)

`plugin.json` 文件是位于 plugin 目录根目录下的必需清单文件。它定义了 plugin 的标识与元数据。

**清单示例**

```json
{
    "$schema": "https://antigravity.google/schemas/v1/plugin.json",
    "name": "my-plugin",
    "description": "A brief description of what my plugin does."
}
```

**字段参考**

| 字段 | 类型 | 必填 | 描述 |
| :-- | :-- | :-- | :-- |
| `name` | String | **是** | plugin 的唯一机器可读名称。仅能包含字母数字字符、连字符和下划线（匹配 `^[a-zA-Z0-9-_]+$`）。该名称用于在 CLI 命令中引用该 plugin。 |
| `description` | String | 否 | 对 plugin 作用的简要人类可读描述，在 plugin 列表中展示。 |

**自动校验**

要在 VS Code 或 WebStorm 等编辑器中启用自动补全与验证，请添加指向官方 schema URL 的 `$schema` 键：

```json
"$schema": "https://antigravity.google/schemas/v1/plugin.json"
```

**完整 JSON Schema**

```json
{
    "$schema": "https://antigravity.google/schemas/v1/plugin.json",
    "title": "Antigravity Plugin Manifest",
    "description": "Schema for Antigravity CLI plugin manifest files (plugin.json)",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The unique, machine-readable name of the plugin. Must contain only alphanumeric characters, hyphens, and underscores.",
            "pattern": "^[a-zA-Z0-9-_]+$"
        },
        "description": {
            "type": "string",
            "description": "A brief human-readable description of the plugin's purpose and capabilities."
        }
    },
    "required": ["name"],
    "additionalProperties": false
}
```

### 通过 CLI 子命令管理 Plugin

CLI 提供了 `plugin`（或复数 `plugins`）子命令体系来管理您的扩展：

*   **列出已安装的 plugin**：显示当前激活的包及其加载的组件。
    
    ```bash
    agy plugin list
    ```
    
*   **安装本地或远程 plugin**：将包目录部署到本地配置中。
    
    ```bash
    agy plugin install /path/to/local/plugin
    ```
    
*   **禁用/启用 plugin**：停用 plugin 的工具而不删除其资产。
    
    ```bash
    agy plugin disable <plugin_name>
    agy plugin enable <plugin_name>
    ```
    
*   **卸载 plugin**：清除包目录并清理注册表。
    
    ```bash
    agy plugin uninstall <plugin_name>
    ```

## Agent Skills

Skill 是声明式的、人类可读的 Markdown 文件，为专业化工程任务概述了明确的指导协议、脚本与目标资源。

注册之后，**Skill 会在 TUI 中自动转换为 slash commands**，允许您手动调用它们（例如，输入 `/refactor-ui`）。

### 创建本地 Workspace Skill

要部署随 Git 仓库一同保存的 workspace 专属 skill：

1.  在项目根目录下创建一个名为 `.agents/skills/` 的目录。
2.  在其中起草一个扩展名为 `.md` 的 Markdown 文件（如 `format-tests.md`）。
3.  定义该 skill 的 Frontmatter 元数据（参见下文示例）。
4.  在元数据下方，为 agent 编写明确的指令。当您在此目录下运行 `agy` 时，该 skill 会被自动编译，并且 `/format-tests` 将在 prompt 输入框中可用。

**Frontmatter 示例：**

```markdown
---
name: format-tests
description: Standardize and re-format Python unittest assertions
---
```

### 共享全局 Skill

要在工作站上的所有 workspace 之间共享 skill，请将目标 Markdown 文件放入全局配置路径中：

```
~/.gemini/antigravity-cli/skills/
```

只要您在任何目录下启动 `agy`，该目录中的任何 Markdown skill 都会自动作为全局 slash command 被导入。

## 管理 Hooks

Hook 会在 agent 操作执行之前或执行之后立即进行拦截。它们非常适合用于运行自动化预检（pre-flight checks）或生成后格式化（例如在写入文件后运行 `prettier`）。

Hook 定义在 plugin 的 `hooks.json` 中，或者配置在您的主要 `settings.json` 文件中。您可以在 TUI 中输入以下命令查看所有已加载且激活的 hook：

```bash
/hooks
```

## Model Context Protocol (MCP)

Model Context Protocol 是一项开放标准，使基础模型能够安全地与本地 API、文件解析器和自定义开发者工具进行交互。

有关在 Antigravity CLI 中配置本地与远程 MCP server、访问交互式 `/mcp` 管理器浮层面板、以及理解 server schema 与身份验证的完整文档，请参阅专属的 [MCP 文档](/docs/mcp)。

## 后续步骤

了解如何从 Gemini CLI 迁移现有配置以及排查连接异常：

*   **[从 Gemini CLI 迁移](/docs/cli/gcli-migration)**：快速迁移您的旧版扩展和配置。
*   **[故障排除](/docs/cli/troubleshooting)**：解决终端 hook 错误、锁定或网络故障。
*   **[权限与 Sandbox](/docs/cli/sandbox)**：为您自定义的 plugin 和 MCP server 配置安全隔离环（containment rings）。