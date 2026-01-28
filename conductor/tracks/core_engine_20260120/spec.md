# Specification: Core Game Engine

This track focuses on building the foundational components of the "Data and Dragons" simulation engine. The goal is to create a fully functional, albeit minimal, gameplay loop that includes scenario progression, interaction with Non-Player Characters (NPCs), and an LLM-based scoring mechanism.

## Key Features

### 1. Scenario Engine
- **State Management:** Develop a robust system for managing the game state, including player progress, scenario status, and NPC interactions.
- **Scenario Loader:** Implement a mechanism to load and parse scenario definitions from a structured format (e.g., YAML or JSON).
- **Progression Logic:** Create the logic to move the player from one scenario to the next based on completion criteria.

### 2. NPC Interaction Module
- **Dialogue System:** Implement a simple dialogue system that allows players to receive information from and communicate with NPCs.
- **NPC Representation:** Define a data structure for NPCs, including their roles, personalities, and the information they possess.

### 3. LLM-based "Judge" Architecture
- **LLM Integration:** Integrate with the chosen LLM (via Pydantic-AI) to send player actions and receive evaluations.
- **Scoring Logic:** Develop the core logic for the "Judge," which takes the LLM's evaluation and combines it with a "virtual dice roll" to produce a final score and outcome for a given action.
- **Prompt Engineering:** Design and implement the initial prompts that will be used to instruct the LLM on how to evaluate player inputs.

## Non-functional Requirements

- **Extensibility:** The engine should be designed with future extensions in mind, making it easy to add new scenarios, NPCs, and scoring mechanics.
- **Testability:** All components should be designed with testability in mind, with clear separation of concerns to facilitate unit and integration testing.
