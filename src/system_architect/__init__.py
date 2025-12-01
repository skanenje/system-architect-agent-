"""
System Architecture Agent - An AI-powered conversational agent for system design.

This package provides tools for:
- Requirements extraction and analysis
- Architecture pattern generation
- Component explanation
- Tech stack recommendations
- Scope creep detection
- Project memory management
"""

__version__ = "0.1.0"
__author__ = "System Architect Agent Team"

from .core.agent import SystemArchitectAgent
from .core.memory import ProjectMemory

__all__ = [
    "SystemArchitectAgent",
    "ProjectMemory",
]
