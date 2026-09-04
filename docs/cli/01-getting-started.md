# Antigravity CLI 入门指南

欢迎使用 Antigravity CLI！本指南为开发者提供了一条清晰、高阶的路线图，指导你安装客户端、启动终端用户界面（TUI），并开始与自主 agent 协同工作。

## 快速上手路线图

按照以下顺序步骤启动你的第一个会话：

1.  **安装客户端（快速通道）**
    
    根据你的操作系统运行对应的快速安装命令：
    
    **macOS / Linux**：
    
    ```
    curl -fsSL https://antigravity.google/cli/install.sh | bash
    ```
    
    **Windows (PowerShell)**：
    
    ```
    irm https://antigravity.google/cli/install.ps1 | iex
    ```
    
    **Windows (CMD)**：
    
    ```
    curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
    
    默认情况下，安装程序会将 `agy` 二进制文件注册到你操作系统的对应目录中：
    
    *   **macOS / Linux**：`~/.local/bin/agy`
    *   **Windows**：`C:\Users\<username>\AppData\Local\agy\bin`（其中 `<username>` 代表你当前登录的 Windows 用户名）。
    
    注意
    
    **高级配置**：有关企业级凭据配置、安全密钥环（keyring）认证权限、代理设置或安装问题排查的详细说明，请参阅 **[安装与认证指南](/docs/cli/install)**。
    
2.  **在项目目录中启动 TUI**
    
    打开一个新的终端窗口，进入你的目标项目代码库目录，然后执行启动命令：
    
    ```
    agy
    ```
    
3.  **完成首次启动设置**
    
    在首次启动时，TUI 会引导你完成简要的交互式设置：
    
    *   **配色方案（Color Scheme）**：选择你偏好的视觉主题（Solarized、Dark、Solarized Light 或标准终端配色）。
    *   **渲染模式（Rendering Mode）**：选择 Alt-Screen 模式（带全屏滚动的独立缓冲区）或 Inline 模式（与终端历史记录融为一体的顺序流式输出）。
    *   **工作区信任（Workspace Trust）**：确认你信任该代码仓库目录。确认后，agent 会对文件建立索引并随时待命。
4.  **运行你的第一个 agent 任务**
    
    在 TUI 界面底部的 prompt 输入框中输入以下指令，并按下 Enter 键：
    
    ```
    Write a simple python script to fetch web page text
    ```
    
    agent 会读取 workspace，对任务进行推理并提出计划。有关在 TUI 中审查代码和运行测试命令的详细分步操作，请参阅 **[上手教程](/docs/cli/tutorial)**。
    

## 相关资源

进一步优化你的本地环境配置并掌握高级协作工具：

*   **[最佳实践](/docs/cli/best-practices)**：掌握验证循环、规划阶段、rule 文件以及会话检查点。
*   **[故障排查](/docs/cli/troubleshooting)**：解决常见的路径、密钥环（keyring）或 SSH 转发错误。
*   **[CLI 参考指南](/docs/cli/reference)**：收录所有 Slash Command、快捷键和 JSON 配置键的高密度参考手册。