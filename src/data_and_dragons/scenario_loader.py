import yaml
from typing import Dict
from data_and_dragons.models import NPC, NPCRef, ResolvedNPC, Scenario

DEFAULT_ROSTER_PATH = "data/npcs.yaml"


class NPCRoster:
    """Loads and provides lookup of company-wide NPCs by id."""

    def __init__(self, roster_path: str = DEFAULT_ROSTER_PATH):
        self.roster_path = roster_path
        self._roster: Dict[str, NPC] = {}

    def load(self) -> "NPCRoster":
        with open(self.roster_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for entry in data.get("npcs", []):
            npc = NPC.model_validate(entry)
            self._roster[npc.id] = npc
        return self

    def get(self, npc_id: str) -> NPC:
        if npc_id not in self._roster:
            raise ValueError(f"NPC '{npc_id}' not found in roster. Check data/npcs.yaml.")
        return self._roster[npc_id]


class ScenarioLoader:
    """Loads a Scenario from a YAML file, resolving NPC references against the company roster."""

    def __init__(self, file_path: str, roster: NPCRoster):
        self.file_path = file_path
        self.roster = roster

    def load(self) -> Scenario:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Resolve roster NPCs referenced by id
        resolved_npcs = []
        for ref_data in data.get("npcs", []):
            ref = NPCRef.model_validate(ref_data)
            base = self.roster.get(ref.npc_id)
            resolved = ResolvedNPC(
                id=base.id,
                name=base.name,
                role=ref.scenario_role if ref.scenario_role else base.role,
                personality=base.personality,
                background=base.background,
                scenario_role=ref.scenario_role,
            )
            resolved_npcs.append(resolved)

        # Pass through one-off NPCs directly
        other_npcs = [
            ResolvedNPC.model_validate(n) for n in data.get("other_npcs", [])
        ]

        return Scenario(
            title=data["title"],
            description=data["description"],
            difficulty=data["difficulty"],
            npcs=resolved_npcs,
            other_npcs=other_npcs,
        )

