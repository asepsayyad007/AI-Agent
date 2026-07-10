<div align="center">

# 🤖 AI Agent

**A fully offline, autonomous AI software engineer that runs on your local machine.**

Built with [Ollama](https://ollama.com) • No API keys • No cloud • Complete privacy

![Version](https://img.shields.io/badge/version-0.9-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

</div>

---

## 🎯 What is AI Agent?

AI Agent is a command-line AI assistant that can write code, browse the web, manage git repos, and execute terminal commands — all running locally on your PC using Ollama. No internet required for the AI itself.

Think of it as your personal offline Copilot that can actually *do* things, not just suggest them.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖥️ **Terminal Execution** | Run any shell command and analyze output |
| 📁 **File Operations** | Read, write, delete, list files and directories |
| 🌿 **Git Operations** | Status, log, diff, add, commit, branch, checkout, push, pull |
| 🌐 **Web Browsing** | Navigate URLs, extract text, take screenshots, click elements |
| 🔍 **Web Search** | Search DuckDuckGo and get summarized results |
| 🧠 **Multi-Model** | Switch between models on the fly (fast, heavy, reasoning) |
| 🔒 **Fully Offline** | No API keys, no cloud, everything runs locally |
| 🔄 **Autonomous Loop** | Agent chains multiple tools until the task is done |
| 🛡️ **Sandboxed Execution** | Filesystem restricted to workspace, command blocklist |
| ✅ **Input Validation** | Tool call schemas with auto-retry on malformed JSON |
| 📊 **Token Management** | Auto-truncation, /tokens command with usage bar |
| 🔄 **Error Recovery** | Retry with backoff, graceful error handling |

---

## 📋 Prerequisites

- **Python 3.10+** — [Download](https://python.org/downloads)
- **Ollama** — [Download](https://ollama.com/download)
- **Git** — [Download](https://git-scm.com/downloads)

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/asepsayyad007/AI-Agent.git
cd AI-Agent
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browser

```bash
python -m playwright install chromium
```

### 4. Pull an Ollama model

```bash
ollama pull qwen2.5-coder:7b
```

> You can also pull additional models for different use cases:
> ```bash
> ollama pull qwen2.5-coder:3b    # Fast, lightweight
> ollama pull qwen2.5-coder:14b   # Heavy, more capable
> ollama pull deepseek-r1:8b      # Reasoning tasks
> ```

### 5. Run the agent

```bash
python app.py
```

---

## 💻 Usage

### Basic Interaction

```
===== AI Agent v0.9 =====
Model: qwen2.5-coder:7b

You > Create a Python Flask app with a home page and an about page

AI:
{ "tool": "write_file", "path": "workspace/app.py", "content": "..." }

Tool Output:
{ "success": true }

AI:
I've created a Flask app with two routes...
```

### Slash Commands

| Command | Description |
|---------|-------------|
| `/model <name>` | Switch model (use preset or full model name) |
| `/models` | List installed models and presets |
| `/clear` | Clear conversation history |
| `/exit` | Exit the agent |
| `/tokens` | Show token usage for current conversation |
| `/confirm` | Toggle tool confirmation mode (off/destructive/all) |

### Model Presets

| Preset | Model | Best For |
|--------|-------|----------|
| `default` | qwen2.5-coder:7b | General coding tasks |
| `fast` | qwen2.5-coder:3b | Quick edits, simple questions |
| `heavy` | qwen2.5-coder:14b | Complex architecture, large refactors |
| `reason` | deepseek-r1:8b | Logic, debugging, problem-solving |

**Switch models mid-conversation:**
```
You > /model fast
Switched to: qwen2.5-coder:3b

You > /model llama3:8b
Switched to: llama3:8b
```

---

## 🛠️ Available Tools

### Terminal
The agent can execute any shell command:
```
You > Check what Python version is installed
AI calls: { "tool": "terminal", "command": "python --version" }
```

### File Operations
Full filesystem access — read, write, delete, list, check existence:
```
You > Create an index.html with a responsive landing page
AI calls: { "tool": "write_file", "path": "workspace/index.html", "content": "..." }
```

### Git Operations
Full git workflow without leaving the chat:
```
You > What's the git status?
You > Commit all changes with message "feat: add authentication"
You > Create a new branch called feature/payment
You > Push to origin
```

Available git tools:
- `git_status` — Branch info, dirty state, staged/changed/untracked files
- `git_log` — Recent commits with hash, message, author, date
- `git_diff` — View changes (working tree or staged)
- `git_add` — Stage files
- `git_commit` — Commit with message
- `git_branch` — List, create, or checkout branches
- `git_checkout` — Switch branches
- `git_push` / `git_pull` — Sync with remote

### Web Browsing
Browse any URL with a headless Chromium browser:
```
You > Go to https://docs.python.org and get the content
You > Take a screenshot of https://example.com
You > Extract all links from https://github.com/trending
```

Browse actions:
- `text` — Extract readable text from a page
- `html` — Get full HTML source
- `screenshot` — Save a full-page screenshot
- `links` — Extract all hyperlinks
- `click` — Click an element by CSS selector
- `type` — Type into an input field

### Web Search
Search the internet via DuckDuckGo:
```
You > Search for "best python testing frameworks 2024"
You > Look up how to use Redis with Python
```

---

## 📁 Project Structure

```
AI-Agent/
├── app.py              # Main entry point — REPL chat loop
├── config.py           # Model configuration & multi-model support
├── requirements.txt    # Python dependencies
├── agent/
│   ├── graph.py        # Ollama chat integration
│   ├── parser.py       # JSON tool call parser
│   ├── prompts.py      # System prompt with tool definitions
│   └── state.py        # Agent state type definition
├── tools/
│   ├── dispatcher.py   # Routes tool calls to handlers
│   ├── terminal.py     # Shell command execution
│   ├── filesystem.py   # File CRUD operations
│   ├── git.py          # Git operations via GitPython
│   └── browser.py      # Web browsing via Playwright
└── workspace/          # Default sandbox directory
```

---

## ⚙️ Configuration

### Changing the Default Model

Edit `config.py` to change presets:

```python
MODELS = {
    "default": "qwen2.5-coder:7b",
    "fast": "qwen2.5-coder:3b",
    "heavy": "qwen2.5-coder:14b",
    "reason": "deepseek-r1:8b",
}
```

Replace with any model you have in Ollama:
```bash
ollama list  # See your installed models
```

### Adding Custom Model Presets

Add new entries to the `MODELS` dictionary:
```python
MODELS = {
    "default": "qwen2.5-coder:7b",
    "fast": "qwen2.5-coder:3b",
    "heavy": "qwen2.5-coder:14b",
    "reason": "deepseek-r1:8b",
    "creative": "llama3:8b",        # Add your own
    "large": "codestral:22b",       # Add your own
}
```

---

## 🧪 Example Use Cases

### Code Generation
```
You > Create a REST API with FastAPI that has CRUD operations for a todo app
You > Write unit tests for the todo API using pytest
You > Add Docker support with a Dockerfile and docker-compose.yml
```

### Git Workflow
```
You > Show me what changed since last commit
You > Stage everything and commit with "refactor: clean up error handling"
You > Create a branch called hotfix/login-bug and switch to it
```

### Research & Learning
```
You > Search for how to implement JWT authentication in Python
You > Go to the FastAPI docs and explain how dependency injection works
You > Find the latest release of React and summarize the changelog
```

### System Tasks
```
You > List all Python files in this project
You > Find and delete all .pyc files
You > Check disk usage of the current directory
```

---

## 🔧 Troubleshooting

### "Connection refused" error
Make sure Ollama is running:
```bash
ollama serve
```

### "Model not found" error
Pull the model first:
```bash
ollama pull qwen2.5-coder:7b
```

### Playwright browser not found
Install the browser binary:
```bash
python -m playwright install chromium
```

### Import errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## 🗺️ Roadmap

- [ ] Task & note management (local markdown-based)
- [ ] Persistent memory across sessions
- [ ] Code analysis & refactoring tools
- [ ] Database operations (SQLite, PostgreSQL)
- [ ] Docker container management
- [ ] Scheduled automation (cron-like tasks)
- [ ] Document processing (PDF, Word, Excel)
- [ ] Security & code audit tools

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ for developers who value privacy and offline capability.**

[Report Bug](https://github.com/asepsayyad007/AI-Agent/issues) · [Request Feature](https://github.com/asepsayyad007/AI-Agent/issues)

</div>
