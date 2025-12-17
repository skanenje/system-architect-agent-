"""
Task Analysis Memory System

Stores Upwork job analysis including requirements, complexity, tech stack, and risks.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class ProjectMemory:
    """
    Memory system for Upwork task analysis.
    Stores job description, requirements, complexity, tech detection, and recommendations.
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.data = {
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "job_description": None,
            "requirements": {
                "functional": [],
                "technical": [],
                "business": [],
                "timeline_budget": [],
                "risks": []
            },
            "complexity_analysis": None,
            "tech_detection": None,
            "tech_recommendations": [],
            "learning_path": None,
            "third_party_requirements": None,
            "portfolio_adaptation": None,
            "notes": []
        }
    
    # ========== Job Description ==========
    
    def set_job_description(self, description: str):
        """Store the job description."""
        self.data["job_description"] = description
    
    def get_job_description(self) -> Optional[str]:
        """Retrieve the job description."""
        return self.data["job_description"]
    
    # ========== Requirements Management ==========
    
    def add_requirement(self, category: str, requirement: str):
        """Add a requirement to the specified category."""
        if category not in self.data["requirements"]:
            raise ValueError(f"Invalid requirement category: {category}")
        
        self.data["requirements"][category].append({
            "text": requirement,
            "added_at": datetime.now().isoformat()
        })
    
    def add_requirements_batch(self, category: str, requirements: List[str]):
        """Add multiple requirements at once."""
        for req in requirements:
            self.add_requirement(category, req)
    
    def get_requirements(self, category: Optional[str] = None) -> Dict[str, List]:
        """Get requirements, optionally filtered by category."""
        if category:
            return {category: self.data["requirements"].get(category, [])}
        return self.data["requirements"]
    
    def get_all_requirements_text(self) -> str:
        """Get a formatted text representation of all requirements."""
        lines = []
        for category, reqs in self.data["requirements"].items():
            if reqs:
                lines.append(f"\n{category.upper()}:")
                for req in reqs:
                    lines.append(f"  - {req['text']}")
        return "\n".join(lines) if lines else "No requirements defined yet."
    
    # ========== Complexity Analysis ==========
    
    def set_complexity_analysis(self, analysis: Dict[str, Any]):
        """Store complexity analysis."""
        self.data["complexity_analysis"] = analysis
    
    def get_complexity_analysis(self) -> Optional[Dict[str, Any]]:
        """Get complexity analysis."""
        return self.data["complexity_analysis"]
    
    # ========== Tech Detection ==========
    
    def set_tech_detection(self, detection: Dict[str, Any]):
        """Store tech detection results."""
        self.data["tech_detection"] = detection
    
    def get_tech_detection(self) -> Optional[Dict[str, Any]]:
        """Get tech detection results."""
        return self.data["tech_detection"]
    
    # ========== Tech Recommendations ==========
    
    def set_tech_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Store tech stack recommendations."""
        self.data["tech_recommendations"] = recommendations
    
    def get_tech_recommendations(self) -> List[Dict[str, Any]]:
        """Get tech stack recommendations."""
        return self.data["tech_recommendations"]
    
    # ========== Notes ==========
    
    def add_note(self, note: str):
        """Add a note or observation."""
        self.data["notes"].append({
            "note": note,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_notes(self) -> List[Dict[str, Any]]:
        """Get all notes."""
        return self.data["notes"]
    
    # ========== Utility Methods ==========
    
    def dump(self) -> Dict[str, Any]:
        """Return the complete memory state."""
        return self.data
    
    def to_json(self, pretty: bool = True) -> str:
        """Export complete learning analysis as JSON string."""
        if pretty:
            return json.dumps(self.data, indent=2)
        return json.dumps(self.data)
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the analysis."""
        complexity = self.data.get("complexity_analysis", {})
        tech_detection = self.data.get("tech_detection", {})
        third_party = self.data.get("third_party_requirements", {})
        
        # Count technologies
        explicit_tech = tech_detection.get('explicit_technologies', {}) if tech_detection else {}
        tech_count = sum(len(techs) for techs in explicit_tech.values())
        
        lines = [
            f"=== Learning Analysis: {self.project_id} ===",
            f"\n🎯 Skill Level: {complexity.get('skill_level', 'Unknown')}",
            f"📈 Complexity Score: {complexity.get('complexity_score', 0)}/15",
            f"⏱️  Learning Time: {complexity.get('learning_time', 'Unknown')}",
            f"🛠️  Technologies: {tech_count} detected",
            f"🔑 API Keys Needed: {third_party.get('total_api_keys_needed', 0) if third_party else 0}",
            f"💰 Monthly Cost: {third_party.get('estimated_monthly_cost', 'Unknown') if third_party else 'Unknown'}",
        ]
        return "\n".join(lines)
