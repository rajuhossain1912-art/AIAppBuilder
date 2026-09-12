"""Evidence-first research primitives."""

from .research_engine import ResearchEngine, ResearchError, ResearchRecord
from .web_research import ResearchComparison, ResearchSource, WebResearch

__all__ = [
    "ResearchEngine",
    "ResearchError",
    "ResearchRecord",
    "ResearchComparison",
    "ResearchSource",
    "WebResearch",
]
