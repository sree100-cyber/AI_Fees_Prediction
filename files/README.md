# Day 1 Lab: Chatbot vs Rule-Based Workflow vs AI Agent

**Course:** Agentic AI: Foundations and Open-Source Practice
**Unit:** Unit 1 — Foundations of AI Agents (sub-topics 1.1 and 1.2)

## Aim

To set up a Python development environment in VS Code, connect it to an open large language model, and implement and compare three systems on the same task: a plain LLM chatbot, a rule-based workflow, and a tool-using AI agent.

## Problem Statement

A college has private fee data that no public LLM has seen:

| Course | Fee |
|---|---|
| CS101 | Rs. 12,000 |
| AI202 | Rs. 18,000 |
| DS303 | Rs. 15,000 |

Three systems answer the same four questions:

1. What is the fee for AI202?
2. What is the total fee for CS101 and AI202 after a 10% scholarship?
3. Is DS303 more expensive than CS101, and by how much?
4. Write a two-line welcome message for new AI students.

## Project Structure

```
day1_lab/
├── .env                # API provider config (NOT committed — see below)
├── .gitignore           # excludes .env
├── requirements.txt      # openai, python-dotenv
├── config.py            # shared settings, provider selection, course data
├── check_setup.py        # connection test — run this first
├── chatbot.py            # System 1: plain LLM chatbot
├── workflow.py            # System 2: rule-based workflow (no LLM)
├── tools.py              # tools used by the agent (fee lookup, calculator)
├── agent.py              # System 3: AI agent (LLM + tools + loop)
├── challenge.py           # bonus question outside all three systems' design
└── README.md
```

## Setup

### 1. Clone and enter the project
```bash
git clone <your-repo-url>
cd day1_lab
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your LLM provider

Create a `.env` file in the project root (this file is git-ignored and must never be committed):

```env
PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
MODEL=qwen/qwen3.8-27b
```

Get a free Groq API key at [console.groq.com](https://console.groq.com) → API Keys → Create API Key.

Alternative providers (Ollama for local, or Hugging Face) are also supported — see `config.py` for details.

### 5. Verify the connection
```bash
python check_setup.py
```
Expected output ends with `Model replied : SETUP OK`.

## Running the Programs

Run in this order:

```bash
python chatbot.py     # System 1 — expect wrong/uncertain answers (no data access)
python workflow.py     # System 2 — exact answers for Q1/Q2, fails Q3/Q4 (rigid rules)
python tools.py        # sanity check for the agent's tools
python agent.py         # System 3 — correctly answers all 4 questions via tool calls
python challenge.py     # bonus: budget question none of the systems were designed for
```

## Results Summary

| Criterion | Chatbot | Workflow | Agent |
|---|---|---|---|
| Q1 correct? | ❌ (no data) | ✅ | ✅ |
| Q2 correct? | ❌ (no data) | ✅ | ✅ |
| Q3 correct? | ❌ (no data) | ❌ (no rule) | ✅ |
| Q4 handled well? | ✅ | ❌ (rejected) | ✅ |
| Challenge question | — | ❌ (rejected) | ✅ |
| Consistent on repeat runs | varies | ✅ always | mostly |
| Strength | Fluent, honest when data is missing | Instant, 100% reliable on matched patterns | Flexible — chains tools to solve novel questions |
| Weakness | No access to private data | Breaks on any unplanned phrasing | Less predictable — model-dependent tool-call reliability |
| Best suited for | General FAQ, no private data needed | High-volume, fixed-format queries | Novel or multi-step queries requiring reasoning |

## Screenshots

Actual terminal output from running this lab (place these in a `screenshots/` folder in your repo root):

### Setup check and chatbot (System 1)
![Setup and chatbot output](screenshots/01_setup_and_chatbot.png)

### Chatbot Q4 + rule-based workflow (System 2) + tools test
![Workflow and tools output](screenshots/02_chatbot_workflow_tools.png)

### Available models + setup check with final model
![Model list and setup](screenshots/03_list_models_and_setup.png)

### AI agent (System 3) — full run
![Agent output](screenshots/04_agent_output.png)

### Challenge question — workflow vs agent
![Challenge output](screenshots/05_challenge_output.png)

## Notes on Model Choice

`openai/gpt-oss-20b` on Groq occasionally produced malformed tool-call names (internal "harmony" format tokens leaking into the tool name), causing a `400 BadRequestError`. Switching to `qwen/qwen3.8-27b` resolved this — it called tools reliably across all test questions, including multi-step chains (lookup → lookup → calculate).

## Security

- `.env` is excluded via `.gitignore` and must **never** be pushed to GitHub.
- If a key is ever exposed, revoke it immediately in the provider's console and generate a new one.

## Discussion

See the lab manual (Section 11) for full discussion questions, covering:
- Why a confidently wrong chatbot answer is more dangerous than "I don't know"
- Why a finance office might still prefer the rigid workflow over the agent
- Risks of non-deterministic agent behavior in production
- Hybrid design: workflow for common cases, agent for the rest

## Result

A Python environment was set up in VS Code and connected to an open LLM via the Groq API. A chatbot, a rule-based workflow, and a tool-using AI agent were implemented and compared on the same task. The chatbot lacked access to private data and could not answer fee-specific questions; the rule-based workflow was perfectly reliable but failed on any question outside its fixed patterns; the AI agent correctly answered all questions, including a novel budget-optimization question outside its original design, by reasoning over multiple tool calls — though sensitivity to model choice (Groq's `gpt-oss-20b` vs `qwen3.8-27b`) was observed in tool-call reliability.
