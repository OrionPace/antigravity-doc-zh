# 安装与认证

安装 Antigravity CLI，配置企业级要求，并建立安全的已认证会话。

## 安装

Antigravity CLI 原生运行在 macOS、Linux 和 Windows 上。使用以下对应操作系统的脚本在你的系统上安装或升级二进制程序。

### macOS 与 Linux

执行原生安装脚本，下载可执行文件并安装到 `~/.local/bin/agy`：

```
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### Windows

安装脚本会将 `agy` 二进制文件注册到你的本地用户目录：`C:\Users\<username>\AppData\Local\agy\bin`（其中 `<username>` 代表你当前登录的 Windows 用户名）。

**PowerShell**：打开 PowerShell 并执行以下安装脚本：

```
irm https://antigravity.google/cli/install.ps1 | iex
```

**CMD**：打开标准命令提示符（Command Prompt）并执行：

```
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### 安装 Flags

执行安装脚本时，你可以附加以下自定义 flags：

*   `--skip-aliases`：跳过 Shell 配置文件别名清理（防止脚本清理或更新旧有的 `agy` 或 `antigravity` Shell 别名）。
*   `--skip-path`：跳过向 Shell 配置文件追加 `PATH`（防止脚本修改 Shell 配置文件中的动态环境变量）。

## 认证工作流

Antigravity CLI 使用安全凭据和令牌配置文件（token profile）与共享的 agent harness 进行通信。

### 本地静默密钥环登录

在本地计算机上启动 `agy` 时，CLI 会尝试访问操作系统的原生安全密钥环（keyring，例如 Apple Keychain、Linux Secret Service/dbus 或 Windows Credential Manager）。如果找到有效的 token profile，CLI 会静默认证你的会话，而无需打开浏览器。

如果未找到保存的会话：

1.  CLI 会自动启动你的本地默认网络浏览器。
2.  使用你已获批的账号凭据进行登录。

### 远程 SSH OAuth 流程

通过 SSH 运行时，CLI 会检测远程连接环境。由于无法启动本地 Web 浏览器，CLI 会发起手动 URL 验证流程：

1.  在远程终端会话中启动 `agy`。
2.  CLI 检测到 SSH 环境并输出一个唯一的安全授权 URL。
3.  复制此 URL 并将其粘贴到本地计算机的 Web 浏览器中。
4.  使用你已获批的凭据登录并完成认证。
5.  浏览器会显示一个唯一的字母数字授权码。
6.  复制该授权码，返回远程 SSH 终端，并将其粘贴到 prompt 提示框中。

## 使用 Gemini API Key

你可以使用自己的 Gemini API Key 运行 Antigravity CLI，而无需登录 Google 账号。模型请求将直接发送到 Gemini API，且 CLI 绝不会建立账号会话。这非常适合在没有浏览器可用于完成登录的 headless mode 和 CI 环境中运行。你可以在 [Google AI Studio](https://aistudio.google.com/app/api-keys) 中创建 API Key。

要使用 Gemini API Key，你必须设置模型提供方（provider）以及包含该 API Key 的环境变量。仅单独设置 `GEMINI_API_KEY` 环境变量不会生效。

### 启用 Gemini API Key

1.  在 `~/.gemini/antigravity-cli/settings.json` 中将 `modelProvider` 设置为 `gemini`：
    
    ```
    {
        "modelProvider": "gemini"
    }
    ```
    
2.  将你的 Key 导出为 `GEMINI_API_KEY`：
    
    ```
    export GEMINI_API_KEY="your-api-key"
    ```
    
    此操作仅对当前 Shell 生效。将相同的命令添加到你的 Shell 配置文件中（如 `~/.zshrc` 或 `~/.bashrc`），即可在不同会话间持久生效。
    
3.  启动 CLI：
    
    ```
    agy
    ```
    

CLI 将跳过登录界面并直接打开主界面。顶部标题栏会显示 **Gemini API key**，而非你的账号邮箱：

![使用 Gemini API Key 认证的 Antigravity CLI，顶部标题栏显示 "Gemini API key" 代替了账号邮箱](/assets/image/docs/cli/install-gemini-api-key.png)

> **注意：** 当使用 `GEMINI_API_KEY` 进行认证时，`/logout` 命令不会生效，因为此时没有需要清除的本地持久化会话。

### 将 CLI 指向自定义 Endpoint

若要将模型请求发送到其他兼容 Gemini 的 Endpoint，请设置 `GOOGLE_GEMINI_BASE_URL` 环境变量：

```
export GOOGLE_GEMINI_BASE_URL="https://your-endpoint.example.com"
```

### 恢复默认认证方式

如果你想恢复使用默认的基于账号的认证：

1.  从 `~/.gemini/antigravity-cli/settings.json` 中移除 `modelProvider`。
2.  重启 CLI 以重新登录你的账号。

> **注意：** 如果你取消设置了 `GEMINI_API_KEY` 环境变量，但仍将 `modelProvider` 设置为 `gemini`，CLI 将无法启动。

### 故障排查

| 现象 | 原因 | 解决方法 |
| --- | --- | --- |
| CLI 启动时退出并报错 `GEMINI_API_KEY` 未设置 | `modelProvider` 为 `gemini` 但环境中缺少该 Key | 导出 `GEMINI_API_KEY`，或移除 `modelProvider` 以使用默认认证 |
| CLI 正常登录并忽略了设置 | `modelProvider` 包含无法识别的值 | `gemini` 是唯一受支持的值。请检查拼写并重启 CLI |
| 通过 `GOOGLE_API_KEY` 或 `.env` 文件设置的 Key 无效 | CLI 仅从环境中的 `GEMINI_API_KEY` 读取凭据，不会加载 `.env` 文件 | 在你的 Shell 或 Shell 配置文件中导出 `GEMINI_API_KEY` |
| 请求在中途失败并报通用模型错误 | Key 无效、已撤销或缺乏访问所请求模型的权限 | 在 Google AI Studio 中验证该 Key。CLI 在启动时仅检查 Key 是否非空，因此不可用的 Key 只有在发起第一次对话时才会暴露出来 |

## 管理你的会话

终止会话将清除活跃凭据和本地缓存目录。

### 退出登录

要断开账号连接并从操作系统的密钥环（keyring）中清除保存的认证配置文件，请在 CLI 的 prompt 输入框中运行以下命令：

```
/logout
```

## 后续步骤

完成安装与认证后，即可开始与本地 agent 交互：

*   **[上手教程](/docs/cli/tutorial)**：配合 agent 创建并运行一个基础 Python 项目。
*   **[Prompt 编写与交互](/docs/cli/prompting)**：探索多行文本编辑、中断命令以及终端媒体粘贴功能。
*   **[权限与沙箱（Permissions & Sandbox）](/docs/cli/sandbox)**：配置安全文件系统目录与命令限制。