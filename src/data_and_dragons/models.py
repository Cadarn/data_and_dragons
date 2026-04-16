from typing import List, Optional
from pydantic import BaseModel, Field

class Player(BaseModel):
    name: str
    score: int = Field(default=0, ge=0)

class NPC(BaseModel):
    name: str
    role: str
    personality: str
    background: str

class Scenario(BaseModel):
    title: str
    description: str
    difficulty: str
    npcs: List[NPC] = Field(default_factory=list)

class Action(BaseModel):
    player_input: str

class GameState(BaseModel):
    player: Player
    current_scenario_index: int = 0
