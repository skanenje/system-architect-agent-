import chromadb
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Retrieval:
    def __init__(self, project_id: str):
        self.chroma = chromadb.Client()
        self.collection = self.chroma.get_or_create_collection(
            name=f"memory_{project_id}"
        )

    def embed(self, text: str):
        """Return embedding vector from OpenAI."""
        response = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return response["embedding"]

    def add(self, text: str, metadata=None):
        """Add text to project memory."""
        embedding = self.embed(text)
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}],
            ids=[metadata.get("id")] if metadata and "id" in metadata else [None],
        )

    def query(self, prompt: str, n=5):
        """Retrieve relevant context for follow-up questions."""
        embedding = self.embed(prompt)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n
        )
        return results["documents"][0] if results["documents"] else []
