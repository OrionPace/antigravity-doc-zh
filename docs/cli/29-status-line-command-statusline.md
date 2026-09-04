# Status Line 命令 (/statusline)

切换 TUI statusline（状态行）的显示状态或配置自定义渲染命令。

## 概述

`/statusline` 命令允许你快速启用或禁用 TUI 底部的 statusline（状态行），或者配置自定义 shell 命令对其进行动态渲染，而无需手动编辑配置文件。

有关如何编写自定义 statusline 脚本以及 JSON 状态载荷（state payload）架构的详细信息，请参阅概念指南 **[Status Line Customization Guide](/docs/cli/statusline)**。

## 使用方法

通过传入以下参数运行 `/statusline` 命令以控制其行为：

### 切换 Status Line 显示状态

输入不带任何参数的 `/statusline` 可在开启和关闭状态之间切换 statusline：

```
/statusline
```

### 显式启用或禁用

你可以显式启用或禁用 statusline：

* **Enable（启用）**：`/statusline on` 或 `/statusline enable`
* **Disable（禁用）**：`/statusline off` 或 `/statusline disable`

```
/statusline off
```

### 配置自定义命令

若要将 agent 状态的 JSON 载荷路由到自定义脚本并在 statusline 中渲染其输出，请将命令作为参数传入：

```
/statusline ~/.gemini/antigravity-cli/statusline.sh
```

这会立即更新你的设置，并开始运行该脚本以渲染 statusline。

### 恢复为默认设置

若要删除自定义命令配置并恢复使用内置默认的 statusline：

```
/statusline delete
```

*（注意：也支持使用 `/statusline reset`）。*

### 查看帮助信息

查看快捷命令参考信息：

```
/statusline help
```

## 下一步

* **[Status Line Guide](/docs/cli/statusline)**：学习如何编写自定义脚本并处理 JSON 载荷。
* **[Window Title Command](/docs/cli/commands/title)**：配置动态终端窗口标题。
* **[CLI Reference](/docs/cli/reference)**：查看所有可用的 Slash Commands。