# Autonomous Traders (MCP + Azure OpenAI + SerpAPI(you can use also Brave API)

This repository is an **autonomous multi-agent equity trading simulation** built with the **OpenAI Agents SDK** and the **Model Context Protocol (MCP)**.

## What this repo uses (important)

- **LLM provider**: **Azure OpenAI** (configure `AZURE_OPENAI_*` in `.env`)  
  This repo is not set up to use `OPENAI_API_KEY` directly.
- **Web research**: **SerpAPI** (configure `SERPAPI_API_KEY`)  
  Brave Search is not used.

## Where the code is

Main project code lives in `6_mcp/`.

For the full, file-by-file explanation, see:
- `6_mcp/PROJECT_EXPLANATION.md`

## Quick start

### 1) Set environment variables

Create a `.env` file at the repo root (never commit it) with at least:

```bash
# Azure OpenAI (LLM)
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# SerpAPI (web search)
SERPAPI_API_KEY=...

# Optional: market data + notifications
POLYGON_API_KEY=...
POLYGON_PLAN=free
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
```

### 2) Install dependencies

From `6_mcp/`:

```bash
cd 6_mcp
uv pip install google-search-results gradio plotly pandas
```

### 3) Run the UI (portfolio + logs)

```bash
cd 6_mcp
uv run app.py
```

Open `http://127.0.0.1:7860`.

### 4) Run the trading loop (agents actually trade)

In a second terminal:

```bash
cd 6_mcp
uv run trading_floor.py
```

## Inspect the simulation database

The simulation writes to `6_mcp/accounts.db` (SQLite):

```bash
cd 6_mcp
sqlite3 accounts.db "SELECT name, balance FROM accounts;"
sqlite3 accounts.db "SELECT datetime, name, type, message FROM logs ORDER BY datetime DESC LIMIT 20;"
```

