# Data and Dragons 🐉📊

> *"Roll for Data Quality."*

A gamified data science consultancy simulator where an LLM acts as the Game Master, judging your technical strategy through a mix of AI reasoning and virtual dice rolls. Navigate high-stakes client scenarios, interact with NPCs, and build your Consultancy Score on the live League Table.

Built as a technical showcase of agentic LLM workflows and automated evaluation.

---

## Overview

Players take on the role of a newly hired data science consultant. Over a series of progressively difficult scenarios — messy datasets, broken models, hostile stakeholders — they must propose solutions in natural language. A **Judge** (powered by an LLM via Pydantic-AI) evaluates their response and combines that with a **virtual dice roll** to determine success or failure.

**Key features:**
- 🎭 **NPC Interactions** — engage with a cast of recurring company colleagues and one-off client characters
- ⚖️ **LLM Judge Architecture** — your natural language answers are evaluated for technical soundness
- 🎲 **Virtual Dice Rolls** — stochastic outcomes mean even great answers carry a hint of risk
- 🏆 **Live League Table** — competitive scoring at conference expo booths
- 🤖 **Adversarial Mode** — try to "hack" the LLM judge and see what happens

---

## Requirements

- Python **3.10+**
- [`uv`](https://github.com/astral-sh/uv) — used for all dependency management and script execution
- An **OpenAI API key** (set as `OPENAI_API_KEY` in your environment)

Install `uv` if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Setup

Clone the repository and sync the environment:

```bash
git clone <repo-url>
cd data_and_dragons

uv sync
```

This installs all dependencies (including dev tools like `pytest`) declared in `pyproject.toml` and creates a local `.venv`.

Configure your environment variables:
```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

---

## Running the Game

```bash
uv run python -m data_and_dragons
```

---

## Running Tests

Tests do **not** require an API key — the LLM is mocked in the test suite.

```bash
uv run pytest tests/
```

To run with coverage:
```bash
uv run pytest tests/ --cov=src/data_and_dragons --cov-report=term-missing
```

---

## Project Structure

```
data_and_dragons/
│
├── data/
│   ├── npcs.yaml               # Company-wide NPC roster (recurring characters)
│   └── scenarios/
│       ├── 01_dirty_data.yaml          # Scenario 1: The Excel Catastrophe
│       └── 02_predictive_misfire.yaml  # Scenario 2: The Predictive Misfire
│
├── src/data_and_dragons/
│   ├── __init__.py
│   ├── __main__.py             # Entry point: `python -m data_and_dragons`
│   ├── models.py               # Core Pydantic data models
│   ├── dice.py                 # d20 dice roll mechanism with Outcome classification
│   ├── scenario_loader.py      # Loads & resolves scenarios + NPC roster from YAML
│   ├── scenario_manager.py     # Manages game state & scenario progression
│   ├── dialogue_manager.py     # NPC interaction tracking & history
│   └── judge.py                # LLM Judge: prompt templates, evaluation, scoring
│
├── tests/
│   ├── test_models.py
│   ├── test_dice.py
│   ├── test_judge.py
│   ├── test_scenario_loader.py
│   ├── test_scenario_manager.py
│   └── test_dialogue_manager.py
│
├── pyproject.toml              # Project metadata and dependencies
└── conductor/                  # Development planning documents (not pushed to origin)
```

---

## Architecture

### Judge Scoring

Each player action is evaluated in two stages:

1. **LLM Evaluation (75%)** — Pydantic-AI sends the player's response to the LLM with the scenario context and NPC profiles. The LLM returns a structured `JudgementResult` with a `technical_score` (0–100), `reasoning`, and `verdict`.

2. **Dice Roll (25%)** — A virtual d20 is rolled. The modifier blends with the LLM score. Two special outcomes override the blend:
   - 🎲 **Critical Fumble (1):** Final score capped at 40% — disaster strikes regardless.
   - 🎲 **Critical Success (20):** +15 point bonus — fortune favours the prepared.

```
final_score = (technical_score × 0.75) + (dice_modifier × 100 × 0.25)
```

### NPC Architecture

NPCs live in two places:

| Source | File | Purpose |
|---|---|---|
| Company roster | `data/npcs.yaml` | Recurring colleagues across all scenarios |
| Scenario one-offs | `data/scenarios/*.yaml` (`other_npcs`) | Unique client contacts, one-time characters |

Scenarios reference roster NPCs by `id` and can extend their role with a `scenario_role` override. All NPCs — both roster and one-offs — are available to address during a scenario.

---

## Adding Content

### Adding a Company NPC

Add to `data/npcs.yaml`:

```yaml
npcs:
  - id: "unique_id"
    name: "Full Name"
    role: "Their job title"
    personality: "A short description of how they behave"
    background: >
      A few sentences about their history and motivations that the LLM
      Judge will use when evaluating player actions.
```

### Adding a Scenario

Create a new file `data/scenarios/NN_scenario_name.yaml`:

```yaml
title: "Scenario Title"
description: >
  The narrative setup. This is what the player reads at the start.
difficulty: "Easy | Medium | Hard"

# Roster NPCs involved (by id from data/npcs.yaml)
npcs:
  - npc_id: "existing_npc_id"
    scenario_role: "Optional: override their role description for this scenario."

# One-off NPCs unique to this scenario (no roster entry needed)
other_npcs:
  - id: "local_id"
    name: "Full Name"
    role: "Their role"
    personality: "Short description"
    background: "Their story."
```

> **Note:** All NPCs in a scenario — both roster and one-offs — are accessible to the player. You can propose asking for help from any company colleague, not just those explicitly listed.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pydantic` | Data models and structured LLM outputs |
| `pydantic-ai` | LLM integration, agentic orchestration, and Judge evaluation |
| `pyyaml` | Loading scenario and NPC definitions from YAML |
| `textual` | *(Track 3)* Rich terminal user interface |

Dev: `pytest`, `pytest-cov`, `pytest-asyncio`

---

## Development

All development follows the conductor workflow defined in `conductor/workflow.md`.

```bash
# Add a production dependency
uv add <library>

# Add a development dependency
uv add --dev <library>

# Run the game
uv run python -m data_and_dragons

# Run tests (no API key required)
uv run pytest tests/
```

Commit format: `<type>(<scope>): <description>` — see `conductor/workflow.md` for full conventions.
