import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from data_and_dragons.models import (
    Action, ActionOutcome, JudgementResult, Player, Scenario, GameState,
)
from data_and_dragons.dice import DiceRoll, Outcome
from data_and_dragons.game_loop import GameLoop


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_scenario(title: str = "Test Scenario") -> Scenario:
    return Scenario(title=title, description="A test.", difficulty="Easy")


def _make_outcome(score: int = 75) -> ActionOutcome:
    return ActionOutcome(
        judgement=JudgementResult(
            technical_score=score,
            reasoning="Solid approach.",
            verdict="success",
        ),
        dice_roll=DiceRoll(value=14, outcome=Outcome.NORMAL, modifier=14 / 20),
        final_score=score,
        narrative="🎲 *You rolled a 14.*\n\nSolid approach.",
    )


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def test_game_loop_loads_scenarios_from_roster_and_files(tmp_path):
    """GameLoop should initialise with a list of scenarios and a Judge."""
    scenarios = [_make_scenario("Scen 1"), _make_scenario("Scen 2")]
    player = Player(name="Hero")
    loop = GameLoop(player=player, scenarios=scenarios)

    assert loop.current_scenario.title == "Scen 1"
    assert loop.is_running is True


def test_game_loop_not_running_with_no_scenarios(tmp_path):
    loop = GameLoop(player=Player(name="Hero"), scenarios=[])
    assert loop.is_running is False


# ---------------------------------------------------------------------------
# Processing a turn
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_game_loop_process_turn_returns_outcome(monkeypatch):
    """process_turn should call the Judge and return an ActionOutcome."""
    scenarios = [_make_scenario()]
    loop = GameLoop(player=Player(name="Hero"), scenarios=scenarios)

    expected = _make_outcome(score=80)
    monkeypatch.setattr(loop.judge, "evaluate", AsyncMock(return_value=expected))

    outcome = await loop.process_turn("I will use Pandas to clean the data.")

    assert isinstance(outcome, ActionOutcome)
    assert outcome.final_score == 80


@pytest.mark.asyncio
async def test_game_loop_updates_player_score_after_turn(monkeypatch):
    """Player score should accumulate across turns."""
    scenarios = [_make_scenario(), _make_scenario("Scen 2")]
    loop = GameLoop(player=Player(name="Hero"), scenarios=scenarios)

    monkeypatch.setattr(loop.judge, "evaluate", AsyncMock(return_value=_make_outcome(score=60)))
    await loop.process_turn("First answer.")

    assert loop.player.score == 60


@pytest.mark.asyncio
async def test_game_loop_records_dialogue_history(monkeypatch):
    """process_turn should record the exchange in the active DialogueManager."""
    npc_scenario = Scenario(
        title="NPC Test",
        description=".",
        difficulty="Easy",
        npcs=[],
    )
    scenarios = [npc_scenario]
    loop = GameLoop(player=Player(name="Hero"), scenarios=scenarios)
    outcome = _make_outcome()
    monkeypatch.setattr(loop.judge, "evaluate", AsyncMock(return_value=outcome))

    await loop.process_turn("My answer here.")

    full_history = loop.scenario_manager.dialogue.get_full_history()
    assert len(full_history) == 1
    assert full_history[0]["player"] == "My answer here."


# ---------------------------------------------------------------------------
# Scenario progression
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_game_loop_advances_after_completing_scenario(monkeypatch):
    """After advance_scenario is called, the current scenario should update."""
    scenarios = [_make_scenario("First"), _make_scenario("Second")]
    loop = GameLoop(player=Player(name="Hero"), scenarios=scenarios)

    assert loop.current_scenario.title == "First"
    loop.advance_scenario()
    assert loop.current_scenario.title == "Second"


def test_game_loop_stops_running_when_no_more_scenarios():
    scenarios = [_make_scenario()]
    loop = GameLoop(player=Player(name="Hero"), scenarios=scenarios)

    loop.advance_scenario()
    assert loop.is_running is False
    assert loop.current_scenario is None
