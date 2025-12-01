"""
Requirements Extraction Engine

Parses free-text project ideas and extracts structured requirements
categorized as: functional, nonfunctional, constraints, assumptions, and risks.
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


class RequirementsExtractor:
    """
    Extracts and categorizes requirements from natural language project descriptions.
    """
    
    def __init__(self):
        self.extraction_prompt_template = """
You are an expert system architect and requirements analyst.

Your task is to analyze a project idea and extract structured requirements.

**Project Idea:**
{project_idea}

**Instructions:**
Extract and categorize requirements into the following categories:

1. **FUNCTIONAL REQUIREMENTS**: What the system must DO. Specific features and capabilities.
   - Focus on user-facing features and system behaviors
   - Be specific and actionable

2. **NONFUNCTIONAL REQUIREMENTS**: Quality attributes and constraints.
   - Performance (latency, throughput)
   - Scalability (expected users, data volume)
   - Availability/Reliability
   - Security requirements
   - Cost constraints

3. **CONSTRAINTS**: Technical or business limitations.
   - Technology constraints (must use X, can't use Y)
   - Budget constraints
   - Timeline constraints
   - Team size/skill constraints
   - Regulatory/compliance requirements

4. **ASSUMPTIONS**: Things we're assuming to be true.
   - User behavior assumptions
   - Technical assumptions
   - Business assumptions
   - Infrastructure assumptions

5. **RISKS/UNKNOWNS**: Potential issues or unclear aspects.
   - Technical risks
   - Business risks
   - Unclear requirements that need clarification
   - Dependencies on external factors

**Output Format:**
Return ONLY a valid JSON object with this exact structure:
{{
  "functional": ["requirement 1", "requirement 2", ...],
  "nonfunctional": ["requirement 1", "requirement 2", ...],
  "constraints": ["constraint 1", "constraint 2", ...],
  "assumptions": ["assumption 1", "assumption 2", ...],
  "risks": ["risk 1", "risk 2", ...]
}}

**Important:**
- Be thorough but concise
- Infer reasonable requirements even if not explicitly stated
- Each item should be a clear, standalone statement
- Return ONLY the JSON, no additional text or markdown formatting
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
            expected_keys = ["functional", "nonfunctional", "constraints", "assumptions", "risks"]
            for key in expected_keys:
                if key not in requirements:
                    requirements[key] = []
            
            return requirements
            
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse requirements JSON: {e}")
            print(f"Response was: {response_text}")
            # Return empty structure on failure
            return {
                "functional": [],
                "nonfunctional": [],
                "constraints": [],
                "assumptions": [],
                "risks": []
            }
        except Exception as e:
            print(f"Error during requirements extraction: {e}")
            return {
                "functional": [],
                "nonfunctional": [],
                "constraints": [],
                "assumptions": [],
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
            "nonfunctional": "Nonfunctional Requirements",
            "constraints": "Constraints",
            "assumptions": "Assumptions",
            "risks": "Risks & Unknowns"
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
