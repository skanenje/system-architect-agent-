"""
Architecture Generator

Analyzes requirements and generates appropriate system architecture
by selecting and customizing architecture templates.
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Any
from architecture_templates import ArchitectureTemplates

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


class ArchitectureGenerator:
    """
    Generates system architecture based on requirements.
    Selects appropriate template and customizes it.
    """
    
    def __init__(self):
        self.templates = ArchitectureTemplates()
    
    def select_architecture_style(self, requirements: Dict[str, List[str]], 
                                   project_idea: str) -> str:
        """
        Determine the most appropriate architecture style based on requirements.
        
        Args:
            requirements: Categorized requirements dictionary
            project_idea: Original project description
            
        Returns:
            Architecture style name: 'monolith', 'microservices', 'event-driven', or 'agentic'
        """
        prompt = f"""
You are an expert system architect. Analyze the following project and determine the MOST APPROPRIATE architecture style.

**Project Idea:**
{project_idea}

**Requirements:**
{json.dumps(requirements, indent=2)}

**Available Architecture Styles:**
1. **monolith** - Single unified application. Best for: MVPs, small-medium apps, simple requirements, small teams
2. **microservices** - Distributed independent services. Best for: large scale, multiple teams, complex domains, need for independent deployment
3. **event-driven** - Event-based async communication. Best for: real-time systems, high throughput, IoT, streaming data
4. **agentic** - AI agents with autonomous workflows. Best for: AI-powered apps, conversational interfaces, autonomous decision-making

**Selection Criteria:**
- Complexity of requirements
- Scale expectations (users, data volume)
- Real-time requirements
- AI/ML requirements
- Team size (if mentioned)
- Time to market
- Operational complexity tolerance

**Instructions:**
Analyze the requirements and respond with ONLY ONE WORD - the architecture style name.
Choose the SIMPLEST architecture that meets the requirements. Don't over-engineer.

Response (one word only):"""

        try:
            response = model.generate_content(prompt)
            style = response.text.strip().lower()
            
            # Validate response
            valid_styles = ['monolith', 'microservices', 'event-driven', 'agentic']
            if style not in valid_styles:
                # Default to monolith if unclear
                print(f"Warning: Unclear architecture style '{style}', defaulting to 'monolith'")
                return 'monolith'
            
            return style
            
        except Exception as e:
            print(f"Error selecting architecture style: {e}")
            return 'monolith'  # Safe default
    
    def customize_architecture(self, template: Dict[str, Any], 
                               requirements: Dict[str, List[str]],
                               project_idea: str) -> Dict[str, Any]:
        """
        Customize the architecture template based on specific requirements.
        
        Args:
            template: Base architecture template
            requirements: Project requirements
            project_idea: Original project description
            
        Returns:
            Customized architecture with specific components
        """
        prompt = f"""
You are an expert system architect. Customize the following architecture template for this specific project.

**Project Idea:**
{project_idea}

**Requirements:**
{json.dumps(requirements, indent=2)}

**Base Architecture Template:**
Style: {template['style']}
Description: {template['description']}

**Template Components:**
{json.dumps(template['typical_components'], indent=2)}

**Your Task:**
1. Select which components from the template are NEEDED for this project
2. Add any ADDITIONAL components specific to this project's requirements
3. For each component, provide:
   - name: Component name
   - type: Component type
   - purpose: What it does
   - justification: Why it's needed for THIS project
   - technologies: Suggested technologies (1-2 options)

**Output Format:**
Return ONLY a valid JSON array of components:
[
  {{
    "name": "Component Name",
    "type": "component_type",
    "purpose": "What it does",
    "justification": "Why needed for this project",
    "technologies": ["Option 1", "Option 2"]
  }},
  ...
]

Be specific to this project. Don't include unnecessary components.
Return ONLY the JSON array, no markdown formatting.
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
            
            components = json.loads(response_text)
            
            return {
                "style": template['style'],
                "description": template['description'],
                "components": components,
                "characteristics": template['characteristics']
            }
            
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse customized components: {e}")
            # Fallback to template components
            return {
                "style": template['style'],
                "description": template['description'],
                "components": template['typical_components'],
                "characteristics": template['characteristics']
            }
        except Exception as e:
            print(f"Error customizing architecture: {e}")
            return {
                "style": template['style'],
                "description": template['description'],
                "components": template['typical_components'],
                "characteristics": template['characteristics']
            }
    
    def generate_data_flows(self, components: List[Dict[str, Any]], 
                           project_idea: str) -> List[Dict[str, Any]]:
        """
        Generate data flow descriptions between components.
        
        Args:
            components: List of architecture components
            project_idea: Original project description
            
        Returns:
            List of data flow descriptions
        """
        component_names = [c['name'] for c in components]
        
        prompt = f"""
You are an expert system architect. Define the data flows between these components.

**Project:**
{project_idea}

**Components:**
{json.dumps(component_names, indent=2)}

**Your Task:**
Define how data flows between these components. For each flow, specify:
- from: Source component
- to: Destination component
- data: What data is being transferred
- protocol: Communication protocol/method

**Output Format:**
Return ONLY a valid JSON array:
[
  {{
    "from": "Component A",
    "to": "Component B",
    "data": "Description of data",
    "protocol": "HTTP/gRPC/etc"
  }},
  ...
]

Focus on the PRIMARY data flows. Don't include every possible interaction.
Return ONLY the JSON array, no markdown formatting.
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
            
            data_flows = json.loads(response_text)
            return data_flows
            
        except Exception as e:
            print(f"Error generating data flows: {e}")
            return []
    
    def generate(self, requirements: Dict[str, List[str]], 
                 project_idea: str) -> Dict[str, Any]:
        """
        Generate complete architecture based on requirements.
        
        Args:
            requirements: Categorized requirements
            project_idea: Original project description
            
        Returns:
            Complete architecture specification
        """
        # Step 1: Select architecture style
        style = self.select_architecture_style(requirements, project_idea)
        print(f"Selected architecture style: {style}")
        
        # Step 2: Get base template
        template = self.templates.get_template(style)
        
        # Step 3: Customize components
        customized = self.customize_architecture(template, requirements, project_idea)
        
        # Step 4: Generate data flows
        data_flows = self.generate_data_flows(customized['components'], project_idea)
        
        # Step 5: Combine into final architecture
        architecture = {
            "style": customized['style'],
            "description": customized['description'],
            "characteristics": customized['characteristics'],
            "components": customized['components'],
            "data_flow": data_flows
        }
        
        return architecture
    
    def format_architecture(self, architecture: Dict[str, Any]) -> str:
        """
        Format architecture as human-readable text.
        
        Args:
            architecture: Architecture specification
            
        Returns:
            Formatted string
        """
        lines = [
            "=== SYSTEM ARCHITECTURE ===\n",
            f"📐 Style: {architecture['style'].upper()}",
            f"📝 Description: {architecture['description']}\n",
            "\n🎯 Characteristics:"
        ]
        
        for char in architecture.get('characteristics', []):
            lines.append(f"   • {char}")
        
        lines.append("\n\n🏗️  Components:")
        for i, comp in enumerate(architecture.get('components', []), 1):
            lines.append(f"\n   {i}. {comp['name']} ({comp.get('type', 'N/A')})")
            lines.append(f"      Purpose: {comp.get('purpose', 'N/A')}")
            if 'justification' in comp:
                lines.append(f"      Why: {comp['justification']}")
            if 'technologies' in comp and comp['technologies']:
                tech_str = ", ".join(comp['technologies'][:2])  # Show max 2
                lines.append(f"      Tech: {tech_str}")
        
        if architecture.get('data_flow'):
            lines.append("\n\n🔄 Data Flows:")
            for i, flow in enumerate(architecture['data_flow'], 1):
                lines.append(f"   {i}. {flow['from']} → {flow['to']}")
                lines.append(f"      Data: {flow['data']}")
                lines.append(f"      Protocol: {flow['protocol']}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the generator
    from dotenv import load_dotenv
    load_dotenv()
    
    generator = ArchitectureGenerator()
    
    test_idea = "AI-powered habit tracker mobile app with offline support and personalized recommendations"
    test_requirements = {
        "functional": [
            "Users can log daily habits",
            "AI generates insights about patterns",
            "Personalized recommendations",
            "Offline functionality with sync"
        ],
        "nonfunctional": [
            "Must work offline",
            "Fast sync when online",
            "Support 10,000 users initially"
        ],
        "constraints": [
            "3 month timeline",
            "Small team"
        ],
        "assumptions": [
            "Users have smartphones",
            "Internet available periodically"
        ],
        "risks": [
            "AI model accuracy",
            "Offline sync conflicts"
        ]
    }
    
    print("Testing Architecture Generation...")
    print(f"\nProject: {test_idea}\n")
    
    architecture = generator.generate(test_requirements, test_idea)
    print(generator.format_architecture(architecture))
