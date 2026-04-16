# Tech Stack

## Programming Languages and Tooling
- **Python:** Chosen for its widespread use in data science and AI. 
- **uv:** An extremely fast Python package and project manager. **ALL** python code execution, testing, and dependency management MUST be done using `uv run` and `uv add`.

## LLM Integration and Agentic Orchestration
- **Pydantic-AI:** This framework will be utilized for integrating with Large Language Models and orchestrating agentic workflows. Its emphasis on structured data and validation (via Pydantic) will be crucial for managing the game state, player inputs, and LLM outputs in a robust and predictable manner, especially for the "Judge" architecture.

## Database
- **SQLite:** Selected for managing the "League Table" and potentially other game state elements. Its file-based nature ensures easy setup, portability, and minimal overhead, making it ideal for prototyping, local development, and deployments at conference expo booths.

## Text User Interface (TUI)
- **Textual:** Used for building a rich, interactive, and visually stunning textual user interface (TUI) for the game, suitable for a terminal but with web-like capabilities. This satisfies the requirement for a "modern and clean" visual identity in the initial textual version.
