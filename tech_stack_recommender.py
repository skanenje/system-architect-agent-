"""
Tech Stack Recommender

Recommends appropriate technology stacks based on architecture and requirements.
Provides 2-3 options with brief rationale.
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Any

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


class TechStackRecommender:
    """
    Recommends technology stacks based on architecture and requirements.
    """
    
    def __init__(self):
        self.recommendation_prompt_template = """
You are an expert technology consultant and full-stack architect.

Your task is to recommend 2-3 viable technology stack options for this project.

**Project Context:**
{project_idea}

**Architecture Style:** {architecture_style}

**Requirements Summary:**
{requirements_summary}

**Key Components:**
{components}

**Your Task:**
Recommend 2-3 complete technology stacks that would work well for this project.

For each stack, evaluate along these dimensions:
1. **Integration Simplicity**: How easy is it to integrate all the pieces?
2. **Performance Expectations**: Will it meet performance requirements?
3. **Ecosystem Maturity**: How mature and well-supported are the technologies?
4. **Developer Ergonomics**: How pleasant is it to work with?

**Output Format:**
Return ONLY a valid JSON array:
[
  {{
    "name": "Stack Name (e.g., 'Modern JavaScript Stack')",
    "description": "Brief 1-sentence description",
    "technologies": {{
      "frontend": "Technology name",
      "backend": "Technology name",
      "database": "Technology name",
      "cache": "Technology name (if applicable)",
      "other": ["Other key technologies"]
    }},
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "considerations": ["consideration 1", "consideration 2"],
    "best_for": "When to choose this stack",
    "integration_simplicity": "high|medium|low",
    "performance": "excellent|good|adequate",
    "ecosystem_maturity": "mature|growing|emerging",
    "developer_ergonomics": "excellent|good|adequate"
  }},
  ...
]

**Guidelines:**
- Be realistic and practical
- Consider the team size and timeline if mentioned
- Don't recommend overly complex stacks for simple projects
- Include both popular and emerging options if appropriate
- Focus on proven combinations that work well together

Return ONLY the JSON array, no markdown formatting.
"""
    
    def recommend(self, project_idea: str,
                 architecture_style: str,
                 requirements: Dict[str, List[str]],
                 components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate tech stack recommendations.
        
        Args:
            project_idea: Original project description
            architecture_style: The chosen architecture style
            requirements: Categorized requirements
            components: List of architectural components
            
        Returns:
            List of recommended tech stacks
        """
        # Format requirements summary
        req_summary = self._format_requirements_summary(requirements)
        
        # Format components list
        comp_list = [f"- {c.get('name', 'Unknown')}: {c.get('purpose', 'N/A')}" 
                     for c in components[:5]]  # Top 5 components
        comp_text = "\n".join(comp_list)
        
        prompt = self.recommendation_prompt_template.format(
            project_idea=project_idea,
            architecture_style=architecture_style,
            requirements_summary=req_summary,
            components=comp_text
        )
        
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            stacks = json.loads(response_text)
            
            # Validate it's a list
            if not isinstance(stacks, list):
                stacks = [stacks]
            
            return stacks[:3]  # Max 3 recommendations
            
        except json.JSONDecodeError as e:
            print(f"Error parsing tech stack recommendations: {e}")
            return self._get_fallback_recommendations(architecture_style)
        except Exception as e:
            print(f"Error generating tech stack recommendations: {e}")
            return self._get_fallback_recommendations(architecture_style)
    
    def _format_requirements_summary(self, requirements: Dict[str, List[str]]) -> str:
        """Create a concise summary of requirements."""
        lines = []
        for category, reqs in requirements.items():
            if reqs:
                # Handle both string and dict formats
                req_texts = []
                for req in reqs[:3]:  # Max 3 per category
                    if isinstance(req, dict):
                        req_texts.append(req.get('text', str(req)))
                    else:
                        req_texts.append(req)
                
                lines.append(f"{category.capitalize()}: {', '.join(req_texts)}")
        
        return "\n".join(lines) if lines else "No specific requirements"
    
    def _get_fallback_recommendations(self, architecture_style: str) -> List[Dict[str, Any]]:
        """Provide basic fallback recommendations if LLM fails."""
        fallbacks = {
            "monolith": [
                {
                    "name": "Modern Full-Stack JavaScript",
                    "description": "Node.js backend with React frontend",
                    "technologies": {
                        "frontend": "React",
                        "backend": "Node.js + Express",
                        "database": "PostgreSQL",
                        "cache": "Redis"
                    },
                    "strengths": ["Single language", "Large ecosystem", "Fast development"],
                    "considerations": ["May not be best for CPU-intensive tasks"],
                    "best_for": "Web applications with real-time features"
                }
            ],
            "microservices": [
                {
                    "name": "Cloud-Native Stack",
                    "description": "Kubernetes-based microservices",
                    "technologies": {
                        "frontend": "React/Vue",
                        "backend": "Go/Node.js services",
                        "database": "PostgreSQL + MongoDB",
                        "infrastructure": "Kubernetes"
                    },
                    "strengths": ["Scalable", "Resilient", "Cloud-native"],
                    "considerations": ["Complex operations", "Requires DevOps expertise"],
                    "best_for": "Large-scale distributed systems"
                }
            ],
            "event-driven": [
                {
                    "name": "Event Streaming Stack",
                    "description": "Kafka-based event-driven architecture",
                    "technologies": {
                        "frontend": "React",
                        "backend": "Java/Python services",
                        "messaging": "Apache Kafka",
                        "database": "PostgreSQL + Elasticsearch"
                    },
                    "strengths": ["Real-time processing", "Scalable", "Decoupled"],
                    "considerations": ["Eventual consistency", "Complex debugging"],
                    "best_for": "Real-time data processing and analytics"
                }
            ],
            "agentic": [
                {
                    "name": "AI Agent Stack",
                    "description": "LLM-powered agentic system",
                    "technologies": {
                        "frontend": "React",
                        "backend": "Python + FastAPI",
                        "ai": "OpenAI/Anthropic API",
                        "vector_db": "Pinecone/ChromaDB",
                        "database": "PostgreSQL"
                    },
                    "strengths": ["AI-native", "Flexible", "Rich ecosystem"],
                    "considerations": ["API costs", "Latency"],
                    "best_for": "AI-powered conversational applications"
                }
            ]
        }
        
        return fallbacks.get(architecture_style, fallbacks["monolith"])
    
    def format_recommendations(self, stacks: List[Dict[str, Any]]) -> str:
        """
        Format tech stack recommendations for display.
        
        Args:
            stacks: List of tech stack recommendations
            
        Returns:
            Formatted string
        """
        if not stacks:
            return "No tech stack recommendations available."
        
        lines = [
            "\n" + "=" * 70,
            "💻 RECOMMENDED TECHNOLOGY STACKS",
            "=" * 70 + "\n"
        ]
        
        for i, stack in enumerate(stacks, 1):
            lines.append(f"\n{'─' * 70}")
            lines.append(f"Option {i}: {stack.get('name', 'Unknown Stack')}")
            lines.append(f"{'─' * 70}")
            
            if 'description' in stack:
                lines.append(f"\n📝 {stack['description']}\n")
            
            # Technologies
            if 'technologies' in stack:
                lines.append("🛠️  Technologies:")
                for key, value in stack['technologies'].items():
                    if isinstance(value, list):
                        value = ", ".join(value)
                    lines.append(f"   • {key.capitalize()}: {value}")
            
            # Strengths
            if 'strengths' in stack and stack['strengths']:
                lines.append("\n✅ Strengths:")
                for strength in stack['strengths']:
                    lines.append(f"   • {strength}")
            
            # Considerations
            if 'considerations' in stack and stack['considerations']:
                lines.append("\n⚠️  Considerations:")
                for consideration in stack['considerations']:
                    lines.append(f"   • {consideration}")
            
            # Best for
            if 'best_for' in stack:
                lines.append(f"\n🎯 Best For: {stack['best_for']}")
            
            # Evaluation metrics (if available)
            metrics = []
            if 'integration_simplicity' in stack:
                metrics.append(f"Integration: {stack['integration_simplicity']}")
            if 'performance' in stack:
                metrics.append(f"Performance: {stack['performance']}")
            if 'ecosystem_maturity' in stack:
                metrics.append(f"Maturity: {stack['ecosystem_maturity']}")
            if 'developer_ergonomics' in stack:
                metrics.append(f"Dev Experience: {stack['developer_ergonomics']}")
            
            if metrics:
                lines.append(f"\n📊 Evaluation: {' | '.join(metrics)}")
            
            lines.append("")
        
        lines.append("=" * 70 + "\n")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the recommender
    from dotenv import load_dotenv
    load_dotenv()
    
    recommender = TechStackRecommender()
    
    test_idea = "AI-powered habit tracker mobile app with offline support"
    test_style = "agentic"
    test_requirements = {
        "functional": ["Log habits", "AI insights", "Recommendations"],
        "nonfunctional": ["Offline support", "10K users"],
        "constraints": ["3 month timeline"],
        "assumptions": [],
        "risks": []
    }
    test_components = [
        {"name": "Mobile App", "purpose": "User interface"},
        {"name": "API Server", "purpose": "Backend logic"},
        {"name": "AI Service", "purpose": "Generate insights"},
        {"name": "Vector DB", "purpose": "Semantic search"}
    ]
    
    print("Testing Tech Stack Recommendations...\n")
    
    stacks = recommender.recommend(test_idea, test_style, test_requirements, test_components)
    print(recommender.format_recommendations(stacks))
