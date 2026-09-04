# Permissions 命令 (/permissions)

在 TUI（终端界面）内以交互方式管理细粒度的 agent 权限 rule（规则）。

## 概述

Antigravity CLI 使用细粒度权限引擎来保障你的工作站安全。虽然你可以在配置文件中手动配置这些 rule，但 `/permissions` 命令会打开一个交互式的 **Permissions Manager**（权限管理器）TUI 面板，以便实时查看、添加、编辑和删除 rule。

有关权限引擎的工作机制、支持的 action 类型以及手动配置的详细信息，请参阅概念指南 **[Permissions Guide](/docs/cli/permissions)**。

## 交互式管理权限

打开 Permissions Manager：

1. 在 prompt 输入框中输入 `/permissions`。
2. 按 Enter 键。

```
/permissions
```

### 导航与快捷键控制

Permissions Manager 包含三个面板：

1. **Scope Picker**（作用域选择器）：选择要编辑的配置作用域（scope）：
    
    * **Project**：仅适用于当前活跃项目的 rule（如果未打开任何项目则处于禁用状态）。
    * **Shared**：在所有 Antigravity 产品间共享的 rule。
    * **Global**：适用于所有会话的全局 rule。
    
    使用 ↑/↓（或 J/K）导航，按 Enter 选中，按 Esc 退出。
    
2. **Rule Viewer**（Rule 查看器）：查看针对所选作用域配置的 rule。
    
    * 使用 ←/→（或 Tab）在 **allowlist**（允许列表）、**denylist**（拒绝列表）和 **asklist**（询问列表）标签页之间切换。
    * 使用 ↑/↓（或 J/K）滚动浏览各个 rule。
    * 按 A 添加新 rule。
    * 按 E（或 Ctrl + G）编辑高亮选中的 rule。
    * 按 D（或 Backspace）删除高亮选中的 rule。
    * 按 Esc 返回 Scope Picker。
3. **Add/Edit Rule**（添加/编辑 Rule）：在输入框中输入或编辑 rule。
    
    * rule 必须遵循 `action(target)` 格式（例如：`command(git)`）。
    * 按 Enter 验证并保存 rule。
    * 按 Esc 取消。

* * *

## 分步操作指南

以下介绍了如何在 TUI 中实时查看、添加、编辑和删除 rule。

### 1. 选择作用域并查看 Rule

当你运行 `/permissions` 时，首先会看到 **Scope Picker**。选择 **Global** 以管理你的全局 rule：

![选择 Global 作用域](/assets/image/docs/cli/permissions-scope.png)

按 Enter 键打开所选作用域的 **Rule Viewer**。你可以使用 ←/→ 在 **allow**、**deny** 和 **ask** 标签页之间切换：

![Global Rule 查看器](/assets/image/docs/cli/permissions-viewer.png)

### 2. 添加权限 Rule

若要允许 agent 自动运行 `git` 命令而无需 prompt 提示确认：

1. 在 Rule Viewer 中按 A。底部的 **Add Rule** 面板随即展开：
    
    ![Add Rule 面板](/assets/image/docs/cli/permissions-add.png)
    
2. 在输入框中输入 `command(git)`：
    
    ![输入 Rule](/assets/image/docs/cli/permissions-add-typed.png)
    
3. 按 Enter 键。该 rule 会被校验并保存。你将返回 Rule Viewer，此时 `command(git)` 已显示在你的 allowlist 中：
    
    ![Rule 保存成功](/assets/image/docs/cli/permissions-viewer-with-rule.png)
    

### 3. 编辑权限 Rule

如果你想限制 agent 仅能自动运行 `git diff`，可以编辑该 rule：

1. 在 Rule Viewer 中，使用 ↑/↓ 高亮选中 `command(git)`。
2. 按 E（或 Ctrl + G）。输入面板打开，并预填了 `command(git)`。
3. 将文本修改为 `command(git diff)`。
4. 按 Enter 键保存。旧 rule 将被新 rule 替换。

### 4. 删除权限 Rule

若要移除某项 rule 并恢复对这些操作的手动 prompt 确认：

1. 在 Rule Viewer 中，高亮选中你想删除的 rule（例如 `command(git diff)`）。
2. 按 D（或 Backspace）。
3. 该 rule 会立即从列表中移除。

## 下一步

* **[Permissions Guide](/docs/cli/permissions)**：了解安全模型、action 类型以及通配符匹配。
* **[Sandbox & Security](/docs/cli/sandbox)**：配置用于执行命令的操作系统原生 sandbox（沙箱）容器。
* **[CLI Reference](/docs/cli/reference)**：查看所有可用的 Slash Commands 和快捷键绑定。