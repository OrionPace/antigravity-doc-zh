# 模型配额 (/usage)

查看活跃模型配额使用情况并刷新配置。

## 概述

Antigravity CLI 提供了 `/usage` 命令（别名为 `/quota`），帮助你监控资源消耗。运行该命令时，CLI 会从后端刷新模型配置与配额状态，并打开一个交互式 TUI（终端界面）面板。

## 查看使用情况

若要打开模型配额（Model Quotas）面板：

1.  在 prompt（提示词输入框）中输入 `/usage`（或 `/quota`）。
2.  按 Enter 键。

```
/usage
```

![Quota & Credits TUI](/assets/image/docs/cli/usage-tui.png)

### 交互式面板功能

该面板展示：

*   **模型配额 (Model Quotas)**：每个受支持模型（例如 Gemini 3.5 Flash、Gemini 3.1 Pro）的使用限额以及剩余请求数/Token 数量明细。
*   **主动刷新 (Active Refresh)**：打开此面板时，CLI 会自动触发对本地磁盘以及后端服务配额的最新检查。

### 导航控制

使用以下快捷键在面板中导航：

| 按键 | 操作 |
| :-- | :-- |
| ↑ / ↓（或 J / K） | 向上或向下滚动一行。 |
| PgUp / PgDn | 向上或向下滚动一页。 |
| G / Shift+G | 跳至列表顶部或底部。 |
| Esc（或 Q） | 关闭面板并返回 prompt 输入框。 |

## 后续步骤

*   **[CLI 参考](/docs/cli/reference)**：查看所有可用的 Slash Commands 与按键绑定。
*   **[设置与渲染](/docs/cli/settings)**：配置默认模型和积分使用偏好。