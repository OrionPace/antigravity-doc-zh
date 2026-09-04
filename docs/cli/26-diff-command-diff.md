# Diff 命令 (/diff)

在 TUI（终端界面）内以交互方式查看和审查 workspace 变更、提交历史以及 agent turn（轮次）差异。

## 概述

`/diff` 命令会打开**交互式 Diff 查看器（Interactive Diff Viewer）**，这是一个全屏面板，可用于审查 workspace 与会话历史中的变更。它支持三种独立模式（VCS、Turn 和 Commit），并提供了交互式的 review（审查）工作流，允许你添加逐行评论来引导 agent 的下一步操作。

## 交互式 Diff 查看器面板

打开 Diff 查看器：

1. 在 prompt 输入框中输入 `/diff`。
2. 按 Enter 键。

```
/diff
```

### 导航与快捷键控制

Diff 查看器提供三种工作模式，你可以使用 Tab（或 → / ← 方向键）在它们之间循环切换：

* **VCS Mode（版本控制模式）**：显示当前活跃 workspace 中所有已修改和未跟踪文件的列表。
    * 自动支持 Git、Mercurial（Hg）和 Jujutsu（JJ）。
    * 使用 ↑/↓ 在文件列表中导航，按 Enter 打开详情视图。
* **Turn Mode（轮次模式）**：显示当前会话中每个 agent turn 所引入的代码变更。
    * 适用于逐步审查 agent 的工作成果。
    * 使用 ↑/↓ 导航，按 Enter 查看详情。
* **Commit Mode（提交模式）**：渲染仓库的交互式提交图/提交树（commit graph/tree）。
    * 使用 ↑/↓ 在提交链中导航。
    * 使用 ←/→ 导航到图中的相邻分支。
    * 按 Enter 加载选定提交的 diff。

* * *

## 分步操作指南

以下介绍了如何使用 Diff 查看器审查代码变更、添加评论并引导 agent。

### 1. 审查工作区变更（VCS 模式）

当你运行 `/diff` 时，默认会以 **VCS Mode** 打开（如果你有尚未提交的变更）。你将看到已修改和未跟踪文件的列表：

![VCS Diff 列表](/assets/image/docs/cli/diff-vcs-list.png)

在某个文件上按 Enter 键可打开其**详情视图（Detail View）**，该视图会展示统一 diff（unified diff）。

* 使用 ↑/↓（方向键）滚动浏览 diff。
* 使用 J/K（或 ←/→）在文件之间快速切换，无需返回列表。
* 使用 N/Shift + N 跳转到下一个/上一个 diff 块（hunk）。

![详情视图](/assets/image/docs/cli/diff-detail.png)

### 2. 添加评论并引导 Agent

在详情视图中，你可以审查代码并直接在特定代码行上编写反馈建议。

**第 1 步：定位代码行**  
滚动到你想要添加评论的代码行。

**第 2 步：打开评论输入框**  
按 C 键。底部会弹出**评论输入框（Comment Input）**浮层：

![评论输入框](/assets/image/docs/cli/diff-comment.png)

**第 3 步：编写反馈内容**  
输入你的反馈意见，按 Enter 键保存（或按 Esc 取消）。

**第 4 步：管理评论**  
已保存的评论会在 diff 中被标记出来。你可以高亮选中该行并按 D 键删除评论。

**第 5 步：退出并提交**  
按 Esc 返回文件列表。再次按 Esc 退出 `/diff`。如果你有未保存的评论，会出现确认界面：

* 按 Shift + Y 确认并退出。你的评论将被格式化并作为下一条 prompt 发送给 agent，从而引导其下一个 turn。
* 按 Shift + N 拒绝并退出，放弃这些评论。

### 3. 审查轮次历史（Turn 模式）

按 Tab 键切换到 **Turn Mode**。此模式会按照引入变更的会话 turn 对修改进行分组，使你能够清晰查看 agent 在先前各个步骤中具体执行了哪些改动：

![Turn Diff 列表](/assets/image/docs/cli/diff-turn-list.png)

### 4. 浏览提交树（Commit 模式）

再次按 Tab 键切换到 **Commit Mode**。这会将仓库的提交历史渲染为可交互的图形。你可以在提交链中上下浏览，或者使用 ←/→ 在分支之间切换跳转：

![Commit 列表](/assets/image/docs/cli/diff-commit-list.png)

高亮选中任意提交并按 Enter 键，即可加载并审查其 diff：

![Commit 详情](/assets/image/docs/cli/diff-commit-detail.png)

* * *

## 快捷键参考指南

### 文件列表视图（VCS 和 Turn 模式）

| 按键 | 操作 |
| :-- | :-- |
| Tab / → / ← | 循环切换模式（VCS → Turn → Commit） |
| ↑ / ↓（或 J / K） | 在文件列表中导航 |
| Enter | 打开选定文件的详情视图（Detail View） |
| Esc | 退出 Diff 查看器 |

### 文件详情视图

| 按键 | 操作 |
| :-- | :-- |
| ↑ / ↓ | 滚动 diff 内容 |
| PgUp / PgDn | 按页滚动 diff |
| J / K（或 → / ←） | 切换到下一个 / 上一个文件 |
| N / Shift + N | 跳转到下一个 / 上一个 diff 块（hunk） |
| C | 在当前行添加/编辑评论 |
| D | 删除当前行上的评论 |
| Esc | 返回文件列表视图 |

### 提交树视图（Commit 模式）

| 按键 | 操作 |
| :-- | :-- |
| ↑ / ↓ | 浏览提交历史 |
| ← / → | 导航到图中的相邻分支 |
| Enter | 加载选定提交的 diff |
| Esc | 退出 Diff 查看器 |

### 退出确认界面

| 按键 | 操作 |
| :-- | :-- |
| Shift + Y | 退出并将评论发送给 agent |
| Shift + N | 退出并放弃评论 |
| Esc | 返回文件列表视图 |

## 另请参阅

* **[Settings & Keybindings](/docs/cli/settings)**：自定义你的 TUI 主题、alt-screen 偏好设置及快捷键绑定。
* **[Conversations](/docs/cli/conversations)**：了解如何管理、分支（fork）与回退（rewind）会话线程。
* **[CLI Reference](/docs/cli/reference)**：所有 Slash Commands 和默认快捷键的快速参考。