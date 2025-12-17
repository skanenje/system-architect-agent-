"""
Tech Stack Detector

Detects required and mentioned technologies from Upwork job descriptions.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class TechDetector:
    """
    Detects technologies and technical requirements from job descriptions.
    """
    
    def __init__(self):
        self.detection_prompt = """
You are an expert at analyzing technical job requirements.

Analyze this Upwork job posting and extract all technical requirements.

**Job Description:**
{job_description}

**Your Task:**
1. Identify EXPLICITLY mentioned technologies (e.g., "React", "Python", "AWS")
2. Detect IMPLICIT technical requirements (e.g., "real-time chat" → WebSockets)
3. Categorize by: frontend, backend, database, infrastructure, tools, other
4. Flag missing or unclear technical specifications

**Output Format:**
Return ONLY valid JSON:
{{
  "explicit_technologies": {{
    "frontend": ["tech1", "tech2"],
    "backend": ["tech1", "tech2"],
    "database": ["tech1"],
    "infrastructure": ["tech1"],
    "tools": ["tech1"],
    "other": ["tech1"]
  }},
  "implicit_requirements": {{
    "frontend": ["requirement → suggested tech"],
    "backend": ["requirement → suggested tech"],
    "database": ["requirement → suggested tech"],
    "infrastructure": ["requirement → suggested tech"]
  }},
  "technical_requirements": [
    "Real-time communication",
    "User authentication",
    "Payment processing",
    ...
  ],
  "missing_specifications": [
    "No database specified",
    "Deployment platform unclear",
    ...
  ],
  "tech_flexibility": "strict|moderate|flexible",
  "notes": "Additional observations about tech requirements"
}}

Return ONLY the JSON, no markdown.
"""
    
    def detect(self, job_description: str) -> dict:
        """Detect technologies from job description."""
        prompt = self.detection_prompt.format(job_description=job_description)
        
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
            print(f"Error detecting tech stack: {e}")
            return {
                "explicit_technologies": {},
                "implicit_requirements": {},
                "technical_requirements": [],
                "missing_specifications": [f"Error during detection: {e}"]
            }
    
    def format_detection(self, detection: dict) -> str:
        """Format tech detection for display."""
        lines = [
            "\n" + "=" * 70,
            "🛠️  TECH STACK DETECTION",
            "=" * 70 + "\n"
        ]
        
        # Explicit technologies
        explicit = detection.get('explicit_technologies', {})
        if any(explicit.values()):
            lines.append("✅ Explicitly Mentioned Technologies:")
            for category, techs in explicit.items():
                if techs:
                    lines.append(f"\n   {category.upper()}:")
                    for tech in techs:
                        lines.append(f"      • {tech}")
            lines.append("")
        
        # Implicit requirements
        implicit = detection.get('implicit_requirements', {})
        if any(implicit.values()):
            lines.append("💡 Implicit Technical Requirements:")
            for category, reqs in implicit.items():
                if reqs:
                    lines.append(f"\n   {category.upper()}:")
                    for req in reqs:
                        lines.append(f"      • {req}")
            lines.append("")
        
        # Technical requirements
        tech_reqs = detection.get('technical_requirements', [])
        if tech_reqs:
            lines.append("📋 Technical Requirements:")
            for req in tech_reqs:
                lines.append(f"   • {req}")
            lines.append("")
        
        # Missing specifications
        missing = detection.get('missing_specifications', [])
        if missing:
            lines.append("⚠️  Missing/Unclear Specifications:")
            for spec in missing:
                lines.append(f"   • {spec}")
            lines.append("")
        
        # Flexibility
        flexibility = detection.get('tech_flexibility', 'unknown')
        lines.append(f"🎯 Tech Stack Flexibility: {flexibility.upper()}")
        
        # Notes
        if 'notes' in detection:
            lines.append(f"\n📝 Notes: {detection['notes']}")
        
        lines.append("\n" + "=" * 70)
        
        return "\n".join(lines)
