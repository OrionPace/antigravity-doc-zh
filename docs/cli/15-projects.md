# 项目（Projects）

在 Antigravity CLI 中管理项目并组织会话 session。

## 启动带项目的会话

### 1. 默认项目执行

在不带任何项目 flag 启动 CLI 时，会话中的所有 conversation（对话）都将位于 `default-cli-project` 中：

```bash
agy
```

### 2. 在指定项目中打开会话

如果你想打开附加到特定现有项目的会话，请传递带目标项目 ID 的 `--project` 参数：

```bash
agy --project=<project_id>
```

### 3. 启动时创建新项目

如果你想创建一个全新项目并在其中初始化 CLI 会话，请传递 `--new-project` 参数：

```bash
agy --new-project
```

### 4. 恢复现有对话

如果你恢复一个对话（无论是在启动时通过 `--conversation=<conv_id>` 还是在会话期间使用 `/resume`），都会自动使用该对话关联的项目。

## 在项目之间转移对话（`/fork`）

在当前活跃的会话中交互时，你可以使用 `/fork` 这个 slash command 将当前对话复制并延续到一个不同的项目中：

```
/fork <project_id>
```

执行后，CLI 会 fork（分叉）你当前的对话，并将新创建的对话与 `<project_id>` 关联。