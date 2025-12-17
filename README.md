# Tech Stack Learning Analyzer 🚀

Analyze any project description and get a complete learning roadmap with tech stack, skill complexity, learning path, API requirements, and portfolio ideas.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get free API key from Google AI Studio
# https://makersuite.google.com/app/apikey

# 3. Create .env file
GEMINI_API_KEY=your_api_key_here

# 4. Start server
python app.py

# 5. Open browser
http://localhost:5000
```

## What It Does

Paste any project description (Upwork job, portfolio idea, etc.) and get:

- **Tech Stack** - All technologies needed
- **Learning Path** - Step-by-step roadmap with time estimates
- **Skill Complexity** - Difficulty level (Beginner → Expert)
- **3rd Party Services** - APIs, costs, and free tier options
- **Portfolio Ideas** - MVP features and deployment suggestions

## Skill Levels

| Level | Score | Learning Time |
|-------|-------|---------------|
| Beginner | 1-3 | 2-4 weeks |
| Intermediate | 4-6 | 1-3 months |
| Advanced | 7-9 | 3-6 months |
| Expert | 10+ | 6+ months |

## Troubleshooting

**Port already in use**: Edit `app.py` and change port to 5001

**Analysis fails**: Check `.env` file exists with valid `GEMINI_API_KEY`

**Slow analysis**: Normal wait time is 30-60 seconds

## License

MIT
