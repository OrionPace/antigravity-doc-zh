# Code Search 命令 (/codesearch)

在 TUI（终端界面）内部交互式搜索 workspace 中的代码，无需退出当前会话或打断 agent。

## 概述

`/codesearch` 命令会打开一个全屏的 **Code Search**（代码搜索）面板，在当前 workspace 中执行搜索，并按文件分组展示匹配项，同时提供上下文并高亮显示匹配文本。该功能非常适合快速定位符号、字符串或模式，并直接跳转到目标文件的对应匹配行。`/codesearch` 直接查询你的 workspace，并即时返回结果。

该命令有两个别名：`/cs` 和 `/search`。

## 执行搜索

1. 在 prompt 输入框中输入 `/codesearch`，后接搜索查询内容。
2. 按 Enter 键。

```
/codesearch UserSession
```

Code Search 面板将打开并按文件对结果进行分组显示。顶部标题栏展示你的查询内容和匹配项数量，每个匹配项都会显示其上下各一行的上下文，匹配文本会被高亮显示：

![Code Search 面板按文件分组展示查询匹配项并高亮显示结果](/assets/image/docs/cli/codesearch-results.png)

### 导航与快捷键控制

该面板完全由键盘驱动：

| 按键 | 操作 |
| :-- | :-- |
| ↑ / ↓ | 在各个匹配项之间移动 |
| ← / → | 跳转到上一个 / 下一个文件组 |
| Enter | 在内置文件查看器中打开高亮的结果并定位到匹配行 |
| Ctrl + G | 在外部编辑器中打开高亮的结果并定位到匹配行 |
| Esc | 关闭面板并返回 prompt |

## 查询语法

默认情况下，查询内容会被解析为**正则表达式（regular expressions）**，且匹配不区分大小写，除非你的查询包含大写字母（smart case，智能大小写）。

### 字面量（固定字符串）匹配

在查询中的任意位置添加 `-F`（或 `--literal`）即可禁用正则表达式，进行字面量文本匹配。当查询中包含如 `.`、`(` 或 `*` 等正则表达式元字符时，这非常有用：

```
/codesearch -F map[string]*UserSession
```

### 按文件路径过滤

使用 `f:`（别名包括 `file:` 和 `path:`）后跟 glob 模式，可以将搜索限制在特定文件中。在过滤器前添加前缀 `-` 则可反向*排除*匹配的文件：

```
/codesearch f:store.go Session
```

```
/codesearch -f:*_test.go NewUserSession
```

![使用 f: 路径过滤器将 Code Search 面板限定在单个文件](/assets/image/docs/cli/codesearch-filter.png)

## 打开文件并针对代码行发表评论

Code Search 不仅仅是一个查看器——你可以打开任意搜索结果，直接在 CLI 内向 agent 提供精准到行级的反馈，无需退出会话。

### 打开结果

使用 ↑ / ↓ 高亮选中某个匹配项，然后按 Enter 键即可在内置文件查看器中打开该文件，并自动滚动到匹配行。或者使用 Ctrl + G 在外部编辑器中打开。

在文件查看器内部，底部状态栏会显示可用操作：

```
↑/↓ scroll · pgup/pgdown page · shift+g bottom · g top · c comment · ctrl+g editor · / search
```

### 在指定代码行添加评论

1. 移动光标（↑ / ↓）到想要批注的代码行。
2. 按 C 键打开该行的行内评论编辑器。
3. 输入你的注释说明。使用 Shift + Enter（或 Alt + Enter）换行，按 Enter 键保存。

保存后的评论会关联到该代码行，并在行号槽（gutter）中标记 💬 图标。你可以按需对多个代码行重复此操作。若要删除评论，将光标移动到该行并按删除键（D）。

![在从 Code Search 打开的文件查看器中留下行评论](/assets/image/docs/cli/codesearch-comment.png)

### 将评论发送给 agent

当你按 Esc 退出文件查看器时，CLI 会收集所有待发送的评论，并询问是否发送它们：

* Y — **send + close**（发送并关闭）：你的评论将作为下一条消息发送给 agent，格式为 `<file>:<line>: <comment>`，以便模型清楚了解你指的是哪些代码行。
* N — **discard + close**（放弃并关闭）：退出且不发送。
* Esc — 取消退出并继续编辑。

![确认是否将未发送的行评论发送给 agent](/assets/image/docs/cli/codesearch-comment-send.png)

这使得 Code Search 成为一种在单一流式交互中快速查找相关代码、并为 agent 提供针对性且基于代码行锚定指令的高效方式。

## 下一步

* **[CLI Features](/docs/cli/features)**：探索交互式 TUI 的其他功能。
* **[Prompting Guide](/docs/cli/prompting)**：了解如何引导 agent 替你搜索和编辑代码。
* **[Resume Command (/resume)](/docs/cli/commands/resume)**：浏览并管理你以往的历史会话。