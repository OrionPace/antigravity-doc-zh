# Headless 模式（无头模式）

以非交互方式运行 Antigravity CLI，用于编写 agent 任务脚本、集成至 CI 流水线以及捕获机器可读的输出。

Headless mode（无头模式，亦称 print 模式）向 agent 发送单次 prompt，流式传输或返回响应后随即退出。无论何时需要在程序中获取 agent 的输出而非在终端界面（TUI）中交互时，都可以使用此模式。

## 运行单次 prompt

通过 `-p`（或其别名 `--print` 和 `--prompt`）传入 prompt，执行一次后退出：

```
agy -p "In one sentence, what is a git rebase?"
```

```
A git rebase rewrites the commit history by transplanting a sequence of commits onto a new base commit, imposing a strictly linear progression of changes that eliminates arbitrary merge artifacts.
```

响应内容输出至 `stdout`。诊断信息（包括错误、身份验证提示、进度和权限声明）则输出至 `stderr`。这种分离机制保证了捕获到的响应内容足够纯净：

```bash
# 仅捕获模型响应；诊断信息仍将打印到终端。
answer=$(agy -p "Name three popular version control systems, comma-separated.")
```

> **注意：** Headless mode 使用您缓存的凭据。请先通过一次交互式 `agy` 会话完成身份验证。在无终端的非交互式环境（例如 CI）中，未认证的运行将直接以 `authentication required` 错误退出，而不会挂起等待。

## 输出格式

`--output-format` flag 用于控制 `stdout` 的数据形态。它支持三个取值：

| 格式 | `stdout` 结构形态 | 适用场景 |
| --- | --- | --- |
| `text` | 纯响应文本（默认） | 人类可读输出、轻量脚本 |
| `json` | 执行完成后打印的一个完整 JSON 对象 | 捕获结果及元数据 |
| `stream-json` | 换行符分隔的 JSON（NDJSON）事件流 | 实时监控执行进度、工具以及 token 消耗 |

### Text

默认格式。响应文本直接输出到 `stdout`，不做任何包装：

```
agy -p "In one sentence, what does the command git bisect do?"
```

```
Git bisect executes a binary search algorithm across a project's commit history to rapidly isolate the precise commit responsible for introducing a defect.
```

### JSON

设置 `--output-format json` 可在运行完成后获取单个 JSON 封装包。CLI 会将其输出在单行中；可通过管道传递给 `jq` 进行美化打印（pretty-print）：

```
agy -p "In one sentence, what is a git rebase?" --output-format json | jq
```

```json
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

该封装包包含以下字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `conversation_id` | string | 对话 ID，用于后续恢复会话 |
| `status` | string | 最终状态（参见 [状态值](#状态值)） |
| `response` | string | agent 的自由文本响应 |
| `error` | string | 错误信息；仅在失败时出现 |
| `duration_seconds` | number | 本次运行的挂钟耗时（秒） |
| `num_turns` | number | 对话中的用户 turn（轮次）数量 |
| `structured_output` | object | 解析后的 schema 对象输出；仅在使用 `--json-schema` 时出现 |
| `json_schema` | object | 所强制执行的 schema；仅在使用 `--json-schema` 时出现 |
| `usage` | object | Token 计数：`input_tokens`、`output_tokens`、`thinking_tokens`、`cache_read_tokens`、`total_tokens` |

#### 基于 Schema 的结构化输出

传入 `--json-schema` 可将回答约束至指定的 schema。解析后的对象将出现在 `structured_output` 中，而 `response` 则保留序列化为字符串的相同负载：

```bash
agy -p "Parse the semantic version string v2.14.3 into an object with integer fields major, minor, and patch." \
  --output-format json \
  --json-schema '{"type":"object","properties":{"major":{"type":"integer"},"minor":{"type":"integer"},"patch":{"type":"integer"}},"required":["major","minor","patch"]}' | jq
```

```json
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

该 flag 接受 schema 字符串、`.json` schema 文件路径或基本类型名称（`string`、`number`、`integer`、`boolean`）。直接从 `structured_output` 中读取解析后的值：

```bash
agy -p "Parse the semantic version string v2.14.3 into an object with integer fields major, minor, and patch." \
  --output-format json \
  --json-schema '{"type":"object","properties":{"major":{"type":"integer"},"minor":{"type":"integer"},"patch":{"type":"integer"}},"required":["major","minor","patch"]}' \
  | jq '.structured_output'
```

### Streaming JSON

设置 `--output-format stream-json` 可随着运行的推进，逐行输出一个 JSON 对象（NDJSON）。使用此格式可实时观察 tool call（工具调用）与 token 使用量。

```
agy -p "In one sentence, what is a git rebase?" --output-format stream-json
```

事件流以单个 `init` 事件开始，接着是任意数量的 `step_update` 事件，并以恰好一个 `result` 事件结束（下方已缩写 `cwd` 和 `tools` 数组）：

```json
{"event":"init","conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","init":{"cwd":"/home/user/project","tools":["ask_permission","run_command","write_to_file","..."],"permission_mode":"request-review"}}
{"event":"step_update","step_update":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","step_index":0,"state":"DONE","step_type":"user_input"}}
{"event":"step_update","step_update":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","step_index":3,"state":"DONE","step_type":"agent_response","text_delta":"Git rebase destructively rewrites a branch's commit history by systematically detaching its unique commits and sequentially reapplying them onto a new base commit.\n","duration_seconds":6.28,"usage":{"input_tokens":10302,"output_tokens":582,"thinking_tokens":551,"cache_read_tokens":8113,"total_tokens":10884}}}
{"event":"step_update","step_update":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","step_index":4,"state":"DONE","step_type":"checkpoint","duration_seconds":0.53,"usage":{"input_tokens":116,"output_tokens":7,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":123}}}
{"event":"result","result":{"conversation_id":"c3b66b04-872b-4fbe-a3a4-058a026ef20a","status":"SUCCESS","response":"Git rebase destructively rewrites a branch's commit history by systematically detaching its unique commits and sequentially reapplying them onto a new base commit.\n","duration_seconds":6.88,"num_turns":1,"usage":{"input_tokens":10418,"output_tokens":589,"thinking_tokens":551,"cache_read_tokens":8113,"total_tokens":11007}}}
```

当响应分块流式传输时，`agent_response` 步骤会在最终变为 `DONE` 之前，发出一个或多个携带部分 `text_delta` 片段的 `ACTIVE` 事件；而对于本例这样简短的响应，则会在单个 `DONE` 事件中一次性送达。

每一行都是一个事件对象，其 `event` 字段标明了事件类型：

| `event` | 负载键（Payload key） | 发出时机 |
| --- | --- | --- |
| `init` | `init` | 仅一次，在流启动时 |
| `step_update` | `step_update` | 每次步骤状态转换或收到 text delta 时 |
| `result` | `result` | 仅一次，在执行结束时（结构与 `json` 格式相同） |

`init` 负载记录了运行配置。`model` 和 `agent` 仅在通过 `--model` 或 `--agent` 显式设置时才会出现；`permission_mode` 默认为 `request-review`（在使用 `--dangerously-skip-permissions` 时为 `always-proceed`）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `cwd` | string | 当前工作目录 |
| `tools` | string[] | 所有可用工具的名称列表 |
| `permission_mode` | string | 生效的权限模式 |
| `model` | string | 使用的模型（覆盖时） |
| `agent` | string | 激活的 agent（覆盖时） |
| `json_schema` | object | 强制执行的 schema（通过 `--json-schema` 设置时） |

每个 `step_update` 负载描述了一个具体步骤。常见的 `step_type` 取值包括 `user_input`、`agent_response`、`tool` 和 `checkpoint`；当步骤正在运行时，`state` 为 `ACTIVE`，步骤完成时为 `DONE`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `conversation_id` | string | 对话 ID |
| `step_index` | number | 步骤的零基索引（从 0 开始） |
| `state` | string | `ACTIVE` 或 `DONE` |
| `step_type` | string | 步骤类别，例如 `agent_response` 或 `tool` |
| `tool_name` | string | 规范工具名（仅在 tool 步骤中出现） |
| `text_delta` | string | 增量响应文本片段 |
| `duration_seconds` | number | 步骤耗时（已知时） |
| `usage` | object | 单步 token 消耗量（已知时） |
| `tool_info` | object | 工具调用详情（参见下文） |
| `subagent_info` | object | Subagent 调用详情 |

#### 流中的 Tool Call

在 tool 步骤中，`tool_info` 携带了调用参数及其执行结果。以下是一个执行了 `echo hello_headless_demo` 的真实 tool 步骤输出：

```json
{"event":"step_update","step_update":{"conversation_id":"edb1c8c1-50ba-4f3f-87eb-412d0e9d47c3","step_index":4,"state":"DONE","step_type":"tool","tool_name":"run_command","duration_seconds":0.07,"tool_info":{"name":"run_command","parameters":{"CommandLine":"echo hello_headless_demo"},"output":"hello_headless_demo\r\n"}}}
```

`tool_info` 包含 `name`、`parameters`、`output`，以及在工具执行失败时包含带有 `type` 和 `message` 的 `error` 对象。生成 subagent 的步骤则会携带 `subagent_info`，并在 `subagents` 列表中列出每个 subagent（包含 `type_name`、`role`、`conversation_id`、`log_uri` 和 `workspace_uris`）。

#### 流中的结构化输出

搭配 `--json-schema` 时，该 schema 将应用于流末尾的终端 `result` 事件，该事件携带与 `json` 格式封装包相同的 `structured_output` 和 `json_schema` 字段。

## 使用 jq 解析输出

`stdout` 是机器可读的，因此 `jq` 可以精准提取您所需的信息。

从 JSON 运行中提取响应文本：

```bash
agy -p "Name three popular version control systems, comma-separated." --output-format json | jq -r '.response'
```

```
Git, Subversion, Mercurial.
```

实时拼接流式文本：

```bash
agy -p "Explain what a merge conflict is in two sentences." --output-format stream-json \
  | jq -j 'select(.event=="step_update") | .step_update.text_delta // empty'
```

从终端 `result` 事件中读取 token 使用量：

```bash
agy -p "In one sentence, what is a git rebase?" --output-format stream-json \
  | jq 'select(.event=="result") | .result.usage'
```

> **提示：** 拼接 `text_delta` 片段时请使用 `jq -j`（连接输出），这样 `jq` 就不会在片段之间自动插入换行符。

## 继续对话

Headless 运行默认是无状态的。使用 `--continue`（`-c`）可以恢复最近一次对话的上下文，或使用 `--conversation` 传入先前某次运行的 `conversation_id`：

```bash
# 继续最近一次对话。
agy -p "Now explain your previous answer in more detail" --continue

# 通过 ID 恢复特定对话。
agy -p "Summarize what we discussed" --conversation 055a398f-db14-4c5f-abbb-1bf03f8120a7
```

上述每条命令都会启动一个全新的进程。若要在单个进程内运行多个 turn（轮次），请参阅 [从 stdin 流式传入 prompt](#从-stdin-流式传入-prompt)。

## 从 stdin 流式传入 prompt

使用 `--input-format stream-json` 可以保持单个持续运行的对话进程，通过标准输入（stdin）逐个向其喂入 prompt。每个 prompt 都会执行一个完整的 turn 并发出其独立的 `result` 事件。

这种方式非常适合需要根据上一个回答动态决定下一个 prompt 的应用程序。由于该进程仅启动一次，后续的 turn 能够跳过冷启动开销，直接复用已预热的对话环境。这使得它比反复执行带有 `--continue` 的独立命令要快得多。

> **注意：** `--input-format stream-json` 必须搭配 `--output-format stream-json` 使用。在流式会话中，CLI 为每个 turn 恰好发出一个 `result` 事件。

### 发送 prompt

以每行一个 JSON 对象的形式写入 `stdin`。`event` 键指定了消息类型（与输出流格式相匹配）。Prompt 表示为带有 `message` 的 `user` 事件：

```json
{ "event": "user", "message": { "content": "Reply with exactly the word: apple. Nothing else." } }
```

您可以将多个 prompt 管道传输到单次会话中：

```bash
printf '%s\n' \
  '{"event":"user","message":{"content":"Reply with exactly the word: apple. Nothing else."}}' \
  '{"event":"user","message":{"content":"What word did I ask you to reply with in my previous message? Answer with just that word."}}' \
  | agy --input-format stream-json --output-format stream-json
```

`content` 字段既可以接受标准字符串，也可以接受文本块列表。以下两种格式等效：

```json
{ "event": "user", "message": { "content": "Reply with exactly: banana" } }
{ "event": "user", "message": { "content": [{ "type": "text", "text": "Reply with exactly: banana" }] } }
```

`text` 是唯一支持的块类型。提交任何其他块类型都会导致会话以错误消息终止，而不是静默丢弃该块。这确保了 agent 绝不会回答您未明确发送的 prompt。

### 读取结果

输出流的运作流程如下：

1. 以单个 `init` 事件开启。
2. 为当前活动的 turn 发出一系列 `step_update` 事件。
3. 以最终的 `result` 事件结束该 turn。

下例展示了上述双 prompt bash 命令的输出（其中 `init` 负载已缩写）：

```json
{"event":"init","conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","init":{"cwd":"/home/user/project","tools":["ask_permission","run_command","write_to_file","..."],"permission_mode":"request-review"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":0,"state":"DONE","step_type":"user_input"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":2,"state":"ACTIVE","step_type":"agent_response","text_delta":"apple"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":2,"state":"DONE","step_type":"agent_response","text_delta":"\n","duration_seconds":1.169607627,"usage":{"input_tokens":30384,"output_tokens":4,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":30388}}}
{"event":"result","result":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","status":"SUCCESS","response":"apple\n","duration_seconds":1.427806958,"num_turns":1,"usage":{"input_tokens":30384,"output_tokens":4,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":30388}}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":3,"state":"DONE","step_type":"user_input"}}
{"event":"step_update","step_update":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","step_index":4,"state":"DONE","step_type":"agent_response","text_delta":"apple\n","duration_seconds":0.895679386,"usage":{"input_tokens":278,"output_tokens":4,"thinking_tokens":0,"cache_read_tokens":30214,"total_tokens":282}}}
{"event":"result","result":{"conversation_id":"9ec58bfd-4d67-4f5e-83a5-9d907e9c6b1f","status":"SUCCESS","response":"apple\n","duration_seconds":2.548755756,"num_turns":2,"usage":{"input_tokens":30662,"output_tokens":8,"thinking_tokens":0,"cache_read_tokens":30214,"total_tokens":30670}}}
```

第二个 turn 结合第一个 turn 的上下文给出了回答 `apple`。请注意，单个 `conversation_id` 追踪整个会话，而 `init` 仅发送一次。

在解析 result 对象时，请注意：响应文本仅适用于当前 turn，而元数据计数器追踪的是整个会话的累积值：

| 字段 | 作用域 |
| --- | --- |
| `response` | 发出该响应的当次 turn |
| `num_turns` | 整个会话累积 |
| `usage` | 整个会话累积 |
| `duration_seconds` | 整个会话累积 |

若要进行筛选并仅查看最终响应，可以通过管道将输出传入 `jq`：

```bash
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

### 通过程序驱动会话

除了预先传入所有 prompt 外，您还可以在脚本中保持 `stdin` 管道处于打开状态。这样您的应用程序就可以在提交下一个 prompt 之前，先评估模型的回答。

> **提示：** 您可以逐行读取 `stdout` 并根据 `event` 字段派发逻辑。请务必在收到当前 prompt 的 `result` 事件后，再写入下一个 prompt。

例如：

```python
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

要正常优雅地关闭会话，只需关闭 `stdin` 即可。进程将在输入管道关闭且当前 turn 执行完毕后退出。如果应用程序写入了最后一个 prompt 并立即关闭管道，在进程终止前它仍会收到最后的 `result`。

正常结束的会话退出码为 `0`，这与标准 headless mode 的行为一致。

### 不支持的消息类型

为防止出现不可预知的行为，CLI 会对输入进行校验。如果遇到格式错误或不受支持的消息，CLI 将按照下表进行响应：

| 输入 | 结果 | 退出码 |
| --- | --- | --- |
| 无法识别的 `event` 名称 | 跳过：向 `stderr` 记录警告日志 | — |
| `control_request` 或 `control_response` 事件 | `ERROR` 结果，会话终止 | `2` |
| 由 CLI 直接处理的 Slash Command（例如 `/model`） | `ERROR` 结果，会话终止 | `2` |
| 缺少 `event` 字段的消息 | `ERROR` 结果，会话终止 | `1` |
| 无效的 JSON 行 | `ERROR` 结果，会话终止 | `1` |
| `text` 以外的内容块类型 | `ERROR` 结果，会话终止 | `1` |

无法识别的 `event` 名称会被安全跳过并发出警告。这确保了基于新版流式协议构建的应用程序在较旧的 CLI 版本上运行时不会发生崩溃：

```
warning: ignoring unsupported stream input message event "future_thing"
```

对于所有其他错误，会话将立即终止。先前完成的任何 turn 仍会保留其 `result` 事件，但格式错误的输入行会中止会话的后续执行。

CLI 能直接响应的 slash command（例如 `/model` 和 `/usage`）会生成文本报告而非标准事件流。流式会话无法使用这些类型的 slash command。例如：

```json
{ "event": "result", "result": { "conversation_id": "4fae3a70-409d-42a4-86ea-9de206a49ff4", "status": "ERROR", "response": "", "error": "/model is answered by the CLI itself and is unavailable with --input-format stream-json; run it as its own --print /model invocation", "duration_seconds": 0, "num_turns": 0, "usage": { "input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0, "cache_read_tokens": 0, "total_tokens": 0 } } }
```

### 常见错误

| 常见错误 | 失败原因 | 解决方法 |
| :-- | :-- | :-- |
| **搭配使用 `--output-format json` 或 `text`** | 这些格式仅在进程退出时发出单个输出封装包，导致除最后一个 turn 外的所有 turn 内容丢失。 | 在此输入模式下务必始终使用 `--output-format stream-json`。 |
| **通过 `-p` flag 传递 prompt** | 流式模式专门监听 `stdin` 上的 prompt。通过命令行 flag 传入的任何 prompt 都将被丢弃。 | 改为将 prompt 作为 `user` 消息写入 `stdin`。 |
| **向事件流中发送 `/model` 或 `/usage`** | CLI 在事件流之外通过内部逻辑处理这些命令，从而打破了 JSON 流。 | 将 `agy -p /model` 作为完全独立的命令单独运行。 |
| **将 `num_turns` 视为单轮计数** | 元数据计数器（如 turn 数、耗时和 token 消耗）追踪的是整个累积会话，而非仅当前 turn。 | 使用 `response` 字段获取当前 turn 的文本。 |
| **等待进程退出后再读取 `stdout`** | 会话在 `stdin` 关闭前将无限期保持开启状态。如果您的脚本等待进程退出信号，它将会发生挂起。 | 随着事件到达逐行读取，并在处理完毕后手动关闭 `stdin`。 |

## 选择模型、思考深度或 agent

列出可用的模型标识（slug），然后为本次运行指定模型：

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

```bash
# 通过 slug 指定模型。
agy -p "Reverse the string antigravity." --model gemini-3.5-flash-medium

# 设置推理思考深度（effort：low、medium 或 high）。
agy -p "Outline a plan to add caching to this service." --effort high

# 选择 agent（可通过 `agy agents` 列出）。
agy -p "Review this function for edge cases." --agent <agent-name>
```

与交互式 UI 不同，当 `--model` 指定了未知模型时，headless 模式不会静默回退。它会以非零退出码及 `ERROR` 状态退出，从而使指定了模型的流水线显式报错暴露问题，而不是以错误模型继续运行。

## Headless 模式下的权限

Headless 模式下不存在交互式提示，因此通常需要人工确认的工具由策略（policy）来处理。

默认情况下，CLI 遵循您设置中的权限模式。当某个工具需要审批但无法获取时，会被软拒绝（soft-denied）：运行继续进行，退出码为 `0`，并在 `stderr` 打印一条通知，指出该工具名称以及如何允许它。在活动 workspace 内读写文件是自动允许的；而 shell 命令等操作默认设置为 **Ask**，在 headless 模式下除非您显式授予权限，否则会被软拒绝。

如需提前授权某个工具，可在 `~/.gemini/antigravity-cli/settings.json` 的 `permissions.allow` 下添加 `action(target)` rule（规则）：

```json
{
  "permissions": {
    "allow": ["command(git)", "command(npm run (build|lint|test))", "write_file(src/)"]
  }
}
```

若要在单次运行中自动批准所有工具，请传入 `--dangerously-skip-permissions`：

```bash
agy -p "Run the test suite and report failures" --dangerously-skip-permissions
```

> **警告：** `--dangerously-skip-permissions` 会批准所有的 tool call，包括文件写入和命令执行。除非您完全信任当前的 prompt 和运行环境，否则建议优先使用限定作用域的 `permissions.allow` rule。完整 rule 语法请参阅 [权限](/docs/cli/permissions)。

## 处理退出码与错误

运行成功时退出码为 `0`。未能生成响应的运行将返回非零退出码，并将原因写入 `stderr`。在 `json` 和 `stream-json` 模式下，失败原因还会反映在 `status` 和 `error` 字段中。

例如，指定一个不存在的模型将以退出码 `1` 退出并返回错误封装包：

```bash
agy -p "hi" --model does-not-exist-model --output-format json; echo "exit=$?"
```

```json
{"conversation_id":"","status":"ERROR","response":"","error":"invalid model selection (--model \"does-not-exist-model\" --effort \"\"): model does-not-exist-model is not recognized as a known model or custom model in settings\nAvailable models:\n  Gemini 3.6 Flash (High)\n  ...","duration_seconds":0,"num_turns":0,"usage":{"input_tokens":0,"output_tokens":0,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":0}}
```

```
exit=1
```

### 状态值

`status` 字段汇报了运行的最终终态：

| 状态 | 含义 |
| --- | --- |
| `SUCCESS` | 运行完成并生成了响应 |
| `ERROR` | 运行因错误而结束 |
| `CANCELED` | 运行被取消 |
| `INTERRUPTED` | 运行被中断（例如收到 `SIGINT`） |
| `INVALID` | 运行进入了无效状态 |
| `WAITING` | 运行在等待输入时结束 |
| `RUNNING` | 运行尚未达到终态 |

默认情况下，单次运行等待响应的最长时间为 5 分钟。可通过 `--print-timeout` 调整上限：

```bash
agy -p "Summarize the design tradeoffs of optimistic locking." --print-timeout 15m
```

## Flag 参数参考

| Flag | 默认值 | 说明 |
| --- | --- | --- |
| `-p`, `--print`, `--prompt` | — | 以非交互方式运行单次 prompt 并打印响应 |
| `--output-format` | `text` | 输出格式：`text`、`json` 或 `stream-json` |
| `--input-format` | `text` | 输入格式：`text` 或 `stream-json`；从 stdin 读取 prompt |
| `--json-schema` | — | 用于强制执行结构化输出的 schema 字符串或文件路径 |
| `--model` | — | 本次运行的模型 slug（参见 `agy models`） |
| `--effort` | — | 推理思考深度：`low`、`medium` 或 `high` |
| `--agent` | — | 本次运行的 agent（参见 `agy agents`） |
| `--continue`, `-c` | `false` | 继续最近一次对话 |
| `--conversation` | — | 通过 ID 恢复指定对话 |
| `--dangerously-skip-permissions` | `false` | 自动批准所有工具权限请求 |
| `--print-timeout` | `5m` | 等待响应的最大超时时长 |
| `--sandbox` | `false` | 启用终端 sandbox 隔离限制运行 |

## 示例：在 CI 中运行 agent

在发生错误时使构建任务失败并保存响应内容：

```bash
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

* [Prompt 与交互](/docs/cli/prompting)：为 agent 编写高效的 prompt。
* [权限](/docs/cli/permissions)：配置 allow、deny 和 ask rule。
* [后台任务与 Subagent](/docs/cli/subagents)：将工作委派给专业 agent。
* [参考](/docs/cli/reference)：完整的命令与 flag 参数参考。