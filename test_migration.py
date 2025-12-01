import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY", "test-key"))

from agent import ArchitectureAgent

def main():
    try:
        agent = ArchitectureAgent("test-project")
        print("Agent instantiated successfully")
    except Exception as e:
        print(f"Error during instantiation: {e}")

if __name__ == "__main__":
    main()
