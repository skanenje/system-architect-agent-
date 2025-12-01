"""
Engine components for various agent capabilities.

This module contains specialized engines for:
- Requirements extraction
- Architecture generation
- Component explanation
- Tech stack recommendations
- Scope creep detection
"""

from .requirements_extractor import RequirementsExtractor
from .architecture_generator import ArchitectureGenerator
from .component_explainer import ComponentExplainer
from .tech_stack_recommender import TechStackRecommender
from .scope_detector import ScopeDetector

__all__ = [
    "RequirementsExtractor",
    "ArchitectureGenerator",
    "ComponentExplainer",
    "TechStackRecommender",
    "ScopeDetector",
]
