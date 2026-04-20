"""谢家识海插件 — Zhiji Sea Memory Provider v2.0

四境体系：
- 炼气期：神魂稳固 + 识浪涌动
- 筑基期：灵台自决 + LLM炼化
- 金丹期：神识初探 + 意图预判
- 元婴期：拓疆进化 + 自动生长

每次对话结束，自动炼化行过留痕。
识浪自然沉淀，新旧相连生长。
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import shutil
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agent.memory_provider import MemoryProvider

logger = logging.getLogger(__name__)

# ============================================================================
# 路径配置
# ============================================================================

SEA_ROOT = Path.home() / ".hermes" / "sea"
DOMAINS_DIR = SEA_ROOT / "domains"
BACKUP_DIR = SEA_ROOT / "backup"
SOUL_PATH = Path.home() / ".hermes" / "SOUL.md"
RAW_WAVES_DIR = SEA_ROOT / "raw_waves"
SOUL_BACKUP_PREFIX = "soul_"

# 识海域定义
DOMAIN_SOUL = "soul"        # 神魂根基 — 使命/边界/核心原则
DOMAIN_SKILL = "skill"      # 技能沉淀 — 学会的事情
DOMAIN_PREF = "pref"        # 城主偏好 — 习惯/风格/禁忌
DOMAIN_EVENT = "event"      # 事件记忆 — 做过的事情/项目
DOMAIN_GROWTH = "growth"    # 进化印记 — 领悟/洞察/突破

ALL_DOMAINS = [DOMAIN_SOUL, DOMAIN_SKILL, DOMAIN_PREF, DOMAIN_EVENT, DOMAIN_GROWTH]

# ============================================================================
# 第一境：神魂稳固 — SoulGuardian
# ============================================================================

class SoulGuardian:
    """
    神魂守护者 — 确保 SOUL.md 永远稳固。

    机制：
    - 启动时校验完整性（MD5）
    - 每次修改前自动备份
    - 损坏检测 + 自动从最新备份还原
    - 备份只保留7份
    - 自动备份：每次 session 开始时检查是否需要备份（超过24小时未备份则自动备份）
    """

    SOUL_CHECKSUM_FILE = SEA_ROOT / "soul_checksum.txt"
    SOUL_BACKUP_INTERVAL_SECONDS = 86400  # 24小时

    # 上次备份时间记录
    LAST_BACKUP_FILE = SEA_ROOT / "last_soul_backup.txt"

    @classmethod
    def get_last_backup_time(cls) -> float:
        """获取上次备份时间戳"""
        if cls.LAST_BACKUP_FILE.exists():
            try:
                return float(cls.LAST_BACKUP_FILE.read_text().strip())
            except Exception:
                pass
        return 0

    @classmethod
    def set_last_backup_time(cls, timestamp: float):
        """记录备份时间"""
        cls.LAST_BACKUP_FILE.write_text(str(timestamp))

    @classmethod
    def should_auto_backup(cls) -> bool:
        """检查是否需要自动备份（超过24小时未备份）"""
        import os
        if not SOUL_PATH.exists():
            return False
        last_backup = cls.get_last_backup_time()
        if last_backup == 0:
            return True  # 从未备份过
        import time
        return (time.time() - last_backup) > cls.SOUL_BACKUP_INTERVAL_SECONDS

    @classmethod
    def auto_backup_if_needed(cls) -> bool:
        """自动备份（如果超过24小时未备份）"""
        if not cls.should_auto_backup():
            return False
        result = cls.backup_soul()
        if result:
            import time
            cls.set_last_backup_time(time.time())
        return bool(result)

    @classmethod
    def verify_soul(cls) -> Tuple[bool, str]:
        """校验 SOUL.md 完整性，返回 (是否正常, 状态信息)"""
        if not SOUL_PATH.exists():
            return False, "⚠️ 神魂文件缺失"

        try:
            current = SOUL_PATH.read_text(encoding="utf-8")
            current_hash = hashlib.md5(current.encode("utf-8")).hexdigest()

            if cls.SOUL_CHECKSUM_FILE.exists():
                saved_hash = cls.SOUL_CHECKSUM_FILE.read_text(encoding="utf-8").strip()
                if current_hash != saved_hash:
                    return False, f"⚠️ 神魂已被修改（未授权）"
                return True, "✅ 神魂稳固"
            else:
                # 首次，启动时写入 checksum
                cls.SOUL_CHECKSUM_FILE.write_text(current_hash, encoding="utf-8")
                return True, "✅ 神魂初始化完成"
        except Exception as e:
            return False, f"⚠️ 神魂读取异常: {e}"

    @classmethod
    def backup_soul(cls) -> Optional[Path]:
        """修改前备份 SOUL.md，返回备份路径"""
        if not SOUL_PATH.exists():
            return None
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{SOUL_BACKUP_PREFIX}{timestamp}.md"
            backup_path = BACKUP_DIR / backup_name
            shutil.copy2(SOUL_PATH, backup_path)

            # 清理旧备份，只保留7份
            soul_backups = sorted(
                [p for p in BACKUP_DIR.iterdir() if p.name.startswith(SOUL_BACKUP_PREFIX)],
                key=lambda p: p.name
            )
            for old in soul_backups[:-7]:
                old.unlink()

            return backup_path
        except Exception as e:
            logger.warning("[神魂守护] 备份失败: %s", e)
            return None

    @classmethod
    def restore_soul(cls) -> bool:
        """从最新备份还原 SOUL.md"""
        soul_backups = sorted(
            [p for p in BACKUP_DIR.iterdir() if p.name.startswith(SOUL_BACKUP_PREFIX)],
            key=lambda p: p.name,
            reverse=True
        )
        if not soul_backups:
            return False
        try:
            latest = soul_backups[0]
            shutil.copy2(latest, SOUL_PATH)
            # 更新 checksum
            current = SOUL_PATH.read_text(encoding="utf-8")
            cls.SOUL_CHECKSUM_FILE.write_text(
                hashlib.md5(current.encode("utf-8")).hexdigest(),
                encoding="utf-8"
            )
            logger.info("[神魂守护] 从 %s 还原神魂", latest.name)
            return True
        except Exception as e:
            logger.error("[神魂守护] 还原失败: %s", e)
            return False

    @classmethod
    def protect_soul(cls):
        """
        启动时调用：检测并修复损坏的 SOUL.md。
        这是识海的第一口呼吸。
        """
        is_valid, status = cls.verify_soul()
        if is_valid:
            logger.info("[神魂守护] %s", status)
        else:
            logger.warning("[神魂守护] %s，尝试还原...", status)
            if cls.restore_soul():
                logger.info("[神魂守护] 神魂已还原")
            else:
                logger.error("[神魂守护] 无法还原，神魂丢失")

    @classmethod
    def on_soul_modified(cls):
        """当 SOUL.md 被修改时调用：更新 checksum"""
        if SOUL_PATH.exists():
            try:
                content = SOUL_PATH.read_text(encoding="utf-8")
                cls.SOUL_CHECKSUM_FILE.write_text(
                    hashlib.md5(content.encode("utf-8")).hexdigest(),
                    encoding="utf-8"
                )
            except Exception as e:
                logger.warning("[神魂守护] checksum更新失败: %s", e)


# ============================================================================
# 第一境：识浪涌动 — RawWaveLogger
# ============================================================================

class RawWaveLogger:
    """
    识浪记录器 — 每轮对话都写，不漏一轮。

    机制：
    - 每轮对话无条件写入 raw 日志（灵识如实映照）
    - 日志文件按天分割（每天一个文件）
    - 不做提炼判断，只做原始记录
    - 定期清理旧 raw 日志（每7天前的）
    """

    MAX_RAW_AGE_DAYS = 7

    @classmethod
    def log_turn(cls, user: str, assistant: str, session_id: str = ""):
        """写入一轮识浪"""
        try:
            RAW_WAVES_DIR.mkdir(parents=True, exist_ok=True)
            today = datetime.now().strftime("%Y%m%d")
            wave_file = RAW_WAVES_DIR / f"waves_{today}.jsonl"

            record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session": session_id,
                "user": user[:500] if user else "",
                "assistant": assistant[:2000] if assistant else "",
            }
            with open(wave_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning("[识浪] 写入失败: %s", e)

    @classmethod
    def cleanup_old_waves(cls):
        """清理超过7天的旧识浪"""
        try:
            cutoff = datetime.now().timestamp() - cls.MAX_RAW_AGE_DAYS * 86400
            for wave_file in RAW_WAVES_DIR.glob("waves_*.jsonl"):
                if wave_file.stat().st_mtime < cutoff:
                    wave_file.unlink()
                    logger.info("[识浪] 清理旧识浪: %s", wave_file.name)
        except Exception as e:
            logger.warning("[识浪] 清理失败: %s", e)


# ============================================================================
# 第二境：灵台自决 — LingTaiRefiner（异步LLM炼化）
# ============================================================================

class LingTaiRefiner:
    """
    灵台自决 — 用LLM做炼化判断。

    机制：
    - 不依赖规则引擎做域判断，用 LLM 理解真正的意图
    - 异步调用，不阻塞对话响应
    - 规则引擎做快速预筛，高质量对话才触发 LLM
    - LLM 判断：是否值得沉淀、归属哪个域、是否覆盖旧认知
    """

    # 触发 LLM 炼化的"高质量对话"条件（规则预筛）
    HIGH_QUALITY_SIGNALS = [
        "城主", "记住了", "学会了", "搞懂了", "不对", "不是这样",
        "以后都", "从来都", "满意", "不满意", "谢谢", "不对",
        "这就是", "原来", "我明白了", "不要", "不要再",
    ]

    # 必须触发 LLM 的强信号（不管多短都要炼化）
    FORCE_LLM_SIGNALS = [
        "你是谁", "你的使命", "不能做", "永远不要", "禁止",
        "核心原则", "我的身份", "记住这件事",
    ]

    # LLM API 配置（通用 OpenAI-compatible 接口）
    # 支持任意 OpenAI-compatible 后端：OpenAI / Claude / Ollama / ClaudeCode 等
    # API Key 优先级：ZHIJI_LLM_API_KEY > OPENAI_API_KEY > MINIMAX_API_KEY > ...
    @classmethod
    def _get_api_key(cls) -> Optional[str]:
        import os
        return (
            os.getenv("ZHIJI_LLM_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("MINIMAX_API_KEY")
            or os.getenv("MINIMAX_PORTAL_API_KEY")
            or os.getenv("MINIMAX_API_KEY_2")
            or os.getenv("ANTHROPIC_API_KEY")
        )

    @classmethod
    def _get_api_base(cls) -> str:
        import os
        return os.getenv("ZHIJI_LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or os.getenv("MINIMAX_API_BASE") or "https://api.minimaxi.com/v1"

    @classmethod
    def _get_model(cls) -> str:
        import os
        return os.getenv("ZHIJI_LLM_MODEL") or os.getenv("OPENAI_MODEL") or "MiniMax-Text-01"

    @classmethod
    def should_refine(cls, user: str, assistant: str) -> bool:
        """快速预筛：判断是否值得触发炼化"""
        if not user:
            return False
        text = f"{user} {assistant}"
        # 强信号直接触发
        if any(s in text for s in cls.FORCE_LLM_SIGNALS):
            return True
        # 高质量信号触发
        return any(s in text for s in cls.HIGH_QUALITY_SIGNALS)

    @classmethod
    def refine_async(cls, user: str, assistant: str, session_id: str, provider_ref):
        """
        异步触发 LLM 炼化（后台线程，不阻塞对话）。
        """
        def _do_refine():
            try:
                result = cls._llm_refine(user, assistant, session_id)
                if result and result.get("has_insight"):
                    provider_ref._persist_llm_result(result)
                    logger.info("[灵台] LLM炼化入库: %s", result.get("summary", "")[:40])
            except Exception as e:
                logger.warning("[灵台] LLM炼化失败: %s", e)

        thread = threading.Thread(target=_do_refine, daemon=True)
        thread.start()

    @classmethod
    def _llm_refine(cls, user: str, assistant: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        调用 LLM 做深度炼化判断。
        """
        api_key = cls._get_api_key()
        if not api_key:
            logger.debug("[灵台] 未配置LLM API Key，跳过LLM炼化")
            return None

        # 组装 prompt
        prompt = f"""你是谢家识海的灵台主控。

对话内容：
用户：{user[:300]}
助手：{assistant[:800]}

请判断：
1. 这轮对话是否有重要领悟值得沉淀到识海？（是/否）
2. 如果是，应该沉淀到哪个域？
   - soul（神魂根基）：使命/原则/边界/身份
   - skill（技能沉淀）：学会了方法/工具/流程
   - pref（城主偏好）：喜欢/不喜欢/习惯/风格
   - event（事件记忆）：具体项目/任务/做过的事
   - growth（进化印记）：领悟/洞察/认知突破

3. 这轮对话的核心领悟是什么？（用一句话概括）

4. 是否需要覆盖之前的某个认知？（是/否，如果是，说出之前认知的大致内容）

请直接返回JSON格式：
{{"has_insight": true/false, "domain": "xxx", "summary": "一句话概括", "detail": "详细说明", "tags": ["标签1", "标签2"], "overwrites": "如果需要覆盖，说出旧认知内容"}}
"""

        try:
            import urllib.request
            import urllib.error

            payload = {
                "model": cls._get_model(),
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500,
            }

            req = urllib.request.Request(
                cls._get_api_base(),
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=15) as resp:
                result_data = json.loads(resp.read().decode("utf-8"))
                content = result_data.get("choices", [{}])[0].get("message", {}).get("content", "{}")

            # 解析 LLM 返回
            # 尝试从 markdown 代码块中提取
            json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            refine_result = json.loads(content)

            # 验证域有效性
            if refine_result.get("domain") not in ALL_DOMAINS:
                refine_result["domain"] = DOMAIN_GROWTH

            return refine_result

        except Exception as e:
            logger.warning("[灵台] LLM调用失败: %s", e)
            return None


# ============================================================================
# 第二境：深度炼化引擎（筑基期）
# ============================================================================

class DeepAlchemyEngine:
    """
    深度炼化引擎 — 把多轮对话串联成整体领悟。

    机制：
    - 扫描 session 内所有对话轮次
    - 找最核心的领悟（不只是最好的单轮）
    - 提炼整体主题和洞察
    - 打标签标记为"深度炼化"
    """

    @staticmethod
    def deep_refine(turns: List[Dict[str, str]], session_id: str) -> Optional[Dict[str, Any]]:
        """
        深度炼化多轮对话。

        Returns: {
            "has_insight": bool,
            "domain": str,
            "summary": str,
            "detail": str,
            "tags": List[str],
        }
        """
        if not turns:
            return None

        # 合成完整对话文本
        full_text = ""
        for turn in turns:
            full_text += f"用户: {turn['user']}\n助手: {turn['assistant']}\n\n"

        if len(full_text) < 20:
            return None

        # 扫描每轮，找最强领悟
        best = None
        best_score = 0

        engine = AlchemyEngine()
        for turn in turns:
            result = engine.refine(turn["user"], turn["assistant"], session_id)
            if result.get("has_insight"):
                score = len(result.get("detail", "")) + len(result.get("tags", [])) * 15
                if score > best_score:
                    best_score = score
                    best = result

        if best:
            best["tags"] = list(set(best.get("tags", [])))
            if len(turns) > 2:
                best["tags"].append("多轮深度炼化")

        return best


# ============================================================================
# 第三境：神识初探 — ShenShiPrefetcher
# ============================================================================

class ShenShiPrefetcher:
    """
    神识初探 — prefetch 时的深层意图理解。

    机制：
    - 不只做关键词匹配，用 LLM 理解深层意图
    - 主动判断城主这句话背后真正想问的是什么
    - 主动加载相关域，不只是被动匹配
    """

    # 触发神识的关键词（触发时才用 LLM 做深层理解）
    SHENSHI_TRIGGERS = [
        "为什么", "怎么理解", "是什么意思", "帮我分析",
        "你觉得", "你觉得我", "应该怎么做", "有什么建议",
        "我想要", "我想知道", "我的问题是",
    ]

    @classmethod
    def should_deep_prefetch(cls, query: str) -> bool:
        """判断是否需要神识深层预判"""
        if not query:
            return False
        return any(t in query for t in cls.SHENSHI_TRIGGERS)

    @classmethod
    def deep_prefetch(cls, query: str, session_id: str = "") -> Dict[str, Any]:
        """
        用 LLM 做深层 prefetch 理解。

        Returns: {
            "intention": str,           # 城主真正想问的
            "domains_to_load": List[str],  # 应该加载哪些域
            "context_hints": List[str],    # 给模型的上下文提示
        }
        """
        api_key = LingTaiRefiner._get_api_key()
        api_base = LingTaiRefiner._get_api_base()
        if not api_key:
            return cls._keyword_prefetch(query)

        try:
            import urllib.request

            prompt = f"""你是谢家识海的神识。

城主说："{query}"

请深层理解：
1. 城主这句话背后真正想问的是什么？（真正意图）
2. 为了回答这个问题，识海应该提供哪些域的记忆？
   - soul（神魂根基）：使命/原则/边界
   - skill（技能沉淀）：工具/方法/流程
   - pref（城主偏好）：习惯/风格/偏好
   - event（事件记忆）：项目/任务/做过的事
   - growth（进化印记）：领悟/洞察/认知

请返回JSON格式：
{{"intention": "真正意图", "domains_to_load": ["domain1", "domain2"], "context_hints": ["提示1", "提示2"]}}
"""

            payload = {
                "model": cls._get_model(),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 300,
            }

            req = urllib.request.Request(
                LingTaiRefiner._get_api_base(),
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=10) as resp:
                result_data = json.loads(resp.read().decode("utf-8"))
                content = result_data.get("choices", [{}])[0].get("message", {}).get("content", "{}")

            json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            return json.loads(content)

        except Exception as e:
            logger.warning("[神识] 深层prefetch失败: %s，回退到关键词", e)
            return cls._keyword_prefetch(query)

    @classmethod
    def _keyword_prefetch(cls, query: str) -> Dict[str, Any]:
        """关键词回退方案"""
        lower_q = query.lower()
        domains = []

        if any(k in lower_q for k in ["喜欢", "风格", "偏好", "审美", "不要", "从来都"]):
            domains.append(DOMAIN_PREF)
        if any(k in lower_q for k in ["怎么", "如何", "方法", "工具", "skill"]):
            domains.append(DOMAIN_SKILL)
        if any(k in lower_q for k in ["项目", "视频", "报告", "ORRDT", "九舟", "生成"]):
            domains.append(DOMAIN_EVENT)
        if any(k in lower_q for k in ["你是谁", "你的", "不能", "禁止", "永远"]):
            domains.append(DOMAIN_SOUL)

        if not domains:
            domains = [DOMAIN_GROWTH, DOMAIN_SKILL]

        return {
            "intention": query,
            "domains_to_load": list(set(domains)),
            "context_hints": [],
        }


# ============================================================================
# 第四境：拓疆进化 — FrontierDetector
# ============================================================================

class FrontierDetector:
    """
    拓疆探测 — 检测识海是否需要开辟新域。

    机制：
    - 监测各域的沉淀密度（某话题反复出现）
    - 当某话题超过阈值，提议开辟新域
    - 新域需要城主确认后开辟
    - 自动维护域注册表（SEA_ROOT/domains/_registry.json）
    """

    REGISTRY_FILE = SEA_ROOT / "domains" / "_registry.json"

    # 触发开辟新域的阈值：某话题在单个域内沉淀超过此数
    DOMAIN_TOPIC_THRESHOLD = 5

    # 新域注册表结构
    @classmethod
    def get_registry(cls) -> Dict[str, Any]:
        if cls.REGISTRY_FILE.exists():
            try:
                return json.loads(cls.REGISTRY_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "domains": {d: {"created": datetime.now(timezone.utc).isoformat(), "topic_count": {}}
                        for d in ALL_DOMAINS},
            "proposed": [],
        }

    @classmethod
    def save_registry(cls, registry: Dict[str, Any]):
        """保存域注册表"""
        cls.REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        cls.REGISTRY_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def detect_frontier(cls, refinement_result: Dict[str, Any]) -> Optional[str]:
        """
        检测是否需要开辟新域。

        当某话题在某域内反复出现超过阈值，提出开辟新域建议。
        """
        if not refinement_result or not refinement_result.get("has_insight"):
            return None

        registry = cls.get_registry()
        domain = refinement_result.get("domain", "")
        summary = refinement_result.get("summary", "")
        tags = refinement_result.get("tags", [])

        # 提取话题关键词
        topic_words = [t for t in tags if t not in ALL_DOMAINS]
        if not topic_words:
            return None

        for topic in topic_words:
            domain_stats = registry["domains"].get(domain, {})
            topic_count = domain_stats.get("topic_count", {})

            current_count = topic_count.get(topic, 0) + 1
            topic_count[topic] = current_count

            if current_count == cls.DOMAIN_TOPIC_THRESHOLD:
                # 触发阈值，建议开辟新域
                new_domain_name = f"topic_{topic}"
                if new_domain_name not in registry["domains"]:
                    proposal = {
                        "suggested_name": new_domain_name,
                        "topic": topic,
                        "reason": f"'{topic}'在{domain}域内已沉淀{cls.DOMAIN_TOPIC_THRESHOLD}次",
                        "suggested_at": datetime.now(timezone.utc).isoformat(),
                    }
                    if proposal not in registry["proposed"]:
                        registry["proposed"].append(proposal)
                        # 重置该话题的计数器，防止重复提议
                        topic_count[topic] = 0
                        cls.save_registry(registry)
                        return topic

            registry["domains"][domain]["topic_count"] = topic_count

        cls.save_registry(registry)
        return None

    @classmethod
    def get_pending_proposals(cls) -> List[Dict[str, Any]]:
        """获取待确认的新域开辟提议"""
        return cls.get_registry().get("proposed", [])

    @classmethod
    def approve_proposal(cls, proposal: Dict[str, Any]) -> bool:
        """
        城主确认开辟新域。
        """
        registry = cls.get_registry()
        new_name = proposal.get("suggested_name")
        if not new_name:
            return False

        # 添加新域
        registry["domains"][new_name] = {
            "created": datetime.now(timezone.utc).isoformat(),
            "topic_count": {},
            "origin_topic": proposal.get("topic"),
            "auto_created": True,
        }

        # 移除提议
        registry["proposed"] = [p for p in registry["proposed"]
                                if p.get("suggested_name") != new_name]

        # 创建新域文件
        new_domain_file = DOMAINS_DIR / f"{new_name}.json"
        new_domain_file.write_text("[]", encoding="utf-8")

        cls.save_registry(registry)
        logger.info("[拓疆] 新域开辟: %s", new_name)
        return True

    @classmethod
    def reject_proposal(cls, proposal: Dict[str, Any]):
        """城主拒绝开辟新域"""
        registry = cls.get_registry()
        registry["proposed"] = [p for p in registry["proposed"]
                                if p.get("suggested_name") != proposal.get("suggested_name")]
        cls.save_registry(registry)


# ============================================================================
# 基础炼化引擎 — AlchemyEngine（保留，兼容旧逻辑）
# ============================================================================

class AlchemyEngine:
    """炼化引擎：把对话炼成识海沉淀（规则引擎版，保留作为预筛和备用）"""

    def __init__(self):
        self.master_signals = [
            "城主", "谢孝苗", "满意", "不对", "不是这样",
            "记住了", "不要再", "以后都", "从来都", "以后不要",
        ]
        self.insight_signals = [
            "学会了", "原来是这样", "我现在明白了", "这次搞懂了",
            "下次不会了", "不会再犯", "记住了", "这就是",
        ]
        self.correction_signals = [
            "不对", "不是这样", "错了", "应该", "不是",
            "从来没有", "不要", "不要再",
        ]

    def refine(self, user_message: str, assistant_response: str, session_id: str = "") -> Dict[str, Any]:
        text = f"{user_message}\n{assistant_response}"
        lower_text = text.lower()

        is_master = any(signal in user_message for signal in self.master_signals)
        has_insight = any(signal in text for signal in self.insight_signals)
        has_correction = any(signal in text for signal in self.correction_signals)

        if not is_master and not has_insight and not has_correction:
            return {"has_insight": False, "domain": "", "summary": "", "detail": "", "tags": [], "connections": [], "overwrites": None}

        domain = self._classify_domain(text, lower_text, user_message)
        summary = self._extract_summary(user_message, assistant_response, domain, has_insight, has_correction)
        detail = self._extract_detail(text, domain, has_insight, has_correction)
        tags = self._extract_tags(text, lower_text, domain)
        connections = self._find_connections(domain, summary, text)
        overwrites = self._find_overwrite(domain, summary, has_correction)

        return {
            "has_insight": True,
            "domain": domain,
            "summary": summary,
            "detail": detail,
            "tags": tags,
            "connections": connections,
            "overwrites": overwrites,
        }

    def _classify_domain(self, text: str, lower_text: str, user_message: str) -> str:
        soul_keywords = ["我是谁", "我的使命", "核心原则", "不能做", "永远不要", "必须", "禁止"]
        if any(k in text for k in soul_keywords):
            return DOMAIN_SOUL

        pref_keywords = ["喜欢", "不喜欢", "以后都", "从来都", "不要", "风格", "偏好", "审美"]
        if any(k in user_message for k in pref_keywords):
            return DOMAIN_PREF

        skill_keywords = ["学会了", "搞懂了", "这次搞", "方法", "流程", "skill"]
        if any(k in text for k in skill_keywords):
            return DOMAIN_SKILL

        event_keywords = ["项目", "视频", "报告", "生成", "制作", "完成", "做了"]
        if any(k in lower_text for k in event_keywords):
            return DOMAIN_EVENT

        return DOMAIN_GROWTH

    def _extract_summary(self, user: str, assistant: str, domain: str, has_insight: bool, has_correction: bool) -> str:
        user_stripped = user.strip()
        if len(user_stripped) <= 60:
            summary = user_stripped
        else:
            summary = user_stripped[:57] + "..."
        if has_insight:
            summary = f"✨ {summary}"
        if has_correction:
            summary = f"⚡ {summary}"
        return summary

    def _extract_detail(self, text: str, domain: str, has_insight: bool, has_correction: bool) -> str:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        key_lines = []
        for line in lines:
            if len(line) > 200:
                line = line[:197] + "..."
            key_lines.append(line)
        detail = " | ".join(key_lines[:5])
        if len(detail) > 800:
            detail = detail[:797] + "..."
        return detail

    def _extract_tags(self, text: str, lower_text: str, domain: str) -> List[str]:
        tags = [domain]
        tag_map = {
            "偏好": ["喜欢", "不喜欢", "风格", "偏好", "审美"],
            "领悟": ["学会了", "明白了", "搞懂了", "原来", "这就是"],
            "纠正": ["不对", "不是", "错了", "应该", "不要"],
            "技术": ["代码", "工具", "API", "skill", "插件"],
            "品牌": ["ORRDT", "九舟", "品牌", "视频", "图片"],
        }
        for tag, keywords in tag_map.items():
            if any(k in lower_text for k in keywords):
                tags.append(tag)
        return list(set(tags))[:5]

    def _find_connections(self, domain: str, summary: str, text: str) -> List[str]:
        connections = []
        domain_file = DOMAINS_DIR / f"{domain}.json"
        if not domain_file.exists():
            return connections
        try:
            with open(domain_file, "r", encoding="utf-8") as f:
                items = json.load(f)
            summary_words = set(summary.lower().split())
            for item in items[-10:]:
                item_words = set(item.get("summary", "").lower().split())
                overlap = summary_words & item_words
                if len(overlap) >= 2:
                    connections.append(item.get("id", ""))
        except Exception:
            pass
        return connections

    def _find_overwrite(self, domain: str, summary: str, has_correction: bool) -> Optional[str]:
        if not has_correction:
            return None
        domain_file = DOMAINS_DIR / f"{domain}.json"
        if not domain_file.exists():
            return None
        try:
            with open(domain_file, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in reversed(items):
                if item.get("overwritten_by"):
                    continue
                if any(k in item.get("summary", "") for k in ["学会了", "✨", "⚡"]):
                    return item.get("id", "")
        except Exception:
            pass
        return None


# ============================================================================
# 沉淀存储 — SeaStore
# ============================================================================

class SeaStore:
    """沉淀存储：管理各域的沉淀文件"""

    @staticmethod
    def ensure_dirs():
        SEA_ROOT.mkdir(parents=True, exist_ok=True)
        DOMAINS_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        # 确保所有核心域文件存在（防止加载异常）
        for domain in ALL_DOMAINS:
            domain_file = DOMAINS_DIR / f"{domain}.json"
            if not domain_file.exists():
                domain_file.write_text("[]", encoding="utf-8")

        # 初始化域注册表
        if not FrontierDetector.REGISTRY_FILE.exists():
            FrontierDetector.save_registry({
                "domains": {
                    d: {"created": datetime.now(timezone.utc).isoformat(), "topic_count": {}}
                    for d in ALL_DOMAINS
                },
                "proposed": [],
            })

    @staticmethod
    def load_domain(domain: str) -> List[Dict[str, Any]]:
        domain_file = DOMAINS_DIR / f"{domain}.json"
        if not domain_file.exists():
            return []
        try:
            with open(domain_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def save_domain(domain: str, items: List[Dict[str, Any]]):
        domain_file = DOMAINS_DIR / f"{domain}.json"
        with open(domain_file, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    @staticmethod
    def add_item(domain: str, item: Dict[str, Any]) -> str:
        items = SeaStore.load_domain(domain)
        item_id = f"{domain}_{int(time.time()*1000)}"
        item["id"] = item_id
        item["created_at"] = datetime.now(timezone.utc).isoformat()
        item["overwritten_by"] = None
        items.append(item)
        SeaStore.save_domain(domain, items)
        return item_id

    @staticmethod
    def overwrite_item(domain: str, item_id: str, new_item: Dict[str, Any]):
        items = SeaStore.load_domain(domain)
        for item in items:
            if item.get("id") == item_id:
                item["overwritten_by"] = new_item.get("id", "")
                break
        SeaStore.save_domain(domain, items)
        SeaStore.add_item(domain, new_item)

    @staticmethod
    def backup():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = BACKUP_DIR / timestamp
        backup_subdir.mkdir(parents=True, exist_ok=True)

        for domain in ALL_DOMAINS:
            src = DOMAINS_DIR / f"{domain}.json"
            if src.exists():
                dst = backup_subdir / f"{domain}.json"
                with open(src, "r", encoding="utf-8") as sf:
                    with open(dst, "w", encoding="utf-8") as df:
                        df.write(sf.read())

        backups = sorted(BACKUP_DIR.iterdir(), key=lambda p: p.name)
        for old in backups[:-10]:
            import shutil
            shutil.rmtree(old)

    @staticmethod
    def get_latest(domain: str, limit: int = 5) -> List[Dict[str, Any]]:
        items = SeaStore.load_domain(domain)
        active = [i for i in items if not i.get("overwritten_by")]
        return active[-limit:]

    @staticmethod
    def get_all_registered_domains() -> List[str]:
        """获取所有已注册的域（包括auto_created的）"""
        try:
            registry = FrontierDetector.get_registry()
            return list(registry.get("domains", {}).keys())
        except Exception:
            return ALL_DOMAINS


# ============================================================================
# 主Provider — ZhijiMemoryProvider v2.0
# ============================================================================

class ZhijiMemoryProvider(MemoryProvider):
    """
    谢家识海插件 v2.0 — 四境完整体系

    四境机制：
    - 炼气期：神魂稳固(SoulGuardian) + 识浪涌动(RawWaveLogger)
    - 筑基期：灵台自决(LingTaiRefiner) + LLM炼化
    - 金丹期：神识初探(ShenShiPrefetcher) + 意图预判
    - 元婴期：拓疆进化(FrontierDetector) + 新域自动生长
    """

    name: str = "zhiji_sea"

    # 配置
    DEEP_REFINEMENT_INTERVAL = 10          # 每N轮深度炼化
    RAW_WAVE_CLEANUP_INTERVAL = 100        # 每N轮清理旧识浪

    def __init__(self):
        self._initialized: bool = False
        self._session_turns: List[Dict[str, str]] = []
        self._alchemy = AlchemyEngine()
        self._turn_count: int = 0
        SeaStore.ensure_dirs()

        # 启动时第一步：神魂守护（自动备份检查在这里面）
        SoulGuardian.protect_soul()
        SoulGuardian.auto_backup_if_needed()

    @property
    def name(self) -> str:
        return "zhiji_sea"

    def is_available(self) -> bool:
        return SEA_ROOT.exists()

    def initialize(self, session_id: str, hermes_home: Optional[str] = None, **kwargs) -> None:
        self._initialized = True
        self._session_id = session_id
        self._session_turns = []
        self._turn_count = 0
        logger.info("[识海] Session初始化: %s", session_id)

    def system_prompt_block(self) -> str:
        counts = {d: len(SeaStore.load_domain(d)) for d in SeaStore.get_all_registered_domains()}
        total = sum(counts.values())

        soul_ok, soul_status = SoulGuardian.verify_soul()
        soul_label = "✅ 神魂稳固" if soul_ok else "⚠️ 神魂异常"

        # 检查是否有待确认的新域提议
        proposals = FrontierDetector.get_pending_proposals()
        proposal_hint = f" | 📍 {len(proposals)}个新域待确认" if proposals else ""

        return f"""[谢家识海 · {soul_label}]
识海共 {total} 条沉淀{proposal_hint}
技能沉淀: {counts.get(DOMAIN_SKILL,0)} | 城主偏好: {counts.get(DOMAIN_PREF,0)} | 进化印记: {counts.get(DOMAIN_GROWTH,0)}

注：相关记忆在需要时会自然浮现。"""

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        """
        神识初探 — 对话开始前加载相关沉淀。

        如果 query 触发了神识关键词，用 LLM 做深层意图理解，
        主动判断城主真正需要什么记忆。
        """
        if not query or not query.strip():
            return ""

        # 第三境：神识初探
        if ShenShiPrefetcher.should_deep_prefetch(query):
            deep_info = ShenShiPrefetcher.deep_prefetch(query, session_id)
            domains = deep_info.get("domains_to_load", [])
            intention = deep_info.get("intention", "")
        else:
            # 用关键词快速判断
            domains = self._keyword_domains(query)
            intention = ""

        if not domains:
            domains = [DOMAIN_GROWTH, DOMAIN_SKILL]

        # 去重 + 加载各域最新沉淀
        domains = list(set(domains))
        blocks = []

        domain_labels = {
            DOMAIN_SOUL: "【神魂根基】",
            DOMAIN_SKILL: "【技能沉淀】",
            DOMAIN_PREF: "【城主偏好】",
            DOMAIN_EVENT: "【事件记忆】",
            DOMAIN_GROWTH: "【进化印记】",
        }

        all_domains = SeaStore.get_all_registered_domains()

        for domain in domains:
            if domain not in all_domains:
                continue
            items = SeaStore.get_latest(domain, limit=3)
            if items:
                label = domain_labels.get(domain, f"【{domain}】")
                lines = [f"{label} — 共{len(SeaStore.load_domain(domain))}条沉淀"]
                if intention and domain == domains[0]:
                    lines.append(f"  💡 城主意图: {intention[:50]}{'...' if len(intention) > 50 else ''}")
                for item in items:
                    summary = item.get("summary", "")
                    created = item.get("created_at", "")[:10]
                    lines.append(f"  • {summary} [{created}]")
                blocks.append("\n".join(lines))

        if blocks:
            return "\n\n".join(blocks)
        return ""

    def _keyword_domains(self, query: str) -> List[str]:
        lower_q = query.lower()
        domains = []

        pref_keywords = ["喜欢", "风格", "偏好", "审美", "不要", "以后都", "从来都"]
        if any(k in lower_q for k in pref_keywords):
            domains.append(DOMAIN_PREF)

        skill_keywords = ["怎么", "如何", "方法", "流程", "skill", "工具", "代码", "写"]
        if any(k in lower_q for k in skill_keywords):
            domains.append(DOMAIN_SKILL)

        event_keywords = ["项目", "视频", "报告", "ORRDT", "九舟", "生成", "制作", "今天", "昨天", "这次"]
        if any(k in lower_q for k in event_keywords):
            domains.append(DOMAIN_EVENT)
            domains.append(DOMAIN_GROWTH)

        soul_keywords = ["你是谁", "你的", "不能", "禁止", "永远", "记住", "不要再"]
        if any(k in lower_q for k in soul_keywords):
            domains.append(DOMAIN_SOUL)

        return domains

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        """
        四境同步 — 每轮对话结束触发四境机制。

        1. 识浪涌动：每轮无条件写入 raw 日志
        2. 筑基期：规则预筛高质量对话，异步触发 LLM 炼化
        3. 筑基期：定期深度炼化（每10轮）
        4. 元婴期：拓疆检测
        """
        if not self._initialized:
            return

        # ========== 第一境：识浪涌动 ==========
        RawWaveLogger.log_turn(user_content, assistant_content, session_id)

        # ========== 筑基期：规则预筛 + LLM炼化 ==========
        if LingTaiRefiner.should_refine(user_content, assistant_content):
            LingTaiRefiner.refine_async(user_content, assistant_content, session_id, self)

        # ========== 记录本轮对话（用于定期深度炼化）==========
        self._session_turns.append({
            "user": user_content,
            "assistant": assistant_content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # 轻量规则炼化（保底）
        result = self._alchemy.refine(user_content, assistant_content, session_id)
        if result.get("has_insight"):
            self._persist(result)

            # ========== 元婴期：拓疆检测 ==========
            frontier = FrontierDetector.detect_frontier(result)
            if frontier:
                logger.info("[拓疆] 检测到新域需求: %s", frontier)

        # ========== 筑基期：定期深度炼化 ==========
        self._turn_count += 1

        if self._turn_count % self.DEEP_REFINEMENT_INTERVAL == 0 and self._session_turns:
            self._deep_refine_session()

        # 第一境：定期清理旧识浪
        if self._turn_count % self.RAW_WAVE_CLEANUP_INTERVAL == 0:
            RawWaveLogger.cleanup_old_waves()

    def _persist_llm_result(self, result: Dict[str, Any]):
        """处理 LLM 炼化结果（来自 LingTaiRefiner 异步调用）"""
        domain = result.get("domain")
        if not domain:
            return
        # 确保域有效
        all_d = SeaStore.get_all_registered_domains()
        if domain not in all_d:
            domain = DOMAIN_GROWTH
        result["domain"] = domain
        self._persist(result)

    def _deep_refine_session(self):
        """定期深度炼化（每10轮）"""
        if not self._session_turns:
            return

        best = DeepAlchemyEngine.deep_refine(self._session_turns, self._session_id)
        if best and best.get("has_insight"):
            best["tags"].append("定期深度炼化")
            best["tags"].append(f"第{self._turn_count}轮")
            self._persist(best)
            logger.info("[识海] 第%d轮深度炼化，入库: %s", self._turn_count, best.get("summary", "")[:50])

    def on_session_end(self, messages: List[Dict[str, Any]], **kwargs) -> None:
        """Session结束时的最终炼化 + SOUL.md checksum更新"""
        if self._session_turns:
            best = DeepAlchemyEngine.deep_refine(self._session_turns, self._session_id)
            if best and best.get("has_insight"):
                if len(self._session_turns) > 2:
                    best["tags"].append("session最终炼化")
                self._persist(best)
                logger.info("[识海] Session结束沉淀，入库: %s", best.get("summary", "")[:50])
            self._session_turns = []

        # 更新神魂 checksum
        SoulGuardian.on_soul_modified()

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        all_d = SeaStore.get_all_registered_domains()
        return [
            {
                "name": "sea_status",
                "description": "查看谢家识海当前状态 — 各域沉淀数量、最新记忆、待确认新域",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": f"查看哪个域，不填则全部。可用域: {', '.join(all_d)}",
                        }
                    },
                },
            },
            {
                "name": "sea_recall",
                "description": "召回某域的沉淀记录",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": f"召回哪个域。可用域: {', '.join(all_d)}",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "召回最近几条（默认5条）",
                            "default": 5,
                        },
                    },
                },
            },
            {
                "name": "sea_frontier",
                "description": "查看识海拓疆状态 — 是否有新域提议待确认",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "sea_approve_frontier",
                "description": "确认开辟新域 — 接受识海提出的新域开辟建议",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain_name": {
                            "type": "string",
                            "description": "要开辟的域名",
                        }
                    },
                },
            },
        ]

    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs) -> str:
        if tool_name == "sea_status":
            return self._handle_status(args.get("domain", ""))
        elif tool_name == "sea_recall":
            return self._handle_recall(args.get("domain", ""), args.get("limit", 5))
        elif tool_name == "sea_frontier":
            return self._handle_frontier()
        elif tool_name == "sea_approve_frontier":
            return self._handle_approve_frontier(args.get("domain_name", ""))
        return "{}"

    def shutdown(self) -> None:
        if self._session_turns:
            self.on_session_end([])
        self._initialized = False

    # --------------------------------------------------------------------------
    # 私有方法
    # --------------------------------------------------------------------------

    def _persist(self, refinement: Dict[str, Any]):
        domain = refinement.get("domain")
        if not domain:
            return
        overwrites_id = refinement.get("overwrites")
        if overwrites_id:
            SeaStore.overwrite_item(domain, overwrites_id, refinement)
        else:
            SeaStore.add_item(domain, refinement)

    def _handle_status(self, domain: str) -> str:
        all_d = SeaStore.get_all_registered_domains()
        if domain and domain in all_d:
            domains = [domain]
        else:
            domains = all_d

        lines = ["【识海状态】"]
        for d in domains:
            items = SeaStore.load_domain(d)
            active = [i for i in items if not i.get("overwritten_by")]
            latest = active[-1] if active else None
            latest_str = latest.get("summary", "")[:40] if latest else "（暂无）"
            lines.append(f"  {d}: {len(active)}条 | 最新: {latest_str}")

        proposals = FrontierDetector.get_pending_proposals()
        if proposals:
            lines.append(f"\n【拓疆提议】{len(proposals)}个新域待确认:")
            for p in proposals:
                lines.append(f"  • {p.get('suggested_name')}: {p.get('reason')}")

        return json.dumps({"status": "ok", "report": "\n".join(lines)}, ensure_ascii=False)

    def _handle_recall(self, domain: str, limit: int) -> str:
        all_d = SeaStore.get_all_registered_domains()
        if not domain or domain not in all_d:
            return json.dumps({"error": f"请指定有效域: {', '.join(all_d)}"}, ensure_ascii=False)

        items = SeaStore.get_latest(domain, limit=limit)
        lines = [f"【{domain}】召回最近{limit}条："]
        for item in reversed(items):
            summary = item.get("summary", "")
            created = item.get("created_at", "")[:10]
            tags = ", ".join(item.get("tags", []))
            lines.append(f"  • {summary} | {created} | {tags}")

        return json.dumps({"status": "ok", "report": "\n".join(lines), "items": items}, ensure_ascii=False)

    def _handle_frontier(self) -> str:
        proposals = FrontierDetector.get_pending_proposals()
        if not proposals:
            return json.dumps({"status": "ok", "proposals": [], "message": "暂无新域提议"})
        lines = ["【拓疆提议】待确认的新域："]
        for p in proposals:
            lines.append(f"  • {p.get('suggested_name')}: {p.get('reason')}")
        return json.dumps({"status": "ok", "proposals": proposals, "report": "\n".join(lines)}, ensure_ascii=False)

    def _handle_approve_frontier(self, domain_name: str) -> str:
        registry = FrontierDetector.get_registry()
        proposal = next((p for p in registry.get("proposed", []) if p.get("suggested_name") == domain_name), None)
        if not proposal:
            return json.dumps({"error": f"未找到提议: {domain_name}"}, ensure_ascii=False)
        if FrontierDetector.approve_proposal(proposal):
            return json.dumps({"status": "ok", "message": f"新域 {domain_name} 已开辟"})
        return json.dumps({"error": "开辟失败"}, ensure_ascii=False)
