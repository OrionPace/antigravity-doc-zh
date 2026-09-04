# Prompt 与交互

掌握基础交互模式、多行编辑工作流、会话中断控制以及终端富媒体粘贴。

## Prompt 输入框

Antigravity CLI 拥有固定置底于终端屏幕下方的 prompt 面板。该面板支持标准用户输入、多行脚本编写以及直接粘贴富媒体。

```
───────────────────────────────────────────────────────────────────────────
> Describe your next engineering task here...
───────────────────────────────────────────────────────────────────────────
```

### 提交 prompt

要发起一次 agent turn（轮次），请在 prompt 面板中输入指令并按下 `Enter`。agent 会立即分析您当前所在的目录 workspace（工作区），读取所需配置，并开始制定执行计划。

### 中断活动会话

如果 agent 发起了非预期的任务，或在命令执行期间陷入循环，可按 `Esc` 立即中止会话。

> [!NOTE]
> **全局 Escape 中断机制**：`Esc` 键充当全局紧急跳出通道。按下 `Esc` 可立即取消任何活跃的 agent turn，关闭所有浮层面板，并将焦点恢复到干净的 prompt 输入框。

## 多行编辑

对于复杂的指令、结构化测试场景或多段落说明，请使用内置的多行编辑功能。

### 快速插入换行

* **标准换行**：按 `Shift+Enter` 或 `ctrl+j` 即可在当前 prompt 窗口中插入换行符，而不会直接提交。
* **macOS Terminal 备用方案**：若使用 Apple Terminal（默认不转发 `Shift+Enter`），请按 `Option+Enter`。请确保在终端偏好设置中勾选了 **Use Option as Meta key（将 Option 键用作 Meta 键）**。
* **通用反斜杠转义**：在当前行末尾输入反斜杠 `\` 并按下 `Enter`。CLI 会自动移除该反斜杠并插入换行。

### 在 `$EDITOR` 中编辑 prompt

若要在您主要的开发编辑器中起草或编辑篇幅较长的 prompt 结构：

1. 在空的 prompt 面板中按 `ctrl+g`。
2. CLI 将启动系统默认的文本编辑器（例如 `vim`、`nano` 或 `code`，可通过 `/config` 或环境变量 `$EDITOR` 进行配置）。
3. 在临时编辑器缓冲区中编写您的多行指令。
4. 保存并退出编辑器。CLI 将自动把编辑后的缓冲区内容导入回终端 prompt 中。

## 附加媒体文件

Antigravity CLI 支持直接从系统剪贴板粘贴富媒体格式。在 prompt 面板中按 `ctrl+v`（或终端原生粘贴快捷键），即可附加截图原型图或录屏视频。

### 支持的文件类型

* **图片**：PNG、JPEG、GIF、WebP、BMP、TIFF 和 SVG。
* **视频**：MP4、MOV、WebM 和 AVI。

## 后续步骤

掌握交互模式后，了解 agent 如何呈现操作并请求核验确认：

* **[审查 Artifact](/docs/cli/artifacts)**：学习检查和管理文件编辑、计划与测试执行。
* **[管理会话](/docs/cli/conversations)**：恢复先前的会话线程并分叉活跃会话。
* **[后台任务与 Subagent](/docs/cli/subagents)**：监控异步运行的后台 agent。