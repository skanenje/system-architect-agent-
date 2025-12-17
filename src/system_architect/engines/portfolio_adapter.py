"""
Portfolio Project Adapter

Converts client projects into portfolio-worthy learning projects.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class PortfolioAdapter:
    """
    Adapts projects for portfolio and learning purposes.
    """
    
    def __init__(self):
        self.adaptation_prompt = """
You are an expert career coach and portfolio advisor for developers.

Help adapt this project into a portfolio piece for learning and showcasing skills.

**Original Project:**
{project_description}

**Skill Level:** {skill_level}

**Your Task:**
Suggest how to adapt this project for portfolio purposes.

**Output Format:**
Return ONLY valid JSON:
{{
  "portfolio_version": {{
    "title": "Portfolio-friendly project name",
    "tagline": "One-line description",
    "mvp_features": [
      "Essential feature 1",
      "Essential feature 2"
    ],
    "nice_to_have_features": [
      "Feature to add later",
      ...
    ],
    "removed_features": [
      {{
        "feature": "Feature from original",
        "reason": "Why to remove/simplify for learning"
      }}
    ],
    "unique_twist": "How to make it stand out from tutorials",
    "estimated_build_time": "X weeks/months",
    "showcase_points": [
      "What to highlight in portfolio",
      "Skills demonstrated",
      ...
    ]
  }},
  "learning_benefits": [
    "Skill you'll learn",
    ...
  ],
  "simplifications": [
    {{
      "original": "Complex feature",
      "simplified": "Simpler version",
      "learning_value": "What you still learn"
    }}
  ],
  "deployment_suggestions": [
    {{
      "platform": "Platform name (e.g., Vercel, Heroku)",
      "cost": "free|paid",
      "difficulty": "easy|medium|hard",
      "why": "Why this platform"
    }}
  ],
  "demo_data_ideas": [
    "Suggestion for demo data/content",
    ...
  ],
  "github_readme_sections": [
    "Section to include in README",
    ...
  ],
  "portfolio_presentation_tips": [
    "Tip for presenting this project",
    ...
  ]
}}

Return ONLY the JSON, no markdown.
"""
    
    def adapt(self, project_description: str, skill_level: str) -> dict:
        """Adapt project for portfolio."""
        prompt = self.adaptation_prompt.format(
            project_description=project_description,
            skill_level=skill_level
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
            print(f"Error adapting for portfolio: {e}")
            return {
                "portfolio_version": {
                    "title": "Portfolio Project",
                    "mvp_features": []
                },
                "error": str(e)
            }
    
    def format_portfolio_adaptation(self, adaptation: dict) -> str:
        """Format portfolio adaptation for display."""
        lines = [
            "\n" + "=" * 70,
            "🎨 PORTFOLIO PROJECT ADAPTATION",
            "=" * 70 + "\n"
        ]
        
        portfolio = adaptation.get('portfolio_version', {})
        
        # Title and tagline
        lines.append(f"📌 Project Title: {portfolio.get('title', 'Unknown')}")
        if 'tagline' in portfolio:
            lines.append(f"💡 Tagline: {portfolio['tagline']}")
        if 'estimated_build_time' in portfolio:
            lines.append(f"⏱️  Build Time: {portfolio['estimated_build_time']}")
        lines.append("")
        
        # MVP features
        mvp = portfolio.get('mvp_features', [])
        if mvp:
            lines.append("✅ MVP Features (Build These First):")
            for feature in mvp:
                lines.append(f"   • {feature}")
            lines.append("")
        
        # Nice to have
        nice_to_have = portfolio.get('nice_to_have_features', [])
        if nice_to_have:
            lines.append("⭐ Nice-to-Have Features (Add Later):")
            for feature in nice_to_have:
                lines.append(f"   • {feature}")
            lines.append("")
        
        # Unique twist
        if 'unique_twist' in portfolio:
            lines.append(f"🎯 Unique Twist:\n   {portfolio['unique_twist']}\n")
        
        # Removed features
        removed = portfolio.get('removed_features', [])
        if removed:
            lines.append("🗑️  Simplified/Removed from Original:")
            for item in removed:
                lines.append(f"   • {item.get('feature', 'Unknown')}")
                lines.append(f"     Reason: {item.get('reason', 'N/A')}")
            lines.append("")
        
        # Learning benefits
        benefits = adaptation.get('learning_benefits', [])
        if benefits:
            lines.append("📚 What You'll Learn:")
            for benefit in benefits:
                lines.append(f"   • {benefit}")
            lines.append("")
        
        # Simplifications
        simplifications = adaptation.get('simplifications', [])
        if simplifications:
            lines.append("🔄 Simplifications for Learning:")
            for simp in simplifications:
                lines.append(f"\n   Original: {simp.get('original', 'Unknown')}")
                lines.append(f"   Simplified: {simp.get('simplified', 'Unknown')}")
                lines.append(f"   Learning Value: {simp.get('learning_value', 'N/A')}")
            lines.append("")
        
        # Deployment
        deployment = adaptation.get('deployment_suggestions', [])
        if deployment:
            lines.append("🚀 Deployment Options:")
            for option in deployment:
                cost_emoji = "🆓" if option.get('cost') == 'free' else "💰"
                lines.append(f"\n   • {option.get('platform', 'Unknown')} {cost_emoji}")
                lines.append(f"     Difficulty: {option.get('difficulty', 'unknown').upper()}")
                lines.append(f"     Why: {option.get('why', 'N/A')}")
            lines.append("")
        
        # Showcase points
        showcase = portfolio.get('showcase_points', [])
        if showcase:
            lines.append("💼 What to Highlight in Portfolio:")
            for point in showcase:
                lines.append(f"   • {point}")
            lines.append("")
        
        # Demo data
        demo_data = adaptation.get('demo_data_ideas', [])
        if demo_data:
            lines.append("🎭 Demo Data Ideas:")
            for idea in demo_data:
                lines.append(f"   • {idea}")
            lines.append("")
        
        # README sections
        readme = adaptation.get('github_readme_sections', [])
        if readme:
            lines.append("📝 GitHub README Sections:")
            for section in readme:
                lines.append(f"   • {section}")
            lines.append("")
        
        # Presentation tips
        tips = adaptation.get('portfolio_presentation_tips', [])
        if tips:
            lines.append("🎤 Portfolio Presentation Tips:")
            for tip in tips:
                lines.append(f"   • {tip}")
            lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
