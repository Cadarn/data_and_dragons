from typing import List, Optional
from data_and_dragons.models import GameState, Scenario
from data_and_dragons.dialogue_manager import DialogueManager


class ScenarioManager:
    """Manages the current game state and progression through scenarios."""

    def __init__(self, state: GameState, scenarios: List[Scenario]):
        self.state = state
        self.scenarios = scenarios
        self._dialogue: Optional[DialogueManager] = (
            DialogueManager(scenarios[state.current_scenario_index])
            if scenarios else None
        )

    @property
    def dialogue(self) -> Optional[DialogueManager]:
        """The active DialogueManager for the current scenario."""
        return self._dialogue

    def get_current_scenario(self) -> Optional[Scenario]:
        if self.state.current_scenario_index < len(self.scenarios):
            return self.scenarios[self.state.current_scenario_index]
        return None

    def has_more_scenarios(self) -> bool:
        return self.state.current_scenario_index < len(self.scenarios) - 1

    def advance_scenario(self):
        self.state.current_scenario_index += 1
        current = self.get_current_scenario()
        self._dialogue = DialogueManager(current) if current is not None else None

