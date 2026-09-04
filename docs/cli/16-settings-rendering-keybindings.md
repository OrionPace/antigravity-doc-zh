# 设置、渲染与 Keybindings

配置持久化偏好设置、自定义快捷键、切换终端显示缓冲区（display buffer），以及管理运行时的 CLI 参数覆盖。

## 配置偏好设置

Antigravity CLI 将用户偏好设置存储在极简且向前兼容的 JSON 配置文件中。

### 配置文件位置

持久化设置以纯 JSON 格式保存：

```
~/.gemini/antigravity-cli/settings.json
```

CLI 采用**稀疏持久化（sparse persistence）**机制，仅将与系统默认值不同的项写入磁盘。这使得配置文件保持整洁、轻量，并与未来的版本更新完全向前兼容。

### 交互式设置面板

若要直接在活跃的终端会话中编辑设置而无需打开原始 JSON 文件：

1.  在 prompt 面板内键入 `/config`（或其别名 `/settings`），然后按 `Enter`。
2.  全屏的**设置编辑器浮层（Settings Editor Overlay）**随即打开。
3.  使用 `↑`/`↓` 在可用选项之间导航。
4.  在高亮选中的参数上按 `Enter` 即可切换其状态或打开文本输入框。
5.  按 `Esc` 保存修改并关闭编辑器。

![交互式设置面板](/assets/image/docs/cli/settings-interactive-panel.png)

## 命令行参数覆盖

你可以使用 CLI 命令行 flag 临时覆盖单个终端会话的持久化偏好设置：

```
agy --sandbox --model="Gemini 3.5 Flash"
```

当覆盖 flag 处于活动状态时，交互式 `/config` 菜单会在被修改的设置旁显示警告指示符：

```
! Tool Permission: strict (overridden by command flag)
```

在这些会话期间，你仍可编辑磁盘上的持久化值，但在关闭会话之前，CLI 会强制执行生效中的运行时 flag 覆盖。

## 视觉渲染模式

TUI 根据终端性能和连接延迟在两种视觉渲染模式之一中运行。

### 备用屏模式（`always`）

该模式利用终端的备用缓冲区（alternate buffer）打开专用显示屏幕，打造沉浸式的独立应用程序界面。

*   **关键特性**：集成回滚查看（scrollback）、支持鼠标滚轮滚动、自定义渲染滚动条，并在退出时完全恢复终端初始状态。
*   **最佳适用场景**：高级终端模拟器（如 iTerm2、Ghostty 或 WezTerm）中的标准本地开发会话。

### 行内模式（`never`）

该模式直接在终端的标准 stdout 管道中按顺序流式渲染输出。

*   **关键特性**：在模拟器的原生回滚缓冲区中保留整个会话历史记录，不捕获鼠标输入，并能与标准命令输出无缝共存。
*   **最佳适用场景**：远程 SSH 终端、`tmux` 或 `screen` 等终端复用器，以及低带宽远程会话。

> [!NOTE]
> **自适应渲染（Adaptive Rendering）**：将 Alt-Screen 模式设置为 `default` 允许 TUI 自动检测你的环境。在高级本地 shell 上默认为 Alt-Screen 模式，而在通过 SSH 运行或非交互式会话中则优雅降级为 Inline 模式。

## 配置项参考

交互式设置面板（`/config`）和 `settings.json` 允许你在多个分类中自定义 CLI 的行为。

### 安全与权限

管理 agent 如何与你的系统和代码库交互：

*   **Tool 权限（`toolPermission`）**：控制 tool（例如运行终端命令）的授权流程。
    *   `request-review`（默认）：在运行写入、bash 或 web 类 tool 之前提示请求你的批准。
    *   `proceed-in-sandbox`：如果终端命令在 sandbox 内运行则自动执行；否则提示审核。
    *   `strict`：对所有非读取类 tool 都进行提示，确保获得最大控制权。
    *   `always-proceed`：无需提示直接运行所有 tool（风险最高，请谨慎使用）。
*   **Artifact 审核（`artifactReviewPolicy`）**：控制 agent 在将生成的 artifact（工件/成果物，如代码文件）写入磁盘前何时提示你进行审核。
    *   `asks-for-review`（默认）：始终提示你审核变更。
    *   `agent-decides`：agent 根据变更的复杂性自主决定是否进行提示。
    *   `always-proceed`：agent 直接写入更改而无需提示（最大化自主性，但增加了未经审核覆盖代码的风险）。
*   **Sandbox 模式（`enableTerminalSandbox`）**：启用（`on`）后，将所有由 agent 发起的终端命令限制在安全的操作系统容器中。
*   **非 Workspace 访问（`allowNonWorkspaceAccess`）**：控制 agent 是否可以读取或写入当前活动项目目录之外的文件。为了安全起见，默认设置为 `off`。

### 显示与渲染

定制 TUI 的视觉体验：

*   **渲染模式（`altScreenMode`）**：控制 TUI 如何利用终端缓冲区。
    *   `default`：自适应模式。在高级本地终端上使用 Alt-screen，在 SSH 上降级为 inline 模式。
    *   `always`：强制使用 Alt-screen 模式，提供支持鼠标和滚动条的沉浸式按页渲染界面。
    *   `never`（可通过 `settings.json` 配置）：强制使用 inline 模式，按顺序渲染输出并在模拟器的回滚缓冲区中保留历史记录。
*   **配色方案（`colorScheme`）**：选择视觉主题。选项包括 `terminal`（继承 shell 配色）、`dark`、`light`、`solarized dark/light`、`tokyo night` 以及对色盲友好的变体。
*   **动画速度（`runningLightSpeed`）**：调整进度指示器动画的速度（`fast`、`medium`、`slow` 或 `off`）。
*   **详细程度（`verbosity`）**：控制详细程度级别。`high` 显示完整的 agent 思考和 tool 步骤；`low` 仅显示精简的进度指示器。

### 编辑器与通知

配置与宿主环境的集成：

*   **编辑器（`editor`）**：用于查看 artifact 或编写 prompt（通过 `Ctrl+G`）的文本编辑器。默认为 `auto`（遵循 `$EDITOR`），但也可以设置为 `vim`、`emacs` 或其他编辑器。
*   **编辑器模式（`editorMode`）**：CLI prompt 输入框内部使用的编辑模型。默认为 `default`（普通平面文本编辑）；将其设置为 `vim` 可启用模态编辑。请参阅 [Vim 编辑器模式](/docs/cli/vim-editor-mode)。该项独立于上方的 `editor` 设置，后者仅用于选择外部程序。
*   **通知（`notifications`）**：启用（`on`）后，当耗时较长的任务完成或需要你关注时，会触发系统桌面通知和终端响铃提示音。

### AI 额度与反馈

管理用量、使用贴士和遥测：

*   **使用 AI 额度（`useG1Credits`）**：*仅限外部构建版本。* 启用（`on`）后，如果你的方案标准配额耗尽，允许 CLI 使用你的个人 AI 额度进行模型调用。
*   **启用遥测（`enableTelemetry`）**：通过发送匿名使用统计数据和崩溃报告来帮助 Google 改进工具。
*   **显示贴士（`showTips`）**：切换 agent 生成响应时是否显示有用的使用贴士。
*   **显示反馈调查（`showFeedbackSurvey`）**：启用任务完成后定期的简短问卷调查，以帮助改善产品体验。

## 自定义状态行与终端标题

针对高级 TUI 环境集成，你可以切换活动指标或部署自定义脚本来生成动态 statusline（状态栏/状态行）并修改终端窗口标题：

*   **[状态行定制](/docs/cli/commands/statusline)**：了解如何管理状态指示面板以及构建自定义格式的 statusline shell 脚本。
*   **[终端标题定制](/docs/cli/commands/title)**：了解如何切换窗口标题输出并将实时 agent 状态导入窗口标题栏中。

## Keybindings 配置

你可以通过将按键映射到特定的 workspace 命令，来自定义 TUI 中的几乎所有键盘快捷键。

### Keybindings 文件位置

自定义映射与你的主设置配置文件保存在同一目录下：

```
~/.gemini/antigravity-cli/keybindings.json
```

### 格式与自定义

该 JSON 结构将单个 TUI 命令操作映射到一个快捷键序列数组：

```json
{
    "cli.clear_screen": ["ctrl+l"],
    "prompt.insert_newline": ["shift+enter", "ctrl+j"],
    "edit.open_editor": ["ctrl+g"]
}
```

若要完全禁用某个默认快捷键，请将其操作映射到一个空数组 `[]`。如果你的 JSON schema 格式错误或无效，CLI 会在这些特定操作上回退到系统默认值，并加载其余有效的映射。

> [!NOTE]
> **受保护的按键（Protected Keys）**：关键导航快捷键如 `cli.exit`（`Ctrl+D` / `Ctrl+C`）和 `cli.enter`（`Enter`）受到系统保护，无法被禁用。

### 恢复默认设置

若要将所有按键恢复为系统默认值，请删除 keybindings 配置文件：

```bash
rm ~/.gemini/antigravity-cli/keybindings.json
```

## 后续步骤

现在你已配置好环境，接下来可以查看安全控制与扩展选项：

*   **[权限与 Sandbox](/docs/cli/sandbox)**：管理安全执行隔离边界。
*   **[Plugin 与 Skill](/docs/cli/plugins)**：创建自定义 skill 并导入旧版 plugin。
*   **[CLI 参考手册](/docs/cli/reference)**：查阅列出所有配置选项、命令和默认按键映射的速查表。