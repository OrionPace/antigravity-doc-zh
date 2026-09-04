# Resume 命令 (/resume)

浏览、搜索并恢复历史会话线程，或通过命令行即时恢复上一次会话。

## 概述

Antigravity CLI 允许你维护多个进行中的开发线程。`/resume` 命令会打开一个交互式的 **Session Picker**（会话选择器）TUI 面板，用于浏览和加载历史会话。你也可以使用命令行 flags 直接从宿主终端恢复会话。

* * *

## 交互式会话选择器

在 TUI 中打开 Session Picker：

1. 在 prompt 输入框中输入 `/resume`（或别名 `/switch`、`/conversation`）。
2. 按 Enter 键。

```
/resume
```

### 1. 浏览与搜索会话

Session Picker 会显示按时间倒序（最新的在前）排列的历史会话列表。

* **Search（搜索）**：输入任意字符即可根据标题、预览文本或唯一 ID 实时过滤会话。
* **Navigate（导航）**：使用 ↑/↓ 在过滤后的列表中滚动。
* **Page（翻页）**：使用 ←/→ 向前或向后翻页浏览更早的历史记录块。
* **Select（选择）**：高亮选中目标会话并按 Enter 加载它。
* **Exit（退出）**：按 Esc 关闭选择器并返回当前 prompt。

![浏览会话](/assets/image/docs/cli/resume-navigate.png)

### 2. 重命名会话

为使历史记录保持井然有序，你可以直接在选择器内重命名会话：

1. 使用 ↑/↓ 高亮选中想要重命名的会话。
2. 按 F2 键。面板底部会打开一个输入框，预填当前标题。
3. 输入新名称并按 Enter 保存，或按 Esc 取消。

![重命名会话](/assets/image/docs/cli/resume-rename.png)

### 3. 删除会话

清理废弃的会话线程：

1. 在列表中高亮选中目标会话。
2. 按 Ctrl + Delete。界面会弹出确认提示。
3. 按 Enter（或 Y）确认删除，或按 Esc（或 N）取消。

![删除会话](/assets/image/docs/cli/resume-delete.png)

### 4. 从 Antigravity 2.0 导入会话

你可以导入并恢复在 Antigravity 2.0 桌面应用中发起的活跃线程：

1. 在 Session Picker 打开的状态下，按 Tab 键从 **CLI** 标签页切换到 **Antigravity** 标签页。
2. 高亮选中你希望导入的桌面端会话。
3. 按 Enter 键。界面会出现 `[Import this? (y/n)]` 确认提示。
4. 按 Enter（或 Y）确认。CLI 会将历史记录、上下文和 tool trajectory（工具轨迹）克隆到你的终端会话中。

![从 Antigravity 2.0 导入](/assets/image/docs/cli/resume-antigravity.png)

* * *

## 命令行快捷操作

在宿主 shell 中启动 `agy` 时，你可以绕过 TUI 选择器直接恢复会话。

### 快速恢复上次会话 (`-c` / `--continue`)

立即恢复与当前活跃 workspace 关联的最近一次会话：

```
agy -c
```

*（备选方式：`agy --continue`）*

### 恢复指定会话 (`--conversation`)

通过唯一 ID 直接加载指定的会话：

```
agy --conversation <conversation-id>
```

* * *

## 底层机制：会话缓存（Session Cache）

当你使用 `-c` / `--continue` 参数时，CLI 会使用以本地 workspace 路径为键（keyed）的缓存来解析目标会话。

### 缓存文件

* **位置**：`~/.gemini/antigravity-cli/cache/last_conversations.json`
* **格式**：一个将绝对 workspace 目录路径与其最近活跃会话 ID 相关联的 JSON Map：
    
    ```json
    {
        "/usr/local/google/home/username/Develop/my-project": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "/usr/local/google/home/username/Develop/another-repo": "f9e8d7c6-b5a4-3210-fedc-ba9876543210"
    }
    ```
    

### 解析工作流

1. **启动（Launch）**：你在 `/path/to/workspace` 目录下运行 `agy -c`。
2. **查找（Lookup）**：CLI 读取 `last_conversations.json` 并查询键 `/path/to/workspace`。
3. **校验（Verification）**：如果找到了 ID，CLI 会查询后端以验证该会话是否仍然存在。
4. **加载（Load）**：
    * 如果验证通过，则加载该会话。
    * 如果该会话已被删除或键不存在，则为该 workspace 启动一个全新的会话。

* * *

## 另请参阅

* **[Managing Conversations](/docs/cli/conversations)**：了解 workspace 作用域以及使用 `/fork` 进行分支管理。
* **[CLI Reference](/docs/cli/reference)**：查看所有可用的 Slash Commands 和默认快捷键。
* **[Settings & Keybindings](/docs/cli/settings)**：配置渲染模式并自定义快捷键绑定。