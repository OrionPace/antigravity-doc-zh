# 管理 AI Credits 与配额

Antigravity CLI 与您的订阅集成，用于监控和管理您的 AI Premium credits 以及使用配额。

有关基础配额、credits 如何消耗以及套餐资格的详细说明，请参阅 **[Plans](/docs/plans)** 主页面。

## 配额跟踪

您可以直接在 CLI 内部监控当前的有效配额和 credit 消耗情况：

*   **Statusline 指示器**：CLI statusline（状态栏）右侧会显示您的剩余 credit 数量（例如：`AI Credits: 42`）。
*   **低配额警报**：当您的剩余 AI credits 低于警告阈值时，statusline 指示器会高亮显示，以警告您配额即将耗尽。

## Slash Commands 与余额管理

您可以直接从 CLI 查询您的 credits 或购买额外配额：

*   **查询余额**：运行 **[AI Credits 命令](/docs/cli/commands/credits)** 打开专属的 credits 面板。该面板展示了您详细的 credit 使用统计信息。
*   **管理 Credits**：您可以轻松购买 AI credits 或升级订阅，这会打开一个包含直接定价与订阅门户链接的面板。

## 配置设置

要控制何时以及如何使用您的 AI credits，您可以在 `settings.json` 文件中切换 credit 设置：

```json
{
    "useG1Credits": true
}
```

*   **使用 AI Credits 选项**：运行 `/config` 或 `/settings` 打开 CLI 设置面板。将 **Use G1 Credits** 字段设置为 **on**，以允许 CLI 在套餐配额耗尽时使用您的个人 credits，或将其设置为 **off** 以限制回退计费。（了解更多信息，请参阅 **[Plans](/docs/plans#overages)** 超额部分）。

## 另请参阅

*   **[AI Credits 命令](/docs/cli/commands/credits)**：在 TUI 中交互式查看和管理您的 credits。
*   **[模型配额命令](/docs/cli/commands/usage)**：监控您针对特定模型的 API 配额。