from typing import Dict, List, Optional
from data_and_dragons.models import ResolvedNPC, Scenario


class DialogueManager:
    """
    Manages NPC interactions within a scenario.

    Provides access to all available NPCs (roster + one-offs), and records
    the full conversation history between the player and each NPC.
    """

    def __init__(self, scenario: Scenario):
        self._scenario = scenario
        # Unified lookup of all NPCs available in this scenario
        self._npcs: Dict[str, ResolvedNPC] = {
            npc.id: npc for npc in scenario.npcs + scenario.other_npcs
        }
        # Per-NPC conversation history: {npc_id: [{player, npc}, ...]}
        self._history: Dict[str, List[Dict[str, str]]] = {npc_id: [] for npc_id in self._npcs}
        # Ordered log of all exchanges across all NPCs
        self._full_history: List[Dict[str, str]] = []

    def get_available_npcs(self) -> List[ResolvedNPC]:
        """Return all NPCs available to interact with in the current scenario."""
        return list(self._npcs.values())

    def get_npc(self, npc_id: str) -> ResolvedNPC:
        """Retrieve a specific NPC by id, or raise if they are not in this scenario."""
        if npc_id not in self._npcs:
            raise ValueError(
                f"NPC '{npc_id}' is not available in this scenario. "
                f"Available: {list(self._npcs.keys())}"
            )
        return self._npcs[npc_id]

    def record_exchange(self, npc_id: str, player_message: str, npc_response: str) -> None:
        """Record a dialogue exchange between the player and an NPC."""
        self.get_npc(npc_id)  # Validates the NPC exists
        exchange = {"player": player_message, "npc": npc_response}
        self._history[npc_id].append(exchange)
        self._full_history.append({"npc_id": npc_id, **exchange})

    def get_history(self, npc_id: str) -> List[Dict[str, str]]:
        """Return all exchanges for a specific NPC."""
        self.get_npc(npc_id)  # Validates the NPC exists
        return self._history[npc_id]

    def get_full_history(self) -> List[Dict[str, str]]:
        """Return all exchanges across all NPCs in chronological order."""
        return self._full_history
