import pytest
from data_and_dragons.models import GameState, Player, Scenario
from data_and_dragons.scenario_manager import ScenarioManager

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
