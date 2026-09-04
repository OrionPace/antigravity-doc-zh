---
layout: doc
---

# Codex CLI 配置指南

介绍 Codex CLI 的核心配置文件、模型切换与行为控制选项。

## 配置文件位置

Codex CLI 会在以下位置读取用户级与项目级配置：

- **全局配置**：`~/.codex/config.json` 或 `~/.codex/settings.yaml`
- **项目级配置**：当前工作目录下的 `.codex/config.json`

## 核心配置项参考

```json
{
  "model": "o3-mini",
  "temperature": 0.2,
  "max_tokens": 4096,
  "approval_mode": "auto-edit",
  "sandbox": {
    "enabled": true,
    "network": false
  }
}
```

### 常用执行模式

1. **Suggest Mode（建议模式）**：生成 diff 供用户手动确认后应用。
2. **Auto-edit Mode（自动编辑模式）**：直接修改文件，但在执行 shell 外部命令前征求确认。
3. **Full-auto Mode（全自主模式）**：适用于独立测试环境的无人值守批处理。
