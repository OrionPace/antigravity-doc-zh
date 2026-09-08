# Headless 模式

以非交互方式运行 Antigravity CLI，用于脚本化 agent 任务、集成 CI 流水线，并捕获机器可读的输出。

Headless 模式（也称为 print 模式）向 agent 发送单个 prompt，流式传输或返回响应，然后退出。当你需要在程序中而非终端界面中获取 agent 的输出时，请使用此模式。

## 运行单个 prompt

使用 `-p`（或其别名 `--print` 和 `--prompt`）传入 prompt，即可运行一次并退出：

```
agy -p "In one sentence, what is a git rebase?"
```

```
A git rebase rewrites the commit history by transplanting a sequence of commits onto a new base commit, imposing a strictly linear progression of changes that eliminates arbitrary merge artifacts.
```

响应输出到 `stdout`。诊断信息——错误、身份验证提示、进度和权限通知——输出到 `stderr`。这种分离方式可确保捕获的响应保持干净：

```
# 仅捕获模型响应；诊断信息仍打印到终端。
answer=$(agy -p "Name three popular version control systems, comma-separated.")
```

> **注意：** Headless 模式使用你缓存的凭据。请先通过交互式 `agy` 会话完成一次身份验证。在无终端的非交互环境中（例如 CI），未完成身份验证的运行会以 `authentication required` 错误退出，而不会挂起。

## 输出格式

`--output-format` 标志控制 `stdout` 的形态。它接受三个值：

| 格式 | `stdout` 形态 | 适用场景 |
| --- | --- | --- |
| `text` | 响应文本（默认） | 人类可读的输出、快速脚本 |
| `json` | 完成时打印一个 JSON 对象 | 捕获结果及元数据 |
| `stream-json` | 换行分隔的 JSON（NDJSON）事件 | 监控进度、工具和 token 用量 |

### 文本

默认格式。响应文本直接输出到 `stdout`，无任何包装：

```
agy -p "In one sentence, what does the command git bisect do?"
```

```
Git bisect executes a binary search algorithm across a project's commit history to rapidly isolate the precise commit responsible for introducing a defect.
```

### JSON

设置 `--output-format json` 可在运行完成后获取单个 JSON 信封。CLI 将其输出为一行；可通过管道传递给 `jq` 进行美化打印：

```
agy -p "In one sentence, what is a git rebase?" --output-format json | jq
```

```
{
  "conversation_id": "055a398f-db14-4c5f-abbb-1bf03f8120a7",
  "status": "SUCCESS",
  "response": "A git rebase rewrites the commit history by transplanting a sequence of commits onto a new base commit, imposing a strictly linear progression of changes that eliminates arbitrary merge artifacts.\n",
  "duration_seconds": 7.16,
  "num_turns": 1,
  "usage": {
    "input_tokens": 10415,
    "output_tokens": 657,
    "thinking_tokens": 616,
    "cache_read_tokens": 8113,
    "total_tokens": 11072
  }
}
```

该信封包含以下字段：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `conversation_id` | string | 会话 ID，用于后续恢复 |
| `status` | string | 终止状态（参见 [状态值](#状态值)） |
| `response` | string | agent 的自由文本响应 |
| `error` | string | 错误消息；仅在失败时出现 |
| `duration_seconds` | number | 运行的墙钟时长 |
| `num_turns` | number | 会话中的用户 turn 数量 |
| `structured_output` | object | 解析后的 schema 输出；仅在指定 `--json-schema` 时出现 |
| `json_schema` | object | 被强制执行的 schema；仅在指定 `--json-schema` 时出现 |
| `usage` | object | token 计数：`input_tokens`、`output_tokens`、`thinking_tokens`、`cache_read_tokens`、`total_tokens` |

#### 使用 schema 的结构化输出

传入 `--json-schema` 可将答案约束到某个 schema。解析后的对象出现在 `structured_output` 中，而 `response` 则包含序列化为字符串的相同负载：

```
agy -p "Parse the semantic version string v2.14.3 into an object with integer fields major, minor, and patch." \
  --output-format json \
  --json-schema '{"type":"object","properties":{"major":{"type":"integer"},"minor":{"type":"integer"},"patch":{"type":"integer"}},"required":["major","minor","patch"]}' | jq
```

```
{
  "conversation_id": "4e502687-290c-4030-b908-5ed6c68fa5dc",
  "status": "SUCCESS",
  "response": "{\"major\":2,\"minor\":14,\"patch\":3}\n",
  "duration_seconds": 4.45,
  "num_turns": 1,
  "structured_output": { "major": 2, "minor": 14, "patch": 3 },
  "json_schema": {
    "type": "object",
    "properties": {
      "major": { "type": "integer" },
      "minor": { "type": "integer" },
      "patch": { "type": "integer" }
    },
    "required": ["major", "minor", "patch"]
  },
  "usage": { "input_tokens": 10522, "output_tokens": 354, "thinking_tokens": 329, "cache_read_tokens": 8112, "total_tokens": 10876 }
}
```

该标志接受 schema 字符串、`.json` schema 文件的路径，或原始类型名称（`string`、`number`、`integer`、`boolean`）。从 `structured_output` 中读取解析后的值：

```
agy -p "Parse the semantic version string v2.14.3 into an object with integer fields major, minor, and patch." \
  --output-format json \
  --json-schema '{"type":"object","properties":{"major":{"type":"integer"},"minor":{"type":"integer"},"patch":{"type":"integer"}},"required":["major","minor","patch"]}' \
  | jq '.structured_output'
```

### 流式 JSON

设置 `--output-format stream-json` 可在运行过程中逐行输出 JSON 对象（NDJSON）。使用此格式可实时观察 tool call 和 token 用量。

```
agy -p "In one sentence, what is a git rebase?" --output-format stream-json
```

流以一个 `init` 事件开始，随后是任意数量的 `step_update` 事件，最后恰好以一个 `result` 事件结束（下文中的 `cwd` 和 `tools` 数组已做省略）：

```
{"event":"init","conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","init":{"cwd":"/home/user/project","tools":["ask_permission","run_command","write_to_file","..."],"permission_mode":"request-review"}}
{"event":"step_update","step_update":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","step_index":0,"state":"DONE","step_type":"user_input"}}
{"event":"step_update","step_update":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","step_index":3,"state":"DONE","step_type":"agent_response","text_delta":"Git rebase destructively rewrites a branch's commit history by systematically detaching its unique commits and sequentially reapplying them onto a new base commit.\n","duration_seconds":6.28,"usage":{"input_tokens":10302,"output_tokens":582,"thinking_tokens":551,"cache_read_tokens":8113,"total_tokens":10884}}}
{"event":"step_update","step_update":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","step_index":4,"state":"DONE","step_type":"checkpoint","duration_seconds":0.53,"usage":{"input_tokens":116,"output_tokens":7,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":123}}}
{"event":"result","result":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","status":"SUCCESS","response":"Git rebase destructively rewrites a branch's commit history by systematically detaching its unique commits and sequentially reapplying them onto a new base commit.\n","duration_seconds":6.88,"num_turns":1,"usage":{"input_tokens":10418,"output_tokens":589,"thinking_tokens":551,"cache_read_tokens":8113,"total_tokens":11007}}}
```

当响应分块流式传输时，`agent_response` step 会在最终 `DONE` 之前发出一个或多个携带部分 `text_delta` 片段的 `ACTIVE` 事件；像本例这样的短响应会在单个 `DONE` 中到达。

每一行都是一个事件对象，其 `event` 字段标识其类型：

| `event` | 负载键 | 发出时机 |
| --- | --- | --- |
| `init` | `init` | 流开始时，一次 |
| `step_update` | `step_update` | 每个 step 转换或文本增量时 |
| `result` | `result` | 结束时，一次（与 `json` 形态相同） |

`init` 负载记录运行配置。`model` 和 `agent` 仅在通过 `--model` 或 `--agent` 设置时出现；`permission_mode` 默认为 `request-review`（在 `--dangerously-skip-permissions` 下为 `always-proceed`）：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `cwd` | string | 工作目录 |
| `tools` | string\[\] | 所有可用工具的名称 |
| `permission_mode` | string | 生效的权限模式 |
| `model` | string | 正在使用的模型（当被覆盖时） |
| `agent` | string | 当前 agent（当被覆盖时） |
| `json_schema` | object | 被强制执行的 schema（当通过 `--json-schema` 设置时） |

每个 `step_update` 负载描述一个 step。已观察到的 `step_type` 值包括 `user_input`、`agent_response`、`tool` 和 `checkpoint`；`state` 在 step 运行时为 `ACTIVE`，完成时为 `DONE`：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `conversation_id` | string | 会话 ID |
| `step_index` | number | step 的从零开始的索引 |
| `state` | string | `ACTIVE` 或 `DONE` |
| `step_type` | string | step 类别，例如 `agent_response` 或 `tool` |
| `tool_name` | string | 工具步骤上的规范工具名称 |
| `text_delta` | string | 增量响应文本 |
| `duration_seconds` | number | step 时长（已知时） |
| `usage` | object | 每个 step 的 token 用量（已知时） |
| `tool_info` | object | tool 调用详情（见下文） |
| `subagent_info` | object | subagent 调用详情 |

#### 流中的 tool call

在工具步骤上，`tool_info` 携带调用及其结果。这是来自执行了 `echo hello_headless_demo` 的运行的真实工具步骤：

```
{"event":"step_update","step_update":{"conversation_id":"edb1c8c1-50ba-4f3f-87eb-412d0e9d47c3","step_index":4,"state":"DONE","step_type":"tool","tool_name":"run_command","duration_seconds":0.07,"tool_info":{"name":"run_command","parameters":{"CommandLine":"echo hello_headless_demo"},"output":"hello_headless_demo\r\n"}}}
```

`tool_info` 包含 `name`、`parameters`、`output`，以及——当工具失败时——一个包含 `type` 和 `message` 的 `error` 对象。生成 subagent 的步骤则携带 `subagent_info`，在 `subagents` 下列出每个 subagent（包含 `type_name`、`role`、`conversation_id`、`log_uri` 和 `workspace_uris`）。

#### 流中的结构化输出

使用 `--json-schema` 时，schema 适用于最终的 `result` 事件，该事件携带与 `json` 信封相同的 `structured_output` 和 `json_schema` 字段。

## 使用 jq 解析输出

`stdout` 是机器可读的，因此 `jq` 可以精确提取你所需的内容。

从 JSON 运行中获取响应文本：

```
agy -p "Name three popular version control systems, comma-separated." --output-format json | jq -r '.response'
```

```
Git, Subversion, Mercurial.
```

按到达顺序拼接流式文本：

```
agy -p "Explain what a merge conflict is in two sentences." --output-format stream-json \
  | jq -j 'select(.event=="step_update") | .step_update.text_delta // empty'
```

从最终的 `result` 事件中读取 token 用量：

```
agy -p "In one sentence, what is a git rebase?" --output-format stream-json \
  | jq 'select(.event=="result") | .result.usage'
```

> **提示：** 拼接 `text_delta` 片段时使用 `jq -j`（连接输出），这样 `jq` 不会在片段之间插入换行符。

## 继续会话

Headless 运行默认是无状态的。使用 `--continue`（`-c`）恢复最近的会话，或使用 `--conversation` 并传入先前运行中的 `conversation_id` 来恢复特定会话：

```
# 继续最近的会话。
agy -p "Now explain your previous answer in more detail" --continue

# 按 ID 恢复特定会话。
agy -p "Summarize what we discussed" --conversation 055a398f-db14-4c5f-abbb-1bf03f8120a7
```

上述每种方式都会启动一个新进程。要在单个进程内运行多个 turn，请参阅 [从 stdin 流式传输 prompts](#从-stdin-流式传输-prompts)。

## 从 stdin 流式传输 prompts

使用 `--input-format stream-json` 可维持单个、连续的会话进程，通过标准输入（stdin）逐个向其提供 prompts。每个 prompt 执行一个完整的 turn 并发出自己的 `result` 事件。

这种方法非常适合需要根据前一个答案动态确定下一个 prompt 的应用程序。由于进程只启动一次，后续 turn 可跳过启动开销并复用已预热（warm-up）的会话。这比使用 `--continue` 重复运行命令要快得多。

> **注意：** `--input-format stream-json` 要求配合 `--output-format stream-json`。在流式会话中，CLI 每个 turn 恰好发出一个 `result` 事件。

### 发送 prompt

向 `stdin` 逐行写入 JSON 对象。`event` 键指定消息类型（与输出流格式一致）。prompt 以包含 `message` 的 `user` 事件表示：

```
{ "event": "user", "message": { "content": "Reply with exactly the word: apple. Nothing else." } }
```

你可以将多个 prompts 通过管道传入单个会话：

```
printf '%s\n' \
  '{"event":"user","message":{"content":"Reply with exactly the word: apple. Nothing else."}}' \
  '{"event":"user","message":{"content":"What word did I ask you to reply with in my previous message? Answer with just that word."}}' \
  | agy --input-format stream-json --output-format stream-json
```

`content` 字段接受标准字符串或文本块列表。以下两种格式等价：

```
{ "event": "user", "message": { "content": "Reply with exactly: banana" } }
{ "event": "user", "message": { "content": [{ "type": "text", "text": "Reply with exactly: banana" }] } }
```

`text` 是唯一支持的块类型。提交任何其他块类型都会以错误消息结束会话，而不是静默丢弃该块。这确保了 agent 永远不会回答你未明确发送的 prompt。

### 读取结果

输出流的工作方式如下：

1.  以单个 `init` 事件开始。
    
2.  为当前 turn 发出一系列 `step_update` 事件。
    
3.  以最终的 `result` 事件结束该 turn。
    

以下示例展示了上述两个 prompt 的 bash 命令的输出（`init` 负载已做省略）：

```
{"event":"init","conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","init":{"cwd":"/home/user/project","tools":["ask_permission","run_command","write_to_file","..."],"permission_mode":"request-review"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":0,"state":"DONE","step_type":"user_input"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":2,"state":"ACTIVE","step_type":"agent_response","text_delta":"apple"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":2,"state":"DONE","step_type":"agent_response","text_delta":"\n","duration_seconds":1.169607627,"usage":{"input_tokens":30384,"output_tokens":4,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":30388}}}
{"event":"result","result":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","status":"SUCCESS","response":"apple\n","duration_seconds":1.427806958,"num_turns":1,"usage":{"input_tokens":30384,"output_tokens":4,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":30388}}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":3,"state":"DONE","step_type":"user_input"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":4,"state":"DONE","step_type":"agent_response","text_delta":"apple\n","duration_seconds":0.895679386,"usage":{"input_tokens":278,"output_tokens":4,"thinking_tokens":0,"cache_read_tokens":30214,"total_tokens":282}}}
{"event":"result","result":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","status":"SUCCESS","response":"apple\n","duration_seconds":2.548755756,"num_turns":2,"usage":{"input_tokens":30662,"output_tokens":8,"thinking_tokens":0,"cache_read_tokens":30214,"total_tokens":30670}}}
```

第二个 turn 从第一个 turn 的上下文中回答了 `apple`。请注意，单个 `conversation_id` 跟踪整个会话，且 `init` 只发送一次。

在解析 result 对象时，请记住响应文本仅适用于当前 turn，而元数据计数器则跟踪累计的会话：

| 字段 | 范围 |
| --- | --- |
| `response` | 发出它的那个 turn |
| `num_turns` | 会话累计 |
| `usage` | 会话累计 |
| `duration_seconds` | 会话累计 |

要过滤并仅查看最终响应，你可以将输出通过管道传递给 `jq`：

```
printf '%s\n' \
  '{"event":"user","message":{"content":"Reply with exactly: one"}}' \
  '{"event":"user","message":{"content":"Reply with exactly: two"}}' \
  | agy --input-format stream-json --output-format stream-json \
  | jq -r 'select(.event=="result") | "\(.result.num_turns): \(.result.response)"'
```

```
1: one

2: two
```

### 以编程方式驱动会话

你可以不在开始时传入所有 prompts，而是在脚本中保持 `stdin` 管道打开。这样你的应用程序可以在提交下一个 prompt 之前评估模型的答案。

> **提示：** 你可以逐行读取 `stdout`，并根据 `event` 字段分发逻辑。在写入下一个 prompt 之前，请等待收到当前 prompt 的 `result` 事件。

例如：

```
import json
import subprocess

proc = subprocess.Popen(
    ["agy", "--input-format", "stream-json", "--output-format", "stream-json"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1,
)


def ask(prompt):
    """发送一个 prompt 并返回该 turn 的响应。"""
    message = {"event": "user", "message": {"content": prompt}}
    proc.stdin.write(json.dumps(message) + "\n")
    proc.stdin.flush()
    for line in proc.stdout:
        event = json.loads(line)
        if event["event"] == "result":
            return event["result"]["response"]


first = ask("Name one popular version control system. Answer with one word.")
print(ask(f"Name a competitor to {first.strip()}. Answer with one word."))

proc.stdin.close()
proc.wait()
```

### 结束会话

要优雅地结束会话，只需关闭 `stdin`。进程会在输入管道关闭且当前 turn 完成后退出。如果应用程序写入最后一个 prompt 后立即关闭管道，它仍会在进程终止前收到最终的 `result`。

干净的会话以 `0` 退出，这与标准 headless 模式行为一致。

### 不支持的消息

为防止不可预测的行为，CLI 会验证输入。如果遇到格式错误或不支持的消息，它会按下表所述进行响应：

| 输入 | 结果 | 退出码 |
| --- | --- | --- |
| 无法识别的 `event` 名称 | 跳过：警告记录到 `stderr` | — |
| `control_request` 或 `control_response` 事件 | `ERROR` 结果，会话结束 | `2` |
| 由 CLI 处理的斜杠命令，如 `/model` | `ERROR` 结果，会话结束 | `2` |
| 缺少 `event` 字段的消息 | `ERROR` 结果，会话结束 | `1` |
| 无效的 JSON 行 | `ERROR` 结果，会话结束 | `1` |
| `text` 以外的内容块类型 | `ERROR` 结果，会话结束 | `1` |

无法识别的 `event` 名称会被安全跳过并附带警告。这确保了针对更新版本流式协议构建的应用程序在旧版 CLI 上运行时不会崩溃：

```
warning: ignoring unsupported stream input message event "future_thing"
```

对于所有其他错误，会话会立即终止。之前已完成的任何 turn 都会保留其 `result` 事件，但格式错误的输入行会中止会话的其余部分。

CLI 可以直接响应的斜杠命令（如 `/model` 和 `/usage`）会产生文本报告，而非标准事件流。流式会话无法利用这些类型的斜杠命令。例如：

```
{ "event": "result", "result": { "conversation_id": "4fae3a70-409d-42a4-86ea-9de206a49ff4", "status": "ERROR", "response": "", "error": "/model is answered by the CLI itself and is unavailable with --input-format stream-json; run it as its own --print /model invocation", "duration_seconds": 0, "num_turns": 0, "usage": { "input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0, "cache_read_tokens": 0, "total_tokens": 0 } } }
```

### 常见错误

| 错误 | 失败原因 | 修复方法 |
| :-- | :-- | :-- |
| **与 `--output-format json` 或 `text` 搭配使用** | 这些格式仅在进程退出时发出单个输出信封，导致除最后一个 turn 外的所有 turn 都会丢失。 | 在此输入模式下始终使用 `--output-format stream-json`。 |
| **使用 `-p` 标志传入 prompt** | 流式模式仅监听 `stdin` 上的 prompts。通过命令行标志传入的任何 prompt 都会被丢弃。 | 将 prompt 作为 `user` 消息发送到 `stdin`。 |
| **向流中发送 `/model` 或 `/usage`** | CLI 在事件流之外内部处理这些命令，会破坏 JSON 流。 | 将 `agy -p /model` 作为完全独立的单独命令运行。 |
| **将 `num_turns` 视为每个 turn 的计数** | 元数据计数器（如 turn 数、时长和用量）跟踪整个累计会话，而非仅当前 turn。 | 使用 `response` 字段获取当前 turn 的文本。 |
| **在读取 `stdout` 之前等待进程退出** | 会话会无限期保持打开，直到 `stdin` 关闭。如果你的脚本等待退出信号，它将挂起。 | 按到达顺序逐行读取事件，并在完成后手动关闭 `stdin`。 |

## 选择模型、effort 或 agent

列出可用的模型 slug，然后为本次运行固定一个：

```
agy models
```

```plaintext
gemini-3.8-flash-high     Gemini 3.8 Flash (High)
gemini-3.8-flash-medium   Gemini 3.8 Flash (Medium)
gemini-3.7-flash-high     Gemini 3.7 Flash (High)
gemini-3.7-flash-medium   Gemini 3.7 Flash (Medium)
gemini-3.6-flash-high     Gemini 3.6 Flash (High)
gemini-3.6-flash-medium   Gemini 3.6 Flash (Medium)
gemini-3.1-pro-high       Gemini 3.1 Pro (High)
claude-sonnet-4-6         Claude Sonnet 4.6 (Thinking)
...
```

```
# 按 slug 固定模型。
agy -p "Reverse the string antigravity." --model gemini-3.5-flash-medium

# 设置推理 effort（low、medium 或 high）。
agy -p "Outline a plan to add caching to this service." --effort high

# 选择 agent（使用 `agy agents` 列出）。
agy -p "Review this function for edge cases." --agent <agent-name>
```

与交互式界面不同，headless 模式在 `--model` 指定未知模型时不会静默回退。它会以非零退出码和 `ERROR` 状态退出，从而使固定了模型的流水线响亮地失败，而不是运行错误的模型。

## Headless 模式下的权限

Headless 模式下没有交互式提示，因此通常会请求确认的工具由策略处理。

默认情况下，CLI 遵循你设置中的权限模式。需要其无法获得的批准的工具会被软拒绝：运行继续，以 `0` 退出，并向 `stderr` 打印一条通知，说明工具名称及如何允许它。在你的活动 workspace 内读写文件是自动允许的；shell 命令等操作默认为 **Ask**，在 headless 模式下会被软拒绝，除非你授予它们权限。

通过在 `~/.gemini/antigravity-cli/settings.json` 的 `permissions.allow` 下添加 `action(target)` 规则来提前授予工具权限：

```
{
  "permissions": {
    "allow": [
      "command(git)",
      "command(regex:npm run (build|lint|test))",
      "write_file(src/)"
    ]
  }
}
```

要为一次运行自动批准所有工具，请传入 `--dangerously-skip-permissions`：

```
agy -p "Run the test suite and report failures" --dangerously-skip-permissions
```

> **警告：** `--dangerously-skip-permissions` 会批准所有 tool call，包括文件写入和命令执行。除非你完全信任 prompt 和环境，否则请优先使用范围限定的 `permissions.allow` 规则。有关完整的规则语法，请参阅 [权限](/docs/cli/permissions)。

## 处理退出码和错误

成功的运行以 `0` 退出。未能产生响应的运行以非零退出，并将原因写入 `stderr`。在 `json` 和 `stream-json` 模式下，失败也会出现在 `status` 和 `error` 字段中。

例如，固定一个未知模型会以 `1` 退出并返回错误信封：

```
agy -p "hi" --model does-not-exist-model --output-format json; echo "exit=$?"
```

```
{"conversation_id":"","status":"ERROR","response":"","error":"invalid model selection (--model \"does-not-exist-model\" --effort \"\"): model does-not-exist-model is not recognized as a known model or custom model in settings\nAvailable models:\n  Gemini 3.6 Flash (High)\n  ...","duration_seconds":0,"num_turns":0,"usage":{"input_tokens":0,"output_tokens":0,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":0}}
```

```
exit=1
```

`status` 字段报告运行的终止状态：

| 状态 | 含义 |
| --- | --- |
| `SUCCESS` | 运行完成并产生了响应 |
| `ERROR` | 运行以错误结束 |
| `CANCELED` | 运行被取消 |
| `INTERRUPTED` | 运行被中断（例如 `SIGINT`） |
| `INVALID` | 运行达到了无效状态 |
| `WAITING` | 运行在等待输入时结束 |
| `RUNNING` | 运行未达到终止状态 |

默认情况下，运行最多等待五分钟以获取响应。使用 `--print-timeout` 调整上限：

```
agy -p "Summarize the design tradeoffs of optimistic locking." --print-timeout 15m
```

## 标志参考

| 标志 | 默认值 | 描述 |
| --- | --- | --- |
| `-p`、`--print`、`--prompt` | — | 以非交互方式运行单个 prompt 并打印响应 |
| `--output-format` | `text` | 输出格式：`text`、`json` 或 `stream-json` |
| `--input-format` | `text` | 输入格式：`text` 或 `stream-json`；在 stdin 上读取 prompts |
| `--json-schema` | — | 用于强制执行结构化输出的 schema 字符串或文件路径 |
| `--model` | — | 本次运行的模型 slug（参见 `agy models`） |
| `--effort` | — | 推理 effort：`low`、`medium` 或 `high` |
| `--agent` | — | 本次运行的 agent（参见 `agy agents`） |
| `--continue`、`-c` | `false` | 继续最近的会话 |
| `--conversation` | — | 按 ID 恢复会话 |
| `--dangerously-skip-permissions` | `false` | 自动批准所有工具权限请求 |
| `--print-timeout` | `5m` | 等待响应的最长时间 |
| `--sandbox` | `false` | 启用终端 sandbox 限制运行 |

## 示例：在 CI 中运行 agent

出错时使任务失败并保存响应：

```
#!/usr/bin/env bash
set -euo pipefail

result=$(agy -p "Name three popular version control systems, comma-separated." \
  --output-format json \
  --print-timeout 10m)

status=$(echo "$result" | jq -r '.status')
if [[ "$status" != "SUCCESS" ]]; then
  echo "Agent run failed: $(echo "$result" | jq -r '.error')" >&2
  exit 1
fi

echo "$result" | jq -r '.response' > result.txt
```

## 后续步骤

*   [Prompting & Interaction](/docs/cli/prompting)：为 agent 编写有效的 prompts。
*   [Permissions](/docs/cli/permissions)：配置 allow、deny 和 ask 规则。
*   [Background Tasks & Subagents](/docs/cli/subagents)：将工作委派给专门的 agents。
*   [Reference](/docs/cli/reference)：完整的命令和标志参考。