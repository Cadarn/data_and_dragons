from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class Player(BaseModel):
    name: str
    score: int = Field(default=0, ge=0)


class NPC(BaseModel):
    """A reusable company NPC, defined in the global NPC roster."""
    id: str
    name: str
    role: str
    personality: str
    background: str


class NPCRef(BaseModel):
    """Scenario reference to a roster NPC, with an optional scenario-specific role extension."""
    npc_id: str
    scenario_role: Optional[str] = None  # Overrides/extends the NPC's default role for this scenario


class ResolvedNPC(BaseModel):
    """An NPC as they appear within a specific scenario — roster data merged with scenario context."""
    id: str
    name: str
    role: str                            # Scenario role if provided, else roster role
    personality: str
    background: str
    scenario_role: Optional[str] = None  # The raw scenario-specific role override, if any


class Scenario(BaseModel):
    title: str
    description: str
    difficulty: str
    npcs: List[ResolvedNPC] = Field(default_factory=list)       # Roster NPCs resolved for this scenario
    other_npcs: List[ResolvedNPC] = Field(default_factory=list) # One-off NPCs unique to this scenario


class Action(BaseModel):
    player_input: str


class GameState(BaseModel):
    player: Player
    current_scenario_index: int = 0


class JudgementResult(BaseModel):
    """Structured evaluation returned by the LLM Judge."""
    technical_score: int = Field(ge=0, le=100, description="0–100 score for technical soundness.")
    reasoning: str = Field(description="The Judge's explanation of the evaluation.")
    verdict: Literal["success", "partial", "failure"] = Field(
        description="Overall verdict on the player's action."
    )


class ActionOutcome(BaseModel):
    """Final outcome of a player action after LLM judgement and dice roll are combined."""
    judgement: JudgementResult
    dice_roll: "DiceRoll"  # Forward ref resolved below
    final_score: int = Field(ge=0, le=100)
    narrative: str = Field(description="What the player sees as the outcome of their action.")


# Resolve forward reference after dice module is importable
from data_and_dragons.dice import DiceRoll  # noqa: E402
ActionOutcome.model_rebuild()
