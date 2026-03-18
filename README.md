# Duolingo Streak Agent

An AI agentic workflow that automatically logs in to Duolingo and solves exercises to maintain your streak, built with the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) and [Playwright](https://playwright.dev/).

## How it works

Two agents run in sequence:

1. **Login Agent** — Opens duolingo.com, logs in using your credentials, and starts a lesson.
2. **Solve Agent** — Solves the current exercise using screenshots for visual feedback, then stops. This loops continuously to complete exercise after exercise.

Both agents operate by taking screenshots, planning actions based on what they see, and executing clicks/keystrokes — a vision-based browser automation loop.

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

## Usage

```bash
uv run python main.py
```

A Chromium browser window will open. The login agent logs in and starts a lesson, then the solve agent loops through exercises automatically.

## Project structure

| File | Description |
|------|-------------|
| [main.py](main.py) | Entry point — runs login then solve agents in a loop |
| [agents_def.py](agents_def.py) | Agent definitions and instructions |
| [tools.py](tools.py) | Playwright-based browser tools (screenshot, click, type, etc.) |
