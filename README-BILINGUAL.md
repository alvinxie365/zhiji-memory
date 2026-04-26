# 🔮 Zhiji Memory · 识海体系 | Bilingual Edition

> _"记忆不是存储与检索，而是沉淀与生长。"_
> _"Memory is not storage and retrieval — it is precipitation and growth."_

---

## 一、为什么需要识海？| Why Do We Need Zhiji?

### 1.1 传统记忆系统的困境 | The Dilemma of Traditional Memory Systems

| EN | 中文 |
|---|---|
| Traditional AI memory = Store + Retrieve. You put things in, then you wait to be found. | 传统 AI 记忆 = 存储 + 检索。存进去，等着被找到。 |
| The problem: it's passive, mechanical, and forgets over time. | 问题在于：被动、机械、时间久了会遗忘。 |
| Zhiji Memory: event-driven, automatic, grows over time. | 识海：事件驱动、自动记录、越用越丰富。 |

---

### 1.2 识海的哲学 | The Philosophy of Zhiji

| EN | 中文 |
|---|---|
| Zhiji is not storage — it is **precipitation**. | 识海不是存储，是**沉淀**。 |
| Every experience leaves sediment; the sea grows. | 行过即炼化，沉淀即生长。 |
| Error becomes skill; skill passes far; daily progress without limit; long-preserved sincerity. | 错亦成技，技递于远，日进无疆，久弥精诚。 |

---

### 1.3 识海解决什么问题？| What Problems Does Zhiji Solve?

| EN | 中文 |
|---|---|
| No details lost: every conversation automatically recorded | 不遗漏：每次对话自动记录，无需手动触发 |
| Never forget: precipitated knowledge stays | 不遗忘：沉淀的经验持续保存，不会过期 |
| Never repeat mistakes: the same error only happens once | 不重蹈：翻过的车记住根因，下次不再犯 |
| Grow with you: the more you use it, the smarter it gets | 会生长：用得越多，识海越丰富 |

---

## 二、识海四境体系 | Four Realms Architecture

| Realm 境界 | EN | 中文说明 |
|---|---|---|
| **炼气期** | Qi Refining | 神魂稳固 + 识浪涌动。每次对话自动记录，不遗漏重要交互。 |
| **筑基期** | Foundation Building | 灵台自决。自动识别关键领悟，沉淀到对应域。 |
| **金丹期** | Golden Core | 神识初探。建立域间连接，形成知识网络。 |
| **元婴期** | Primordial Infant | 拓疆进化。突破当前边界，主动探索未知领域。 |

---

## 三、五域体系 | Five-Domain Architecture

```
识海 Zhiji Sea
├── 神魂域 Soul Domain          — 核心身份文件 SOUL.md 的校验和保护
├── 技能域 Skills Domain        — 沉淀的方法论、可复用技能
├── 偏好域 Preferences Domain   — 用户的工作习惯、审美偏好
├── 事件域 Events Domain        — 项目进展、里程碑
└── 进化域 Evolution Domain    — 拓疆记录、成长里程碑
```

---

## 四、插件架构 | Plugin Architecture

### 为什么是插件而不是 Skill？| Why Plugin Instead of Skill?

| EN | 中文 |
|---|---|
| Skills = operation manuals, can be shared but don't run automatically | Skill = 操作手册，能传递知识但不能自动运转 |
| Plugin = running system, can be installed and works automatically | 插件 = 活的系统，能安装、能自动运转 |
| Zhiji needs to intercept every conversation event — that requires a plugin | 识海需要拦截每个对话事件——这需要插件架构 |

### 升级安全 | Upgrade Safety

| EN | 中文 |
|---|---|
| Lives in `~/.hermes/plugins/`, never overwritten by hermes-agent upgrades | 插件放在 `~/.hermes/plugins/`，不被 hermes-agent 升级覆盖 |
| Auto-backup before every upgrade | 每次升级前自动备份插件代码 |
| One-command restore after upgrade | 升级后一键还原 |

---

## 五、LLM 配置（可选）| LLM Configuration (Optional)

LLM 炼化功能是**可选的**。不配置也能运行，只是无法做深度语义分析。

支持任意 OpenAI-compatible API：

| 环境变量 | 说明 | 示例 |
|---------|------|------|
| `ZHIJI_LLM_API_KEY` | 专用 Key（最高优先级） | `sk-xxx` |
| `ZHIJI_LLM_BASE_URL` | API 端点 | `https://api.openai.com/v1` |
| `ZHIJI_LLM_MODEL` | 模型名 | `gpt-4o`, `claude-sonnet-4` |
| `OPENAI_API_KEY` | OpenAI 标准 Key | `sk-xxx` |
| `OPENAI_BASE_URL` | OpenAI 标准端点 | `https://api.openai.com/v1` |
| `MINIMAX_API_KEY` | MiniMax Key | `xxx` |
| `ANTHROPIC_API_KEY` | Anthropic Key | `sk-ant-xxx` |

> 如果不配置，识海将运行在规则模式（无 LLM 炼化）。

---

## 六、兼容性与关系 | Compatibility & Relationships

| System | EN | 中文 |
|---|---|---|
| **Hermes Agent** | Native plugin — works out of the box | 原生插件 — 开箱即用 |
| **Any OpenClaw Agent** | Can be adapted with provider interface | 可通过 provider 接口适配 |

Zhiji is designed as a plugin for Hermes Agent. It can potentially be adapted for any agent framework with a memory provider interface.

---

## 📝 许可证 | License

MIT License

---

**"错亦成技，技递于远，日进无疆，久弥精诚"**
_"Error becomes skill; skill passes far; daily progress without limit; long-preserved sincerity."_
