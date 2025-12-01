"""Command-line interface for System Architecture Agent."""

import uuid
import os
from dotenv import load_dotenv
from .core.agent import ArchitectureAgent

# Load environment variables
load_dotenv()


def print_header():
    """Print welcome header."""
    print("\n" + "=" * 70)
    print("🏗️  SYSTEM ARCHITECTURE AGENT - POC")
    print("=" * 70)
    print("\nTransform your project ideas into structured system architectures")
    print("with requirements extraction, component explanations, and more!\n")
    print("Type '/help' for available commands or 'exit' to quit.\n")
    print("=" * 70 + "\n")


def print_help():
    """Print available commands."""
    help_text = """
📚 AVAILABLE COMMANDS:

General:
  /help              - Show this help message
  exit               - Exit the application

Architecture Views:
  /architecture      - Show current architecture
  /requirements      - Show all requirements
  /decisions         - Show architectural decisions
  /summary           - Show project summary

Actions:
  /explain <name>    - Deep dive into a specific component
  /export            - Export project state as JSON

During Planning:
  - Just describe your project idea when prompted
  - Component explanations are generated automatically

During Q&A:
  - Ask any question about the architecture
  - Scope creep detection is automatic
  - Reference specific components for detailed explanations
"""
    print(help_text)


def main():
    """Main application loop."""
    print_header()
    
    # Generate project ID
    project_id = str(uuid.uuid4())[:8]
    
    # Initialize agent
    print(f"🆔 Project ID: {project_id}")
    print("Initializing agent...\n")
    
    try:
        agent = ArchitectureAgent(project_id)
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("\nPlease ensure:")
        print("1. You have set GEMINI_API_KEY in your .env file")
        print("2. All dependencies are installed (pip install -r requirements.txt)")
        return
    
    # ===== PLANNING PHASE =====
    print("=" * 70)
    print("📝 PLANNING PHASE")
    print("=" * 70 + "\n")
    
    idea = input("Describe your project idea:\n> ")
    
    if not idea.strip():
        print("❌ No project idea provided. Exiting.")
        return
    
    print("\n" + "=" * 70)
    print("🚀 Generating architectural plan...")
    print("=" * 70 + "\n")
    print("This may take a minute as we:")
    print("  1. Extract requirements")
    print("  2. Generate architecture")
    print("  3. Explain components")
    print("  4. Recommend tech stacks\n")
    
    try:
        output = agent.plan(idea, explain_components=True)
        print("\n" + output)
    except Exception as e:
        print(f"\n❌ Error during planning: {e}")
        print("Please try again or check your API key and internet connection.")
        return
    
    # ===== Q&A PHASE =====
    print("\n" + "=" * 70)
    print("💬 Q&A PHASE - Ask follow-up questions")
    print("=" * 70)
    print("\nYou can now:")
    print("  • Ask questions about the architecture")
    print("  • Request component explanations")
    print("  • Propose changes (scope creep detection active)")
    print("  • Use commands (type /help for list)\n")
    print("=" * 70 + "\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            # Handle exit
            if user_input.lower() == "exit":
                print("\n👋 Thank you for using System Architecture Agent!")
                print(f"Project ID: {project_id}")
                print("\nGoodbye!\n")
                break
            
            # Handle commands
            if user_input.startswith("/"):
                command_parts = user_input.split(maxsplit=1)
                command = command_parts[0].lower()
                args = command_parts[1] if len(command_parts) > 1 else ""
                
                if command == "/help":
                    print_help()
                
                elif command == "/architecture":
                    print("\n" + agent.show_architecture() + "\n")
                
                elif command == "/requirements":
                    print("\n" + agent.show_requirements() + "\n")
                
                elif command == "/decisions":
                    print("\n" + agent.show_decisions() + "\n")
                
                elif command == "/summary":
                    print("\n" + agent.memory.get_summary() + "\n")
                
                elif command == "/explain":
                    if not args:
                        print("❌ Please specify a component name. Example: /explain Database")
                    else:
                        print(f"\n{agent.get_component_explanation(args)}\n")
                
                elif command == "/export":
                    json_output = agent.export_to_json()
                    filename = f"architecture_{project_id}.json"
                    
                    try:
                        with open(filename, 'w') as f:
                            f.write(json_output)
                        print(f"\n✅ Project exported to: {filename}\n")
                    except Exception as e:
                        print(f"\n❌ Error exporting: {e}\n")
                        print("JSON output:")
                        print(json_output)
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type '/help' for available commands.")
                
                continue
            
            # Regular Q&A
            print()  # Blank line for readability
            answer = agent.answer(user_input)
            print(answer + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Type 'exit' to quit properly.\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("Please try again or type '/help' for commands.\n")


if __name__ == "__main__":
    main()
