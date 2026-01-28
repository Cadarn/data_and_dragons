# Initial Concept
A system to manage Data and Dragons, a data science consultancy simulator

# Primary Objective
To develop an extensible, LLM-orchestrated simulation engine that gamifies the data science lifecycle. The system serves as a technical showcase for agentic workflows and automated evaluation, allowing users to navigate a "day-in-the-life" of a data science consultant through a series of complex, high-stakes scenarios.

## Key Pillars of the Product:
- Narrative Simulation: Deliver six progressively difficult scenarios where players interact with NPCs (stakeholders, peers, and clients) to solve data-centric business problems.
- Hybrid Evaluation Engine: Implement a "Judge" architecture that merges the reasoning capabilities of a Large Language Model (LLM) with stochastic "virtual dice" rolls to determine success or failure based on the player’s natural language input.
- Adversarial Engagement: Provide a sandbox environment where players can succeed through sound technical strategy or attempt to "hack" the LLM judge via creative prompt engineering, highlighting both the power and the edge cases of generative AI.
- Competitive Analytics: Facilitate a live-updating League Table to drive engagement at conference expo booths, ranking players based on a "Consultancy Score" (a composite metric of technical efficacy, efficiency, and luck).
- Agentic Showcase: Demonstrate how LLMs can act as autonomous Game Masters—managing state, dialogue, and scoring without the need for rigid, pre-defined branching logic.

# Product Requirements

## Target Users
"Data and Dragons" is designed for a diverse audience, encompassing:
- **Aspiring Data Scientists:** Individuals eager to practice and hone their data science skills within a safe, simulated environment.
- **Experienced Data Scientists:** Professionals looking for an engaging and novel way to interact with LLM-driven simulations and explore their capabilities.
- **Tech Enthusiasts/Conference Attendees:** A broader audience curious about the advancements in LLMs and agentic solutions, seeking an interactive and demonstrative experience at events.

## Core Functional Requirements
The game will implement the following core functionalities:
- **Scenario Progression:** Players will experience a narrative arc through a series of six progressively challenging scenarios, each designed to test different aspects of data science consultancy.
- **NPC Interaction:** The game will feature interactive Non-Player Characters (NPCs) representing various stakeholders (clients, colleagues, managers), with whom players will communicate to gather information, present findings, and negotiate solutions.
- **LLM-based Scoring:** A sophisticated scoring system will leverage an LLM as a "Judge," evaluating player actions and decisions based on natural language input. This system will also incorporate elements of chance through "virtual dice rolls" to reflect the unpredictable nature of real-world projects.
- **League Table:** A dynamic, live-updating leaderboard will track and display player scores and rankings, fostering a competitive and engaging environment, particularly suitable for conference expo settings.