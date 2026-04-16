import pytest
import yaml
from pathlib import Path
from data_and_dragons.models import Scenario
from data_and_dragons.scenario_loader import ScenarioLoader, NPCRoster

ROSTER_YAML = """
npcs:
  - id: "sarah_jenkins"
    name: "Sarah Jenkins"
    role: "Senior Consultant"
    personality: "Supportive but demanding"
    background: "Ten-year veteran."
  - id: "todd_harris"
    name: "Todd Harris"
    role: "Client Project Manager"
    personality: "Anxious and tech-illiterate"
    background: "Believes in spreadsheets."
"""

SCENARIO_YAML = """
title: "The Excel Catastrophe"
description: "A dirty data nightmare."
difficulty: "Easy"
npcs:
  - npc_id: "todd_harris"
    scenario_role: "The client contact handing over the data."
  - npc_id: "sarah_jenkins"
other_npcs:
  - id: "janet_bloom"
    name: "Janet Bloom"
    role: "Regional Sales Director"
    personality: "Impatient"
    background: "Visiting for the quarterly review."
"""


@pytest.fixture
def roster(tmp_path: Path) -> NPCRoster:
    roster_file = tmp_path / "npcs.yaml"
    roster_file.write_text(ROSTER_YAML)
    return NPCRoster(str(roster_file)).load()


def test_roster_loads_npcs(roster: NPCRoster):
    npc = roster.get("sarah_jenkins")
    assert npc.name == "Sarah Jenkins"
    assert npc.role == "Senior Consultant"


def test_roster_raises_for_unknown_npc(roster: NPCRoster):
    with pytest.raises(ValueError, match="not found in roster"):
        roster.get("ghost_npc")


def test_scenario_loader_resolves_roster_npcs(tmp_path: Path, roster: NPCRoster):
    scenario_file = tmp_path / "scenario.yaml"
    scenario_file.write_text(SCENARIO_YAML)

    loader = ScenarioLoader(str(scenario_file), roster)
    scenario = loader.load()

    assert isinstance(scenario, Scenario)
    assert len(scenario.npcs) == 2
    
    # Todd should have his scenario_role applied as the active role
    todd = next(n for n in scenario.npcs if n.id == "todd_harris")
    assert todd.role == "The client contact handing over the data."
    assert todd.scenario_role == "The client contact handing over the data."

    # Sarah has no scenario_role override — should fall back to roster role
    sarah = next(n for n in scenario.npcs if n.id == "sarah_jenkins")
    assert sarah.role == "Senior Consultant"
    assert sarah.scenario_role is None


def test_scenario_loader_resolves_other_npcs(tmp_path: Path, roster: NPCRoster):
    scenario_file = tmp_path / "scenario.yaml"
    scenario_file.write_text(SCENARIO_YAML)

    loader = ScenarioLoader(str(scenario_file), roster)
    scenario = loader.load()

    assert len(scenario.other_npcs) == 1
    janet = scenario.other_npcs[0]
    assert janet.name == "Janet Bloom"
    assert janet.id == "janet_bloom"


def test_scenario_loader_raises_on_unknown_npc_ref(tmp_path: Path, roster: NPCRoster):
    bad_scenario = """
title: "Bad Scenario"
description: "References a ghost."
difficulty: "Easy"
npcs:
  - npc_id: "ghost_npc"
"""
    scenario_file = tmp_path / "bad_scenario.yaml"
    scenario_file.write_text(bad_scenario)

    loader = ScenarioLoader(str(scenario_file), roster)
    with pytest.raises(ValueError, match="not found in roster"):
        loader.load()
