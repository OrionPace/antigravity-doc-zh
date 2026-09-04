# Vim 编辑器模式（Vim editor mode）

使用模态 Vim keybindings 编辑 prompt，替代默认的普通平面文本编辑器。

Vim 编辑器模式取代了 CLI 中每个多行输入区域的编辑模型：

| 输入区域 | 在该区域中编辑的内容 |
| :-- | :-- |
| Prompt 输入框 | 发送给 agent 的消息，包括多行 prompt 和 slash command。 |
| [`/diff`](/docs/cli/commands/diff) 中的评审评论编辑器 | 你在发生变更的文件上留下的评审意见。 |
| Artifact 评审面板中的评论编辑器 | 在接受生成的 [artifact](/docs/cli/artifacts) 之前对其提出的反馈。 |

它还会在帮助浮层中添加一个 `vim` 标签页，并在 [statusline（状态行）](/docs/cli/statusline) 中添加一个模式徽章。

## 启用 Vim 编辑器模式

Vim 编辑器模式默认处于关闭状态。可以从交互式设置面板中开启，或直接在 `settings.json` 中启用。

### 使用设置面板

1.  在 prompt 面板内键入 `/settings` 并按 `Enter`。
2.  使用 `↑`/`↓` 导航至 **Editor Mode**。
3.  按 `Enter` 选择 `vim`。
4.  设置 **Editor Mode › Insert First** 以选择每个 prompt 启动时处于哪个模式。保持 `off` 从 Normal 模式启动，或设置为 `on` 从 Insert 模式启动并可通过单纯按 `Enter` 提交。请参阅 [在 Insert 模式下启动](#在-insert-模式下启动)。
5.  按 `Esc` 保存并关闭编辑器。

### 使用 `settings.json`

在你的配置文件中设置 `editorMode`：

```json
{
    "editorMode": "vim",
    "vimInsertFirst": false
}
```

CLI 在启动时会从 `~/.gemini/antigravity-cli/settings.json` 加载此文件。`editorMode` 接受 `"default"` 和 `"vim"`。`vimInsertFirst` 控制每个新 prompt 从哪个模式启动，仅在 `editorMode` 为 `"vim"` 时生效；请参阅 [在 Insert 模式下启动](#在-insert-模式下启动)。

> [!NOTE]
> `editorMode` 与 [`editor` 设置](/docs/cli/settings) 无关。`editor` 用于选取按 `Ctrl+G` 启动的外部程序，因此将 `editor` 设置为 `"vim"` 会在单独窗口中打开 Vim，对 prompt 本身没有任何影响。而 `editorMode` 才是控制 CLI prompt 输入框内部模态编辑的设置项。

## 模式切换

Vim 编辑器模式启动时处于 NORMAL 模式。按 `i` 开始输入，按 `Esc` 返回 NORMAL 模式。

| 命令 | 操作 | 来源模式 |
| :-- | :-- | :-- |
| `Esc`, `Ctrl+C` | 进入 NORMAL 模式 | INSERT, VISUAL |
| `i` | 在光标前插入 | NORMAL |
| `I` | 在行首第一个非空白字符处插入 | NORMAL |
| `a` | 在光标后插入 | NORMAL |
| `A` | 在行尾插入 | NORMAL |
| `o` | 在下方新开一行并插入 | NORMAL |
| `O` | 在上方新开一行并插入 | NORMAL |
| `v` | 启动字符级选择 | NORMAL |
| `V` | 启动行级选择 | NORMAL |

状态行会报告当前模式：

| 模式 | 徽章标记 |
| :-- | :-- |
| NORMAL | 无 |
| INSERT | `-- INSERT --` |
| VISUAL | `-- VISUAL --` |
| VISUAL LINE | `-- V-LINE --` |

徽章区域为空意味着你当前处于 NORMAL 模式。如果你运行了[自定义状态行](#在自定义状态行中显示模式)，除非将其与默认状态行堆叠，否则它将替换此徽章。

> [!TIP]
> 在 NORMAL 模式下按 `?` 可打开快捷键浮层，或运行 `/help` 并选择 `vim` 标签页以查看完整的速查表。

## 提交 prompt

Enter 在每个模式下的行为各不相同，因此你可以编写多行 prompt 而不会发生意外提交。

| 场景上下文 | `Enter` | `Ctrl+S` / `Ctrl+Enter` | `ZZ` |
| :-- | :-- | :-- | :-- |
| NORMAL 模式 | 提交 | 提交 | 提交 |
| INSERT 模式 | 插入换行 | 提交 | — |
| INSERT 模式，insert-first 开启 | 提交 | 提交 | — |

`ZZ` 在 NORMAL 和 VISUAL 模式下均可提交，符合写入并退出缓冲区的肌肉记忆。

### 在 Insert 模式下启动

当你希望每个新 prompt 都在 INSERT 模式下开始，且按单纯的 `Enter` 即可提交时，请设置 `vimInsertFirst`。这既保留了默认的打字体验，又保留了只需一次 `Esc` 即可进入 NORMAL 模式的便利。

```json
{
    "editorMode": "vim",
    "vimInsertFirst": true
}
```

**Editor Mode › Insert First** 选项仅在 Editor Mode 设置为 `vim` 时才会出现在 `/settings` 中。在默认模式下该选项不起作用。

## 光标移动

所有光标移动命令（motion）在 NORMAL 和 VISUAL 模式下均可单独使用，也可作为操作符（operator）的目标范围。

| 按键 | 移动操作 |
| :-- | :-- |
| `h` `l` | 左、右 |
| `j` `k` | 下、上 |
| `0` `$` | 行首、行尾 |
| `^` | 行内第一个非空白字符 |
| `w` `b` `e` | 下一个单词、上一个单词、词尾 |
| `W` `B` `E` | 同上，将空格分隔的文本块视为单词 |
| `gg` `G` | 输入内容起始、输入内容末尾 |
| `f{char}` `F{char}` | 跳转到下一个或上一个 `{char}` 字符上 |
| `t{char}` `T{char}` | 停在下一个或上一个 `{char}` 字符的前一个字符处 |
| `;` `,` | 正向、反向重复上一次 `f`/`F`/`t`/`T` 操作 |

## 编辑文本

编辑命令分为三类：立即生效的单键命令、等待 motion 的操作符（operator），以及选择定界区域的文本对象（text object）。

### 单键命令

| 按键 | 操作 |
| :-- | :-- |
| `x` | 删除光标下的字符 |
| `r{char}` | 将光标下的字符替换为 `{char}` |
| `D` `C` | 从光标处删除或更改至行尾 |
| `o` `O` | 在下方或上方新开一行并进入 INSERT 模式 |
| `p` `P` | 粘贴在光标之后或光标之前 |
| `u` `U` | 撤销（undo）、重做（redo）。`Ctrl+R` 不执行重做，而是打开 artifact 审核 |

命令不接受数字计数前缀（count prefix），因此 `3dd` 只会删除一行。若要一次性操作多行，请使用 `V` 选中它们后按操作符。同样也不支持使用 `.` 重复上一次更改。

系统提供了一个未命名寄存器（unnamed register），而非通常的 `"a`–`"z` 寄存器组。删除操作会填充该寄存器，因此 `x`、`D`、`C`、`d` 和 `c` 留下的文本均可通过 `p` 粘贴回来。

粘贴具有行感知能力（linewise-aware）。使用 `dd` 或 `yy` 复制（yank）的文本会粘贴到下方的新行（`p`）或上方的新行（`P`）。其他内容则按行内（inline）方式粘贴。

### 操作符与移动（Operators and motions）

将操作符与任意 motion 结合使用，即可作用于其覆盖的跨度范围。

| 操作符 | 操作 | 单词形式 | 整行 |
| :-- | :-- | :-- | :-- |
| `d` | 删除（Delete） | `dw` `de` `db` | `dd` |
| `c` | 更改（Change，删除后进入 INSERT 模式） | `cw` `ce` `cb` | `cc` |
| `y` | 复制（Yank） | `yw` `ye` `yb` | `yy` |

```
dw     删除到下一个单词的开头
d$     删除到行尾
c^     更改回第一个非空白字符
yG     复制到输入内容末尾
dfx    正向删除直到并包含下一个 "x"
```

`cw` 会更改到当前单词的末尾，与原生 Vim 的行为保持一致。

### 文本对象（Text objects）

将操作符与 `i`（内部，inside）或 `a`（环绕，around）以及界定符配对。

| 文本对象 | 选择范围 |
| :-- | :-- |
| `iw` `aw` | 一个单词，不含/包含周围空格 |
| `iW` `aW` | 空格分隔的文本块 |
| `i"` `a"` `i'` `a'` | 单引号或双引号内的文本 |
| `i(` `a(` `i)` `a)` | 圆括号内的文本 |
| `i[` `a[` `i]` `a]` | 方括号内的文本 |
| `i{` `a{` `i}` `a}` | 花括号内的文本 |

反引号用法相同：将 `i` 或 `a` 与反引号配对即可选择行内代码。

```
ci"    更改最近引号内的文本
da(    删除括号组（包含圆括号在内）
yiw    复制光标下的单词
```

## 使用选区

按 `v` 或 `V` 开启选择，使用任意 motion 移动，然后应用命令。再次按 `v`、`V` 或按 `Esc` 即可退出选区。

| 按键 | 对选区的操作 |
| :-- | :-- |
| `d` `x` | 删除 |
| `c` | 更改 |
| `y` | 复制（Yank） |
| `r{char}` | 将选中的每个字符替换为 `{char}` |
| `~` | 切换大小写 |
| `u` `U` | 转换为小写、转换为大写 |

> [!NOTE]
> `~`、`u` 和 `U` 仅在 VISUAL 模式下更改大小写。在 NORMAL 模式下，`u` 和 `U` 分别代表撤销与重做。

## 运行 slash 命令与 shell 命令

在 NORMAL 模式下按 `/` 或 `!`。CLI 会插入该字符并自动切换到 INSERT 模式，因此无需先按 `i` 即可直接使用 slash command 和 shell 命令。

```
/settings     从 NORMAL 模式打开设置面板
!ls -la       从 NORMAL 模式运行 shell 命令
```

## 自定义提交与换行键

可以在 `~/.gemini/antigravity-cli/keybindings.json` 中重新映射三种 Vim 操作。以下是默认设置：

```json
{
    "vim.insert.insert_newline": ["alt+enter", "ctrl+j", "enter", "shift+enter"],
    "vim.insert.submit": ["ctrl+enter", "ctrl+s"],
    "vim.normal.submit": ["ctrl+enter", "ctrl+s"]
}
```

Motion、操作符和文本对象是固定的，无法重新映射。

### 仅在 NORMAL 模式下使用 Enter 提交

这是默认行为。`Enter` 在 NORMAL 模式下提交，在 INSERT 模式下插入换行，因此你可以自由输入并通过简单的 `Esc` `Enter` 组合键进行提交。无需额外配置，保持 `vimInsertFirst` 为 `off` 即可：

```json
{
    "editorMode": "vim",
    "vimInsertFirst": false
}
```

### 在 INSERT 模式下也使用 Enter 提交

将 `enter` 从 `vim.insert.insert_newline` 移至 `vim.insert.submit`。此时 `Shift+Enter`、`Alt+Enter` 和 `Ctrl+J` 仍可用于插入换行：

```json
{
    "vim.insert.insert_newline": ["alt+enter", "ctrl+j", "shift+enter"],
    "vim.insert.submit": ["ctrl+enter", "ctrl+s", "enter"]
}
```

将 `vimInsertFirst` 设置为 `true` 无需编辑 keybindings 即可实现相同的提交行为，但它同时也会改变每个新 prompt 开始时所处的模式。

> [!WARNING]
> `Enter` 在 NORMAL 模式下始终执行提交。重新映射 `vim.normal.submit` 只能增加按键，永远无法移除 `Enter`。

## 在自定义状态行中显示模式

[自定义状态行](/docs/cli/statusline) 会替换内置状态行，模式徽章也会随之消失。你有两种方法可以找回模式显示。

保留内置状态行，并将你的脚本堆叠在下方：

```json
{
    "statusLine": {
        "type": "command",
        "command": "~/.gemini/antigravity-cli/statusline.sh",
        "stack_with_default": true
    }
}
```

或者自行渲染模式。当 `editorMode` 为 `"vim"` 时，传递给你脚本的 JSON payload 会携带一个 `vim` 对象：

```json
{
    "vim": {
        "mode": "INSERT"
    }
}
```

`mode` 的取值为 `NORMAL`、`INSERT`、`VISUAL` 或 `VISUAL LINE`。当 Vim 编辑器模式关闭时，该字段完全不存在，因此脚本可以将该字段的存在与否作为启用判断依据：

```bash
#!/bin/bash
input=$(cat)
mode=$(echo "$input" | jq -r '.vim.mode // empty')
[ -n "$mode" ] && printf -- '-- %s -- ' "$mode"
echo "$input" | jq -r '.model.display_name'
```

> [!NOTE]
> `vim.mode` 会如实报告 `NORMAL`，这与内置徽章不同——内置徽章在该模式下不渲染任何内容。打印所有模式的脚本将显示内置状态行从不显示的 `-- NORMAL --` 徽章。

## 后续步骤

*   **[设置、渲染与 Keybindings](/docs/cli/settings)**：配置其余偏好设置并重新映射按键。
*   **[状态行定制](/docs/cli/statusline)**：控制状态行与 Vim 模式徽章一同展示的内容。
*   **[CLI 参考手册](/docs/cli/reference)**：查阅每个配置键与默认 keybindings。