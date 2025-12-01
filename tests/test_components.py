"""
Quick test script to verify the System Architecture Agent POC components.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_memory():
    """Test the enhanced memory system."""
    print("Testing Memory System...")
    from memory import ProjectMemory
    
    mem = ProjectMemory("test-123")
    mem.set_initial_idea("Test project")
    mem.add_requirement("functional", "User login")
    mem.set_architecture_style("monolith")
    mem.add_component({"name": "API Server", "purpose": "Handle requests"})
    mem.add_decision("Use monolith", "Simple for MVP")
    
    print("✅ Memory system working")
    print(f"   - Requirements: {len(mem.get_requirements()['functional'])}")
    print(f"   - Architecture: {mem.get_architecture_style()}")
    print(f"   - Components: {len(mem.get_components())}")
    print(f"   - Decisions: {len(mem.get_decisions())}")
    print()

def test_templates():
    """Test architecture templates."""
    print("Testing Architecture Templates...")
    from architecture_templates import ArchitectureTemplates
    
    templates = ArchitectureTemplates.get_all_templates()
    print(f"✅ Templates loaded: {list(templates.keys())}")
    
    monolith = ArchitectureTemplates.get_monolith_template()
    print(f"   - Monolith components: {len(monolith['typical_components'])}")
    print()

def test_requirements_extractor():
    """Test requirements extraction (requires API key)."""
    print("Testing Requirements Extractor...")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Skipping (no API key)")
        print()
        return
    
    from requirements_extractor import RequirementsExtractor
    
    extractor = RequirementsExtractor()
    test_idea = "Build a simple todo app"
    
    print(f"   Extracting requirements from: '{test_idea}'")
    requirements = extractor.extract(test_idea)
    
    total_reqs = sum(len(reqs) for reqs in requirements.values())
    print(f"✅ Extracted {total_reqs} requirements")
    for category, reqs in requirements.items():
        if reqs:
            print(f"   - {category}: {len(reqs)}")
    print()

def test_architecture_generator():
    """Test architecture generation (requires API key)."""
    print("Testing Architecture Generator...")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Skipping (no API key)")
        print()
        return
    
    from architecture_generator import ArchitectureGenerator
    
    generator = ArchitectureGenerator()
    test_requirements = {
        "functional": ["User can create tasks", "User can mark tasks complete"],
        "nonfunctional": ["Fast response time"],
        "constraints": ["Small team"],
        "assumptions": [],
        "risks": []
    }
    test_idea = "Simple todo app"
    
    print(f"   Generating architecture for: '{test_idea}'")
    architecture = generator.generate(test_requirements, test_idea)
    
    print(f"✅ Generated {architecture['style']} architecture")
    print(f"   - Components: {len(architecture['components'])}")
    print(f"   - Data flows: {len(architecture.get('data_flow', []))}")
    print()

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("System Architecture Agent - Component Tests")
    print("=" * 60 + "\n")
    
    try:
        test_memory()
        test_templates()
        test_requirements_extractor()
        test_architecture_generator()
        
        print("=" * 60)
        print("✅ All basic tests passed!")
        print("=" * 60 + "\n")
        
        if not os.getenv("GEMINI_API_KEY"):
            print("⚠️  Note: Some tests were skipped because GEMINI_API_KEY is not set")
            print("   Set it in .env to test LLM-powered features\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
