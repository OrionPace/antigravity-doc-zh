import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Antigravity & Codex 中文知识库',
  description: 'Google Antigravity CLI 与 Codex 社区中文文档 · 每日自动同步',
  base: '/antigravity-doc-zh/',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  head: [
    ['meta', { name: 'theme-color', content: '#1a73e8' }],
    ['meta', { name: 'robots', content: 'index,follow' }],
    ['link', { rel: 'icon', href: '/antigravity-doc-zh/favicon.ico' }],
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: 'Antigravity CLI (36篇)', link: '/cli/00-overview' },
      { text: 'Codex CLI 专区', link: '/codex/' },
      { text: '关于与项目状态', link: '/about/' },
    ],

    sidebar: {
      '/cli/': [
      {
        text: '入门与基础',
        collapsed: false,
        items: [
          { text: 'Antigravity CLI 概览', link: '/cli/00-overview' },
          { text: 'Antigravity CLI 入门指南', link: '/cli/01-getting-started' },
          { text: '安装与认证', link: '/cli/02-installation-auth' },
          { text: 'Antigravity CLI 上手教程', link: '/cli/03-tutorial' },
          { text: '使用 AGY CLI', link: '/cli/04-using-agy-cli' },
          { text: 'Antigravity CLI 特性', link: '/cli/05-features' },
          { text: '从 Gemini CLI 迁移', link: '/cli/06-migration' },
        ]
      },
      {
        text: '交互与运行模式',
        collapsed: false,
        items: [
          { text: 'Prompt 与交互', link: '/cli/07-prompting-interaction' },
          { text: '审查 Artifact', link: '/cli/08-reviewing-artifacts' },
          { text: '管理会话', link: '/cli/09-managing-conversations' },
          { text: '选择执行模式', link: '/cli/10-choose-an-execution-mode' },
          { text: 'Headless 模式（无头模式）', link: '/cli/11-headless-mode' },
        ]
      },
      {
        text: '核心架构与机制',
        collapsed: false,
        items: [
          { text: '后台任务与 subagent', link: '/cli/12-background-tasks-subagents' },
          { text: 'Sandbox（沙箱）', link: '/cli/13-sandbox' },
          { text: 'Permissions（权限）', link: '/cli/14-permissions' },
          { text: '项目（Projects）', link: '/cli/15-projects' },
          { text: '设置、渲染与 Keybindings', link: '/cli/16-settings-rendering-keybindings' },
          { text: 'Vim 编辑器模式（Vim editor mode）', link: '/cli/17-vim-editor-mode' },
          { text: '管理 AI Credits 与配额', link: '/cli/18-ai-credits' },
          { text: 'Model Context Protocol (MCP)', link: '/cli/19-mcp' },
          { text: 'Plugins 与 Skills', link: '/cli/20-plugins-skills' },
          { text: 'Statusline 自定义', link: '/cli/21-status-line-customization' },
          { text: '终端标题自定义', link: '/cli/22-terminal-title-customization' },
        ]
      },
      {
        text: 'CLI 核心命令专篇',
        collapsed: false,
        items: [
          { text: 'Agents 命令 (/agents)', link: '/cli/23-agents-command-agents' },
          { text: 'Code Search 命令 (/codesearch)', link: '/cli/24-code-search-command-codesearch' },
          { text: 'AI Credits 命令 (/credits)', link: '/cli/25-ai-credits-command-credits' },
          { text: 'Diff 命令 (/diff)', link: '/cli/26-diff-command-diff' },
          { text: 'Permissions 命令 (/permissions)', link: '/cli/27-permissions-command-permissions' },
          { text: 'Resume 命令 (/resume)', link: '/cli/28-resume-command-resume' },
          { text: 'Status Line 命令 (/statusline)', link: '/cli/29-status-line-command-statusline' },
          { text: '窗口标题命令 (/title)', link: '/cli/30-window-title-command-title' },
          { text: '模型配额 (/usage)', link: '/cli/31-model-quotas-usage' },
          { text: '语音听写 (/voice)', link: '/cli/32-voice-dictation-voice' },
        ]
      },
      {
        text: '最佳实践与参考手册',
        collapsed: false,
        items: [
          { text: 'Antigravity CLI 最佳实践', link: '/cli/33-best-practices' },
          { text: '故障排查', link: '/cli/34-troubleshooting' },
          { text: 'CLI 参考', link: '/cli/35-cli-reference' },
        ]
      },
    ],
      '/codex/': [
        {
          text: 'Codex CLI 指南',
          collapsed: false,
          items: [
            { text: 'Codex 简介与概览', link: '/codex/' },
            { text: '快速上手 (Getting Started)', link: '/codex/getting-started' },
            { text: '配置指南 (Configuration)', link: '/codex/configuration' },
            { text: '记忆桥接 (Memory Bridge)', link: '/codex/memory-bridge' },
          ]
        }
      ],
      '/about/': [
        {
          text: '关于本项目',
          items: [
            { text: '项目概览与背景', link: '/about/' },
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/OrionPace/antigravity-doc-zh' }
    ],

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
              modal: {
                noResultsText: '无相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭',
                },
              },
            },
          },
        },
      },
    },

    docFooter: { prev: '上一页', next: '下一页' },
    outline: { label: '本页目录', level: [2, 3] },
    darkModeSwitchLabel: '主题外观',
    sidebarMenuLabel: '目录菜单',
    returnToTopLabel: '返回顶部',
    langMenuLabel: '多语言',

    footer: {
      message: 'Antigravity & Codex 社区中文知识库 · 非官方整理 · 每日差量自动同步',
      copyright: '基础设施代码采用 MIT 许可；文档内容归对应官方所有并遵循开源引用规范',
    },
  },
})
