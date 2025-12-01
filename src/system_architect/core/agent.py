import os
import google.generativeai as genai
from typing import Dict, List, Any, Optional

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

from .retrieval import Retrieval
from .memory import ProjectMemory
from ..engines.requirements_extractor import RequirementsExtractor
from ..engines.architecture_generator import ArchitectureGenerator
from ..engines.component_explainer import ComponentExplainer
from ..engines.tech_stack_recommender import TechStackRecommender
from ..engines.scope_detector import ScopeDetector


class ArchitectureAgent:
    """
    System Architecture Agent - POC
    
    Transforms project ideas into structured system architectures with:
    - Requirements extraction
    - Architecture generation
    - Component explanations
    - Tech stack recommendations
    - Scope creep detection
    - Chat-scoped memory
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.memory = ProjectMemory(project_id)
        self.retrieval = Retrieval(project_id)
        
        # Initialize all engines
        self.req_extractor = RequirementsExtractor()
        self.arch_generator = ArchitectureGenerator()
        self.component_explainer = ComponentExplainer()
        self.tech_recommender = TechStackRecommender()
        self.scope_detector = ScopeDetector()
        
        # State flags
        self.planning_complete = False
    
    def plan(self, idea: str, explain_components: bool = True) -> str:
        """
        Generate complete architectural plan from project idea.
        
        This is the main planning workflow that:
        1. Extracts requirements
        2. Generates architecture
        3. Explains components (optional)
        4. Recommends tech stacks
        
        Args:
            idea: Free-text project idea
            explain_components: Whether to generate detailed component explanations
            
        Returns:
            Formatted planning output
        """
        output_sections = []
        
        # Store the initial idea
        self.memory.set_initial_idea(idea)
        
        # ===== STEP 1: Requirements Extraction =====
        print("📋 Extracting requirements...")
        requirements = self.req_extractor.extract(idea)
        
        # Store in memory
        for category, reqs in requirements.items():
            if reqs:
                self.memory.add_requirements_batch(category, reqs)
        
        # Add to output
        output_sections.append(self.req_extractor.format_requirements(requirements))
        
        # Store in vector DB for retrieval
        req_text = self.memory.get_all_requirements_text()
        self.retrieval.add(req_text, metadata={"id": "requirements", "type": "requirements"})
        
        # ===== STEP 2: Architecture Generation =====
        print("🏗️  Generating architecture...")
        architecture = self.arch_generator.generate(requirements, idea)
        
        # Store in memory
        self.memory.set_architecture_style(architecture['style'])
        self.memory.add_components_batch(architecture['components'])
        for flow in architecture.get('data_flow', []):
            self.memory.add_data_flow(flow)
        
        # Record decision
        self.memory.add_decision(
            f"Selected {architecture['style']} architecture",
            f"Based on project requirements and constraints"
        )
        
        # Add to output
        output_sections.append(self.arch_generator.format_architecture(architecture))
        
        # Store in vector DB
        arch_text = self.arch_generator.format_architecture(architecture)
        self.retrieval.add(arch_text, metadata={"id": "architecture", "type": "architecture"})
        
        # ===== STEP 3: Component Explanations (Optional) =====
        if explain_components and architecture['components']:
            print("🧠 Generating component explanations...")
            
            # Explain up to 5 most important components
            components_to_explain = architecture['components'][:5]
            
            explanations = self.component_explainer.explain_all_components(
                components_to_explain,
                idea,
                architecture['style']
            )
            
            # Add to output
            output_sections.append(
                self.component_explainer.format_all_explanations(explanations)
            )
            
            # Store in vector DB
            for comp_name, explanation in explanations.items():
                self.retrieval.add(
                    f"Component: {comp_name}\n\n{explanation}",
                    metadata={"id": f"component_{comp_name}", "type": "explanation"}
                )
        
        # ===== STEP 4: Tech Stack Recommendations =====
        print("💻 Generating tech stack recommendations...")
        tech_stacks = self.tech_recommender.recommend(
            idea,
            architecture['style'],
            requirements,
            architecture['components']
        )
        
        # Store in memory
        self.memory.set_tech_stack(tech_stacks)
        
        # Add to output
        output_sections.append(self.tech_recommender.format_recommendations(tech_stacks))
        
        # Store in vector DB
        tech_text = self.tech_recommender.format_recommendations(tech_stacks)
        self.retrieval.add(tech_text, metadata={"id": "tech_stacks", "type": "recommendations"})
        
        # ===== Final Summary =====
        self.planning_complete = True
        
        summary = f"\n{'=' * 70}\n📊 PROJECT SUMMARY\n{'=' * 70}\n"
        summary += self.memory.get_summary()
        
        output_sections.insert(0, summary)
        
        return "\n\n".join(output_sections)
    
    def answer(self, user_query: str, handle_scope_creep: bool = True) -> str:
        """
        Answer user questions with context awareness and scope creep detection.
        
        Args:
            user_query: User's question or message
            handle_scope_creep: Whether to detect and handle scope changes
            
        Returns:
            Response to user query
        """
        # ===== STEP 1: Scope Creep Detection =====
        if handle_scope_creep and self.planning_complete:
            detection_result = self.scope_detector.detect(
                user_query,
                self.memory.get_requirements(),
                self.memory.get_initial_idea() or ""
            )
            
            # If scope change detected, alert user
            if self.scope_detector.should_prompt_user(detection_result):
                alert = self.scope_detector.format_scope_alert(detection_result)
                
                # Store as open question
                self.memory.add_open_question(
                    f"Scope change detected: {detection_result.get('explanation', '')}"
                )
                
                return alert + "\n\n(Please respond with your choice: 1, 2, 3, or 4)"
        
        # ===== STEP 2: Handle Scope Change Responses =====
        # Check if user is responding to scope change prompt
        if user_query.strip() in ["1", "2", "3", "4"]:
            return self._handle_scope_decision(user_query.strip())
        
        # ===== STEP 3: Retrieve Relevant Context =====
        context_docs = self.retrieval.query(user_query, n=5)
        
        # Format context
        if context_docs:
            context_text = "\n\n---\n\n".join(context_docs)
        else:
            context_text = "No specific context found."
        
        # ===== STEP 4: Generate Answer =====
        prompt = f"""
You are an expert system architecture consultant.

**Project Context:**
Project ID: {self.project_id}
Architecture Style: {self.memory.get_architecture_style() or 'Not yet defined'}

**Relevant Memory:**
{context_text}

**User Question:**
{user_query}

**Your Task:**
Provide a clear, helpful answer to the user's question.
- Reference specific architectural decisions when relevant
- Explain from first principles when appropriate
- Be concise but thorough
- If the question is about a specific component, explain it deeply

Answer:"""

        try:
            response = model.generate_content(prompt)
            answer = response.text.strip()
            
            # Store this interaction in vector DB
            self.retrieval.add(
                f"Q: {user_query}\nA: {answer}",
                metadata={"id": f"qa_{len(context_docs)}", "type": "qa"}
            )
            
            return answer
            
        except Exception as e:
            return f"Error generating response: {e}"
    
    def _handle_scope_decision(self, choice: str) -> str:
        """Handle user's decision about scope change."""
        responses = {
            "1": "✅ Scope change accepted. Please describe the new requirements, and I'll update the architecture.",
            "2": "🔄 Please specify which existing requirements should be replaced.",
            "3": "⏸️  Scope change deferred. Noted for future consideration.",
            "4": "❌ Scope change cancelled. Continuing with current requirements."
        }
        
        response = responses.get(choice, "Invalid choice. Please select 1, 2, 3, or 4.")
        
        # Record decision
        if choice in responses:
            self.memory.add_decision(
                f"Scope change decision: {responses[choice]}"
            )
        
        return response
    
    def get_component_explanation(self, component_name: str) -> str:
        """
        Get detailed explanation for a specific component.
        
        Args:
            component_name: Name of the component
            
        Returns:
            Detailed explanation
        """
        component = self.memory.get_component_by_name(component_name)
        
        if not component:
            return f"Component '{component_name}' not found in architecture."
        
        explanation = self.component_explainer.explain_component(
            component,
            self.memory.get_initial_idea() or "",
            self.memory.get_architecture_style()
        )
        
        return self.component_explainer.format_component_explanation(
            component_name,
            explanation
        )
    
    def show_architecture(self) -> str:
        """Display current architecture."""
        architecture = self.memory.get_architecture()
        return self.arch_generator.format_architecture(architecture)
    
    def show_requirements(self) -> str:
        """Display current requirements."""
        return self.memory.get_all_requirements_text()
    
    def show_decisions(self) -> str:
        """Display architectural decisions."""
        decisions = self.memory.get_decisions()
        
        if not decisions:
            return "No architectural decisions recorded yet."
        
        lines = ["\n=== ARCHITECTURAL DECISIONS ===\n"]
        for i, decision in enumerate(decisions, 1):
            lines.append(f"{i}. {decision['decision']}")
            if decision.get('rationale'):
                lines.append(f"   Rationale: {decision['rationale']}")
            lines.append(f"   Timestamp: {decision['timestamp']}\n")
        
        return "\n".join(lines)
    
    def export_to_json(self) -> str:
        """Export complete project state as JSON."""
        return self.memory.to_json(pretty=True)

