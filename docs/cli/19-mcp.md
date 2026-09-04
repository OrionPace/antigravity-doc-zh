# Model Context Protocol (MCP)

Antigravity 支持 [Model Context Protocol (MCP)](https://modelcontextprotocol.io)，这是一项开放标准，允许 AI agent 与编辑器安全地连接到本地开发者工具、数据库、文件解析器以及外部远程 API。该集成不仅为 AI 模型提供了实时上下文，还赋予其超出当前即时 workspace 范围的执行能力。

在本指南中，您将学习如何在各类 Antigravity 产品中连接和配置 MCP server。您也可以直接跳转查看对应产品中的 MCP server 说明：[Antigravity 2.0](/docs/mcp#antigravity-20)、[Antigravity IDE](/docs/mcp#antigravity-ide)、[Antigravity CLI](/docs/mcp#antigravity-cli) 或 [Antigravity SDK](/docs/mcp#antigravity-sdk)。

## 什么是 MCP？

MCP 充当了 Antigravity 与更广泛开发环境之间的通用桥梁。无需再手动将数据库 schema、日志或 API 规范复制粘贴到 prompt 或聊天面板中，MCP 允许 Antigravity 直接获取结构化上下文，或在需要时代表您执行安全的操作。

### 添加上下文

借助 MCP，Antigravity 可以利用来自已连接 MCP server 的实时数据来辅助其推理与建议：

*   编写 SQL 查询时，Antigravity 可以检查您实时的 Neon、Supabase 或 AlloyDB schema，以推荐正确的表名和列名。
*   调试部署故障时，Antigravity 可以直接从 Netlify 或 Heroku 拉取近期的构建日志。

### 添加自定义工具

借助 MCP，Antigravity 可以执行由您已连接 server 所定义的特定且安全的操作：

*   为该 TODO 创建一条 Linear issue。
*   在 Notion 或 GitHub 中搜索身份验证模式。

## Antigravity 2.0

在 Antigravity 2.0 中，您可以通过 **Settings（设置）** 的 **Installed MCP Servers（已安装的 MCP Server）** 区域来管理您的 MCP server。

要查看和更新您的 MCP server：

1.  点击屏幕左下角的 **Settings** 按钮。
2.  选择 **Customizations（自定义）** 并查看 **Installed MCP Servers** 部分。

要从 **Installed MCP Servers** 区域安装 MCP server：

1.  点击 **Add MCP**。这将连接到 MCP Store（一个可搜索的可用 MCP server 列表）。
2.  搜索或向下滚动到您想要安装的 MCP server。
3.  点击 **Add**。

在此界面管理您的 MCP server：

*   **卸载**：点击列表中 MCP server 旁边的垃圾桶图标。
*   **禁用/启用**：点击列表中 MCP server 旁边的开关切换。
*   **刷新**：点击刷新按钮。

## Antigravity IDE

在 Antigravity IDE 中，管理 MCP server 最简单的方式是通过内置的 MCP Store。在 MCP Store 中，您可以浏览、发现并安装受支持的 MCP server。您也可以通过更新 `mcp_config.json` 来安装自定义 server。

使用 MCP Store 的步骤：

1.  点击编辑器 agent 侧边栏顶部的 **…**（更多）按钮，并选择 **MCP Servers**。
2.  悬停在任意受支持的 server 上并点击 **Install**。（或者，点击某个 server 查看详情后再点击 **Install**。）
3.  按照屏幕上的提示进行操作。

安装完成后，来自该 server 的资源和工具将自动在编辑器中可用。

连接到商店中未列出的自定义 MCP server：

1.  点击编辑器 agent 侧边栏顶部的 **…** 按钮，并选择 **MCP Servers**。
2.  点击 **Manage MCP Servers**。
3.  点击 **View raw config**。
4.  使用您的自定义 [MCP server 配置](/docs/mcp#mcp-configuration-structure) 修改 `mcp_config.json` 文件。

该配置文件全局位于 `~/.gemini/config/mcp_config.json`（或在您的 workspace 本地位于 `.agents/mcp_config.json`）。

## Antigravity CLI

Antigravity CLI 同时支持本地 `stdio` 进程和远程主机 MCP server 配置。在 Antigravity CLI 上安装 MCP server 最简单的方式是使用 **交互式 MCP 管理器（Interactive MCP Manager）**。您也可以手动编辑全局 server 配置或 workspace 级别的 `mcp_config.json`。

### 交互式 MCP 管理器

在 prompt 面板中输入 `/mcp` 并按 `Enter` 键即可打开交互式 **MCP Manager 浮层面板**。该面板允许您：

*   查看活动、已断开或加载中 server 的实时状态环。
*   手动重载 server 配置或检查实时连接日志。

### 全局与 Workspace Server 配置

与传统配置不同，Antigravity CLI 将 MCP 定义拆分为专用的分散配置文件：

*   **全局 server 配置**：配置在 `~/.gemini/config/mcp_config.json`。
*   **Workspace 本地配置**：配置在当前活动项目下的 `.agents/mcp_config.json`。

您可以直接使用自定义 [MCP server 配置](/docs/mcp#mcp-configuration-structure) 修改这些文件。

> [!NOTE]
> **远程连接 Schema**：在声明基于远程 SSE、Streamable HTTP 或 websocket 的 MCP 连接时，必须定义 `serverUrl` 字段。不支持诸如 `url` 或 `httpUrl` 等旧字段。

## Antigravity SDK

在基于 [Antigravity SDK](/docs/sdk/overview) 构建的 Python 应用程序中，MCP server（`stdio`、`SSE` 或 `HTTP`）可以通过编程方式在统一执行管道下与内置工具及自定义 Python 函数一同连接。

SDK 会自动发现您 workspace 的 `.agents/mcp_config.json` 文件中配置的 server。您也可以直接使用本地配置实例化 agent：

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
```

## MCP 配置结构

无论是在 Antigravity 2.0、Antigravity IDE 还是 Antigravity CLI 中配置自定义 server，配置文件都遵循标准化格式。文件包含一个唯一的 `mcpServers` 对象，您可以在其中定义要连接的各个 server：

```json
{
  "mcpServers": {
    "sqlite-explorer": {
      "command": "node",
      "args": ["/usr/local/bin/sqlite-mcp-server.js"],
      "env": {
        "SQLITE_DB_PATH": "/var/data/app.db"
      }
    },
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

### MCP 配置属性

`mcpServers` 下的每个 server 条目均支持以下属性：

**传输协议 Transport（必选其一）：**

*   **`command`** (string): 用于 `stdio` 传输的可执行文件路径。
*   **`serverUrl`** (string): 远程 `Streamable HTTP` 或 `SSE` server 的 URL。

**可选属性：**

*   **`args`** (string[]): 用于 `stdio` 传输的命令行参数。
*   **`env`** (object): 用于 `stdio` server 进程的环境变量。
*   **`cwd`** (string): `stdio` server 的工作目录。
*   **`headers`** (object): 针对远程 server 的自定义 HTTP 请求头。
*   **`authProviderType`** (string): 身份验证提供方。支持 `"google_credentials"` 以使用 Google Application Default Credentials (ADC)。
*   **`oauth`** (object): OAuth 客户端凭证（`clientId`, `clientSecret`）。
*   **`disabled`** (boolean): 临时禁用该 server，无需删除其配置。
*   **`disabledTools`** (string[]): 要对模型隐藏/禁用的工具名称列表。

## MCP 身份验证

已连接的 MCP server 可以使用内置 Google 凭证、自动 OAuth 流程或自定义 HTTP 标头对外部服务进行安全身份验证。

### Google 凭证

将 `authProviderType` 设置为 `"google_credentials"` 以使用 Google Application Default Credentials (ADC)。

```json
{
  "mcpServers": {
    "my-gcp-service": {
      "serverUrl": "https://example.googleapis.com/mcp/",
      "authProviderType": "google_credentials"
    }
  }
}
```

这要求在本地配置好 Application Default Credentials。要进行设置，请运行：

```bash
gcloud auth application-default login
```

如果您之前已经登录过，请确保通过运行以下命令设置了配额项目：

```bash
gcloud auth application-default set-quota-project {QUOTA_PROJECT}
```

### OAuth

Antigravity 可以为支持动态客户端注册（DCR）的 server 自动处理 OAuth。对于这些 server，无需额外配置：

```json
{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/"
    }
  }
}
```

如果该 server 不支持动态客户端注册，您可以手动提供客户端凭证：

```json
{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret"
      }
    }
  }
}
```

如果您手动提供了客户端凭证，请确保将以下地址注册到您的 OAuth 提供商的重定向 URI（redirect URI）中：

```
https://antigravity.google/oauth-callback
```

连接到启用了 OAuth 的 server 时：

1.  使用 `Cmd+,`（Mac）或 `Ctrl+,`（Windows/Linux）打开 [**Agent Settings**](/docs/settings)。
2.  导航至 **Customizations** 标签页，并点击对应 server 旁边的 **Authenticate** 按钮。
    
    ![Click Authenticate](/assets/image/docs/tools/mcp-oauth-authenticate.png)
    
3.  在浏览器中完成身份验证并复制授权码。
    
    ![Copy authorization code](/assets/image/docs/tools/mcp-oauth-copy-code.png)
    
4.  将授权码粘贴回设置面板并点击 **Submit**。
    
    ![Paste auth code](/assets/image/docs/tools/mcp-oauth-paste-code.png)

验证成功后，server 将自动重新连接。

![Authenticated server](/assets/image/docs/tools/mcp-oauth-authenticated.png)

访问令牌（Access token）存储在 `~/.gemini/antigravity/mcp_oauth_tokens.json` 中。过期的 token 会自动刷新，无效的 token 会被移除。

### 自定义请求头（Custom Headers）

对于需要自定义 HTTP 请求头的远程 server（例如 API key 或 bearer token），请将其添加到 `headers` 对象中。例如：

```json
{
  "mcpServers": {
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

## MCP 权限与访问控制

对 Model Context Protocol 工具和资源的访问受 Antigravity 的 [permissions 系统（权限系统）](/docs/permissions) 管控。默认情况下，未显式配置策略的 MCP 工具在 **Ask** 模式下运行，在执行前需要您的批准。您可以在策略配置中允许特定工具或整个 server：

*   `mcp(server/tool)`: 匹配特定 server 上的特定工具。
*   `mcp(server/*)`: 匹配指定 server 上的所有工具。
*   `mcp(*)`: 全局通配符，匹配所有已连接 server 上的任何 MCP 工具。

## 受支持的 MCP Server

MCP Store 为各类开发者平台、数据库及生产力服务提供了直接集成：

### 数据库与存储（14 个 server）

*   AlloyDB for PostgreSQL
*   BigQuery
*   Bigtable Admin remote MCP
*   ClickHouse
*   Cloud SQL (MySQL, PostgreSQL, SQL Server, Managed)
*   Dataplex
*   MCP Toolbox for Databases
*   MongoDB
*   Neon
*   Pinecone
*   Prisma
*   Redis
*   Spanner
*   Supabase

### 开发者工具与 CI/CD（13 个 server）

*   Apigee MCP
*   Atlassian
*   Cloud CLI Execution
*   GitHub
*   GitLab Orbit
*   GKE OneMCP
*   Harness
*   Heroku
*   Home Developer MCP
*   Linear
*   Netlify
*   Postman
*   SonarQube

### 前端与设计（6 个 server）

*   Chrome DevTools
*   Dart
*   Figma Dev Mode MCP
*   Locofy
*   Lovable MCP
*   Mobbin MCP

### 分析、AI 与云（13 个 server）

*   Airweave
*   Antimetal
*   Arize
*   Firebase
*   Google Cloud Quotas
*   Looker
*   Notion
*   PayPal
*   Perplexity Ask
*   PostHog
*   Sequential Thinking
*   Stripe
*   Windsor AI