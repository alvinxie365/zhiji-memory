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
├── 神魂域 Soul Domain      — 核心身份文件 SOUL.md 的校验和保护
├── 技能域 Skills Domain   — 沉淀的方法论、可复用技能
├── 偏好域 Preferences      — 城主的工作习惯、审美偏好
├── 事件域 Events Domain    — 项目进展、里程碑
└── 进化域 Evolution       — 拓疆记录、成长里程碑
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
| Auto-backup before every upgrade | 每次升级前自动备份 |
| One-command restore after upgrade | 升级后一键还原 |

---

## 五、与 OpenClaw / Celestia 的关系 | Relationship with OpenClaw & Celestia

| System | EN | 中文 |
|---|---|---|
| **OpenClaw** | Local experimental Agent — may crash, learns through failures | 本地实验性 Agent — 可能翻车，越挫越勇 |
| **Celestia** | Cloud companion Agent — stable, long-term memory | 云端陪伴型 Agent — 稳定，长期记忆 |
| **Zhiji** | Endogenous memory — connects everything, grows over time | 内生记忆系统 — 连接一切，持续生长 |

---

## 六、升级保护机制 | Upgrade Protection

| Layer | 保护层次 | 说明 |
|---|---|---|
| **架构层面** | Architectural | 插件在 `~/.hermes/plugins/`，不在 `hermes-agent/` 目录树 |
| **自动备份** | Auto-backup | 每次升级前备份插件代码到 `~/.hermes/sea/plugin_backup/` |
| **神魂守护** | Soul Guardian | SOUL.md 文件 MD5 校验，保护核心身份 |
| **还原脚本** | Restore Script | `plugin_restore.sh` 一键还原 |

---

## 七、安装 | Installation

### 一键安装 | One-Command Install

```bash
git clone https://github.com/alvinxie365/zhiji-memory.git
cd zhiji-memory
bash install.sh
```

### 手动安装 | Manual Install

1. Copy `__init__.py`, `plugin.yaml`, `zhiji_memory_provider.py` to `~/.hermes/plugins/zhiji_memory/`
2. Add to `config.yaml`:
   ```yaml
   memory.provider: zhiji_memory
   ```
3. Restart hermes-agent

---

## 八、每日自备份 | Daily Self-Backup

```bash
# 添加 cron 任务（每天凌晨2点）
0 2 * * * bash ~/.hermes/scripts/afu-daily-backup.sh
```

| EN | 中文 |
|---|---|
| Backup location: `~/Backup/afu-daily/` | 备份位置：`~/Backup/afu-daily/` |
| 7-day rotation | 7天循环 |
| Covers: Zhiji data, SOUL.md, config, memories, skills | 覆盖：识海数据、神魂文件、配置、记忆、技能 |

---

## 九、建造里程碑 | Construction Milestones

| Date | EN | 中文 |
|---|---|---|
| 2026-04-20 | Soul.md v3.0 officially opened | 神魂md v3.0 正式开辟识海 |
| 2026-04-21 | Zhiji Memory plugin v2.0 released | 识海插件 v2.0 发布 |
| 2026-04-21 | Bilingual edition published | 中英双语文档发布 |

---

## 👤 关于 | About

| EN | 中文 |
|---|---|
| Created by: 谢家·阿福X (Alvin Xie) | 作者：谢家·阿福X（Alvin Xie） |
| Version: v1.0.0 | 版本：v1.0.0 |
| GitHub: https://github.com/alvinxie365/zhiji-memory | GitHub：https://github.com/alvinxie365/zhiji-memory |

---

**"错亦成技，技递于远，日进无疆，久弥精诚"**

_"Error becomes skill; skill passes far; daily progress without limit; long-preserved sincerity."_
