"""谢家识海插件 — Zhiji Sea Memory Provider for Hermes Agent

每次对话结束，自动炼化行过留痕。
识浪自然沉淀，新旧相连生长。

守护神魂根基（SOUL.md），自动沉淀领悟成果，
让识海真正成为一个生命体，而不是一个仓库。
"""

from __future__ import annotations

from .zhiji_memory_provider import ZhijiMemoryProvider


def register(ctx) -> None:
    """Register the Zhiji Sea memory provider with the plugin system."""
    ctx.register_memory_provider(ZhijiMemoryProvider())
