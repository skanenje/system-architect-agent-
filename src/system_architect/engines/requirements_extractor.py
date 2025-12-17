"""
Requirements Extraction Engine

Parses Upwork job descriptions and extracts structured requirements
categorized as: functional, technical, business, timeline, and risks.
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class RequirementsExtractor:
    """
    Extracts and categorizes requirements from natural language project descriptions.
    """
    
    def __init__(self):
        self.extraction_prompt_template = """
You are an expert at analyzing Upwork job postings and extracting requirements.

Analyze this Upwork job description and extract structured requirements.

**Job Description:**
{project_idea}

**Instructions:**
Extract and categorize requirements:

1. **FUNCTIONAL REQUIREMENTS**: Features and capabilities the project must have
   - User-facing features
   - Core functionality
   - Specific behaviors

2. **TECHNICAL REQUIREMENTS**: Technical specifications and constraints
   - Required technologies/frameworks
   - Performance requirements
   - Security requirements
   - Scalability needs
   - Integration requirements

3. **BUSINESS REQUIREMENTS**: Business goals and constraints
   - Target audience
   - Business objectives
   - Success criteria
   - Compliance/regulatory needs

4. **TIMELINE & BUDGET**: Project constraints
   - Deadlines
   - Budget constraints
   - Milestone expectations
   - Delivery schedule

5. **RISKS & UNCLEAR ITEMS**: Potential issues or missing information
   - Ambiguous requirements
   - Technical challenges
   - Missing specifications
   - Clarifications needed

**Output Format:**
Return ONLY valid JSON:
{{
  "functional": ["requirement 1", "requirement 2", ...],
  "technical": ["requirement 1", "requirement 2", ...],
  "business": ["requirement 1", "requirement 2", ...],
  "timeline_budget": ["constraint 1", "constraint 2", ...],
  "risks": ["risk 1", "risk 2", ...]
}}

Return ONLY the JSON, no markdown.
"""
    
    def extract(self, project_idea: str) -> Dict[str, List[str]]:
        """
        Extract structured requirements from a project idea.
        
        Args:
            project_idea: Free-text description of the project
            
        Returns:
            Dictionary with categorized requirements
        """
        prompt = self.extraction_prompt_template.format(project_idea=project_idea)
        
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove trailing ```
            
            response_text = response_text.strip()
            
            # Parse JSON
            requirements = json.loads(response_text)
            
            # Validate structure
            expected_keys = ["functional", "technical", "business", "timeline_budget", "risks"]
            for key in expected_keys:
                if key not in requirements:
                    requirements[key] = []
            
            return requirements
            
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse requirements JSON: {e}")
            print(f"Response was: {response_text}")
            return {
                "functional": [],
                "technical": [],
                "business": [],
                "timeline_budget": [],
                "risks": []
            }
        except Exception as e:
            print(f"Error during requirements extraction: {e}")
            return {
                "functional": [],
                "technical": [],
                "business": [],
                "timeline_budget": [],
                "risks": []
            }
    
    def format_requirements(self, requirements: Dict[str, List[str]]) -> str:
        """
        Format requirements as human-readable text.
        
        Args:
            requirements: Dictionary of categorized requirements
            
        Returns:
            Formatted string representation
        """
        lines = ["=== EXTRACTED REQUIREMENTS ===\n"]
        
        category_names = {
            "functional": "Functional Requirements",
            "technical": "Technical Requirements",
            "business": "Business Requirements",
            "timeline_budget": "Timeline & Budget",
            "risks": "Risks & Unclear Items"
        }
        
        for key, display_name in category_names.items():
            reqs = requirements.get(key, [])
            if reqs:
                lines.append(f"\n📋 {display_name}:")
                for i, req in enumerate(reqs, 1):
                    lines.append(f"   {i}. {req}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the extractor
    from dotenv import load_dotenv
    load_dotenv()
    
    extractor = RequirementsExtractor()
    
    test_idea = """
    I want to build an AI-powered habit tracker mobile app. 
    Users should be able to log daily habits, get AI-generated insights 
    about their patterns, and receive personalized recommendations. 
    The app should work offline and sync when online. 
    I want to launch in 3 months with a small team.
    """
    
    print("Testing Requirements Extraction...")
    print(f"\nProject Idea: {test_idea}\n")
    
    requirements = extractor.extract(test_idea)
    print(extractor.format_requirements(requirements))
    
    print("\n\nRaw JSON:")
    print(json.dumps(requirements, indent=2))
