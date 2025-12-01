# Quick Start Guide - System Architecture Agent

## 🚀 Get Started in 3 Steps

### Step 1: Setup (One-time)
```bash
# Clone and navigate
cd system-architect-agent-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### Step 2: Run
```bash
python main.py
```

### Step 3: Describe Your Project
```
> Describe your project idea:
> I want to build [your project description]
```

That's it! The agent will:
1. ✅ Extract requirements
2. ✅ Generate architecture
3. ✅ Explain components
4. ✅ Recommend tech stacks

---

## 💬 Example Conversations

### Example 1: Simple Web App
```
> I want to build a blog platform where users can write and publish articles

[Agent generates monolith architecture with web server, database, auth system]

> How does the authentication system work?
[Detailed first-principles explanation]

> What if I need to support 1 million users?
[Agent explains scaling strategies]
```

### Example 2: AI Application
```
> Build a chatbot that answers questions about our product documentation

[Agent generates agentic architecture with LLM, vector DB, RAG pipeline]

> Explain the Vector Database component
[Deep dive into semantic search and embeddings]

> Add voice input support
[Scope creep detected! Agent asks for confirmation]
```

### Example 3: Real-time System
```
> IoT dashboard showing sensor data in real-time from 10,000 devices

[Agent generates event-driven architecture with Kafka, stream processing]

> Show me the data flows
[Displays how data moves through the system]

> /export
[Exports complete architecture to JSON]
```

---

## 🎮 Available Commands

| Command | What It Does | Example |
|---------|--------------|---------|
| `/help` | Show all commands | `/help` |
| `/architecture` | View current architecture | `/architecture` |
| `/requirements` | View extracted requirements | `/requirements` |
| `/decisions` | View architectural decisions | `/decisions` |
| `/summary` | Quick project overview | `/summary` |
| `/explain <name>` | Deep dive into component | `/explain Database` |
| `/export` | Save to JSON file | `/export` |
| `exit` | Quit the application | `exit` |

---

## 🎯 Pro Tips

### 1. Be Specific in Your Initial Description
❌ **Vague**: "Build a social media app"
✅ **Better**: "Build a photo-sharing app like Instagram with filters, stories, and real-time messaging for 100K users"

### 2. Ask Follow-up Questions
The agent maintains context, so you can:
- Ask "why" questions
- Request deeper explanations
- Explore alternatives
- Discuss trade-offs

### 3. Use Scope Detection Wisely
When the agent detects scope creep:
- **Option 1**: Accept and expand scope
- **Option 2**: Replace existing requirements
- **Option 3**: Defer for later
- **Option 4**: Cancel the change

### 4. Export Your Work
Always export before exiting:
```
> /export
✅ Project exported to: architecture_abc123.json
```

---

## 🏗️ Architecture Patterns Explained

### When to Use Each Pattern

#### 🏢 Monolith
**Use when:**
- Building an MVP
- Small team (1-5 people)
- Simple requirements
- Need fast time-to-market

**Example projects:**
- Blog platforms
- Small SaaS tools
- Internal tools
- Portfolio websites

---

#### 🔷 Microservices
**Use when:**
- Large scale (100K+ users)
- Multiple teams
- Complex domain
- Need independent deployment

**Example projects:**
- E-commerce platforms
- Multi-tenant SaaS
- Enterprise applications
- Marketplace platforms

---

#### ⚡ Event-Driven
**Use when:**
- Real-time requirements
- High throughput
- IoT/sensor data
- Async workflows

**Example projects:**
- IoT dashboards
- Real-time analytics
- Streaming platforms
- Financial trading systems

---

#### 🤖 Agentic
**Use when:**
- AI-powered features
- Conversational interfaces
- Autonomous workflows
- RAG (Retrieval Augmented Generation)

**Example projects:**
- AI chatbots
- Document Q&A systems
- AI assistants
- Recommendation engines

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "Error: GEMINI_API_KEY not found"
**Solution**: Set your API key
```bash
echo "GEMINI_API_KEY=your_key" > .env
```

### Agent responses are slow
**Normal**: First request may take 30-60 seconds as it:
- Extracts requirements
- Generates architecture
- Explains components
- Recommends tech stacks

Subsequent Q&A is much faster!

### Scope detection too sensitive
**Solution**: Just say "no" or choose option 4 to cancel

---

## 📚 Learning Resources

### Understanding Architecture Patterns
- [Monolith vs Microservices](https://martinfowler.com/articles/microservices.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [AI Agent Patterns](https://www.anthropic.com/research/building-effective-agents)

### Tech Stack Decisions
- [Stack Overflow Developer Survey](https://survey.stackoverflow.co/)
- [ThoughtWorks Tech Radar](https://www.thoughtworks.com/radar)

---

## 🎓 Sample Projects to Try

### Beginner
1. "Todo list app with user accounts"
2. "Recipe sharing website"
3. "Personal finance tracker"

### Intermediate
1. "Project management tool with real-time collaboration"
2. "E-commerce store with payment processing"
3. "Social media platform for developers"

### Advanced
1. "Multi-tenant SaaS analytics platform"
2. "Real-time multiplayer game backend"
3. "AI-powered code review assistant"

---

## 💡 Best Practices

### 1. Start Simple
Begin with core features, then iterate:
```
> Build a task manager
[Get architecture]

> Add team collaboration
[Scope detected, decide to accept]

> Add AI task suggestions
[Architecture evolves]
```

### 2. Ask "Why" Questions
```
> Why did you choose a monolith over microservices?
> What are the trade-offs of using Redis?
> When would this architecture become a bottleneck?
```

### 3. Explore Alternatives
```
> What if I used PostgreSQL instead of MongoDB?
> Compare REST API vs GraphQL for this project
> Show me a microservices version of this architecture
```

### 4. Document Decisions
The agent tracks decisions automatically, but you can:
```
> /decisions
[See all architectural decisions and rationale]

> /export
[Save complete project state]
```

---

## 🎉 You're Ready!

Start the agent and describe your project idea. The AI will guide you through creating a solid architecture!

```bash
python main.py
```

**Happy architecting!** 🏗️✨
