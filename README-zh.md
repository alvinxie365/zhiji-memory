# 🔮 识海 · Zhiji Memory

> _"记忆不是存储与检索，而是沉淀与生长。"_

识海是 Hermes Agent 的内生记忆系统，替代旧的 RAG/向量搜索，以"神魂稳固 + 识浪涌动 + 沉淀生长"为核心，让 AI 在每次对话中自动成长。

**由谢家打造 · https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf**

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **五域分离** | 神魂、技能、偏好、事件、进化各自独立存储 |
| **事件驱动** | 无需手动触发，每次对话自动记录 |
| **四境进化** | 炼气→筑基→金丹→元婴，逐层生长 |
| **升级安全** | 插件放在 `~/.hermes/plugins/`，不被 hermes-agent 升级覆盖 |
| **神魂守护** | SOUL.md 文件校验，保护核心身份不被篡改 |
| **7天循环备份** | 内置每日自备份脚本 |

---

## 📖 文档（中英双语）

> 📄 **中英双语完整建造手册：**
> https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf

---

## 📦 安装

### 一键安装（推荐）

```bash
git clone https://github.com/alvinxie365/zhiji-memory.git
cd zhiji-memory
bash install.sh
```

### 手动安装

1. 把 `__init__.py`、`plugin.yaml`、`zhiji_memory_provider.py` 三个文件复制到 `~/.hermes/plugins/zhiji_memory/`
2. 在 `config.yaml` 中添加：
   ```yaml
   memory.provider: zhiji_memory
   ```
3. 重启 hermes-agent

---

## 🏔️ 四境体系

| 境界 | 能力 | 说明 |
|------|------|------|
| **炼气期** | 神魂稳固 + 识浪涌动 | 每次对话自动记录，不遗漏重要交互 |
| **筑基期** | 灵台自决 | 自动识别关键领悟，沉淀到对应域 |
| **金丹期** | 神识初探 | 建立域间连接，形成知识网络 |
| **元婴期** | 拓疆进化 | 突破当前边界，主动探索未知领域 |

---

## 五域架构

```
识海
├── 神魂域（soul）     — 核心身份文件 SOUL.md 的校验和保护
├── 技能域（skills）   — 沉淀的方法论、可复用技能
├── 偏好域（preferences）— 城主的工作习惯、审美偏好
├── 事件域（events）   — 项目进展、里程碑
└── 进化域（evolution） — 拓疆记录、成长里程碑
```

---

## 🔧 配置

### 启用识海插件

```yaml
# ~/.hermes/config.yaml
memory.provider: zhiji_memory
```

### 每日自备份（推荐）

```bash
# 添加 cron 任务，每天凌晨2点自动备份
0 2 * * * bash ~/.hermes/scripts/afu-daily-backup.sh
```

---

## 📁 目录结构

```
zhiji-memory/
├── __init__.py                      # 插件入口
├── plugin.yaml                       # 插件元信息
├── zhiji_memory_provider.py          # 核心插件代码（~50KB）
├── install.sh                       # 一键安装脚本
├── UNINSTALL.sh                     # 卸载脚本
├── README.md                        # 英文版
├── README-zh.md                    # 中文版（本文件）
└── skill-sea-of-consciousness.md    # Skill 文档（知识传递）
```

---

## 👤 关于

- **作者**：谢家·阿福X（Alvin Xie）
- **来源**：谢家 Hermes Agent 的内生进化实验
- **版本**：v1.0.0
- **中英双语文档**：https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf

---

## 🛡️ 备份策略

| 层次 | 位置 | 保护 |
|------|------|------|
| **每日备份** | `~/Backup/afu-daily/` | 7天循环，本地 |
| **插件备份** | `~/.hermes/sea/plugin_backup/` | 升级前自动备份 |
| **还原脚本** | `~/.hermes/sea/plugin_restore.sh` | 升级后一键还原 |

---

## 🤝 问题反馈

https://github.com/alvinxie365/zhiji-memory/issues

---

**"错亦成技，技递于远，日进无疆，久弥精诚"**
