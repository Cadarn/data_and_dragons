import pytest
from data_and_dragons.models import GameState, Player, Scenario, ResolvedNPC
from data_and_dragons.scenario_manager import ScenarioManager


def _make_npc(npc_id: str, name: str) -> ResolvedNPC:
    return ResolvedNPC(id=npc_id, name=name, role="Role", personality="P", background="B")


def test_scenario_manager_initialization():
    player = Player(name="Hero")
    scenarios = [
        Scenario(title="Scen 1", description="First", difficulty="Easy"),
        Scenario(title="Scen 2", description="Second", difficulty="Hard")
    ]
    state = GameState(player=player)

    manager = ScenarioManager(state=state, scenarios=scenarios)
    assert manager.get_current_scenario().title == "Scen 1"


def test_scenario_manager_progression():
    player = Player(name="Hero")
    scenarios = [
        Scenario(title="Scen 1", description="First", difficulty="Easy"),
        Scenario(title="Scen 2", description="Second", difficulty="Hard")
    ]
    state = GameState(player=player)

    manager = ScenarioManager(state=state, scenarios=scenarios)

    assert manager.has_more_scenarios() is True
    manager.advance_scenario()

    assert manager.get_current_scenario().title == "Scen 2"
    assert manager.has_more_scenarios() is False

    manager.advance_scenario()
    assert manager.get_current_scenario() is None


def test_scenario_manager_has_dialogue_manager():
    """ScenarioManager should expose a DialogueManager for the current scenario."""
    npc = _make_npc("sarah_jenkins", "Sarah Jenkins")
    scenarios = [
        Scenario(title="Scen 1", description="First", difficulty="Easy", npcs=[npc]),
    ]
    manager = ScenarioManager(state=GameState(player=Player(name="Hero")), scenarios=scenarios)

    assert manager.dialogue is not None
    available = manager.dialogue.get_available_npcs()
    assert any(n.name == "Sarah Jenkins" for n in available)


def test_dialogue_resets_on_scenario_advance():
    """Each new scenario should get a fresh DialogueManager with its own NPCs."""
    npc1 = _make_npc("todd_harris", "Todd Harris")
    npc2 = _make_npc("priya_natarajan", "Priya Natarajan")
    scenarios = [
        Scenario(title="Scen 1", description="First", difficulty="Easy", npcs=[npc1]),
        Scenario(title="Scen 2", description="Second", difficulty="Hard", npcs=[npc2]),
    ]
    manager = ScenarioManager(state=GameState(player=Player(name="Hero")), scenarios=scenarios)

    # Record something in scenario 1's dialogue
    manager.dialogue.record_exchange("todd_harris", "Hello.", "Hi.")
    assert len(manager.dialogue.get_history("todd_harris")) == 1

    # Advance — should get a fresh dialogue for scenario 2
    manager.advance_scenario()
    assert manager.dialogue is not None
    available_names = [n.name for n in manager.dialogue.get_available_npcs()]
    assert "Priya Natarajan" in available_names
    assert "Todd Harris" not in available_names


def test_dialogue_is_none_after_last_scenario():
    scenarios = [Scenario(title="Only", description=".", difficulty="Easy")]
    manager = ScenarioManager(state=GameState(player=Player(name="Hero")), scenarios=scenarios)
    manager.advance_scenario()
    assert manager.dialogue is None

