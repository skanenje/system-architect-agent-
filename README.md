# System Architect Agent (PoC)

An AI-powered assistant designed to help you brainstorm and structure system architectures for your software projects. This Proof of Concept (PoC) leverages Google's Gemini models for content generation and embeddings, along with ChromaDB for context-aware memory.

## Features

- **Architectural Planning**: Generates a concise project summary, a list of major components, and a high-level architecture explanation based on your project idea.
- **Context-Aware Q&A**: Maintains a memory of the generated plan and allows you to ask follow-up questions to refine the architecture.
- **Vector Search**: Uses ChromaDB to retrieve relevant context from previous interactions to provide accurate answers.

## Prerequisites

- Python 3.8+
- A Google Gemini API Key

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd system-architect-agent-
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Set up your environment variables:**

    Create a `.env` file in the root directory (or rename `.env.example` if available) and add your Gemini API key:

    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

    Alternatively, you can export it in your shell:

    ```bash
    export GEMINI_API_KEY=your_actual_api_key_here
    ```

## Usage

1.  **Run the agent:**

    ```bash
    python main.py
    ```

2.  **Interact with the agent:**
    -   Enter your project idea when prompted.
    -   Review the generated architectural summary.
    -   Ask follow-up questions to dive deeper into specific components or decisions.
    -   Type `exit` to quit the application.

## Project Structure

-   `main.py`: The entry point of the application. Handles user interaction loop.
-   `agent.py`: Contains the `ArchitectureAgent` class, which orchestrates the planning and answering logic.
-   `memory.py`: Manages the project's memory (summary and components).
-   `retrieval.py`: Handles vector embeddings and retrieval using ChromaDB and Gemini.
-   `requirements.txt`: Lists the Python dependencies.
