import pytest
import yaml
from pathlib import Path
from data_and_dragons.models import Scenario
from data_and_dragons.scenario_loader import ScenarioLoader

def test_scenario_loader_loads_valid_yaml(tmp_path: Path):
    scenario_yaml = """
title: "The Big Boss"
description: "A tough scenario."
difficulty: "Hard"
npcs:
  - name: "Boss"
    role: "CEO"
    personality: "Aggressive"
    background: "Wants money"
"""
    file_path = tmp_path / "scenario_1.yaml"
    file_path.write_text(scenario_yaml)
    
    loader = ScenarioLoader(str(file_path))
    scenario = loader.load()
    
    assert isinstance(scenario, Scenario)
    assert scenario.title == "The Big Boss"
    assert len(scenario.npcs) == 1
    assert scenario.npcs[0].name == "Boss"

def test_scenario_loader_raises_on_invalid_yaml(tmp_path: Path):
    file_path = tmp_path / "scenario_invalid.yaml"
    file_path.write_text("invalid_yaml: [missing bracket")
    
    loader = ScenarioLoader(str(file_path))
    with pytest.raises(Exception):
        loader.load()
