import uuid
from agent import ArchitectureAgent

def main():
    print("=== System Architecture Agent (PoC) ===")
    project_id = str(uuid.uuid4())[:8]
    agent = ArchitectureAgent(project_id)

    idea = input("\nDescribe your project idea:\n> ")
    print("\n--- Generating Architectural Summary ---\n")
    output = agent.plan(idea)
    print(output)

    print("\n--- Ask follow-up questions (type 'exit' to quit) ---\n")

    while True:
        q = input("> ")
        if q.lower() == "exit":
            break
        answer = agent.answer(q)
        print("\n" + answer + "\n")

if __name__ == "__main__":
    main()
