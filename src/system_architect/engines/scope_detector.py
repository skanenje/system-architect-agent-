"""
Scope Creep Detector

Detects when user messages introduce new requirements or features
that weren't in the original scope.
"""

import os
import google.generativeai as genai
from typing import Dict, List, Tuple, Optional

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


class ScopeDetector:
    """
    Detects scope creep by comparing new user messages against existing requirements.
    """
    
    def __init__(self):
        self.detection_prompt_template = """
You are an expert project manager and requirements analyst.

Your task is to determine if a user message introduces NEW SCOPE to the project.

**Original Requirements:**
{original_requirements}

**User Message:**
"{user_message}"

**Your Task:**
Analyze if this message introduces:
1. **New features** not in original requirements
2. **New constraints** not previously mentioned
3. **Changed requirements** that modify existing scope

**Classification:**
- **NEW_SCOPE**: Message adds entirely new features or requirements
- **MODIFICATION**: Message changes or refines existing requirements
- **CLARIFICATION**: Message asks questions or clarifies existing requirements (NOT scope change)
- **NO_CHANGE**: Message doesn't affect scope at all

**Output Format:**
Return ONLY a valid JSON object:
{{
  "classification": "NEW_SCOPE|MODIFICATION|CLARIFICATION|NO_CHANGE",
  "confidence": "high|medium|low",
  "detected_changes": ["change 1", "change 2", ...],
  "explanation": "Brief explanation of your classification"
}}

Return ONLY the JSON, no markdown formatting.
"""
    
    def detect(self, user_message: str, 
               current_requirements: Dict[str, List[str]],
               initial_idea: str) -> Dict[str, any]:
        """
        Detect if user message introduces scope creep.
        
        Args:
            user_message: The user's new message
            current_requirements: Current project requirements
            initial_idea: Original project idea
            
        Returns:
            Detection result with classification and details
        """
        # Format requirements for prompt
        req_text = self._format_requirements(current_requirements)
        full_context = f"Original Idea: {initial_idea}\n\nRequirements:\n{req_text}"
        
        prompt = self.detection_prompt_template.format(
            original_requirements=full_context,
            user_message=user_message
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
            
            import json
            result = json.loads(response_text)
            
            # Validate result
            valid_classifications = ["NEW_SCOPE", "MODIFICATION", "CLARIFICATION", "NO_CHANGE"]
            if result.get("classification") not in valid_classifications:
                result["classification"] = "CLARIFICATION"
            
            return result
            
        except Exception as e:
            print(f"Error detecting scope creep: {e}")
            # Default to clarification on error
            return {
                "classification": "CLARIFICATION",
                "confidence": "low",
                "detected_changes": [],
                "explanation": "Unable to analyze scope change"
            }
    
    def _format_requirements(self, requirements: Dict[str, List[str]]) -> str:
        """Format requirements dictionary as text."""
        lines = []
        for category, reqs in requirements.items():
            if reqs:
                lines.append(f"\n{category.upper()}:")
                for req in reqs:
                    # Handle both string and dict formats
                    if isinstance(req, dict):
                        lines.append(f"  - {req.get('text', str(req))}")
                    else:
                        lines.append(f"  - {req}")
        return "\n".join(lines) if lines else "No requirements defined"
    
    def should_prompt_user(self, detection_result: Dict[str, any]) -> bool:
        """
        Determine if we should prompt the user about scope change.
        
        Args:
            detection_result: Result from detect()
            
        Returns:
            True if user should be prompted
        """
        classification = detection_result.get("classification", "CLARIFICATION")
        confidence = detection_result.get("confidence", "low")
        
        # Prompt for new scope or modifications with medium/high confidence
        if classification in ["NEW_SCOPE", "MODIFICATION"]:
            if confidence in ["medium", "high"]:
                return True
        
        return False
    
    def format_scope_alert(self, detection_result: Dict[str, any]) -> str:
        """
        Format a scope change alert for the user.
        
        Args:
            detection_result: Result from detect()
            
        Returns:
            Formatted alert message
        """
        classification = detection_result.get("classification", "UNKNOWN")
        changes = detection_result.get("detected_changes", [])
        explanation = detection_result.get("explanation", "")
        
        if classification == "NEW_SCOPE":
            header = "🚨 NEW SCOPE DETECTED"
            message = "Your message introduces new features or requirements:"
        elif classification == "MODIFICATION":
            header = "⚠️  SCOPE MODIFICATION DETECTED"
            message = "Your message modifies existing requirements:"
        else:
            return ""
        
        lines = [
            f"\n{'=' * 60}",
            header,
            f"{'=' * 60}\n",
            message
        ]
        
        for i, change in enumerate(changes, 1):
            lines.append(f"  {i}. {change}")
        
        lines.extend([
            f"\nExplanation: {explanation}",
            "\nHow would you like to proceed?",
            "  1. Accept and add to scope",
            "  2. Replace existing requirements",
            "  3. Defer for later",
            "  4. Cancel (ignore this change)",
            f"\n{'=' * 60}\n"
        ])
        
        return "\n".join(lines)
    
    def extract_new_requirements(self, user_message: str, 
                                 detection_result: Dict[str, any]) -> Dict[str, List[str]]:
        """
        Extract new requirements from the user message.
        
        Args:
            user_message: The user's message
            detection_result: Detection result
            
        Returns:
            Dictionary of new requirements by category
        """
        if detection_result.get("classification") not in ["NEW_SCOPE", "MODIFICATION"]:
            return {
                "functional": [],
                "nonfunctional": [],
                "constraints": [],
                "assumptions": [],
                "risks": []
            }
        
        prompt = f"""
Extract new requirements from this user message.

**User Message:**
"{user_message}"

**Detected Changes:**
{detection_result.get('detected_changes', [])}

**Your Task:**
Extract the new requirements and categorize them.

**Output Format:**
Return ONLY a valid JSON object:
{{
  "functional": ["req1", "req2", ...],
  "nonfunctional": ["req1", "req2", ...],
  "constraints": ["constraint1", ...],
  "assumptions": ["assumption1", ...],
  "risks": ["risk1", ...]
}}

Return ONLY the JSON, no markdown formatting.
"""
        
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
            
            import json
            new_reqs = json.loads(response_text)
            
            # Ensure all categories exist
            for category in ["functional", "nonfunctional", "constraints", "assumptions", "risks"]:
                if category not in new_reqs:
                    new_reqs[category] = []
            
            return new_reqs
            
        except Exception as e:
            print(f"Error extracting new requirements: {e}")
            return {
                "functional": [],
                "nonfunctional": [],
                "constraints": [],
                "assumptions": [],
                "risks": []
            }


if __name__ == "__main__":
    # Test the detector
    from dotenv import load_dotenv
    load_dotenv()
    
    detector = ScopeDetector()
    
    initial_idea = "AI-powered habit tracker mobile app"
    current_requirements = {
        "functional": [
            "Users can log daily habits",
            "AI generates insights",
            "Personalized recommendations"
        ],
        "nonfunctional": [
            "Must work offline",
            "Support 10,000 users"
        ],
        "constraints": ["3 month timeline"],
        "assumptions": ["Users have smartphones"],
        "risks": ["AI model accuracy"]
    }
    
    # Test cases
    test_messages = [
        "Can you explain the database component?",  # CLARIFICATION
        "Add real-time chat between users",  # NEW_SCOPE
        "Actually, we need to support 100,000 users",  # MODIFICATION
    ]
    
    print("Testing Scope Creep Detection...\n")
    
    for msg in test_messages:
        print(f"User Message: \"{msg}\"")
        result = detector.detect(msg, current_requirements, initial_idea)
        print(f"Classification: {result['classification']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Explanation: {result['explanation']}")
        
        if detector.should_prompt_user(result):
            print(detector.format_scope_alert(result))
        
        print("\n" + "=" * 70 + "\n")
