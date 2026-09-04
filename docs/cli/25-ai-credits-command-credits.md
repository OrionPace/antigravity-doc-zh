# AI Credits 命令 (/credits)

以交互方式查看和管理你的 AI Premium 积分（credits）。

## 概述

`/credits` 命令会在 TUI 中打开一个专属面板，展示你当前的 AI Premium 积分余额、消耗历史记录，以及用于管理订阅或购买额外积分的链接。

有关积分追踪机制、低额度告警以及设置配置的详细信息，请参阅概念指南 **[AI Credits Guide](/docs/cli/credits)**。

## 使用 Credits 命令

查看你的积分状态：

1. 在 prompt 输入框中输入 `/credits`。
2. 按 `Enter` 键。

```
/credits
```

Credits 面板将显示：

* **Active Balance（当前可用余额）**：你剩余的 AI Premium 积分。
* **Usage Summary（使用概览）**：当前账单周期内消耗积分的明细分解。
* **Quick Links（快捷链接）**：购买更多积分或升级套餐的操作（将打开相应的 Web 门户页面）。

按 `Esc` 键关闭面板并返回主 prompt。

## 下一步

* **[AI Credits Guide](/docs/cli/credits)**：了解积分消耗、告警与相关设置。
* **[Model Quotas Command](/docs/cli/commands/usage)**：监控针对特定模型的 API 配额。
* **[CLI Reference](/docs/cli/reference)**：查看所有可用的 Slash Commands。