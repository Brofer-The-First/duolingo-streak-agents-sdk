# Duolingo Streak Agent

An AI agentic workflow that automatically logs in to Duolingo and solves exercises to maintain your streak, built with the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) and [Playwright](https://playwright.dev/).

## How it works

By default, login is handled manually via hardcoded click coordinates (`manual_login`). Optionally, an AI agent can handle login instead (see [Configuration](#configuration)).

After login, the solve agent loops continuously:

1. **Login** — Opens duolingo.com, logs in using your credentials, and starts a lesson. Done either manually (default) or by the Login Agent.
2. **Solve Agent** — Solves the current exercise using screenshots for visual feedback, then loops to the next exercise.

The Solve Agent operates by taking screenshots, planning actions based on what it sees, and executing clicks/keystrokes — a vision-based browser automation loop.

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An OpenAI API key
- A Duolingo account

### Install dependencies

```bash
uv pip install -r requirements.txt
playwright install chromium
```

### Configure credentials

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
DUOLINGO_EMAIL=your_duolingo_email
DUOLINGO_PASSWORD=your_duolingo_password
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENTIC_LOGIN` | `false` | Set to `true` to use the AI Login Agent instead of the hardcoded manual login sequence |

## Usage

```bash
uv run python main.py
```

A Chromium browser window will open. By default, login is performed via `manual_login` (hardcoded clicks). Then the solve agent loops through exercises automatically.

## Project structure

| File | Description |
|------|-------------|
| [main.py](main.py) | Entry point — runs login then solve agents in a loop |
| [agents_def.py](agents_def.py) | Agent definitions and instructions |
| [tools.py](tools.py) | Playwright-based browser tools (screenshot, click, type, etc.) |
