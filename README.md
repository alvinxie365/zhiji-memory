# 🔮 Zhiji Memory

> _"Memory is not storage and retrieval — it is precipitation and growth."_

Zhiji Memory is an **endogenous memory system** for Hermes Agent, replacing old RAG/vector-search with a "Soul → Tidal Wave → Precipitation → Growth" architecture. It makes AI grow naturally through every conversation.

**Built with love by [Xie Family](https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf) · 谢家**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Five Domains** | Soul, Skills, Preferences, Events, Evolution — each stored independently |
| **Event-Driven** | No manual triggers — every conversation is automatically recorded |
| **Four Realms** | Qi Refining → Foundation Building → Golden Core → Primordial Infant |
| **Upgrade-Safe** | Lives in `~/.hermes/plugins/`, never overwritten by hermes-agent upgrades |
| **Soul Guardian** | SOUL.md checksum protection — core identity cannot be tampered with |
| **7-Day Backup** | Built-in daily backup script with 7-day rotation |

---

## 📖 Documentation (Bilingual)

> 📄 **Chinese + English Bilingual Document:**
> https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf

The complete construction manual with both Chinese and English content.

---

## 📦 Installation

### One-Command Install (Recommended)

```bash
git clone https://github.com/alvinxie365/zhiji-memory.git
cd zhiji-memory
bash install.sh
```

### Manual Install

1. Copy `__init__.py`, `plugin.yaml`, `zhiji_memory_provider.py` to `~/.hermes/plugins/zhiji_memory/`
2. Add to `config.yaml`:
   ```yaml
   memory.provider: zhiji_memory
   ```
3. Restart hermes-agent

---

## 🏔️ Four Realms Architecture

| Realm | Ability | Description |
|-------|---------|-------------|
| **Qi Refining** | Soul Guardian + Tidal Waves | Automatically record every conversation |
| **Foundation Building** | Spirit Tower Self-Decision | Auto-identify key insights, precipitate to right domain |
| **Golden Core** | Spirit Sense Discovery | Build cross-domain connections, form knowledge network |
| **Primordial Infant** | Frontier Expansion | Break current boundaries, actively explore unknown areas |

---

## Five-Domain Architecture

```
Zhiji Sea (识海)
├── Soul Domain (soul)      — Core identity file SOUL.md checksum & protection
├── Skills Domain (skills)  — Precipitated methodology, reusable skills
├── Preferences Domain      — Work habits, aesthetic preferences
├── Events Domain           — Project progress, milestones
└── Evolution Domain       — Frontier expansion records, growth milestones
```

---

## 🔧 Configuration

### Enable the Plugin

```yaml
# ~/.hermes/config.yaml
memory.provider: zhiji_memory
```

### Daily Self-Backup (Recommended)

```bash
# Add cron job — runs at 2am daily
0 2 * * * bash ~/.hermes/scripts/afu-daily-backup.sh
```

---

## 📁 Directory Structure

```
zhiji-memory/
├── __init__.py                      # Plugin entry point
├── plugin.yaml                       # Plugin metadata
├── zhiji_memory_provider.py          # Core plugin code (~50KB)
├── install.sh                       # One-command install script
├── UNINSTALL.sh                     # Clean uninstall script
├── README.md                        # English version (this file)
├── README-zh.md                     # Chinese version
└── skill-sea-of-consciousness.md    # Skill document (knowledge transfer)
```

---

## 👤 About

- **Created by**: Xie Family · 阿福X (Alvin Xie)
- **Origin**: Endogenous evolution experiment of Xie Family Hermes Agent
- **Version**: v1.0.0
- **Chinese Doc**: https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf

---

## 🛡️ Backup Strategy

| Layer | Location | Protection |
|-------|----------|------------|
| **Daily Backup** | `~/Backup/afu-daily/` | 7-day rotation, local |
| **Plugin Backup** | `~/.hermes/sea/plugin_backup/` | Auto before every upgrade |
| **Restore Script** | `~/.hermes/sea/plugin_restore.sh` | One-command restore after upgrade |

---

## 🤝 Contributing

Issues and PRs welcome!

https://github.com/alvinxie365/zhiji-memory/issues

---

**"错亦成技，技递于远，日进无疆，久弥精诚"**

_"Error becomes skill; skill passes far; daily progress without limit; long-preserved sincerity."_
