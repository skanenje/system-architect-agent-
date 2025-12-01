# System Architecture Agent (POC)

An AI-powered conversational agent that transforms project ideas into structured system architectures with deep technical explanations, requirements analysis, and scope management.

## 🎯 What It Does

The System Architecture Agent is your AI consultant for system design. Give it a project idea, and it will:

1. **Extract Requirements** - Automatically categorizes your needs into functional, nonfunctional, constraints, assumptions, and risks
2. **Generate Architecture** - Selects the best architecture pattern (monolith, microservices, event-driven, or agentic) and customizes it for your project
3. **Explain Components** - Provides first-principles explanations of each component, including trade-offs and scaling characteristics
4. **Recommend Tech Stacks** - Suggests 2-3 viable technology stacks with detailed evaluation
5. **Detect Scope Creep** - Monitors conversations for new requirements and alerts you to scope changes
6. **Maintain Context** - Keeps chat-scoped memory of all decisions, requirements, and architectural choices

## ✨ Key Features

### Requirements Extraction (FR-2)
- Parses free-text project ideas
- Categorizes into 5 requirement types
- Produces structured JSON representation
- Stores in searchable memory

### Architecture Generation (FR-3)
- **4 Architecture Templates**: Monolith, Microservices, Event-Driven, Agentic
- Intelligent style selection based on requirements
- Customized component lists
- Data flow descriptions
- Architecture decision recording

### Component Explanation Engine (FR-4)
- First-principles explanations for each component
- Covers: purpose, computational problems solved, trade-offs, scaling limits
- Explains WHY each component exists in YOUR architecture
- Deep technical reasoning, not surface-level descriptions

### Tech Stack Recommendations (FR-7)
- 2-3 practical stack options per project
- Evaluated on: integration simplicity, performance, ecosystem maturity, developer ergonomics
- Specific technology suggestions for each layer
- Best-for scenarios

### Scope Creep Detection (FR-6)
- Compares new messages against existing requirements
- Classifies as: NEW_SCOPE, MODIFICATION, CLARIFICATION, or NO_CHANGE
- Prompts user for decision when scope changes detected
- Options: Accept, Replace, Defer, or Cancel

### Enhanced Memory (FR-5)
- Chat-scoped project memory
- Stores: requirements, architecture, components, data flows, decisions, open questions
- Vector search for context-aware Q&A
- JSON export capability

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd system-architect-agent-
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Usage

Run the agent:
```bash
python main.py
```

**Example Session:**
```
> Describe your project idea:
> I want to build an AI-powered habit tracker mobile app with offline support

[Agent extracts requirements, generates architecture, explains components, recommends tech stacks]

> Can you explain the Vector Database component?
[Agent provides deep first-principles explanation]

> Add real-time chat between users
[Scope creep detected! Agent prompts for decision]
```

## 📚 Available Commands

During the Q&A phase, you can use these commands:

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/architecture` | Display current architecture |
| `/requirements` | Show all extracted requirements |
| `/decisions` | Show architectural decisions made |
| `/summary` | Show project summary |
| `/explain <component>` | Deep dive into a specific component |
| `/export` | Export project state as JSON |
| `exit` | Exit the application |

## 🏗️ Architecture Patterns

The agent supports 4 architecture templates:

### 1. Monolith
- **Best for**: MVPs, small-medium apps, simple requirements
- **Characteristics**: Simple deployment, shared database, tight coupling
- **Typical components**: Web server, database, cache, background workers

### 2. Microservices
- **Best for**: Large scale, multiple teams, complex domains
- **Characteristics**: Independent deployment, fault isolation, horizontal scaling
- **Typical components**: API gateway, domain services, service databases, message queue

### 3. Event-Driven
- **Best for**: Real-time systems, high throughput, IoT
- **Characteristics**: Loose coupling, eventual consistency, real-time capabilities
- **Typical components**: Event producers, event bus, consumers, stream processors

### 4. Agentic
- **Best for**: AI-powered apps, autonomous systems, conversational interfaces
- **Characteristics**: Autonomous decision-making, tool integration, state management
- **Typical components**: Agent orchestrator, LLM service, vector DB, tool registry

## 📁 Project Structure

```
system-architect-agent-/
├── main.py                          # CLI entry point
├── agent.py                         # Main orchestrator
├── memory.py                        # Enhanced project memory
├── retrieval.py                     # Vector storage & retrieval
├── requirements_extractor.py        # Requirements extraction engine
├── architecture_generator.py        # Architecture generation
├── architecture_templates.py        # Architecture pattern templates
├── component_explainer.py           # Component explanation engine
├── tech_stack_recommender.py        # Tech stack recommendations
├── scope_detector.py                # Scope creep detection
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🎓 Example Use Cases

### 1. MVP Planning
"I want to build a SaaS tool for project management with real-time collaboration"
- Agent suggests monolith architecture
- Explains why WebSockets are needed
- Recommends Node.js + React stack

### 2. Scaling Existing System
"We have 100K users and need to scale our monolith"
- Agent suggests microservices migration
- Explains service boundaries
- Recommends gradual migration strategy

### 3. AI Application
"Build a chatbot that can search our documentation and answer questions"
- Agent suggests agentic architecture
- Explains RAG (Retrieval Augmented Generation)
- Recommends vector database + LLM stack

## 🔬 POC Scope

### ✅ Implemented (Must-Haves)
- [x] Requirements extraction (FR-2)
- [x] Architecture generation (FR-3)
- [x] Component explanations (FR-4)
- [x] Chat-scoped memory (FR-5)
- [x] Scope creep detection (FR-6)
- [x] Tech stack recommendations (FR-7)

### ❌ Out of Scope (Per PRD)
- External tool calls (web search, code execution)
- Long-term memory across sessions
- Multi-agent workflows
- Detailed cost/latency equations
- Project timelines or milestone planning
- Code generation
- DevOps infrastructure details

## 🤝 Contributing

This is a POC (Proof of Concept). Feedback and suggestions are welcome!

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- Built with [Google Gemini](https://deepmind.google/technologies/gemini/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)
- Inspired by the need for better architecture planning tools

