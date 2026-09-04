---
layout: home

hero:
  name: AI Terminal Docs
  text: Antigravity CLI & Codex 社区中文知识库
  tagline: 面向中文开发者的前沿 Terminal AI Coding Agent 官方文档翻译、核心机制剖析与每日实时同步镜像。
  actions:
    - theme: brand
      text: 📖 Antigravity CLI 完整指南 (36篇)
      link: /cli/00-overview
    - theme: alt
      text: ⚡ Codex CLI 专区
      link: /codex/
    - theme: alt
      text: ⭐️ GitHub 仓库
      link: https://github.com/OrionPace/antigravity-doc-zh

features:
  - title: ⚡ 36 篇 Antigravity 全量手册
    details: 从快速入门、设置与 Vim 模式，到 34 个核心命令（/agents, /diff, /resume 等）完整本地化，100% 保留命令与真实操作手感。
  - title: 🔒 严格术语保留（防误翻机制）
    details: 绝非粗暴机器直译。核心固化命令、CLI 参数与配置项严格保留英文，skill、subagent、artifact 等专有名词双轨呈现，代码可直接复制运行。
  - title: 🔄 逐日哈希差量自动同步
    details: 基于官方原生 Markdown 端点与 SHA-256 指纹比对，每日自动检测 Google 上游变动，差量增量维护，实现永不断更的活文档。
  - title: 🤖 双子星生态（Antigravity & Codex）
    details: 汇聚 Google 与 OpenAI 最硬核的终端智能体实践，涵盖环境配置、Prompting 技巧与跨 Agent 记忆桥接方案。
---

::: info 💡 欢迎查阅与参与
本站为社区维护的开源文档镜像站，致力于消除网络访问门槛与浏览器插件错翻问题。文档每日通过 GitHub Actions 自动化流水线维护。
:::

## 核心专区导航

| 专区 | 篇幅与状态 | 核心内容 | 快速入口 |
| :--- | :--- | :--- | :--- |
| **Antigravity CLI** | **36 篇（全量就绪）** | 官方全部 36 篇教程、Headless 模式、Sandboxing、34 个命令详解 | [进入阅读 →](/cli/00-overview) |
| **Codex CLI** | **精选架构指南** | 快速上手、配置文件、执行模式、与 Antigravity 协同实践 | [进入阅读 →](/codex/) |
| **自动同步流水线** | **已激活运行** | 官方 sitemap 探测、SHA-256 差量哈希拦截、GitHub Actions 自动化 | [查看项目状态 →](/about/) |

## 为什么拒绝浏览器插件翻译？

许多开发者使用沉浸式翻译插件阅读英文官网，但经常遇到：
1. **命令被误翻**：例如将 `/agents` 翻译为 `/代理`，将 `/diff` 翻译为 `/差异`，导致在终端粘贴时直接报错；
2. **术语变形**：将 `skill` 翻译成“技能”，丢失了对应 `.gemini/skills/` 文件夹的系统映射；
3. **网络阻碍**：官方页面加载缓慢。

本项目在翻译时预置了严格的 **工程术语字典与不可翻译词清单**，确保你看到的代码和命令就是能直接跑的原汁原味命令！
