"""
Third Party Requirements Detector

Identifies external services, APIs, and credentials needed for projects.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class ThirdPartyDetector:
    """
    Detects 3rd party services, APIs, and external requirements.
    """
    
    def __init__(self):
        self.detection_prompt = """
You are an expert at identifying external service dependencies in projects.

Analyze this project and identify ALL 3rd party requirements.

**Project Description:**
{project_description}

**Detected Features:**
{features}

**Your Task:**
Identify every external service, API, or 3rd party tool needed.

**Output Format:**
Return ONLY valid JSON:
{{
  "authentication_services": [
    {{
      "service": "Service name (e.g., Auth0, Firebase Auth)",
      "purpose": "What it's used for",
      "api_key_required": true|false,
      "pricing": "free|freemium|paid",
      "free_tier_limits": "Description of free tier",
      "setup_complexity": "easy|medium|hard",
      "alternatives": ["alternative1", "alternative2"]
    }}
  ],
  "payment_services": [...],
  "cloud_storage": [...],
  "email_services": [...],
  "sms_services": [...],
  "maps_location": [...],
  "analytics": [...],
  "monitoring": [...],
  "cdn_hosting": [...],
  "database_services": [...],
  "ai_ml_services": [...],
  "other_apis": [...],
  "development_tools": [
    {{
      "tool": "Tool name",
      "purpose": "What it's for",
      "required_for": "development|deployment|testing",
      "cost": "free|paid"
    }}
  ],
  "total_api_keys_needed": number,
  "estimated_monthly_cost": "Free|$X-Y|$X+",
  "free_tier_viable": true|false,
  "setup_guide": [
    "Step 1: Sign up for X",
    "Step 2: Get API key from Y",
    ...
  ]
}}

Return ONLY the JSON, no markdown.
"""
    
    def detect(self, project_description: str, features: list) -> dict:
        """Detect 3rd party requirements."""
        features_text = "\n".join([f"- {f}" for f in features]) if features else "No specific features listed"
        
        prompt = self.detection_prompt.format(
            project_description=project_description,
            features=features_text
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
            print(f"Error detecting 3rd party requirements: {e}")
            return {
                "total_api_keys_needed": 0,
                "estimated_monthly_cost": "Unknown",
                "error": str(e)
            }
    
    def format_third_party(self, detection: dict) -> str:
        """Format 3rd party requirements for display."""
        lines = [
            "\n" + "=" * 70,
            "🔌 3RD PARTY SERVICES & API REQUIREMENTS",
            "=" * 70 + "\n",
            f"🔑 Total API Keys Needed: {detection.get('total_api_keys_needed', 0)}",
            f"💰 Estimated Monthly Cost: {detection.get('estimated_monthly_cost', 'Unknown')}",
            f"🆓 Free Tier Viable: {'Yes ✅' if detection.get('free_tier_viable') else 'No ❌'}\n",
            "=" * 70 + "\n"
        ]
        
        # Categories to display
        categories = [
            ('authentication_services', '🔐 Authentication Services'),
            ('payment_services', '💳 Payment Services'),
            ('cloud_storage', '☁️  Cloud Storage'),
            ('email_services', '📧 Email Services'),
            ('sms_services', '📱 SMS Services'),
            ('maps_location', '🗺️  Maps & Location'),
            ('analytics', '📊 Analytics'),
            ('monitoring', '🔍 Monitoring'),
            ('cdn_hosting', '🌐 CDN & Hosting'),
            ('database_services', '🗄️  Database Services'),
            ('ai_ml_services', '🤖 AI/ML Services'),
            ('other_apis', '🔧 Other APIs')
        ]
        
        for key, title in categories:
            services = detection.get(key, [])
            if services:
                lines.append(f"{title}:")
                for service in services:
                    pricing_emoji = "🆓" if service.get('pricing') == 'free' else "💵" if service.get('pricing') == 'freemium' else "💰"
                    lines.append(f"\n   • {service.get('service', 'Unknown')} {pricing_emoji}")
                    lines.append(f"     Purpose: {service.get('purpose', 'N/A')}")
                    lines.append(f"     API Key: {'Required' if service.get('api_key_required') else 'Not required'}")
                    lines.append(f"     Setup: {service.get('setup_complexity', 'unknown').upper()}")
                    
                    if service.get('free_tier_limits'):
                        lines.append(f"     Free Tier: {service['free_tier_limits']}")
                    
                    alternatives = service.get('alternatives', [])
                    if alternatives:
                        lines.append(f"     Alternatives: {', '.join(alternatives)}")
                
                lines.append("")
        
        # Development tools
        tools = detection.get('development_tools', [])
        if tools:
            lines.append("🛠️  Development Tools:")
            for tool in tools:
                cost_emoji = "🆓" if tool.get('cost') == 'free' else "💰"
                lines.append(f"\n   • {tool.get('tool', 'Unknown')} {cost_emoji}")
                lines.append(f"     Purpose: {tool.get('purpose', 'N/A')}")
                lines.append(f"     Required for: {tool.get('required_for', 'unknown')}")
            lines.append("")
        
        # Setup guide
        setup_guide = detection.get('setup_guide', [])
        if setup_guide:
            lines.append("=" * 70)
            lines.append("📋 SETUP GUIDE")
            lines.append("=" * 70 + "\n")
            for step in setup_guide:
                lines.append(f"   {step}")
            lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
