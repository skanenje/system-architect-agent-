"""
Component Explanation Engine

Generates deep, first-principles explanations for architectural components.
Explains purpose, trade-offs, scaling limits, and computational problems solved.
"""

import os
import google.generativeai as genai
from typing import Dict, Any, List

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


class ComponentExplainer:
    """
    Generates detailed, first-principles explanations for architectural components.
    """
    
    def __init__(self):
        self.explanation_prompt_template = """
You are an expert system architect and computer science educator.

Your task is to explain an architectural component from FIRST PRINCIPLES.

**Component:**
Name: {component_name}
Type: {component_type}
Purpose: {component_purpose}

**Project Context:**
{project_context}

**Your Task:**
Provide a deep, educational explanation covering:

1. **Purpose & Role**: What this component does in the system
2. **Computational Problem**: What fundamental computational or data-handling problem does it solve?
3. **How It Works**: Brief explanation of the underlying mechanism/approach
4. **Key Trade-offs**: What are you gaining and what are you giving up?
   - Performance vs Complexity
   - Consistency vs Availability
   - Cost vs Capability
   - etc.
5. **Scaling Characteristics**: How does this component behave under load?
   - What are its scaling limits?
   - When does it become a bottleneck?
   - How would you scale it?
6. **Why It Exists Here**: Why is this component necessary for THIS specific architecture?

**Style Guidelines:**
- Explain like you're teaching a smart engineer who wants to understand deeply
- Use concrete examples where helpful
- Be technical but clear
- Avoid jargon without explanation
- Focus on fundamental concepts, not specific technologies

**Output Format:**
Write a clear, structured explanation (3-5 paragraphs).
Use markdown formatting for readability.
"""
    
    def explain_component(self, component: Dict[str, Any], 
                         project_context: str,
                         architecture_style: str = None) -> str:
        """
        Generate a first-principles explanation for a component.
        
        Args:
            component: Component dictionary with name, type, purpose, etc.
            project_context: Description of the overall project
            architecture_style: The architecture style (monolith, microservices, etc.)
            
        Returns:
            Detailed explanation text
        """
        component_name = component.get('name', 'Unknown Component')
        component_type = component.get('type', 'Unknown Type')
        component_purpose = component.get('purpose', 'No purpose specified')
        
        # Add architecture context if available
        if architecture_style:
            project_context += f"\n\nArchitecture Style: {architecture_style}"
        
        prompt = self.explanation_prompt_template.format(
            component_name=component_name,
            component_type=component_type,
            component_purpose=component_purpose,
            project_context=project_context
        )
        
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error explaining component {component_name}: {e}")
            return f"Unable to generate explanation for {component_name}"
    
    def explain_all_components(self, components: List[Dict[str, Any]], 
                              project_context: str,
                              architecture_style: str = None) -> Dict[str, str]:
        """
        Generate explanations for all components.
        
        Args:
            components: List of component dictionaries
            project_context: Description of the overall project
            architecture_style: The architecture style
            
        Returns:
            Dictionary mapping component names to explanations
        """
        explanations = {}
        
        for component in components:
            component_name = component.get('name', 'Unknown')
            print(f"Generating explanation for: {component_name}...")
            
            explanation = self.explain_component(
                component, 
                project_context,
                architecture_style
            )
            
            explanations[component_name] = explanation
        
        return explanations
    
    def format_component_explanation(self, component_name: str, 
                                    explanation: str) -> str:
        """
        Format a component explanation for display.
        
        Args:
            component_name: Name of the component
            explanation: Explanation text
            
        Returns:
            Formatted string
        """
        lines = [
            f"\n{'=' * 70}",
            f"🔍 COMPONENT: {component_name}",
            f"{'=' * 70}\n",
            explanation,
            f"\n{'=' * 70}\n"
        ]
        return "\n".join(lines)
    
    def format_all_explanations(self, explanations: Dict[str, str]) -> str:
        """
        Format all component explanations for display.
        
        Args:
            explanations: Dictionary of component name -> explanation
            
        Returns:
            Formatted string with all explanations
        """
        lines = [
            "\n" + "=" * 70,
            "📚 COMPONENT EXPLANATIONS (First Principles)",
            "=" * 70 + "\n"
        ]
        
        for component_name, explanation in explanations.items():
            lines.append(self.format_component_explanation(component_name, explanation))
        
        return "\n".join(lines)
    
    def explain_trade_off(self, option_a: str, option_b: str, 
                         context: str) -> str:
        """
        Explain the trade-offs between two architectural options.
        
        Args:
            option_a: First option
            option_b: Second option
            context: Project context
            
        Returns:
            Trade-off analysis
        """
        prompt = f"""
You are an expert system architect.

Compare these two architectural options for the given context:

**Context:**
{context}

**Option A:** {option_a}
**Option B:** {option_b}

**Your Task:**
Provide a balanced trade-off analysis covering:
1. Strengths of each option
2. Weaknesses of each option
3. When to choose Option A
4. When to choose Option B
5. Recommendation for this specific context

Be concise but thorough. Use bullet points for clarity.
"""
        
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating trade-off analysis: {e}")
            return "Unable to generate trade-off analysis"


if __name__ == "__main__":
    # Test the explainer
    from dotenv import load_dotenv
    load_dotenv()
    
    explainer = ComponentExplainer()
    
    test_component = {
        "name": "Vector Database",
        "type": "data_store",
        "purpose": "Semantic search and RAG (Retrieval Augmented Generation)",
        "technologies": ["Pinecone", "ChromaDB"]
    }
    
    test_context = """
    AI-powered habit tracker mobile app. Users log habits, get AI-generated insights,
    and receive personalized recommendations. The app uses AI to understand user patterns
    and provide contextual advice.
    """
    
    print("Testing Component Explanation...")
    print(f"\nComponent: {test_component['name']}")
    print(f"Context: {test_context}\n")
    
    explanation = explainer.explain_component(test_component, test_context, "agentic")
    print(explainer.format_component_explanation(test_component['name'], explanation))
    
    print("\n" + "=" * 70)
    print("Testing Trade-off Analysis...")
    print("=" * 70 + "\n")
    
    trade_off = explainer.explain_trade_off(
        "Monolith Architecture",
        "Microservices Architecture",
        "Small team building an MVP habit tracker in 3 months"
    )
    print(trade_off)
