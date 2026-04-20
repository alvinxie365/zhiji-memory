---
name: sea-of-consciousness
description: 谢家识海 v2.0 — 四境完整体系（炼气/筑基/金丹/元婴）
triggers:
  - 每次对话结束自动炼化
  - 新session开始前prefetch
  - 城主问“还记得什么”
  - 城主说“记住”
  - 识海提出新域开辟建议
---

# 识海体系 v2.0 — 四境完整

## 核心理念

识海不是仓库，是生命体。

> 识海不灭·抗升级永久法则：识海数据在 ~/.hermes/sea/，不在 hermes-agent/ 目录树，天然抗升级。

## 四境体系

### 炼气期：神魂稳固 + 识浪涌动

**SoulGuardian（神魂守护）**
- 启动时校验 SOUL.md MD5，损坏则自动从备份还原
- 每次 session 结束更新 checksum
- 备份只保留7份

**RawWaveLogger（识浪记录）**
- 每轮对话**无条件**写入 raw 日志（不漏一轮）
- 按天分割文件（waves_YYYYMMDD.jsonl）
- 每7天自动清理旧识浪
- 位置：~/.hermes/sea/raw_waves/

### 筑基期：灵台自决 + LLM炼化

**LingTaiRefiner（灵台自决）**
- 规则引擎做快速预筛（高质量对话才触发 LLM）
- 强信号直接触发（"你是谁"/"永远不要"等）
- 异步调用 LLM，不阻塞对话响应
- LLM 判断：是否值得沉淀、归属哪个域、是否覆盖旧认知

**DeepAlchemyEngine（深度炼化引擎）**
- 扫描 session 内所有对话轮次
- 找最核心领悟（不只是最好的单轮）
- 提炼整体主题和洞察

### 金丹期：神识初探 + 意图预判

**ShenShiPrefetcher（神识预判）**
- prefetch 时用 LLM 理解深层意图
- 主动判断城主这句话背后真正想问的是什么
- 主动加载相关域，不只是被动关键词匹配
- 无 LLM 时回退到关键词方式

### 元婴期：拓疆进化 + 自动生长

**FrontierDetector（拓疆探测）**
- 监测各域沉淀密度（某话题反复出现）
- 某话题在单域内沉淀超过5次，提议开辟新域
- 新域需要城主确认（sea_approve_frontier）后才开辟
- 自动维护域注册表（SEA_ROOT/domains/_registry.json）

## 运转机制

### 每轮对话结束（sync_turn）

1. **识浪涌动**：无条件写入 raw 日志（灵识如实映照）
2. **规则预筛**：判断是否触发 LLM 炼化
3. **异步炼化**：触发则后台调用 LLM（不阻塞）
4. **轻量炼化**：规则引擎保底沉淀
5. **拓疆检测**：判断是否需要新域
6. **定期深度炼化**：每10轮触发一次
7. **定期清理**：每100轮清理7天前的 raw 日志

### session结束（on_session_end）

1. 深度炼化整 session 对话
2. 更新 SOUL.md checksum
3. 清空 session 记录

### 新session开始（prefetch）

1. 判断是否触发神识（"为什么"/"怎么理解"等）
2. 触发则用 LLM 做深层意图理解
3. 不触发则用关键词快速判断
4. 相关沉淀自然浮现

## 域体系

### 核心五域（预设）

| 域 | 说明 |
|---|---|
| soul | 神魂根基 — 使命/原则/边界 |
| skill | 技能沉淀 — 学会的方法/工具 |
| pref | 城主偏好 — 习惯/风格/禁忌 |
| event | 事件记忆 — 做过的事/项目 |
| growth | 进化印记 — 领悟/洞察/突破 |

### 自动域（按需生长）

- topic_xxx 格式
- 由 FrontierDetector 提议
- 城主确认后开辟

## 工具

| 工具 | 说明 |
|---|---|
| sea_status | 查看识海状态、各域沉淀数、待确认新域 |
| sea_recall | 召回某域的沉淀记录 |
| sea_frontier | 查看拓疆提议 |
| sea_approve_frontier | 确认开辟新域 |

## 存储结构

```
~/.hermes/sea/
├── soul_checksum.txt       # SOUL.md MD5校验
├── raw_waves/             # 原始识浪（每日分割）
│   └── waves_YYYYMMDD.jsonl
├── domains/               # 五域沉淀
│   ├── _registry.json     # 域注册表（含拓疆提议）
│   ├── soul.json
│   ├── skill.json
│   ├── pref.json
│   ├── event.json
│   └── growth.json
└── backup/                # 备份
    ├── soul_YYYYMMDD_HHMMSS.md
    └── YYYYMMDD_HHMMSS/
```

## 触发关键词

**必须触发LLM炼化（强信号）：**
你是谁/你的使命/不能做/永远不要/禁止/核心原则/我的身份/记住这件事

**高质量对话（规则预筛）：**
城主/记住了/学会了/搞懂了/不对/不是这样/以后都/从来都/满意/不满意/谢谢/这就是/原来/我明白了/不要

**触发神识深层prefetch：**
为什么/怎么理解/是什么意思/帮我分析/你觉得/应该怎么做/有什么建议/我想要/我想知道

## 下一步进化方向

1. **神魂写入守护**：当 SOUL.md 被修改时自动检测并提示城主确认
2. **识浪精华提炼**：定期从 raw_waves 中提炼精华（超过7天的 raw 可以做深度理解）
3. **跨session神识**：跨 session 追踪城主意图（同一个项目多次对话串联）
4. **域自动进化**：某域内容过多时自动拆分为子域

---

## 运维要点（v2.1 补充）

### 依赖的环境变量

| 变量 | 说明 |
|---|---|
| `MINIMAX_API_BASE` | LLM API 基础地址，如 `https://api.minimaxi.com/v1` |
| `MINIMAX_API_KEY` / `MINIMAX_PORTAL_API_KEY` | API Key，按优先级自动选用 |

### 初始化流程

插件加载时自动执行：
1. `ensure_dirs()` — 创建所有必要的目录和文件
2. 域文件不存在时自动创建空数组
3. `_registry.json` 不存在时自动初始化
4. `SoulGuardian.auto_backup_if_needed()` — 检查是否需要备份 SOUL.md

### 拓疆计数器重置

**关键规则**：提议开辟新域后，对应话题的计数器必须归零。

如果计数器没有归零，同一话题会持续触发重复提议。

计数器在以下时机归零：
- 城主确认开辟新域后
- 城主拒绝提议后

### 故障自检清单

```bash
# 1. 检查域文件是否存在
ls ~/.hermes/sea/domains/

# 2. 检查域注册表
cat ~/.hermes/sea/domains/_registry.json

# 3. 检查 SOUL.md checksum
cat ~/.hermes/sea/soul_checksum.txt

# 4. 查看是否有待确认的拓疆提议
# 调用 sea_frontier 工具

# 5. 手动触发 SOUL.md 备份
python3 -c "
import sys
sys.path.insert(0, '~/.hermes/hermes-agent')
from plugins.memory.zhiji_memory.zhiji_memory_provider import SoulGuardian
SoulGuardian.backup_soul()
"
```
