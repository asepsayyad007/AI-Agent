# Implementation Plan: AI Agent v0.8 → Production Offline Assistant

## Overview

This document outlines the roadmap for transforming the AI Agent from a v0.8 prototype into a production-grade offline AI assistant. The plan is organized into three phases, each building incrementally on the previous one.

---

## Timeline

| Version | Phase | Focus | Target |
|---------|-------|-------|--------|
| v0.6 | — | Initial prototype | ✅ Complete |
| v0.7 | — | Tool integration (browser, git, filesystem) | ✅ Complete |
| v0.8 | — | LangGraph agent loop, dispatcher | ✅ Complete |
| **v0.9** | **Phase 1** | **Security, stability, resilience** | Week 1–2 |
| **v1.0** | **Phase 2** | **Usability, UX, persistence** | Week 3–4 |
| **v1.1+** | **Phase 3** | **Power user features, testing, plugins** | Week 5+ |

---

## Target Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      CLI Interface                        │
│  (Rich Live streaming, multi-line input, /commands)      │
├─────────────────────────────────────────────────────────┤
│                    Session Manager                        │
│  (auto-save, load, history, context summarization)       │
├─────────────────────────────────────────────────────────┤
│                   Agent Core (LangGraph)                  │
│  ┌───────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Planner  │  │  Tool Router  │  │ Context Manager │  │
│  └───────────┘  └──────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                    Security Layer                         │
│  (sandbox, validation, command blocklist, path checks)   │
├─────────────────────────────────────────────────────────┤
│                    Tool Layer (Plugins)                   │
│  ┌──────────┐ ┌────────┐ ┌─────┐ ┌───────┐ ┌───────┐  │
│  │filesystem│ │terminal│ │ git │ │browser│ │plugins│  │
│  └──────────┘ └────────┘ └─────┘ └───────┘ └───────┘  │
├─────────────────────────────────────────────────────────┤
│                   Ollama LLM Backend                      │
│  (streaming, retry, timeout, token management)           │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1 (v0.9) — Critical Security & Stability

### 1.1 Sandboxed Execution

Restrict all tool operations to a safe boundary to prevent accidental or malicious damage.

- [ ] Add `WORKSPACE_DIR` configuration variable (default: `./workspace`)
- [ ] Implement path traversal prevention in `tools/filesystem.py`
  - Resolve all paths to absolute and verify they start with `WORKSPACE_DIR`
  - Reject paths containing `..` that escape the sandbox
- [ ] Add command blocklist for `tools/terminal.py`
  - Block: `rm -rf /`, `format`, `mkfs`, `dd`, `shutdown`, `reboot`, `:(){:|:&};:`
  - Block network-altering commands: `iptables`, `ufw`, `netsh`
- [ ] Restrict filesystem operations to `WORKSPACE_DIR` only
  - Read: allowed within workspace
  - Write: allowed within workspace
  - Delete: requires confirmation + workspace-only
- [ ] Add `ALLOW_NETWORK` flag (default: `False` for offline mode)
- [ ] Write unit tests for sandbox boundary enforcement

### 1.2 Error Handling & Recovery

Make the agent resilient to LLM failures, tool crashes, and unexpected states.

- [ ] Implement retry logic for Ollama API calls
  - Exponential backoff: 1s, 2s, 4s (max 3 retries)
  - Distinguish between transient errors (connection reset) and permanent errors (model not found)
- [ ] Add configurable timeout for LLM calls
  - `LLM_TIMEOUT = 120` seconds (default)
  - Surface timeout errors gracefully to the user
- [ ] Implement graceful degradation
  - If Ollama is unreachable: inform user, offer retry or exit
  - If a tool fails: report error, allow agent to re-plan
- [ ] Add try/except wrappers around all tool executions in `tools/dispatcher.py`
- [ ] Implement circuit breaker pattern for repeated failures
  - After 5 consecutive tool failures, pause and ask user for guidance
- [ ] Add `--debug` flag to surface full tracebacks

### 1.3 Token/Context Management

Prevent context window overflow and give users visibility into token usage.

- [ ] Integrate `tiktoken` (or equivalent offline tokenizer) for token counting
  - Count tokens per message in conversation history
  - Track cumulative token usage per session
- [ ] Add `MAX_CONTEXT_TOKENS` configuration (default: `4096` for small models, configurable)
- [ ] Implement auto-summarization when context exceeds threshold
  - At 80% capacity: summarize older messages into a condensed context block
  - Preserve system prompt and last N messages intact
  - Use the LLM itself to generate summaries
- [ ] Add `/tokens` command to display:
  - Current token count
  - Maximum allowed
  - Percentage used
  - Estimated remaining capacity
- [ ] Implement sliding window fallback if summarization fails

### 1.4 Input Validation

Validate all tool arguments before execution to prevent crashes and injection.

- [ ] Define JSON schemas for each tool's expected input
  - `filesystem`: `{"action": str, "path": str, "content"?: str}`
  - `terminal`: `{"command": str, "cwd"?: str}`
  - `git`: `{"action": str, "args"?: list}`
  - `browser`: `{"url": str, "action"?: str}`
- [ ] Implement validation layer in `tools/dispatcher.py`
  - Validate tool call arguments against schema before execution
  - Return structured error to LLM on validation failure
- [ ] Add retry-on-failure mechanism
  - If LLM produces invalid tool call: feed error back, request corrected output
  - Max 2 retries before giving up on that tool call
- [ ] Sanitize string inputs (strip null bytes, limit length)
- [ ] Add type coercion for common LLM mistakes (e.g., `"true"` → `True`)

---

## Phase 2 (v1.0) — Usability & UX

### 2.1 Streaming Responses

Eliminate the "waiting for response" dead time and provide real-time feedback.

- [ ] Enable `stream=True` in Ollama API calls
- [ ] Implement `Rich Live` display for streaming tokens
  - Show tokens as they arrive
  - Render markdown formatting in real-time
- [ ] Add typing indicator while waiting for first token
- [ ] Handle stream interruption gracefully (Ctrl+C mid-stream)
- [ ] Buffer tool calls until complete before executing

### 2.2 Persistent Sessions

Allow users to save, resume, and review conversation history.

- [ ] Create session storage directory: `~/.ai-agent/sessions/`
- [ ] Implement auto-save on every exchange
  - Format: JSON with metadata (timestamp, model, token count)
  - Filename: `session_{timestamp}.json`
- [ ] Add `/save [name]` command — save current session with optional label
- [ ] Add `/load [name|id]` command — restore a previous session
- [ ] Add `/history` command — list recent sessions with summaries
- [ ] Add `/clear` command — start fresh session (with confirmation)
- [ ] Implement session metadata index for fast lookup

### 2.3 Configuration File

Provide a user-editable config file for all settings.

- [ ] Add `pyyaml` to `requirements.txt`
- [ ] Create default config at `~/.ai-agent/config.yaml` on first run
  ```yaml
  model: "qwen2.5-coder:7b"
  max_context_tokens: 4096
  workspace_dir: "./workspace"
  llm_timeout: 120
  allow_network: false
  stream: true
  auto_save: true
  log_level: "INFO"
  confirm_destructive: true
  ```
- [ ] Implement config loader with defaults + override hierarchy
  - Default → config file → environment variables → CLI flags
- [ ] Add `/config` command to view/edit settings at runtime
- [ ] Validate config on load, warn on invalid values

### 2.4 Logging

Add structured logging for debugging and audit trails.

- [ ] Create log directory: `~/.ai-agent/logs/`
- [ ] Implement structured logging with Python `logging` module
  - Format: `[timestamp] [level] [module] message`
  - Levels: DEBUG, INFO, WARNING, ERROR
- [ ] Add log rotation (max 10MB per file, keep 5 files)
- [ ] Log all tool executions with input/output
- [ ] Log all LLM requests/responses (configurable, off by default for privacy)
- [ ] Add `/log` command to show recent log entries
- [ ] Separate log streams: `agent.log`, `tools.log`, `errors.log`

---

## Phase 3 (v1.1+) — Power User Features

### 3.1 Multi-line Input

- [ ] Detect multi-line input mode (e.g., triple backtick or `\` at end of line)
- [ ] Support paste of multi-line content
- [ ] Add visual indicator for multi-line mode
- [ ] Submit on empty line or explicit Ctrl+D

### 3.2 Tool Confirmation Mode

- [ ] Add `/confirm` command with modes:
  - `on` — confirm every tool execution
  - `destructive` — confirm only destructive operations (delete, overwrite, terminal)
  - `off` — execute all tools without confirmation
- [ ] Default: `destructive`
- [ ] Show tool call details before confirmation prompt
- [ ] Allow user to edit tool arguments before confirming

### 3.3 Plugin System

- [ ] Define tool plugin interface (base class with `name`, `description`, `schema`, `execute`)
- [ ] Auto-discover plugins from `~/.ai-agent/plugins/` directory
- [ ] Auto-discover plugins from `./plugins/` in workspace
- [ ] Hot-reload plugins without restarting agent
- [ ] Add `/plugins` command to list loaded plugins
- [ ] Provide example plugin template

### 3.4 Project Context Awareness

- [ ] Auto-detect project type on startup (Python, Node.js, Rust, etc.)
- [ ] Read and summarize key files: `README.md`, `pyproject.toml`, `package.json`
- [ ] Inject project context into system prompt
- [ ] Add `/context` command to view/edit injected context
- [ ] Support `.ai-agent-context` file for custom project instructions

### 3.5 Clipboard Integration

- [ ] Add `/copy` command — copy last response to clipboard
- [ ] Add `/paste` command — paste clipboard content as user input
- [ ] Use `pyperclip` library (cross-platform)
- [ ] Handle clipboard unavailability gracefully (headless environments)

### 3.6 Token Usage Display

- [ ] Show token count after each response (optional, configurable)
- [ ] Display cost estimate if using paid models
- [ ] Add `/usage` command for session-level statistics
- [ ] Track tokens per tool call vs. conversation

### 3.7 Unit Tests

- [ ] Set up `pytest` with project structure
- [ ] Write tests for:
  - [ ] Sandbox path validation
  - [ ] Command blocklist enforcement
  - [ ] Token counting accuracy
  - [ ] Input validation schemas
  - [ ] Session save/load round-trip
  - [ ] Config loading and defaults
  - [ ] Tool dispatcher routing
  - [ ] Error handling and retry logic
- [ ] Add GitHub Actions CI workflow
  ```yaml
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: "3.11"
        - run: pip install -r requirements.txt
        - run: pytest tests/ -v --tb=short
  ```
- [ ] Add coverage reporting (target: 80%+)

### 3.8 Auto-update Check

- [ ] On startup, check local version against latest release (if online)
- [ ] If offline, skip silently
- [ ] Show non-intrusive notification if update available
- [ ] Add `/version` command to display current version and check status

---

## Implementation Notes

### Dependencies to Add

| Package | Purpose | Phase |
|---------|---------|-------|
| `tiktoken` | Token counting | 1 |
| `jsonschema` | Input validation | 1 |
| `pyyaml` | Configuration file | 2 |
| `pyperclip` | Clipboard integration | 3 |
| `pytest` | Unit testing | 3 |
| `pytest-cov` | Coverage reporting | 3 |

### Key Design Decisions

1. **Offline-first**: All features must work without internet. Network features are opt-in.
2. **Backward compatible**: Existing `config.py` values become defaults; new config system layers on top.
3. **Non-breaking upgrades**: Sessions from v0.9 should load in v1.0+.
4. **Minimal dependencies**: Prefer stdlib where possible. Each new dependency must justify itself.
5. **LangGraph preservation**: The existing agent graph architecture remains the backbone. New features plug into existing nodes or add new ones.

### File Structure (Target)

```
AI-Agent/
├── agent/
│   ├── graph.py          # LangGraph agent loop
│   ├── nodes.py          # Agent nodes (plan, execute, respond)
│   ├── parser.py         # LLM output parsing
│   ├── prompts.py        # System/user prompts
│   ├── state.py          # Agent state definition
│   └── context.py        # NEW: token/context management
├── tools/
│   ├── dispatcher.py     # Tool routing + validation
│   ├── filesystem.py     # Sandboxed file operations
│   ├── terminal.py       # Sandboxed command execution
│   ├── git.py            # Git operations
│   ├── browser.py        # Web browsing
│   └── schemas.py        # NEW: JSON schemas for validation
├── core/
│   ├── config.py         # NEW: YAML config loader
│   ├── logging.py        # NEW: structured logging
│   ├── session.py        # NEW: session persistence
│   ├── sandbox.py        # NEW: security boundary enforcement
│   └── streaming.py      # NEW: streaming response handler
├── plugins/              # NEW: plugin directory
├── tests/                # NEW: pytest test suite
│   ├── test_sandbox.py
│   ├── test_validation.py
│   ├── test_context.py
│   └── test_session.py
├── app.py                # CLI entry point
├── config.py             # Legacy config (deprecated in v1.0)
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml        # NEW: GitHub Actions
└── README.md
```

### Migration Path

- **v0.8 → v0.9**: Add security layer around existing tools. No breaking changes to user workflow.
- **v0.9 → v1.0**: Add streaming and persistence. Old `config.py` values auto-migrate to YAML on first run.
- **v1.0 → v1.1**: Additive features only. Plugin system is opt-in.

---

## Getting Started

To begin implementation, start with Phase 1.1 (Sandboxed Execution) as it forms the security foundation for everything else. Each task is designed to be completed independently and merged incrementally.

```bash
# Create feature branch
git checkout -b feat/v0.9-security

# Start with sandbox implementation
# See Task 1.1 above
```
