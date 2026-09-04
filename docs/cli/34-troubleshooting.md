# 故障排查

诊断并解决与安装 PATH、本地自动更新锁、Keyring 访问权限以及 SSH 剪贴板转发相关的常见异常。

## 快速参考

查阅下方的速查表以识别异常现象并获取即时解决方案：

| 错误表现 | 潜在原因 | 目标解决方案 |
| :-- | :-- | :-- |
| **`agy: command not found`** | shell 环境中缺失二进制文件所在目录。 | [配置 shell PATH](#配置-shell-path) |
| **`keyring: secure lock out`** | 缺少系统服务权限或存在活跃锁定。 | [授权 Keyring 权限](#授权-keyring-权限) |
| **`SSH Clipboard paste failures`** | 协议流被阻止或缺失转发配置。 | [启用终端模拟器剪贴板转发](#启用终端模拟器剪贴板转发) |
| **`Advisory lock / update failures`** | 自动更新程序线程被锁定或目录路径为只读。 | [解决自动更新程序锁定与失败问题](#解决自动更新程序锁定与失败问题) |

* * *

## 配置 shell PATH

### 症状表现

执行 `agy` 时返回 shell 终端错误：

```
bash: agy: command not found
```

### 原因分析

安装程序将二进制文件下载到 `~/.local/bin`（或 `C:\Users\<username>\AppData\Local\agy\bin`），但你当前 shell 的活跃 `$PATH` 环境变量未索引该目录。

### 解决方案

确保你的终端会话加载了二进制文件路径。

**macOS & Linux**：

1.  打开你的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）。
2.  在文件末尾验证或追加以下行：
    
    ```bash
    export PATH="~/.local/bin:$PATH"
    ```
    
3.  重新加载你的配置文件：
    
    ```bash
    source ~/.zshrc
    ```
    

**Windows (PowerShell)**：

1.  以管理员身份打开 PowerShell 终端并执行：
    
    ```powershell
    [System.Environment]::SetEnvironmentVariable("Path", [System.Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Program Files\Google\antigravity-cli", "User")
    ```
    
2.  重启你的终端模拟器以刷新系统注册表环境。

* * *

## 授权 Keyring 权限

### 症状表现

启动时，CLI 挂起、打印 DBUS 警告或抛出 keyring 访问异常：

```
Error: failed to retrieve token: secret keyring is locked
```

### 原因分析

Antigravity CLI 利用安全钥匙串库（Apple Keychain、基于 dbus 的 Linux secret-service，或 Windows Credential Manager）来加密你的会话令牌。如果后台守护进程被锁定或处于 headless（无头）状态，CLI 将无法读取凭据。

### 解决方案

**macOS**：

1.  打开 **钥匙串访问 (Keychain Access)** 应用。
2.  搜索 `Antigravity CLI` 安全项。
3.  右键单击，选择 **显示简介 (Get Info)**，切换到 **访问控制 (Access Control)** 选项卡，确认 `agy` 在允许的应用列表中。
4.  如果在 Mac 上的 headless SSH 会话中运行，请执行以下解锁命令序列：
    
    ```bash
    security unlock-keychain -p "your_keychain_password" login.keychain
    ```
    

**Linux**：

确保你的系统密钥环（例如 GNOME Keyring 或 KWallet）已解锁且可访问。

如果你在 headless 模式（无头模式）环境或通过 SSH 运行，请确保 D-Bus 会话处于活跃状态并且你的 keyring 守护进程正在运行。通常可以通过运行以下命令来初始化 D-Bus 会话：

```bash
export $(dbus-launch)
```

如果仍遇到访问问题，请确保你的用户账户具备访问 keyring 服务的必要权限，或者联系技术支持。

* * *

## 启用终端模拟器剪贴板转发

### 症状表现

在 SSH 终端内通过 `Ctrl+V` 粘贴屏幕截图或媒体文件时返回失败通知：

```
Error: local pasteboard is empty or unreachable over SSH connection
```

### 原因分析

标准 SSH 流不转发图形剪贴板内容。图形上传需要特定的终端复用器协议支持。

### 解决方案

请验证你正在使用受支持的终端模拟器及相应配置。

1.  **使用 iTerm2 或 Ghostty**：这些模拟器支持高级剪贴通道。
2.  **配置 iTerm2 转发**：
    *   打开 iTerm2 首选项（`Cmd+,`）。
    *   进入 **General** 选项卡，选择 **Selection** 子菜单。
    *   勾选 **Applications in terminal may access clipboard**（启用 OSC 52 写入通道）。
3.  **绕过复用器**：如果在 `tmux` 内运行，确保你的当前配置正确映射了标准剪贴通道：
    
    ```tmux
    set -s set-clipboard on
    ```
    

* * *

## 解决自动更新程序锁定与失败问题

### 症状表现

启动 `agy` 时挂起、无法应用升级，或返回建议性锁（advisory lock）警告：

```
Warning: another background updater process is already active (update.lock)
```

### 原因分析

Antigravity CLI 包含一个在后台运行的静态链接原生自动更新程序。它在 `~/.gemini/antigravity-cli/updater/` 中使用一个 15 分钟生存时间（TTL）的去抖标记（`last_check.timestamp`）和一个建议锁（`update.lock`），以防止并发进程冲突。如果后台更新程序进程挂起、崩溃而未释放锁，或者对可执行文件目录缺少用户文件系统写入权限，后续更新将被阻止。

### 解决方案

*   **释放建议锁**：手动清除后台锁文件：
    
    ```bash
    rm -f ~/.gemini/antigravity-cli/updater/update.lock
    ```
    
*   **退出/禁用自动更新**：在你的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中将环境变量 `AGY_CLI_DISABLE_AUTO_UPDATE` 设置为 `true`：
    
    ```bash
    export AGY_CLI_DISABLE_AUTO_UPDATE=true
    ```
    
*   **验证目录写入权限**：确保你的用户配置拥有目标安装目录（Unix 上为 `~/.local/bin/`，Windows 上为 `%LOCALAPPDATA%\agy\bin`）的所有权与写入权限。

* * *

## 后续步骤

访问我们的快速参考手册或配置高级权限：

*   **[CLI 参考](/docs/cli/reference)**：列出所有 slash commands 与可视化设置键的紧凑表格。
*   **[权限](/docs/cli/permissions)**：配置细粒度的允许和拒绝操作策略。
*   **[沙箱](/docs/cli/sandbox)**：强制执行操作系统级容器隔离边界。
*   **[插件与技能](/docs/cli/plugins)**：创建你自己的自定义 skill（技能）。