# Implementation Plan: Core Game Engine

This plan outlines the tasks required to build the core game engine for "Data and Dragons."

## Phase 1: Project Setup and Initial Data Structures [checkpoint: aea4205]

- [x] 4f02f5c Task: Initialize Python project structure with `pyproject.toml`.
- [x] 8db5f5a Task: Add `pydantic` and `pydantic-ai` as dependencies.
- [x] 0698f59 Task: Define core data models using Pydantic for `GameState`, `Player`, `Scenario`, `NPC`, and `Action`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Project Setup and Initial Data Structures' (Protocol in workflow.md)

## Phase 2: Scenario Engine Implementation

- [x] 658862c Task: Implement a `ScenarioLoader` to read scenario definitions from a YAML file.
    - [ ] Write tests for `ScenarioLoader`.
    - [ ] Implement `ScenarioLoader`.
- [x] bf38a8c Task: Implement the `ScenarioManager` to handle game state and progression.
    - [ ] Write tests for `ScenarioManager`.
    - [ ] Implement `ScenarioManager`.
- [x] 4e05c24 Task: Create initial scenario definitions in YAML for the first two scenarios.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Scenario Engine Implementation' (Protocol in workflow.md)

## Phase 3: NPC Interaction Module

- [x] cd05d86 Task: Implement a basic `DialogueManager` to handle NPC interactions.
- [x] cd05d86 Task: Integrate `DialogueManager` with the `ScenarioManager`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: NPC Interaction Module' (Protocol in workflow.md)

## Phase 4: LLM-based "Judge" Architecture

- [~] Task: Implement the `Judge` class, virtual dice roll, and prompt templates.
    - [ ] Write tests for the `Judge` class.
    - [ ] Implement the `Judge` class.
    - [ ] Implement the "virtual dice roll" mechanism.
    - [ ] Implement prompt templates for evaluating player actions.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: LLM-based "Judge" Architecture' (Protocol in workflow.md)

## Phase 5: Initial Game Loop and CLI

- [ ] Task: Create a basic command-line interface (CLI) to interact with the game engine.
- [ ] Task: Implement the main game loop that ties together all the components.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Initial Game Loop and CLI' (Protocol in workflow.md)
