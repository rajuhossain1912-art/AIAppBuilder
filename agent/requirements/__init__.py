"""Requirement intake and normalization primitives."""

from .capability_catalog import CapabilityMatch, classify_capabilities
from .requirements_engine import RequirementEngine, RequirementSet

__all__ = [
    "CapabilityMatch",
    "RequirementEngine",
    "RequirementSet",
    "classify_capabilities",
]
