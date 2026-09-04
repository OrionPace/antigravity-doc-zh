# 选择执行模式

控制 Antigravity CLI 在会话期间修改文件或执行命令前是否暂停确认。

## 开始之前

* [安装 Antigravity CLI](/docs/cli/install)
* 准备一个包含待编辑源码的有效项目代码仓库

## 可选模式

每种执行模式都在对话自主度与开发者监督度之间做出了不同的权衡。下表展示了 Antigravity CLI 在各模式下如何处理文件操作与计划制定。

| 模式 | 行为 | 适用场景 |
| :-- | :-- | :-- |
| `default` | 在修改或创建文件前暂停，进行交互式 diff 审查。 | 标准开发、审查敏感代码变更以及谨慎的代码重构。 |
| `accept-edits` | 自动批准文件编辑与创建操作（`mkdir`、`touch`、文件写入）。 | 快速原型设计、在受信任代码上快速迭代，以及减少 prompt 打断。 |
| `plan` | 自动添加 `/plan` 指令前缀，在编写代码前分析并列出步骤大纲。 | 探索陌生架构或设计复杂的多步骤特性。 |

> **注意：** 通过 `/permissions` 或 `--dangerously-skip-permissions` 配置的工具权限 rule（规则）在所有执行模式下将继续监管 shell 命令（`run_command`）。

## 在会话中循环切换执行模式

您可以在会话进行中切换执行模式，而无需中断当前活跃任务或重启终端。

1. 在 prompt 输入框内按 `Shift+Tab`，即可在以下序列中循环切换：`default` → `accept-edits` → `plan` → `default`
    
2. 观察 prompt 输入框下方的状态栏指示器，确认当前激活的模式（`[accept-edits]` 或 `[plan]`）。
    

> **提示：** 当 Antigravity CLI 在 `default` 模式下暂停等待待处理的文件编辑确认时，您可以按 `Shift+Tab` 立即切换到 `accept-edits` 模式并自动批准所有待处理的文件修改。

## 在 default 模式下审查修改

在 `default` 模式（`request-review`）下，Antigravity CLI 在向磁盘应用任何文件写入操作之前都会暂停，并呈现内联的语法高亮 diff 预览。

```
# 以默认交互式审查模式启动
agy
```

当收到待处理文件修改提示时：

* 按 `y` 接受更改并将文件保存至磁盘。
* 按 `n` 拒绝修改并保持现有文件不变。
* 按 `f`（`KeyViewDiff`）打开全屏可滚动的 diff 审查界面（包含 3 行上下文与 hunk 分隔符）。
* 按 `Ctrl+G` 在您的 `$EDITOR` 中打开该文件进行手动调整。
* 在 prompt 输入框中输入具体指令并按 `Enter` 拒绝此次编辑，同时告知 agent 应当做出怎样的不同修改。

![default 模式下的文件编辑 diff 审查面板，显示代码行修改与操作选项](/assets/image/docs/cli/modes-edit-file-preview.png)

### 新文件创建预览

当 Antigravity CLI 创建全新文件时，确认面板会显示仅包含新增内容的 diff 预览，带有专用的 `"Create file"` 标题以及明确的允许/拒绝提示：

```
Create file: src/utils/formatter.ts
Allow create this file? [y/n/f]
```

![在 default 模式下创建新文件时显示的纯新增 diff 确认面板](/assets/image/docs/cli/modes-create-file-preview.png)

## 使用 accept-edits 模式自动批准编辑

当您希望 Antigravity CLI 在文件系统中长时间连续工作而不因每次文件修改而中断时，请选择 `accept-edits` 模式。

```
# 直接以 accept-edits 模式启动
agy --mode=accept-edits
```

在这个模式下，所有标准的文件读取、创建和替换操作（`write_to_file`、`replace_file_content`、`multi_replace_file_content`）均会自动执行。在会话期间生成的 subagent（子代理）也会继承 `accept-edits` 设置，从而防止后台文件写入排队等待手动审批。

![CLI 在 accept-edits 模式下运行，展示状态指示器与自动文件修改](/assets/image/docs/cli/modes-accept-edits-status.png)

## 使用 plan 模式在编辑前分析任务

在处理复杂重构、多文件架构改动或对陌生代码库进行调研时，请使用 `plan` 模式。

```
# 直接以 planning 模式启动
agy --mode=plan
```

通过 `Shift+Tab` 循环切换或使用 `--mode` flag 激活 `plan` 模式后，CLI 会自动在您的 prompt 前添加 `/plan` 指令前缀。agent 会使用只读工具（`code_search`、`grep_search`、`view_file`）调研相关文件，并在编写代码之前呈现一份结构化的执行大纲供您审批。

![CLI 在 plan 模式下运行，分析代码并构建执行大纲](/assets/image/docs/cli/modes-plan-execution.png)

## 持久化或覆盖您的默认模式

您可以跨会话永久设置偏好的启动执行模式，也可以针对单次调用进行临时覆盖。

### 使用交互式设置面板

在会话中打开交互式设置面板以检查或更新您的默认配置：

```
/settings
```

![高亮显示 Agent Mode 选项的交互式设置面板](/assets/image/docs/cli/modes-settings-panel.png)

使用 `↑`/`↓` 导航至 **Agent Mode**，按 `Enter` 或 `Space` 选择默认模式（`default`、`accept-edits` 或 `plan`），然后按 `Ctrl+S` 保存。修改此选项会立即同步您运行时的 `CycleMode`。

### 在 `settings.json` 中设置 `agentMode`

直接在用户或项目配置文件中设置 `agentMode`：

```
{
    "agentMode": "accept-edits"
}
```

CLI 在启动时会从 `~/.gemini/antigravity-cli/settings.json` 加载该文件，并应用您选择的基准执行模式。

### 命令行 Flag 覆盖

传入 `--mode` flag 可以在单次终端运行中临时覆盖持久化的默认模式：

```
# 覆盖 settings.json，以 planning 模式运行
agy --mode=plan
```

## 常见错误

| 常见错误 | 失败原因 | 解决方法 |
| :-- | :-- | :-- |
| 期望在 `Shift+Tab` 循环中看到 `sandbox` | `sandbox` 是操作系统隔离权限设置，并非执行模式 | 在 `/permissions` 中配置 sandbox 自动批准 rule |
| 使用旧版 `/planning` 或 `/fast` 命令 | 这些过时命令已在 `1.1.0` 中移除 | 按 `Shift+Tab` 循环切换模式，或在 prompt 前输入 `/plan` |
| 传入 `--permission-mode` | `agy` 使用 `--mode`（`--mode=accept-edits` 或 `--mode=plan`）来覆盖执行模式 | 运行 `agy --mode=accept-edits` 或查看 `agy --help` |

## 后续步骤

* [权限](/docs/cli/permissions)：配置细粒度工具审批 rule 与通配符匹配
* [设置、渲染与键位绑定](/docs/cli/settings)：自定义配置覆盖项与交互偏好设置
* [后台任务与 Subagent](/docs/cli/subagents)：管理并行 subagent 执行与异步任务队列