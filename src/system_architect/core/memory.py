import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class ProjectMemory:
    """
    Enhanced project memory system that maintains structured information
    about requirements, architecture, decisions, and open questions.
    Aligned with PRD data model specification.
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.data = {
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "initial_idea": None,
            "requirements": {
                "functional": [],
                "nonfunctional": [],
                "constraints": [],
                "assumptions": [],
                "risks": []
            },
            "architecture": {
                "style": None,  # monolith|microservices|event-driven|agentic
                "components": [],
                "data_flow": []
            },
            "decisions": [],
            "open_questions": [],
            "tech_stack": []
        }
    
    # ========== Initial Idea ==========
    
    def set_initial_idea(self, idea: str):
        """Store the original project idea."""
        self.data["initial_idea"] = idea
    
    def get_initial_idea(self) -> Optional[str]:
        """Retrieve the original project idea."""
        return self.data["initial_idea"]
    
    # ========== Requirements Management ==========
    
    def add_requirement(self, category: str, requirement: str):
        """
        Add a requirement to the specified category.
        
        Args:
            category: One of 'functional', 'nonfunctional', 'constraints', 'assumptions', 'risks'
            requirement: The requirement text
        """
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
        """
        Get requirements, optionally filtered by category.
        
        Args:
            category: If specified, return only that category. Otherwise return all.
        """
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
    
    # ========== Architecture Management ==========
    
    def set_architecture_style(self, style: str):
        """
        Set the architecture style.
        
        Args:
            style: One of 'monolith', 'microservices', 'event-driven', 'agentic'
        """
        valid_styles = ['monolith', 'microservices', 'event-driven', 'agentic']
        if style not in valid_styles:
            raise ValueError(f"Invalid architecture style. Must be one of: {valid_styles}")
        
        self.data["architecture"]["style"] = style
    
    def get_architecture_style(self) -> Optional[str]:
        """Get the current architecture style."""
        return self.data["architecture"]["style"]
    
    def add_component(self, component: Dict[str, Any]):
        """
        Add an architectural component.
        
        Args:
            component: Dict with keys like 'name', 'purpose', 'type', 'explanation', etc.
        """
        self.data["architecture"]["components"].append(component)
    
    def add_components_batch(self, components: List[Dict[str, Any]]):
        """Add multiple components at once."""
        for component in components:
            self.add_component(component)
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Get all architectural components."""
        return self.data["architecture"]["components"]
    
    def get_component_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a component by name."""
        for component in self.data["architecture"]["components"]:
            if component.get("name", "").lower() == name.lower():
                return component
        return None
    
    def add_data_flow(self, flow: Dict[str, Any]):
        """
        Add a data flow description.
        
        Args:
            flow: Dict with keys like 'from', 'to', 'data', 'protocol', etc.
        """
        self.data["architecture"]["data_flow"].append(flow)
    
    def get_data_flows(self) -> List[Dict[str, Any]]:
        """Get all data flows."""
        return self.data["architecture"]["data_flow"]
    
    def get_architecture(self) -> Dict[str, Any]:
        """Get the complete architecture definition."""
        return self.data["architecture"]
    
    # ========== Decisions Management ==========
    
    def add_decision(self, decision: str, rationale: Optional[str] = None):
        """
        Record an architectural decision.
        
        Args:
            decision: The decision made
            rationale: Why this decision was made
        """
        self.data["decisions"].append({
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_decisions(self) -> List[Dict[str, Any]]:
        """Get all architectural decisions."""
        return self.data["decisions"]
    
    # ========== Open Questions Management ==========
    
    def add_open_question(self, question: str):
        """Add an open question that needs clarification."""
        self.data["open_questions"].append({
            "question": question,
            "added_at": datetime.now().isoformat(),
            "resolved": False
        })
    
    def resolve_question(self, question_index: int, answer: str):
        """Mark a question as resolved with an answer."""
        if 0 <= question_index < len(self.data["open_questions"]):
            self.data["open_questions"][question_index]["resolved"] = True
            self.data["open_questions"][question_index]["answer"] = answer
            self.data["open_questions"][question_index]["resolved_at"] = datetime.now().isoformat()
    
    def get_open_questions(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """
        Get open questions.
        
        Args:
            include_resolved: If True, include resolved questions as well
        """
        if include_resolved:
            return self.data["open_questions"]
        return [q for q in self.data["open_questions"] if not q.get("resolved", False)]
    
    # ========== Tech Stack Management ==========
    
    def set_tech_stack(self, tech_stack: List[Dict[str, Any]]):
        """Store recommended tech stack options."""
        self.data["tech_stack"] = tech_stack
    
    def get_tech_stack(self) -> List[Dict[str, Any]]:
        """Get tech stack recommendations."""
        return self.data["tech_stack"]
    
    # ========== Utility Methods ==========
    
    def dump(self) -> Dict[str, Any]:
        """Return the complete memory state."""
        return self.data
    
    def to_json(self, pretty: bool = True) -> str:
        """Export memory as JSON string."""
        if pretty:
            return json.dumps(self.data, indent=2)
        return json.dumps(self.data)
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the project state."""
        lines = [
            f"=== Project: {self.project_id} ===",
            f"\nArchitecture Style: {self.data['architecture']['style'] or 'Not defined'}",
            f"Components: {len(self.data['architecture']['components'])}",
            f"Requirements: {sum(len(reqs) for reqs in self.data['requirements'].values())}",
            f"Decisions Made: {len(self.data['decisions'])}",
            f"Open Questions: {len(self.get_open_questions())}",
        ]
        return "\n".join(lines)
