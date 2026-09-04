# Antigravity CLI 上手教程

学习如何启动 Antigravity CLI、与本地自主 agent 协同工作、审查生成的文件并执行终端测试命令。

## 概览

本指南将带你完成一次快速上手演练。你将指挥一个自主 agent 创建一个 Python 工具脚本，审查所做的更改并验证其执行结果。

## 分步指南

1.  **创建干净的项目目录并启动 Antigravity TUI**
    
    ```
    mkdir agy-demo && cd agy-demo
    agy
    ```
    
    注意
    
    **首次启动**：如果是首次运行 `agy`，请按照终端提示完成静默身份认证。有关故障排查详情，请参阅 [安装与认证](/docs/cli/install)。
    
2.  **Prompt agent 生成一个 Python 网页抓取脚本**
    
    在屏幕底部的 prompt 输入框中输入以下指令，并按下 Enter 键：
    
    ```
    Write a simple python script to fetch web page text
    ```
    
    agent 会读取 workspace，确认当前不存在任何文件，并制定创建脚本的方案。随着 agent 进行推理和调度操作，你将看到实时的进度更新。
    
3.  **打开 Artifact 审查界面以检查提议的代码**
    
    一旦 agent 完成文件生成，界面将出现通知。按下 Ctrl + R 进入 **Artifact 审查（Artifact Review）** 界面。
    
    *   使用 ↑/↓ 导航至新创建的 `main.py`。
    *   审查完整的文件内容与 diff。
    *   按下 Y 批准创建 `main.py`。
    *   按下 Esc 关闭审查面板并返回主 prompt 界面。
4.  **配合 agent 执行测试命令以验证输出**
    
    指示 agent 运行该 Python 脚本以验证其行为。在 prompt 输入框中输入以下命令并按下 Enter 键：
    
    ```
    Run the python script and show me the output
    ```
    
    agent 会提议运行 `python3 main.py`。按下 Y 确认并执行该命令。agent 会在本地运行该脚本，并将标准输出直接流式传输到你的终端屏幕上。
    
5.  **退出 Antigravity 会话**
    
    完成任务后，在 prompt 输入框中按下 Ctrl + D（或输入 `/exit`）即可关闭 TUI 并恢复你原本的 Shell 会话。
    

## 后续步骤

现在你已经完成了第一个由 agent 协助的工作流，接下来可以学习如何配置 CLI 并掌握核心概念：

*   **[安装与认证](/docs/cli/install)**：有关安装 `agy` 和配置 SSH 配置文件的详细说明。
*   **[Prompt 编写与交互](/docs/cli/prompting)**：多行输入、粘贴媒体文件以及主动中断控制的最佳实践。
*   **[审查 Artifact](/docs/cli/artifacts)**：深入探讨“透明即信任（Trust through Transparency）”架构模式。