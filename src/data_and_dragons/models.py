from typing import List, Optional
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
    role: str                           # Scenario role if provided, else roster role
    personality: str
    background: str
    scenario_role: Optional[str] = None # The raw scenario-specific role override, if any


class Scenario(BaseModel):
    title: str
    description: str
    difficulty: str
    npcs: List[ResolvedNPC] = Field(default_factory=list)  # Roster NPCs resolved for this scenario
    other_npcs: List[ResolvedNPC] = Field(default_factory=list)  # One-off NPCs unique to this scenario


class Action(BaseModel):
    player_input: str


class GameState(BaseModel):
    player: Player
    current_scenario_index: int = 0
