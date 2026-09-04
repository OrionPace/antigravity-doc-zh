# Antigravity CLI 最佳实践

掌握工作流、prompt 架构与本地配置选项，在保持稳健控制的同时最大化提升 agent（智能体/代理）执行效率。

## 建立验证闭环

确保自主 agent 输出可靠、正确修改的最有效方法，就是为 agent 提供本地验证机制（例如单元测试、构建命令或格式化脚本）。

在要求 agent 实现代码更改之前：

1.  确保你的 workspace（工作区）目录已准备好测试套件。
2.  如果测试尚不存在，请先指示 agent 编写标准测试块。
3.  一旦 agent 提出了代码修改，指示它运行本地测试命令来验证其成果。
4.  观察 agent 执行命令并根据测试输出自动进行迭代修正。

```
> Implement feature X in main.py. Run npm test afterward to verify the build.
```

## 探索、规划，然后执行

当复杂的代码修改被清晰划分为探索、规划和执行三个不同阶段时，自主本地 agent 的运行准确率最高。

*   **探索 (Exploration)**：在编写任何更改之前，先要求 agent 解释目标代码库如何解决特定问题，或者某接口是在何处定义的。
*   **规划 (Planning)**：要求 agent 提供实施计划。agent 将在 implementation plan artifact（实施计划工件）中列出目标文件、所需依赖项以及逻辑覆盖方案。
*   **执行 (Execution)**：一旦你批准了结构化计划，指示 agent 应用这些修改。

```
> Explore how our router resolves `/docs/:page`. Write down an implementation plan to add `/docs/best-practices`.
```

## 丰富 Prompt 上下文

为本地 agent 提供高保真度指示，以收窄推理边界并最大限度降低 token 开销。

### 目标文件自动补全

在 prompt 输入框中键入 `@` 即可触发 **交互式路径建议 (Interactive Path Suggestion)** 浮层。高亮并选中某个路径会将 workspace 文件的绝对路径直接导入到你的 prompt 中。这有助于 agent 精准定位代码搜索范围。

### 附加视觉证据

如果正在排查视觉 UI 问题、渲染 bug 或前端布局不一致的情况，可以截取屏幕截图或录制视频并复制，然后在 prompt 输入框内按 `Ctrl+V` 粘贴附加该媒体。agent 将查阅该媒体文件以诊断问题。

## 配置 Workspace 环境

优化你的本地工作站 rule（规则）与安全边界，以契合你的工程开发流程。

### 编写代码库 Rule 文件

在 workspace 根目录下创建一个 `GEMINI.md` 或 `AGENTS.md` 文件，列出特定的目录规范、代码风格范式、测试命令参数以及弃用警告。agent 在启动时会自动解析这些 rule，并在提出更改建议之前查阅它们。

### 建立结构化权限

根据你的项目风险级别，在 `~/.gemini/antigravity-cli/settings.json` 中调整你的安全防线：

*   **`request-review`**（默认）：在执行任何写入操作、bash 命令或远程网络调用之前向你发起确认提示。
*   **`proceed-in-sandbox`**：将所有终端执行限制在安全 sandbox（沙箱）隔离环内。安全命令自主执行，而高危命令则提示进行人工审查。
*   **`strict`**：始终对所有非只读操作进行提示，提供完全透明的逐行把控。

```json
{
    "toolPermission": "proceed-in-sandbox",
    "enableTerminalSandbox": true
}
```

## 主动管理 TUI 会话

利用活跃会话导航工具，从工程死胡同中恢复，或对 agent 的中间循环进行纠偏。

### 及早纠偏 (`Esc`)

如果你观察到 agent 正在执行错误的搜索模式或编写违背你意图的代码，请立即按下全局退出键 `Esc` 中断当前 turn（轮次），重新获得干净的 prompt 输入焦点。

### 使用 `/rewind` 回滚历史

如果 agent 连续做了多次修改引入了构建错误，你无需废弃整个会话。输入 `/rewind`（或 `/undo`）即可将对话线程回滚到先前的稳定检出状态。

### 使用 `/fork` 创建实验分支

如果你不确定哪种实现方案最优：

1.  先达到一个稳定的基准对话线程。
2.  输入 `/fork` 派生一个完全相同的并行会话。
3.  在分支会话中测试你的探索性代码修改。
4.  如果该方案失败，运行 `/resume` 切回稳定的主分支。

## 自动化与脚本化

Antigravity CLI 旨在与标准 shell 管道工具无缝配合运行。

### 运行非交互式命令 (`-p`)

若要自动化快速查询或将 agent 集成到 git hook（钩子）中，请使用单次 prompt 标志 `-p`：

```bash
agy -p "Review this git diff and draft a conventional commit message" --cwd $(pwd)
```

### 利用并行 Subagent 扇出任务

对于大规模扫描或跨多个文件的重构任务，指示主 agent 生成并发的后台 subagent（子代理）。agent 管理器将自主调度后台线程，而你可以继续在主屏幕上进行工作。

## 相关资源

了解如何配置设置以及自定义视觉布局：

*   **[设置、渲染与按键绑定](/docs/cli/settings)**：自定义键盘热键和缓冲区。
*   **[权限与沙箱](/docs/cli/sandbox)**：强制执行文件系统隔离约束。
*   **[插件与技能](/docs/cli/plugins)**：创建你自己的自定义 slash commands。