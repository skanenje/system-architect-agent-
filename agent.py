import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

from retrieval import Retrieval
from memory import ProjectMemory

class ArchitectureAgent:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.memory = ProjectMemory(project_id)  # Pass project_id to memory
        self.retrieval = Retrieval(project_id)

    def plan(self, idea: str):
        """Generate initial summary + components."""
        prompt = f"""
        You are a system architecture assistant.
        Based on the project idea below, produce:

        1. A concise project summary (5–7 sentences)
        2. A list of major components (bullet points only)
        3. A high-level architecture explanation

        Project Idea:
        {idea}
        """

        response = model.generate_content(prompt)

        output = response.text

        # Memory: store full summary
        self.memory.save_summary(output)
        self.retrieval.add(output, metadata={"id": "initial_plan"})

        return output

    def answer(self, user_query: str):
        """Retrieve memory + answer questions."""
        context_docs = self.retrieval.query(user_query)

        prompt = f"""
        You are an architecture assistant.
        Use the following project memory if helpful:

        Memory:
        {context_docs}

        User Question:
        {user_query}

        Provide a clear, concise answer.
        """

        completion = model.generate_content(prompt)

        return completion.text
