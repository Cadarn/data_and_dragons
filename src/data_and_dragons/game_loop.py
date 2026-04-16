from typing import List, Optional
from data_and_dragons.models import Action, ActionOutcome, GameState, Player, Scenario
from data_and_dragons.scenario_manager import ScenarioManager
from data_and_dragons.judge import Judge

# The name used in dialogue history for the "game master" narrator NPC
_GM_NPC_ID = "_game_master"


class GameLoop:
    """
    Ties together the ScenarioManager, DialogueManager, and Judge into a single
    orchestration object.

    Responsibilities:
    - Track the active player and their score.
    - Drive scenario progression.
    - Route player input through the Judge and record outcomes.
    """

    def __init__(
        self,
        player: Player,
        scenarios: List[Scenario],
        judge: Optional[Judge] = None,
    ):
        self.player = player
        self.judge = judge or Judge()
        self._state = GameState(player=player)
        self.scenario_manager = ScenarioManager(state=self._state, scenarios=scenarios)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def current_scenario(self) -> Optional[Scenario]:
        return self.scenario_manager.get_current_scenario()

    @property
    def is_running(self) -> bool:
        return self.current_scenario is not None

    # ------------------------------------------------------------------
    # Core loop
    # ------------------------------------------------------------------

    async def process_turn(self, player_input: str) -> ActionOutcome:
        """
        Process a single player turn:
          1. Evaluate the player's input with the Judge.
          2. Accumulate the score onto the player.
          3. Record the exchange in the active dialogue history.

        Returns the full ActionOutcome.
        """
        scenario = self.current_scenario
        if scenario is None:
            raise RuntimeError("process_turn called but no scenario is active.")

        action = Action(player_input=player_input)
        outcome = await self.judge.evaluate(scenario=scenario, action=action)

        # Accumulate score
        self.player.score += outcome.final_score

        # Record the exchange in dialogue history using a sentinel GM id
        dm = self.scenario_manager.dialogue
        if dm is not None and _GM_NPC_ID not in [n.id for n in dm.get_available_npcs()]:
            # Directly append to full history for narrator exchanges (no NPC ref needed)
            dm._full_history.append({
                "npc_id": _GM_NPC_ID,
                "player": player_input,
                "npc": outcome.narrative,
            })

        return outcome

    # ------------------------------------------------------------------
    # Progression
    # ------------------------------------------------------------------

    def advance_scenario(self) -> None:
        """Move to the next scenario, resetting the active dialogue context."""
        self.scenario_manager.advance_scenario()
