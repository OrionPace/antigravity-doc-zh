---
layout: doc
---

# Codex CLI 快速上手

本指南介绍如何在本地环境中安装并启动 Codex CLI。

## 环境要求

- Node.js >= 18 或 Python >= 3.10（取决于发行版本）
- 具有有效 API 额度的 OpenAI API Key
- 支持的终端环境（macOS Terminal, Linux bash/zsh, Windows PowerShell）

## 安装与启动

根据官方推荐的包管理器进行安装：

```bash
# 全局安装
npm install -g @openai/codex-cli
# 或使用 uv / pipx
pipx install codex-cli
```

### 配置 API Key

在你的终端配置文件（如 `~/.bashrc` 或 `~/.zshrc`）中设置环境变量：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

在 Windows PowerShell 中：

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

## 首次运行

进入任意项目根目录，直接输入命令：

```bash
codex
```

启动后即可直接用自然语言与 agent 交互，提出重构、纠错或编写测试的需求。
