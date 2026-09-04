# 审查 Artifact

在将更改真正应用到本地文件系统之前，审查生成的代码、评估方案实施计划、添加行级反馈评论，并验证视觉媒体资产。

## 协同工作与共同掌控

**Artifact（工件/成果物）** 是 agent 为完成任务并向您传达其进展与思考而创建的结构化成果交付物。Artifact 包括富 Markdown 大纲（例如实施计划 Implementation Plan）、代码变更 diff、架构图以及各类视觉媒体文件。

随着 agent 在更长时间跨度内以更高的自主度运行，artifact 实现了高效的异步协同。您无需实时同步监控每一次单独的 tool call（工具调用），而只需在关键里程碑节点审查高阶交付物。

由于自主运行的 agent 偶有偏离目标或产生方案幻觉的可能，artifact 工作流充当了至关重要的交互式协同把控（co-steering）机制。根据您的配置，agent 会在中间里程碑节点暂停，允许您检查拟定的计划或代码修改、提供行内批注，并在任何更改真正写入本地文件系统之前对 agent 进行重定向。

TUI（终端界面）将这些资产划分为两个交互层级：

* **Artifact Picker 浮层面板（选择器）**：包含审查状态标记、快速预览开关以及可折叠文件夹的高阶清单菜单。
* **Artifact Detail Viewer 详情查看器**：支持行内评论、语法高亮以及图表缩放的全屏代码审查界面。

## /artifact 概述

当 agent 生成或修改文件时，TUI 状态栏会更新提示通知（`/artifact to review`）。在 prompt 输入框内按 `ctrl+r` 即可打开全屏 **Artifact Picker 面板**。

```
                                                                                                    10 artifacts · /artifact to review
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
>
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Action required (10 left)
› [ ] new release_notes.md   open  approve reject
  utils.py
  [ ] new performance_report.md
  api_client.py
  config_manager.py
  [ ] new user_guide.md
  run_tests.py
  data_processor.py
  [ ] new system_architecture.md
  [ ] new project_overview.md

Keyboard: ↑/↓ Navigate  y/n Approve/reject  shift+a Approve all  p Preview  esc Done
```

### 交互键位绑定

使用以下面板专用控制键审查文件清单：

| 按键 | TUI 命令 | 操作行为 |
| :-- | :-- | :-- |
| **`↑`** / **`↓`** | `nav.scroll_line` | 在条目列表中上下滚动高亮选中项。 |
| **`h`** / **`l`** | `nav.switch_button` | 聚焦并在行内按钮间切换：**open**、**approve** 和 **reject**（亦支持左/右方向键）。 |
| **`p`** | `confirm.preview` | 切换**快速行内文件预览**。在当前选中行正下方展开 12 行代码的缩进截断预览块。 |
| **`y`** | `confirm.approve` | 立即批准高亮选中的文件。状态标记更新为绿色对勾（`✓ approved`）。 |
| **`n`** | `confirm.reject` | 立即拒绝高亮选中的文件。状态标记更新为红色叉号（`✗ rejected`）。 |
| **`Shift+A`** | `confirm.approve_all` | 一键批量批准所有待处理的操作文件。 |
| **`Shift+R`** | `confirm.reject_all` | 一键批量拒绝所有待处理的操作文件。 |
| **`Enter`** | `nav.confirm` | 执行当前聚焦的按钮操作。若聚焦于 `open` 按钮，则启动全屏 Detail Viewer。 |
| **`Esc`** | `nav.escape` | 保存当前审查状态，将批准/拒绝决定提交回 agent 线程，并将焦点返回到 prompt 输入框。 |

### 代码文件与视觉媒体

为了有序组织 workspace 资产，选择器根据格式类型对文件进行归类：

* **待操作代码文件（Actionable Code Files）**：需要明确批准的标准编程源代码、配置文件和规划 Markdown。
* **可折叠媒体抽屉（Collapsible Media Drawer）**：视觉资产文件（如 PNG、JPG、WebP、SVG、MP4 或 WebM 媒体）被归入专用的 **“Media”** 折叠抽屉标题下。
    * 高亮选中 **Media** 标题行并按 `Enter` 即可展开或折叠媒体列表。
    * 高亮选中某个具体媒体项并按 `Enter`，将在操作系统的原生媒体查看器中打开该文件。

* * *

## 查看 Artifact

若要对文件的代码结构或拟定逻辑进行深入审查，请选择 `open`（或在已高亮选中的代码行上直接按 `Enter`），以打开 **Artifact Detail Viewer**。

```
implementation_plan.md
>   1      Implementation Plan: Alpha-Centauri Telemetry Scaling Engine
    2
    3     This document provides a highly detailed, step-by-step engineering implementation plan to upgrade the Alpha-Centauri
    4     telemetry ingestion pipeline. It outlines current gaps, proposed architecture improvements, execution timelines, risks,
    5     and verification procedures.
    6     ──────
    7     ## 1. Executive Summary
    8
    9     As sensor deployments scale from 100 to 10,000 active nodes, the existing synchronous Python-based ingestion system (
   10     data_processor.py ) faces critical CPU and write latency bottlenecks.
   11
   12     This implementation plan details the migration to an asynchronous, remote-buffered pipeline utilizing distributed
   13     message
   14     queues, multi-threaded worker pools, and an optimized column-oriented storage layer.
   15     ──────
   16     ## 2. Current Architecture vs. Target Architecture
   17
   18     ### Gap Analysis
   19
   20      Feature    | Existing (v1.2)   | Target (v2.0)     | Gap to Resolve
   21     ------------|-------------------|-------------------|---------------------------
   22      Concurrency| Sync, 1-thread    | Async, concurrent | Cannot scale peak bursts
   23      Buffer     | None (direct API) | Message Queue     | Outage data loss
   24      Storage    | Flat JSON         | Columnar CNS      | Slow queries, high consumption
   25      Config     | Load on launch    | Dynamic polling   | Requires restarts to update
   26
   27     ### Architectural Schema
   28
   29         Ingestion Layer │ Buffering Layer │ Processing Layer │ Storage Layer
   30
   31         ┌─────────────┐   ┌─────────────┐
   32         │ "Sensor 1"  │   │ "Sensor 2"  │
   33         └─────────────┘   └─────────────┘
   34                │ HTTP POST           │ HTTP POST
   35                ▼                     ▼
   36         ┌──────────────────┐
   37         │ "Load Balancer"  │
   38         └──────────────────┘
   39                  │
   40                  ▼
   41         ┌────────────────────────┐   ┌────────────────────────┐
   42         │ "Ingestion Gateway A"  │   │ "Ingestion Gateway B"  │
   43         └────────────────────────┘   └────────────────────────┘
   44                     │ Publish                    │ Publish
   45                     ▼                            ▼
   46         ┌──────────────────────────────────────────┐
   47         │       "Distributed Message Queue"        │
   48         └──────────────────────────────────────────┘
   49                        │ Stream Consume
   50                        ▼
   51         ┌──────────────────────┐   ┌──────────────────────┐
   52         │  "Worker Process 1"  │   │  "Worker Process 2"  │
   53         └──────────────────────┘   └──────────────────────┘
   54                    │ Read Config               │ Read Config
   55                    ▼                           ▼
   56         ┌───────────────────────────┐   ┌───────────────────────────┐
   57         │  "Dynamic Config Service" │   │  "Columnar Storage (CNS)" │
  [0%  L1  1-57/135]

  ↑/↓ scroll · pgup/pgdown page · shift+g bottom · g top · c comment · m raw mermaid · ctrl+=/ctrl+- zoom 100%
  l hide lines · esc close
```

### 审查与导航

* **滚动浏览**：使用 `j`/`k`（或标准方向键）按行或按页滚动浏览。
* **边界跳转**：按 `g` 跳转到文件顶部，按 `Shift+G` 直接跳转到底部。
* **切换行号栏**：按 `l` 切换开启或关闭行号指示栏，获得更清爽的源代码呈现。

### 细粒度行级批注

如果某段特定代码需要修正：

1. 导航并将光标定位到目标行。
2. 按 `c` 打开直接挂载到该行的行内多行文本编辑缓冲区。
3. 撰写描述性的反馈意见，按 `Esc` 保存并提交该批注。该行将更新显示直观的评论指示图标（`💬`）。
4. 若要删除当前批注反馈，将光标移动到带有批注的行并按 `d`。

### 自定义 Mermaid 架构图渲染

如果当前文档包含结构化系统流程图、数据库实体关系或系统架构布局：

* **循环切换渲染模式 (`m`)**：按 `m` 键在以下视觉渲染模式间循环切换：
    * **Kitty Graphics Image**：在兼容 Kitty 图形协议的终端仿真器内，将图表直接原生渲染为行内图形。
    * **ASCII Box Art**（默认）：将图表渲染为清晰、高性能的文本字符图，兼容所有终端 shell。
    * **Raw Code**：直接展示原始 Markdown 代码块内容。
* **缩放图形**：当 Kitty Graphics 图像模式处于激活状态时，按 `ctrl+=` 放大图像，按 `ctrl+-` 缩小图像。

按 `Esc` 关闭 Detail Viewer 并返回主选择器清单。

## 后续步骤

配置首选项设置并查看 agent 自主权参数：

* **[管理会话](/docs/cli/conversations)**：恢复先前的会话并分叉分支。
* **[设置、渲染与键位绑定](/docs/cli/settings)**：自定义键盘快捷键与视觉缓冲区。
* **[权限与沙箱](/docs/cli/sandbox)**：配置安全参数与隔离限制列表。