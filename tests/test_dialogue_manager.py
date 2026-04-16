import pytest
from data_and_dragons.models import ResolvedNPC, Scenario
from data_and_dragons.dialogue_manager import DialogueManager


@pytest.fixture
def scenario_with_npcs() -> Scenario:
    return Scenario(
        title="Test Scenario",
        description="A test.",
        difficulty="Easy",
        npcs=[
            ResolvedNPC(
                id="sarah_jenkins",
                name="Sarah Jenkins",
                role="Senior Consultant",
                personality="Supportive but demanding",
                background="Ten-year veteran.",
            ),
            ResolvedNPC(
                id="todd_harris",
                name="Todd Harris",
                role="Client Project Manager",
                personality="Anxious and tech-illiterate",
                background="Loves spreadsheets.",
            ),
        ],
        other_npcs=[
            ResolvedNPC(
                id="janet_bloom",
                name="Janet Bloom",
                role="Regional Sales Director",
                personality="Impatient",
                background="Visiting for the quarterly review.",
            )
        ],
    )


def test_dialogue_manager_lists_available_npcs(scenario_with_npcs: Scenario):
    """All NPCs — roster and one-offs — should be available."""
    dm = DialogueManager(scenario_with_npcs)
    available = dm.get_available_npcs()
    names = [n.name for n in available]

    assert "Sarah Jenkins" in names
    assert "Todd Harris" in names
    assert "Janet Bloom" in names
    assert len(available) == 3


def test_dialogue_manager_get_npc_by_id(scenario_with_npcs: Scenario):
    dm = DialogueManager(scenario_with_npcs)
    npc = dm.get_npc("sarah_jenkins")
    assert npc.name == "Sarah Jenkins"


def test_dialogue_manager_raises_for_unknown_npc(scenario_with_npcs: Scenario):
    dm = DialogueManager(scenario_with_npcs)
    with pytest.raises(ValueError, match="NPC 'ghost' is not available"):
        dm.get_npc("ghost")


def test_dialogue_manager_records_and_retrieves_history(scenario_with_npcs: Scenario):
    dm = DialogueManager(scenario_with_npcs)
    dm.record_exchange(npc_id="sarah_jenkins", player_message="I'll use Pandas.", npc_response="Good choice.")

    history = dm.get_history(npc_id="sarah_jenkins")
    assert len(history) == 1
    assert history[0]["player"] == "I'll use Pandas."
    assert history[0]["npc"] == "Good choice."


def test_dialogue_manager_history_is_per_npc(scenario_with_npcs: Scenario):
    """History for one NPC should not bleed into another."""
    dm = DialogueManager(scenario_with_npcs)
    dm.record_exchange("sarah_jenkins", "Hello Sarah.", "Hello.")
    dm.record_exchange("todd_harris", "Hello Todd.", "Hi!")

    assert len(dm.get_history("sarah_jenkins")) == 1
    assert len(dm.get_history("todd_harris")) == 1
    assert dm.get_history("sarah_jenkins")[0]["player"] == "Hello Sarah."


def test_dialogue_manager_full_history(scenario_with_npcs: Scenario):
    """get_full_history should return all exchanges across all NPCs."""
    dm = DialogueManager(scenario_with_npcs)
    dm.record_exchange("sarah_jenkins", "Hello.", "Hi.")
    dm.record_exchange("todd_harris", "Hey.", "Yo.")

    full = dm.get_full_history()
    assert len(full) == 2
    assert full[0]["npc_id"] == "sarah_jenkins"
    assert full[1]["npc_id"] == "todd_harris"
