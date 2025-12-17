"""
Skill Complexity Analyzer

Analyzes the learning difficulty and skill requirements for projects.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class ComplexityAnalyzer:
    """
    Analyzes skill complexity and learning requirements for projects.
    """
    
    def __init__(self):
        self.analysis_prompt = """
You are an expert programming instructor and skill assessment specialist.

Analyze this project to determine the SKILL COMPLEXITY and learning requirements.

**Project Description:**
{job_description}

**Your Task:**
Analyze the LEARNING DIFFICULTY based on:
1. **Technical Skills Required**: What programming concepts must you know?
2. **Learning Curve**: How steep is the learning curve for each technology?
3. **Prerequisite Knowledge**: What must you already know before starting?
4. **Concept Difficulty**: How complex are the underlying concepts?
5. **Time to Learn**: Realistic time to learn these skills from scratch or improve them?

**Skill Levels:**
- **BEGINNER (1-3)**: Basic programming, simple concepts, gentle learning curve (2-4 weeks to learn)
- **INTERMEDIATE (4-6)**: Solid fundamentals needed, moderate concepts, standard patterns (1-3 months to learn)
- **ADVANCED (7-9)**: Deep knowledge required, complex patterns, architectural thinking (3-6 months to learn)
- **EXPERT (10+)**: Mastery level, cutting-edge tech, system design expertise (6+ months to learn)

**Output Format:**
Return ONLY valid JSON:
{{
  "skill_level": "BEGINNER|INTERMEDIATE|ADVANCED|EXPERT",
  "complexity_score": 1-15,
  "learning_time": "X weeks/months to learn these skills",
  "prerequisite_knowledge": [
    "What you should already know",
    ...
  ],
  "core_skills_required": [
    {{
      "skill": "Skill name",
      "difficulty": "beginner|intermediate|advanced|expert",
      "learning_time": "X weeks/months",
      "why_needed": "Explanation"
    }}
  ],
  "challenging_concepts": [
    "Concept that will be hard to learn",
    ...
  ],
  "learning_curve": "gentle|moderate|steep|very_steep",
  "skill_breakdown": {{
    "frontend": "beginner|intermediate|advanced|expert",
    "backend": "beginner|intermediate|advanced|expert",
    "database": "beginner|intermediate|advanced|expert",
    "devops": "beginner|intermediate|advanced|expert",
    "architecture": "beginner|intermediate|advanced|expert"
  }},
  "good_for_learning": true|false,
  "reasoning": "Brief explanation of skill complexity"
}}

Return ONLY the JSON, no markdown.
"""
    
    def analyze(self, project_description: str) -> dict:
        """Analyze skill complexity of project."""
        prompt = self.analysis_prompt.format(job_description=project_description)
        
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
            print(f"Error analyzing complexity: {e}")
            return {
                "skill_level": "INTERMEDIATE",
                "complexity_score": 5,
                "learning_time": "Unknown",
                "reasoning": f"Error during analysis: {e}"
            }
    
    def format_analysis(self, analysis: dict) -> str:
        """Format skill complexity analysis for display."""
        lines = [
            "\n" + "=" * 70,
            "📊 SKILL COMPLEXITY ANALYSIS",
            "=" * 70 + "\n",
            f"🎯 Skill Level: {analysis.get('skill_level', 'UNKNOWN')}",
            f"📈 Complexity Score: {analysis.get('complexity_score', 0)}/15",
            f"⏱️  Learning Time: {analysis.get('learning_time', 'Unknown')}",
            f"📚 Learning Curve: {analysis.get('learning_curve', 'unknown').upper()}",
            f"✅ Good for Learning: {'Yes 👍' if analysis.get('good_for_learning') else 'Consider carefully ⚠️'}\n",
            "=" * 70 + "\n"
        ]
        
        # Prerequisites
        prereqs = analysis.get('prerequisite_knowledge', [])
        if prereqs:
            lines.append("📋 Prerequisites (What You Should Already Know):")
            for prereq in prereqs:
                lines.append(f"   • {prereq}")
            lines.append("")
        
        # Core skills
        core_skills = analysis.get('core_skills_required', [])
        if core_skills:
            lines.append("🎓 Core Skills You'll Need to Learn:")
            for skill in core_skills:
                diff_emoji = "🟢" if skill.get('difficulty') == 'beginner' else "🟡" if skill.get('difficulty') == 'intermediate' else "🟠" if skill.get('difficulty') == 'advanced' else "🔴"
                lines.append(f"\n   {diff_emoji} {skill.get('skill', 'Unknown')} [{skill.get('difficulty', 'unknown').upper()}]")
                lines.append(f"      Time: {skill.get('learning_time', 'unknown')}")
                lines.append(f"      Why: {skill.get('why_needed', 'N/A')}")
            lines.append("")
        
        # Challenging concepts
        challenges = analysis.get('challenging_concepts', [])
        if challenges:
            lines.append("⚠️  Challenging Concepts to Master:")
            for challenge in challenges:
                lines.append(f"   • {challenge}")
            lines.append("")
        
        # Skill breakdown
        breakdown = analysis.get('skill_breakdown', {})
        if breakdown:
            lines.append("💪 Skill Level Breakdown:")
            for area, level in breakdown.items():
                emoji = "🟢" if level == "beginner" else "🟡" if level == "intermediate" else "🟠" if level == "advanced" else "🔴"
                lines.append(f"   {emoji} {area.capitalize()}: {level.upper()}")
            lines.append("")
        
        # Reasoning
        if 'reasoning' in analysis:
            lines.append(f"💡 Analysis:\n{analysis['reasoning']}\n")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
