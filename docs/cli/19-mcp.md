# Model Context Protocol (MCP)

Antigravity 支持 [Model Context Protocol (MCP)](https://modelcontextprotocol.io)，这是一个开放标准，可让 AI agent 与编辑器安全地连接本地开发者工具、数据库、文件解析器以及外部远程 API。此集成让 AI 模型能够获取超出当前 workspace 范围的实时上下文与执行能力。

在本指南中，你将学习如何在 Antigravity 各产品中连接与配置 MCP server。你也可以直接跳转到 [Antigravity 2.0](/docs/mcp#antigravity-20)、[Antigravity IDE](/docs/mcp#antigravity-ide)、[Antigravity CLI](/docs/mcp#antigravity-cli) 或 [Antigravity SDK](/docs/mcp#antigravity-sdk) 的 MCP server 相关信息。

## 什么是 MCP？

MCP 充当 Antigravity 与更广泛开发环境之间的通用桥梁。无需手动将数据库 schema、日志或 API 规范复制粘贴到 prompt 或聊天面板中，MCP 让 Antigravity 能够直接获取结构化上下文，或在需要时代表你执行安全操作。

### 添加上下文

借助 MCP，Antigravity 可以使用来自已连接 MCP server 的实时数据来支撑其推理与建议：

*   在编写 SQL 查询时，Antigravity 可以检查你实时的 Neon、Supabase 或 AlloyDB schema，以建议正确的表名与列名。
*   在调试部署失败时，Antigravity 可以直接从 Netlify 或 Heroku 拉取最近的构建日志。

### 添加自定义工具

借助 MCP，Antigravity 可以执行由你已连接 server 定义的特定安全操作：

*   为这个 TODO 创建一个 Linear issue。
*   在 Notion 或 GitHub 中搜索认证模式。

## Antigravity 2.0

在 Antigravity 2.0 中，你可以通过 **Settings** 的 **Installed MCP Servers** 部分管理 MCP server。

查看与更新 MCP server：

1.  点击屏幕左下角的 **Settings** 按钮。
2.  选择 **Customizations**，查看 **Installed MCP Servers** 部分。

从 **Installed MCP Servers** 部分安装 MCP server：

1.  点击 **Add MCP**。这将带你进入 MCP Store，一个可搜索的可用 MCP server 列表。
2.  搜索或向下滚动到你想要安装的 MCP server。
3.  点击 **Add**。

在此界面管理 MCP server：

*   **Uninstall**：点击列表中 MCP server 旁边的垃圾桶图标。
*   **Disable/enable**：点击列表中 MCP server 旁边的切换开关。
*   **Refresh**：点击刷新按钮。

## Antigravity IDE

在 Antigravity IDE 中，管理 MCP server 最简单的方式是通过内置的 MCP Store。在 MCP Store 中，你可以浏览、发现并安装受支持的 MCP server。你也可以通过更新 `mcp_config.json` 来安装自定义 server。

使用 MCP Store：

1.  点击编辑器 agent 侧边面板顶部的 **…**，然后选择 **MCP Servers**。
2.  将鼠标悬停在任意受支持的 server 上并点击 **Install**。（或者，点击某个 server 查看详情，然后点击 **Install**。）
3.  按照屏幕上的提示操作。

安装完成后，该 server 的资源与工具将自动对编辑器可用。

连接 MCP Store 中未列出的自定义 MCP server：

1.  点击编辑器 agent 侧边面板顶部的 **…**，然后选择 **MCP Servers**。
2.  点击 **Manage MCP Servers**。
3.  点击 **View raw config**。
4.  使用你的自定义 [MCP server 配置](/docs/mcp#mcp-configuration-structure)修改 `mcp_config.json` 文件。

配置文件全局位于 `~/.gemini/config/mcp_config.json`（或位于你 workspace 下的本地路径 `.agents/mcp_config.json`）。

## Antigravity CLI

Antigravity CLI 同时支持本地 `stdio` 进程与远程主机 MCP server 配置。在 Antigravity CLI 上安装 MCP server 最简单的方式是使用 **Interactive MCP Manager**。你也可以手动编辑全局 server 设置或 workspace 级别的 `mcp_config.json`。

### Interactive MCP Manager

在 prompt 面板中输入 `/mcp` 并按 `Enter`，打开交互式 **MCP Manager Overlay**。此面板让你可以：

*   查看处于 active、disconnected 或 loading 状态的 server 的实时状态环。
*   手动重新加载 server 配置或检查实时连接日志。

### 全局与 Workspace Server 配置

与旧版设置不同，Antigravity CLI 将 MCP 定义分离到专用的稀疏配置中：

*   **全局 server 设置：** 配置于 `~/.gemini/config/mcp_config.json`。
*   **Workspace 本地设置：** 配置于你当前项目下的 `.agents/mcp_config.json`。

你可以使用自定义 [MCP server 配置](/docs/mcp#mcp-configuration-structure)直接修改这些文件。

注意

**远程连接 Schema**：在声明远程 SSE、Streamable HTTP 或基于 websocket 的 MCP 连接时，你必须定义 `serverUrl` 字段。不支持 `url` 或 `httpUrl` 等旧版字段。

## Antigravity SDK

在使用 [Antigravity SDK](/docs/sdk/overview) 构建的 Python 应用中，MCP server（`stdio`、`SSE` 或 `HTTP`）可以在统一的执行管线中以编程方式连接，与内置工具和自定义 Python 函数并列运行。

SDK 会自动发现你 workspace 的 `.agents/mcp_config.json` 文件中配置的 server。你也可以直接使用本地配置实例化 agent：

```
import asyncio
from google.antigravity import Agent, LocalAgentConfig
```

## MCP 配置结构

无论是为 Antigravity 2.0、Antigravity IDE 还是 Antigravity CLI 配置自定义 server，配置文件都遵循标准化格式。该文件包含一个 `mcpServers` 对象，你可以在其中定义想要连接的每个 server：

```
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

`mcpServers` 下的每个 server 条目支持以下属性：

**Transport（必选其一）：**

*   **`command`**（string）：用于 `stdio` transport 的可执行文件路径。
*   **`serverUrl`**（string）：远程 `Streamable HTTP` 或 `SSE` server 的 URL。

**可选：**

*   **`args`**（string\[\]）：用于 `stdio` transport 的命令行参数。
*   **`env`**（object）：用于 `stdio` server 进程的环境变量。
*   **`cwd`**（string）：用于 `stdio` server 的工作目录。
*   **`headers`**（object）：用于远程 server 的自定义 HTTP header。
*   **`authProviderType`**（string）：认证提供方。支持 `"google_credentials"`，用于 Google Application Default Credentials (ADC)。
*   **`oauth`**（object）：OAuth 客户端凭据（`clientId`、`clientSecret`）。
*   **`disabled`**（boolean）：临时禁用某个 server，而不移除其配置。
*   **`disabledTools`**（string\[\]）：不向模型提供的工具名称。

## MCP 认证

已连接的 MCP server 可以使用内置 Google 凭据、自动 OAuth 流程或自定义 HTTP header 对外部服务进行安全认证。

### Google 凭据

将 `authProviderType` 设置为 `"google_credentials"`，以使用 Google Application Default Credentials (ADC)。

```
{
  "mcpServers": {
    "my-gcp-service": {
      "serverUrl": "https://example.googleapis.com/mcp/",
      "authProviderType": "google_credentials"
    }
  }
}
```

这需要在本地配置 Application Default Credentials。要进行设置，请运行：

```
gcloud auth application-default login
```

如果你之前已登录，请通过运行以下命令确保已设置 quota project：

```
gcloud auth application-default set-quota-project {QUOTA_PROJECT}
```

### OAuth

Antigravity 可以为支持动态客户端注册（DCR）的 server 自动处理 OAuth。对于这些 server，无需额外配置：

```
{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/"
    }
  }
}
```

如果 server 不支持动态客户端注册，你可以手动提供客户端凭据：

```
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

如果你手动提供了客户端凭据，请确保在你的 OAuth 提供方中将以下地址注册为 redirect URI：

```
https://antigravity.google/oauth-callback
```

连接到启用 OAuth 的 server 时：

1.  使用 `Cmd+,`（Mac）或 `Ctrl+,`（Windows/Linux）打开 [**Agent Settings**](/docs/settings)。
    
2.  导航到 **Customizations** 标签页，点击 server 旁边的 **Authenticate** 按钮。
    
    ![点击 Authenticate](/assets/image/docs/tools/mcp-oauth-authenticate.png)
    
3.  在浏览器中完成认证，并复制授权码。
    
    ![复制授权码](/assets/image/docs/tools/mcp-oauth-copy-code.png)
    
4.  将授权码粘贴回设置面板，并点击 **Submit**。
    
    ![粘贴授权码](/assets/image/docs/tools/mcp-oauth-paste-code.png)
    

认证完成后，server 将自动重新连接。

![已认证的 server](/assets/image/docs/tools/mcp-oauth-authenticated.png)

访问令牌存储在 `~/.gemini/antigravity/mcp_oauth_tokens.json` 中。过期的令牌会自动刷新，无效的令牌会被移除。

### 自定义 Header

对于需要自定义 HTTP header（例如 API key 或 bearer token）的远程 server，请将它们添加到 `headers` 对象中。例如：

```
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

对 Model Context Protocol 工具与资源的访问由 Antigravity 的 [权限系统](/docs/permissions)管理。默认情况下，未配置的 MCP 工具以 **Ask** 模式运行，需要你批准后才能执行。你可以在策略配置中允许特定工具或整个 server：

*   `mcp(server/tool)`：匹配特定 server 上的特定工具。
*   `mcp(server/*)`：匹配指定 server 上的所有工具。
*   `mcp(*)`：全局通配符，匹配所有已连接 server 上的任意 MCP 工具。

## 受支持的 MCP Server

MCP Store 为各种开发者平台、数据库与生产力服务提供直接集成：

数据库与存储（14 个 server）

*   [AlloyDB for PostgreSQL](https://cloud.google.com/alloydb/docs/ai/use-alloydb-mcp)
*   [BigQuery](https://cloud.google.com/bigquery/docs/use-bigquery-mcp)
*   [Bigtable Admin remote MCP](https://docs.cloud.google.com/bigtable/docs/use-bigtable-mcp)
*   [ClickHouse](https://clickhouse.com/docs/use-cases/AI/MCP)
*   [Cloud SQL (MySQL, PostgreSQL, SQL Server, Managed)](https://docs.cloud.google.com/sql/docs/mysql/use-cloudsql-mcp)
*   [Dataplex](https://docs.cloud.google.com/dataplex/docs/use-remote-mcp)
*   [MCP Toolbox for Databases](https://mcp-toolbox.dev/documentation/introduction/)
*   [MongoDB](https://github.com/mongodb-js/mongodb-mcp-server)
*   [Neon](https://github.com/neondatabase-labs/mcp-server-neon)
*   [Pinecone](https://github.com/pinecone-io/pinecone-mcp)
*   [Prisma](https://github.com/prisma/prisma?tab=readme-ov-file#mcp-server)
*   [Redis](https://github.com/redis/mcp-redis)
*   [Spanner](https://docs.cloud.google.com/spanner/docs/use-spanner-mcp)
*   [Supabase](https://github.com/supabase-community/supabase-mcp)

开发者工具与 CI/CD（13 个 server）

*   [Apigee MCP](https://docs.cloud.google.com/apigee/docs/reference/apis/apihub/mcp)
*   [Atlassian](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)
*   [Cloud CLI Execution](https://docs.cloud.google.com/sdk/use-gcloud-mcp)
*   [GitHub](https://github.com/github/github-mcp-server)
*   [GitLab Orbit](https://docs.gitlab.com/orbit/remote/access/mcp/)
*   [GKE OneMCP](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/use-gke-mcp)
*   [Harness](https://github.com/harness/mcp-server)
*   [Heroku](https://github.com/heroku/heroku-mcp-server)
*   [Home Developer MCP](https://developers.home.google.com/mcp/developer)
*   [Linear](https://linear.app/changelog/2025-05-01-mcp)
*   [Netlify](https://github.com/netlify/netlify-mcp)
*   [Postman](https://github.com/postmanlabs/postman-mcp-server)
*   [SonarQube](https://github.com/SonarSource/sonarqube-mcp-server)

前端与设计（6 个 server）

*   [Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp)
*   [Dart](https://dart.dev/tools/mcp-server)
*   [Figma Dev Mode MCP](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server)
*   [Locofy](https://www.locofy.ai/docs/export-and-deployment/locofy-mcp/)
*   [Lovable MCP](https://docs.lovable.dev/integrations/lovable-mcp-server)
*   [Mobbin MCP](https://mobbin.com/mcp)

分析、AI 与云（16 个 server）

*   [Airweave](https://github.com/airweave-ai/airweave)
*   [Antimetal](https://docs.antimetal.com/connect)
*   [Arize](https://github.com/Arize-ai/arize-tracing-assistant)
*   [Cloud Audit Manager](https://docs.cloud.google.com/audit-manager/docs/reference/auditmanager/mcp)
*   [CrowdStrike](https://github.com/CrowdStrike/falcon-mcp)
*   [Firebase](https://firebase.google.com/docs/ai-assistance/mcp-server)
*   [Google Cloud Quotas](https://cloud.google.com/docs/quotas/overview)
*   [Looker](https://mcp-toolbox.dev/documentation/connect-to/ides/looker_mcp/)
*   [Notion](https://github.com/makenotion/notion-mcp-server)
*   [PayPal](https://developer.paypal.com/tools/mcp-server/)
*   [Perplexity Ask](https://github.com/ppl-ai/modelcontextprotocol)
*   [PostHog](https://posthog.com/mcp)
*   [Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
*   [Splunk](https://splunkbase.splunk.com/app/7931)
*   [Stripe](https://github.com/stripe/agent-toolkit/tree/main/modelcontextprotocol)
*   [Windsor AI](https://windsor.ai/documentation/windsor-mcp/)