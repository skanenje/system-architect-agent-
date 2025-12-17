"""
Learning Path Generator

Creates structured learning roadmaps for mastering project tech stacks.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class LearningPathGenerator:
    """
    Generates learning paths and roadmaps for tech stacks.
    """
    
    def __init__(self):
        self.generation_prompt = """
You are an expert programming instructor and mentor.

Create a structured learning path for this project's tech stack.

**Project Description:**
{project_description}

**Detected Tech Stack:**
{tech_stack}

**Your Task:**
Create a comprehensive learning roadmap that helps someone master these technologies.

**Output Format:**
Return ONLY valid JSON:
{{
  "learning_order": [
    {{
      "technology": "Technology name",
      "category": "frontend|backend|database|devops|tool",
      "priority": "high|medium|low",
      "learning_time": "X weeks/months",
      "difficulty": "beginner|intermediate|advanced|expert",
      "prerequisites": ["prereq1", "prereq2"],
      "learning_steps": [
        {{
          "step": 1,
          "title": "Step title",
          "description": "What to learn",
          "estimated_time": "X hours/days",
          "resources": ["resource1", "resource2"],
          "practice_project": "Small project to practice this step"
        }}
      ],
      "key_concepts": ["concept1", "concept2"],
      "common_pitfalls": ["pitfall1", "pitfall2"],
      "mastery_indicators": ["You can do X", "You understand Y"]
    }}
  ],
  "total_learning_time": "X months",
  "recommended_sequence": "Brief explanation of learning order",
  "parallel_learning": ["Tech1 and Tech2 can be learned together"],
  "practice_projects": [
    {{
      "title": "Project title",
      "description": "What to build",
      "technologies_practiced": ["tech1", "tech2"],
      "difficulty": "beginner|intermediate|advanced"
    }}
  ]
}}

Return ONLY the JSON, no markdown.
"""
    
    def generate(self, project_description: str, tech_stack: dict) -> dict:
        """Generate learning path."""
        tech_text = json.dumps(tech_stack, indent=2)
        prompt = self.generation_prompt.format(
            project_description=project_description,
            tech_stack=tech_text
        )
        
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"Error generating learning path: {e}")
            return {
                "learning_order": [],
                "total_learning_time": "Unknown",
                "recommended_sequence": f"Error: {e}"
            }
    
    def format_learning_path(self, learning_path: dict) -> str:
        """Format learning path for display."""
        lines = [
            "\n" + "=" * 70,
            "📚 LEARNING PATH & ROADMAP",
            "=" * 70 + "\n",
            f"⏱️  Total Learning Time: {learning_path.get('total_learning_time', 'Unknown')}\n"
        ]
        
        # Recommended sequence
        if 'recommended_sequence' in learning_path:
            lines.append(f"🎯 Strategy: {learning_path['recommended_sequence']}\n")
        
        # Parallel learning
        parallel = learning_path.get('parallel_learning', [])
        if parallel:
            lines.append("💡 Parallel Learning Opportunities:")
            for item in parallel:
                lines.append(f"   • {item}")
            lines.append("")
        
        # Learning order
        learning_order = learning_path.get('learning_order', [])
        if learning_order:
            lines.append("=" * 70)
            lines.append("📖 STEP-BY-STEP LEARNING ROADMAP")
            lines.append("=" * 70 + "\n")
            
            for i, tech in enumerate(learning_order, 1):
                priority_emoji = "🔴" if tech.get('priority') == 'high' else "🟡" if tech.get('priority') == 'medium' else "🟢"
                
                lines.append(f"\n{i}. {tech.get('technology', 'Unknown')} {priority_emoji}")
                lines.append(f"   Category: {tech.get('category', 'unknown').upper()}")
                lines.append(f"   Difficulty: {tech.get('difficulty', 'unknown').upper()}")
                lines.append(f"   Time: {tech.get('learning_time', 'unknown')}")
                
                # Prerequisites
                prereqs = tech.get('prerequisites', [])
                if prereqs:
                    lines.append(f"   Prerequisites: {', '.join(prereqs)}")
                
                # Key concepts
                concepts = tech.get('key_concepts', [])
                if concepts:
                    lines.append(f"\n   🎓 Key Concepts to Master:")
                    for concept in concepts[:5]:
                        lines.append(f"      • {concept}")
                
                # Learning steps
                steps = tech.get('learning_steps', [])
                if steps:
                    lines.append(f"\n   📝 Learning Steps:")
                    for step in steps[:3]:  # Show first 3 steps
                        lines.append(f"      {step.get('step')}. {step.get('title')} ({step.get('estimated_time', 'unknown')})")
                        lines.append(f"         {step.get('description', '')}")
                
                # Common pitfalls
                pitfalls = tech.get('common_pitfalls', [])
                if pitfalls:
                    lines.append(f"\n   ⚠️  Common Pitfalls:")
                    for pitfall in pitfalls[:3]:
                        lines.append(f"      • {pitfall}")
                
                # Mastery indicators
                mastery = tech.get('mastery_indicators', [])
                if mastery:
                    lines.append(f"\n   ✅ You've Mastered It When:")
                    for indicator in mastery[:3]:
                        lines.append(f"      • {indicator}")
                
                lines.append("")
        
        # Practice projects
        projects = learning_path.get('practice_projects', [])
        if projects:
            lines.append("=" * 70)
            lines.append("🛠️  PRACTICE PROJECTS")
            lines.append("=" * 70 + "\n")
            
            for project in projects:
                lines.append(f"• {project.get('title', 'Unknown')} [{project.get('difficulty', 'unknown').upper()}]")
                lines.append(f"  {project.get('description', '')}")
                techs = project.get('technologies_practiced', [])
                if techs:
                    lines.append(f"  Technologies: {', '.join(techs)}")
                lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
