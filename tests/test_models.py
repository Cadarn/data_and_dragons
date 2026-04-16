import pytest
from pydantic import ValidationError
from data_and_dragons.models import GameState, Player, Scenario, NPC, Action

def test_player_model():
    p = Player(name="Alice", score=0)
    assert p.name == "Alice"
    assert p.score == 0

    with pytest.raises(ValidationError):
        Player(name="Bob", score="not_a_number")

def test_npc_model():
    npc = NPC(name="CEO", role="Client", personality="Aggressive", background="Needs results ASAP")
    assert npc.name == "CEO"
    assert npc.role == "Client"

def test_scenario_model():
    s = Scenario(
        title="Predictive Analytics",
        description="Predict customer churn",
        difficulty="Medium",
        npcs=[NPC(name="Data Lead", role="Ally", personality="Helpful", background="")]
    )
    assert s.title == "Predictive Analytics"
    assert len(s.npcs) == 1

def test_action_model():
    a = Action(player_input="I will use XGBoost")
    assert a.player_input == "I will use XGBoost"

def test_game_state_model():
    p = Player(name="Alice", score=10)
    g = GameState(player=p, current_scenario_index=0)
    assert g.player.name == "Alice"
    assert g.current_scenario_index == 0
